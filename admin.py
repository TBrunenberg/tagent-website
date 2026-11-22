"""Schrijft het beheerscherm (/admin) en de proefversie (/admin/demo) naar dist/."""
import json, os, shutil
import yaml
import cms

ROOT = os.path.dirname(os.path.abspath(__file__))
DECAP_VERSION = "3.18.0"

# Huisstijl van de site, toegepast op het beheerscherm.
THEME = """
:root{--ink:#0C0C0A;--ink2:#151513;--bone:#EEEAE3;--paper:#F6F3EE;--muted:#5A5650;--ember:#FF6A2B;--ember-dark:#A8410F}
@font-face{font-family:"Geist";font-weight:400;font-display:swap;src:url(../assets/fonts/geist-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Geist";font-weight:500;font-display:swap;src:url(../assets/fonts/geist-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"Geist";font-weight:600;font-display:swap;src:url(../assets/fonts/geist-latin-600-normal.woff2) format("woff2")}
html,body{background:var(--paper)!important}
body,button,input,textarea,select{font-family:Geist,system-ui,sans-serif!important}
::selection{background:rgba(255,106,43,.25)}
:focus-visible{outline:2px solid var(--ember)!important;outline-offset:2px}
a{color:var(--ember-dark)}
input[type=checkbox],input[type=radio],input[type=range]{accent-color:var(--ember)}
/* kopbalk */
header,[class*="AppHeaderContainer"],[class*="AppHeader"]{background:var(--ink)!important;color:var(--bone)!important;box-shadow:none!important}
[class*="AppHeaderContainer"] a,[class*="AppHeaderContainer"] button,[class*="AppHeader"] a{color:rgba(238,234,227,.82)!important}
[class*="AppHeaderContainer"] a.header-link-active,[class*="AppHeaderContainer"] a[aria-current]{color:var(--bone)!important}
[class*="AppHeaderContainer"] svg{color:inherit}
[class*="AppHeaderQuickNewButton"],[class*="QuickNewButton"]{background:var(--ember)!important;color:var(--ink)!important}
/* knoppen */
[class*="PublishButton"],[class*="SaveButton"],[class*="LoginButton"],[class*="ToolbarButton"][class*="Publish"]{background:var(--ink)!important;color:var(--bone)!important;border-radius:999px!important}
[class*="PublishButton"]:hover,[class*="SaveButton"]:hover{background:#1E1D1A!important}
/* zijbalk en kaarten */
[class*="SidebarContainer"] a[class*="active"],[class*="SidebarNavLink"][class*="active"]{color:var(--ember-dark)!important;border-left-color:var(--ember)!important}
[class*="CollectionTopHeading"],[class*="EditorControlPane"] label{letter-spacing:-.01em}
[class*="ControlContainer"] label,[class*="FieldLabel"]{color:var(--muted)!important}
[class*="ObjectControl"] [class*="TopBar"],[class*="ListItemTopBar"]{background:#ECE8E1!important}
/* inlogscherm */
[class*="LoginPage"],section[class*="LoginPage"]{background:var(--ink)!important}
[class*="LoginPage"] button{background:var(--ember)!important;color:var(--ink)!important;border-radius:999px!important;font-weight:500!important}
"""

PAGE = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Beheer – Tagent</title>
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}admin/admin-theme.css">
{head_extra}
</head>
<body>
{body_extra}
<script src="{prefix}admin/decap/decap-cms.js"></script>
<script>{init}</script>
</body>
</html>
"""


def _repo_files():
    """Inhoud van content/ als boom voor de test-repo-backend van de proefversie."""
    tree = {}
    base = os.path.join(ROOT, "content")
    for d, _, files in os.walk(base):
        for f in files:
            if not f.endswith(".yml"):
                continue
            rel = os.path.relpath(os.path.join(d, f), ROOT).split(os.sep)
            node = tree
            for part in rel[:-1]:
                node = node.setdefault(part, {})
            node[rel[-1]] = {"content": open(os.path.join(d, f), encoding="utf-8").read()}
    return tree


def write(out, site_url, repo, identity_url, gateway_url):
    adm = os.path.join(out, "admin")
    os.makedirs(os.path.join(adm, "demo"), exist_ok=True)
    shutil.copytree(os.path.join(ROOT, "vendor", "decap"), os.path.join(adm, "decap"), dirs_exist_ok=True)
    with open(os.path.join(adm, "admin-theme.css"), "w", encoding="utf-8") as fh:
        fh.write(THEME)

    backend = {"name": "git-gateway", "repo": repo, "branch": "main", "identity_url": identity_url, "gateway_url": gateway_url,
               "commit_messages": {"create": "Nieuw: {{collection}} {{slug}}", "update": "Bijgewerkt: {{collection}} {{slug}}",
                                   "delete": "Verwijderd: {{collection}} {{slug}}", "uploadMedia": "Foto toegevoegd: {{path}}", "deleteMedia": "Foto verwijderd: {{path}}"}}
    cfg = cms.decap_config(site_url, repo, backend)
    cfg["logo_url"] = "../assets/logo-512.png"
    with open(os.path.join(adm, "config.yml"), "w", encoding="utf-8") as fh:
        fh.write("# Gegenereerd door build.py (admin.py). Niet met de hand aanpassen.\n")
        yaml.safe_dump(cfg, fh, allow_unicode=True, sort_keys=False, width=10000)
    with open(os.path.join(adm, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(PAGE.format(prefix="../", head_extra="", body_extra="", init=""))

    # Proefversie: zelfde schermen, niets wordt opgeslagen.
    demo = dict(cfg)
    demo["backend"] = {"name": "test-repo"}
    demo["load_config_file"] = False
    demo["site_url"] = demo["display_url"] = site_url
    demo["logo_url"] = "../../assets/logo-512.png"
    bar = ('<div style="position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:99999;padding:10px 18px;border-radius:999px;'
           'background:#0C0C0A;color:#EEEAE3;font:500 14px Geist,system-ui,sans-serif;box-shadow:0 10px 30px -10px rgba(0,0,0,.5)">'
           'Proefversie: niets wordt opgeslagen</div>')
    init = ("window.repoFiles = " + json.dumps(_repo_files(), ensure_ascii=False) + ";\n"
            "CMS.init({ config: " + json.dumps(demo, ensure_ascii=False) + " });")
    with open(os.path.join(adm, "demo", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(PAGE.format(prefix="../../", head_extra="<script>window.CMS_MANUAL_INIT = true;</script>", body_extra=bar, init=init))
