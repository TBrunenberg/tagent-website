#!/usr/bin/env python3
"""Genereert de site voor het webdesignbedrijf (werknaam) op de Kader-basis.
Merknaam staat op één plek: BRAND. Vervang die als de naam bekend is."""
import os, shutil, json

BRAND = "Tagent"
FULL = "Tagent"
from icons import ICON_D, SUF
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist")

ARR = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>'
ARR14 = ARR.replace('width="16" height="16"', 'width="14" height="14"')
CHECK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#FF6A2B" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex:none"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'

LASTMOD = "2026-11-22"
EMAIL = "info@tagent.nl"
TEL = "+31 (0)6 1554 1022"
TEL_HREF = "tel:+31615541022"
WEB3FORMS_KEY = ""  # toegangssleutel van web3forms.com (gekoppeld aan info@tagent.nl); leeg = verzenden via e-mailprogramma
MENU = [("index.html", "Home"), ("diensten.html", "Diensten"), ("werkwijze.html", "Werkwijze"),
        ("over-ons.html", "Over ons"), ("kennismaking.html", "Kennismaking")]

def btn(href, text, kind="light", sm=False, arrow=True):
    cls = f"btn btn-{kind}" + (" btn-sm" if sm else "")
    if not arrow:
        return f'<a class="{cls}" href="{href}">{text}</a>'
    return f'<a class="{cls}" href="{href}">{text}<span class="arr">{ARR}</span></a>'

def head(title, desc, extra_css=""):
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<script>if('scrollRestoration' in history)history.scrollRestoration='manual';try{{if(sessionStorage.getItem('tr')){{sessionStorage.removeItem('tr');if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('tr-in','tr-hold')}}}}catch(e){{}}</script>
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/web.css">
<link rel="preload" href="assets/fonts/geist-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/geist-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<meta name="theme-color" content="#0C0C0A">
<!--SEO-->
<style>
@font-face{{font-family:"Geist";font-style:normal;font-weight:400;font-display:swap;src:url(assets/fonts/geist-latin-400-normal.woff2) format("woff2")}}
@font-face{{font-family:"Geist";font-style:normal;font-weight:500;font-display:swap;src:url(assets/fonts/geist-latin-500-normal.woff2) format("woff2")}}
@font-face{{font-family:"Geist";font-style:normal;font-weight:600;font-display:swap;src:url(assets/fonts/geist-latin-600-normal.woff2) format("woff2")}}
@font-face{{font-family:"Instrument Serif";font-style:italic;font-weight:400;font-display:swap;src:url(assets/fonts/instrument-serif-latin-400-italic.woff2) format("woff2")}}
.tr{{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:#0C0C0A;color:#EEEAE3;transform:translateY(-100%);visibility:hidden;pointer-events:none}}
.tr::before{{content:"";position:absolute;inset:0;background:radial-gradient(70% 55% at 50% 110%,rgba(255,106,43,.30),transparent 65%),radial-gradient(50% 40% at 50% -10%,rgba(238,234,227,.05),transparent 70%)}}
.tr-mark{{position:relative;display:flex;align-items:center;gap:16px;font:600 clamp(32px,4vw,44px)/1 Geist,system-ui,sans-serif;letter-spacing:-.035em}}
.tr-mark svg{{opacity:0;transform:scale(.7) rotate(-12deg);transition:opacity .5s ease .12s,transform .7s cubic-bezier(.2,.8,.2,1) .12s}}
.tr-name{{display:inline-block;overflow:hidden;padding:0 .04em .14em;margin-bottom:-.14em}}
.tr-name span{{display:inline-block;transform:translateY(110%);transition:transform .7s cubic-bezier(.2,.8,.2,1) .2s}}
.tr.is-enter,html.tr-in .tr{{visibility:visible;transform:none;pointer-events:auto}}
.tr.is-enter{{transition:transform .65s cubic-bezier(.76,0,.24,1)}}
.tr.is-enter .tr-mark svg,html.tr-in .tr .tr-mark svg{{opacity:1;transform:none}}
.tr.is-enter .tr-name span,html.tr-in .tr .tr-name span{{transform:none}}
html.tr-in .tr:not(.is-leave) *{{transition:none}}
html.tr-in .tr.is-leave{{transform:translateY(100%);transition:transform .85s cubic-bezier(.76,0,.24,1)}}
html.tr-in .tr.is-leave .tr-mark{{opacity:0;transform:translateY(-24px);transition:opacity .35s ease,transform .6s cubic-bezier(.2,.8,.2,1)}}
html.tr-in .tr{{animation:trsafe .85s cubic-bezier(.76,0,.24,1) 4s forwards}}
@keyframes trsafe{{to{{transform:translateY(100%);visibility:hidden}}}}
html.tr-hold #dc-root *{{animation-play-state:paused!important}}
@media (prefers-reduced-motion: reduce){{.tr{{display:none}}}}
.skip{{position:fixed;left:16px;top:-80px;z-index:100;padding:10px 18px;border-radius:999px;background:#EEEAE3;color:#0C0C0A;font:500 14px Geist,system-ui,sans-serif;text-decoration:none;transition:top .2s}}.skip:focus{{top:16px}}
body{{margin:0}}
a{{color:inherit}}a:hover{{color:inherit}}
html,body{{height:100%;overflow:hidden;margin:0}}
#dc-root{{position:fixed;inset:0;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;scroll-behavior:smooth}}
{extra_css}
</style>
</head>
<body>
<template id="dc-tpl">

<div class="page" style="font-family: Geist, system-ui, sans-serif; background: #0C0C0A; color: #EEEAE3">
'''

def nav(cur):
    links = "\n".join(
        f'<a class="nav-link is-current" href="{h}" aria-current="page">{t}</a>' if h == cur
        else f'<a class="nav-link" href="{h}">{t}</a>' for h, t in MENU)
    cta = "" if cur == "kennismaking.html" else f'<div class="nav-cta">{btn("kennismaking.html", "Plan een kennismaking", sm=True)}</div>'
    return f'''
<header class="nav">
<div class="wrap nav-in">
<a href="index.html" class="logo" aria-label="{BRAND}, naar de homepage">{ICON_D.format(s=24)}{BRAND}</a>
<nav class="nav-links" aria-label="Hoofdmenu">
{links}
</nav>
{cta}
</div>
</header>
'''

def cta_block(title, lead, img="cta.webp", second=("werkwijze.html", "Bekijk de werkwijze")):
    return f'''
<section style="padding: clamp(12px, 2vw, 24px)">
<div class="media" style="border-radius: 32px; min-height: 680px; display: flex; align-items: center; justify-content: center">
<img class="kb" src="assets/{img}" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover">
<img class="kb-2" src="assets/{img}" alt="" style="width: 100%; height: 100%; object-fit: cover">
<div style="position: absolute; inset: 0; background: rgba(12,12,10,.35)"></div>
<div class="reveal" style="position: relative; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 36px; padding: 80px 24px">
<h2 class="h1" style="max-width: 14ch">{title}</h2>
<p class="lead" style="max-width: 32rem; color: rgba(238,234,227,.82)">{lead}</p>
<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px">
{btn("kennismaking.html", "Plan een kennismaking")}
<a class="btn btn-ghost" href="{second[0]}">{second[1]}</a>
</div>
</div>
</div>
</section>
'''

def footer():
    col = lambda title, items: '<div style="display: flex; flex-direction: column; gap: 4px"><span class="label" style="margin-bottom: 12px">' + title + '</span>' + "".join(
        f'<a class="ulink" href="{h}">{t}</a>' if h else f'<span style="padding-block: 10px; color: #A19C93">{t}</span>' for h, t in items) + '</div>'
    return f'''
<footer class="wrap" style="padding-top: 120px; padding-bottom: 32px; display: flex; flex-direction: column; gap: 80px">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 56px">
<div style="flex: 1 1 280px; max-width: 22rem; display: flex; flex-direction: column; gap: 20px">
<p class="h3" style="font-size: 28px">Jouw website, maar dan <em class="serif-i">beter.</em></p>
<a class="btn btn-light btn-sm" href="kennismaking.html" style="align-self: flex-start">Plan een kennismaking<span class="arr">{ARR14}</span></a>
</div>
<div style="flex: 2 1 520px; display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 32px">
{col("Diensten", [("diensten.html#nieuw", "Nieuwe website"), ("diensten.html#redesign", "Redesign"), ("diensten.html#beheerscherm", "Beheerscherm"), ("diensten.html#beheer", "Beheer")])}
{col("Werkwijze", [("werkwijze.html", "Zo werkt het"), ("werkwijze.html#vragen", "Veelgestelde vragen"), ("over-ons.html", "Over ons")])}
{col("Contact", [("kennismaking.html", "Kennismaking"), ("mailto:" + EMAIL, EMAIL), (TEL_HREF, TEL)])}
</div>
</div>
<div aria-hidden="true" style="font-weight: 600; font-size: clamp(60px, 17vw, 300px); line-height: 1; letter-spacing: -.07em; color: #1E1D1A; user-select: none; white-space: nowrap; overflow: hidden; padding-bottom: .12em; margin-bottom: -.2em">{BRAND}</div>
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; padding-top: 24px; border-top: 1px solid rgba(238,234,227,.12)">
<span class="label">© 2026 {FULL}</span>
<span style="display: flex; flex-wrap: wrap; gap: 24px"><a class="label" href="privacy.html">Privacy</a><a class="label" href="kennismaking.html">Contact</a></span>
</div>
</footer>
'''

BASE_LOGIC = '''
  componentDidMount() {
    try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
    if (!location.hash) {
      var r = document.getElementById('dc-root'); if (r) r.scrollTop = 0;
      try { window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); } catch (e) { window.scrollTo(0, 0); }
    }
    var fit = function () {
      document.querySelectorAll('.hs-track').forEach(function (t) {
        var p = t.parentElement, cs = getComputedStyle(p);
        var w = p.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        t.style.setProperty('--hs-end', Math.min(0, w - t.scrollWidth) + 'px');
      });
    };
    fit(); setTimeout(fit, 600); window.addEventListener('resize', fit);
  }'''

def tail(logic_body="", height=6000):
    logic = "class Component extends DCLogic {" + BASE_LOGIC + logic_body + "\n}"
    if "renderVals" not in logic_body:
        logic = logic[:-1] + "  renderVals() { return {}; }\n}"
    return f'''
</div>
</template>
<div id="dc-root"><!--PRE--></div>
<script type="text/plain" id="dc-logic" data-props='{{"$preview":{{"width":1440,"height":{height}}}}}'>
{logic}
</script>
<script src="assets/runtime.js"></script>
<script>
(function () {{
  var tr = document.getElementById('tr'), de = document.documentElement;
  if (!tr) return;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function leave() {{
    if (!de.classList.contains('tr-in')) return;
    tr.classList.add('is-leave');
    de.classList.remove('tr-hold');
    setTimeout(function () {{ de.classList.remove('tr-in'); tr.className = 'tr'; }}, 900);
  }}
  if (de.classList.contains('tr-in')) {{
    var wait = document.fonts && document.fonts.ready ? Promise.race([document.fonts.ready, new Promise(function (r) {{ setTimeout(r, 450); }})]) : Promise.resolve();
    wait.then(function () {{ setTimeout(leave, 420); }});
  }}
  addEventListener('pageshow', function (e) {{ if (e.persisted) {{ de.classList.remove('tr-in', 'tr-hold'); tr.className = 'tr'; }} }});
  document.addEventListener('click', function (e) {{
    var a = e.target.closest && e.target.closest('a');
    if (!a || reduce || e.defaultPrevented || e.button !== 0) return;
    var h = a.getAttribute('href');
    if (!h || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.hasAttribute('download')) return;
    if (/^(mailto:|tel:|#|javascript:)/i.test(h)) return;
    var u = new URL(h, location.href);
    if (u.origin !== location.origin) return;
    if (u.pathname === location.pathname && u.hash) return;
    e.preventDefault();
    try {{ sessionStorage.setItem('tr', '1'); }} catch (x) {{}}
    tr.className = 'tr is-enter';
    setTimeout(function () {{ location.href = u.href; }}, 680);
  }}, true);
}})();
</script>
</body>
</html>
'''

def words(text, rng=76):
    parts = [p for p in text.split(" ") if p != "<br>"]
    breaks = set()
    k = 0
    for p in text.split(" "):
        if p == "<br>": breaks.add(k - 1)
        else: k += 1
    n = len(parts)
    out = []
    for i, t in enumerate(parts):
        s = 8 + i * rng / n
        out.append(f'<span class="w" style="animation-range:contain {s:.1f}% contain {s + rng / n + 4:.1f}%">{t} </span>' + ("<br>" if i in breaks else ""))
    return "".join(out)

def browser(url, inner, style="", cls="win"):
    return f'''<div class="{cls}" style="{style}"><div class="bw-top"><span class="ui-dot"></span><span class="ui-dot"></span><span class="ui-dot"></span><span class="bw-url">{url}</span></div>{inner}</div>'''

def minisite(title, img="d1.webp", extra="", buttons=("Reserveer", "Bekijk menu")):
    btns = "".join(f'<span class="ms-btn{" ghost" if i else ""}">{b}</span>' for i, b in enumerate(buttons))
    return f'''<div class="ms"><div class="ms-nav"><span>Jouw zaak</span><span><i></i><i></i><i></i></span></div>
<div class="ms-title">{title}</div>
<div class="ms-img"><img src="assets/{img}" alt=""></div>
{extra}<div class="ms-row">{btns}</div></div>'''

def page_hero(title_lines, lead, img, visual="", height="min(calc(100svh - 72px), 720px)"):
    lines = "".join(f'<span class="line"><span style="animation-delay: {0.15 + i * 0.15:.2f}s">{l}</span></span>' for i, l in enumerate(title_lines))
    return f'''
<section style="position: relative; height: {height}; min-height: 560px; overflow: hidden">
<div class="media hero-out" style="position: absolute; inset: 0">
<img class="kb" src="assets/{img}" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover">
<img class="kb-2" src="assets/{img}" alt="" style="width: 100%; height: 100%; object-fit: cover">
<div class="scrim"></div>
</div>
{visual}
<div class="wrap text-out" style="position: relative; height: 100%; display: flex; flex-direction: column; justify-content: center; gap: 32px; padding-block: 48px">
<h1 class="h1 hero-h">{lines}</h1>
<p class="lead fade-up" style="max-width: 36rem; animation-delay: .55s; color: rgba(238,234,227,.82)">{lead}</p>
</div>
</section>
'''

pages = {}

DIENSTEN_VIS = '<div class="hero-site hero-out hero-mid" aria-hidden="true"><div class="win" style="text-align: left"><div class="bw-top"><span class="ui-dot"></span><span class="ui-dot"></span><span class="ui-dot"></span><span class="bw-url">Diensten · <b>van ontwerp tot beheer</b></span></div>' + "".join(f'<div class="t-in" style="display: flex; align-items: center; gap: 12px; padding: 13px 16px;{" border-top: 1px solid rgba(238,234,227,.1);" if i else ""} font-size: 14px; animation-delay: {0.7 + i * 0.18:.2f}s">{CHECK}<span>{t}</span><span class="muted" style="margin-left: auto; font-size: 12px">{d}</span></div>' for i, (t, d) in enumerate([("Nieuwe website", "ontwerp"), ("Redesign", "alles mee"), ("Beheerscherm", "zelf aanpassen"), ("Livegang", "eigen domein"), ("Beheer", "per maand of jaar")])) + '</div></div>'
WERKWIJZE_VIS = '<div class="hero-site hero-out hero-mid" aria-hidden="true"><div class="win" style="padding: 20px; display: flex; flex-direction: column; gap: 16px; text-align: left"><div style="display: flex; justify-content: space-between; align-items: center"><span style="font-weight: 500">Planning</span><span class="pill pill-ember t-pop" style="animation-delay: 2.2s">' + CHECK + 'Ontwerp akkoord</span></div>' + "".join(f'<div style="display: flex; flex-direction: column; gap: 8px"><div style="display: flex; justify-content: space-between; font-size: 13px"><span>{n} {t}</span><span class="muted">{st}</span></div><div class="step-bar"><i class="t-gx" style="animation-delay: {0.6 + k * 0.3:.2f}s; {"" if k < 3 else ("transform: scaleX(.35)" if k == 3 else "transform: scaleX(0)")}"></i></div></div>' for k, (n, t, st) in enumerate([("01", "Kennismaking", "completed"), ("02", "Ontwerp", "completed"), ("03", "Samen doorlopen", "completed"), ("04", "Livegang", "in progress"), ("05", "Beheer", "scheduled")])) + '</div></div>'
OVER_VIS = ('<div class="hero-site hero-out hero-mid" aria-hidden="true"><div class="win" style="padding: 22px; display: flex; flex-direction: column; gap: 14px; text-align: left">'
    '<div style="display: flex; align-items: center; gap: 12px; padding-bottom: 6px"><span class="ui" style="width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex: none">' + ICON_D.format(s=22) + '</span>'
    '<div style="display: flex; flex-direction: column; gap: 2px"><span style="font-weight: 600; font-size: 16px; letter-spacing: -.01em">Tagent</span><span class="muted" style="font-size: 12.5px">Utrecht en omstreken</span></div>'
    '<span class="pill pill-ember t-pop" style="margin-left: auto; animation-delay: 2.1s">' + CHECK + 'Op maat</span></div>'
    + "".join(f'<div class="t-pop" style="display: flex; align-items: center; gap: 10px; padding-top: 12px; border-top: 1px solid rgba(238,234,227,.1); font-size: 13.5px; animation-delay: {0.7 + i * 0.3:.2f}s">{CHECK}<span>{a}</span><span class="muted" style="margin-left: auto">{b}</span></div>'
              for i, (a, b) in enumerate([("Websiteontwerp", "eerste ontwerp op maat"), ("Beheerscherm", "zelf aanpassen"), ("Optimalisatie", "snel en vindbaar"), ("Beheer", "optioneel")]))
    + '</div></div>')

# =====================================================================
# HOME
# =====================================================================
hero_site = '<div class="hero-site hero-out" aria-hidden="true">' + browser(
    '<b>jouwbedrijf.nl</b>',
    '''<div class="ms">
<div class="ms-nav t-in" style="animation-delay: .7s"><span>Jouw zaak</span><span><i></i><i></i><i></i></span></div>
<div class="ms-title t-in" style="animation-delay: .9s">Vers van de <em class="serif-i">zaak.</em></div>
<div class="ms-img t-pop" style="animation-delay: 1.15s; height: 110px"><img src="assets/d1.webp" alt=""></div>
<div class="ms-line t-gx" style="width: 88%; animation-delay: 1.4s"></div>
<div class="ms-line t-gx" style="width: 62%; animation-delay: 1.5s"></div>
<div class="ms-row t-in" style="animation-delay: 1.7s"><span class="ms-btn">Reserveer</span><span class="ms-btn ghost">Bekijk menu</span></div>
</div>''', style="position: relative") + '''
<div class="t-pop" style="display: flex; align-items: center; gap: 10px; margin-top: 14px; animation-delay: 2.1s"><span class="pill pill-ember">''' + CHECK + '''Nieuw ontwerp klaar</span><span class="scribble" style="font-size: 22px">eerst zien, dan beslissen</span></div>
</div>'''

old_win = browser('oud.jouwbedrijf.nl', '''<div class="old">
<div class="old-hd">Welkom op onze website!!</div>
<div class="old-nav"><span>Home</span><span>Over ons</span><span>Menu</span><span>Contact</span><span>Gastenboek</span></div>
<div class="old-body"><div class="old-side"><span>Nieuws</span><span>Fotoalbum</span><span>Links</span><span>Route</span></div>
<div style="display: flex; flex-direction: column; gap: 6px"><b>Wij zijn al jaren uw adres voor ...</b><span>Klik hier voor onze openingstijden. Bel voor een afspraak of reservering. Deze site is het best te bekijken in 1024x768.</span><div class="old-ph">foto.jpg</div></div></div>
</div>''', style="position: relative")

new_win = browser('<b>jouwbedrijf.nl</b>', minisite('Vers van de <em class="serif-i">zaak.</em>', 'ember.webp'), style="position: relative; box-shadow: 0 0 0 1px rgba(255,106,43,.55), 0 60px 120px -40px rgba(0,0,0,.8)")

statement = ("Een website is de eerste kennismaking met een bedrijf. <br> Bij een verouderde website "
             "haakt een bezoeker af nog vóór het eerste contact.")

def card(num, title, text, scene, link=None):
    lk = f'<a class="ulink" href="{link[0]}" style="align-self: flex-start">{link[1]} {ARR}</a>' if link else ""
    return f'''
<article class="card reveal" style="display: flex; flex-direction: column">
{scene}
<div style="padding: 36px; display: flex; flex-wrap: wrap; gap: 16px 40px; justify-content: space-between">
<p class="label">{num}</p>
<div style="flex: 1 1 320px; display: flex; flex-direction: column; gap: 12px">
<h3 class="h3">{title}</h3>
<p class="body muted">{text}</p>
{lk}
</div>
</div>
</article>'''

def chip(name, r0, kind="pg"):
    return f'<div class="win s-in" style="padding: 9px 11px; display: flex; align-items: center; gap: 8px; font-size: 12px; white-space: nowrap; overflow: hidden; animation-range: cover {r0}% cover {r0 + 3}%"><span style="width: 16px; height: 12px; border: 1.3px solid rgba(238,234,227,.55); border-radius: 3px; flex: none; position: relative"></span><span style="overflow: hidden; text-overflow: ellipsis">{name}</span></div>'

fan = lambda col, rng: f'''<svg viewBox="0 0 300 40" preserveAspectRatio="none" aria-hidden="true" style="width: 100%; height: 40px; display: block">
<path class="s-draw" pathLength="1000" vector-effect="non-scaling-stroke" d="M 150 0 C 150 24, 50 16, 50 40" fill="none" stroke="{col}" stroke-width="1.5" style="stroke-dasharray: 1000; --len: 1000; animation-range: {rng}"></path>
<path class="s-draw" pathLength="1000" vector-effect="non-scaling-stroke" d="M 150 0 L 150 40" fill="none" stroke="{col}" stroke-width="1.5" style="stroke-dasharray: 1000; --len: 1000; animation-range: {rng}"></path>
<path class="s-draw" pathLength="1000" vector-effect="non-scaling-stroke" d="M 150 0 C 150 24, 250 16, 250 40" fill="none" stroke="{col}" stroke-width="1.5" style="stroke-dasharray: 1000; --len: 1000; animation-range: {rng}"></path></svg>'''
fan_in = lambda col, rng: fan(col, rng).replace("M 150 0 C 150 24, 50 16, 50 40", "M 50 0 C 50 24, 150 16, 150 40").replace("M 150 0 C 150 24, 250 16, 250 40", "M 250 0 C 250 24, 150 16, 150 40")

scene1 = f'''<div class="scene" style="position: relative; height: 540px; background: #0C0C0A; overflow: hidden; display: flex; align-items: center; justify-content: center; color: #EEEAE3; padding: 28px 20px">
<img class="plx" src="assets/d1.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .5">
<div style="position: relative; width: min(560px, 100%); display: flex; flex-direction: column; align-items: center">
<div class="win s-pop" style="padding: 10px 16px; display: flex; align-items: center; gap: 10px; animation-range: cover 10% cover 14%"><span class="pulse-dot"></span><span>jouwbedrijf.nl</span><span class="pill" style="padding: 3px 9px; font-size: 11px">huidige site</span></div>
{fan("rgba(238,234,227,.5)", "cover 14% cover 18%")}
<div style="width: 100%; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px">
{chip("Home", 18)}{chip("Over ons", 20)}{chip("Menukaart", 22)}{chip("Reserveren", 24)}{chip("Contact", 26)}{chip("Privacy", 28)}
</div>
{fan_in("rgba(255,106,43,.7)", "cover 31% cover 34%")}
<div class="win s-pop" style="padding: 11px 16px; display: flex; align-items: center; gap: 10px; box-shadow: 0 0 0 1px rgba(255,106,43,.7), 0 40px 80px -30px rgba(0,0,0,.8); animation-range: cover 34% cover 38%">{CHECK}<span>Nieuw ontwerp · 6 pagina's</span></div>
<span class="scribble s-pop" style="margin-top: 16px; font-size: 22px; animation-range: cover 38% cover 42%">teksten mee, indien gewenst</span>
</div>
</div>'''

scene2 = f'''<div class="scene" style="position: relative; height: 480px; background: #0C0C0A; overflow: hidden; display: flex; align-items: center; justify-content: center; color: #EEEAE3; padding: 28px 20px">
<img class="plx" src="assets/d3.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .55">
<div style="position: relative; width: min(400px, 100%)">
{browser('<b>ontwerp</b> · versie 2', minisite('Vers van de <em class="serif-i">zaak.</em>', 'd3.webp'), style="position: relative")}
<span class="pin s-pop" style="right: -18px; top: 120px; animation-range: cover 14% cover 18%"><b>1</b>Foto groter?</span>
<span class="pin s-pop" style="left: -22px; top: 168px; animation-range: cover 19% cover 23%"><b>2</b>Openingstijden erbij</span>
<div style="position: absolute; left: 0; right: 0; bottom: -58px; display: flex; justify-content: center; gap: 10px; align-items: center">
<span class="s-press" style="padding: 9px 16px; border-radius: 999px; background: #EEEAE3; color: #0C0C0A; font-size: 13px; font-weight: 500; animation-range: cover 26% cover 30%">Akkoord</span>
<span class="pill pill-ember s-pop" style="animation-range: cover 30% cover 34%">{CHECK}Ontwerp akkoord</span>
</div>
</div>
</div>'''

def adm_page(name, on=True, cur=False, tog_cls="", rng=""):
    st = f' style="animation-range: {rng}"' if rng else ""
    return f'<div class="adm-pg{" on" if cur else ""}"><span>{name}</span><span class="toggle{" toggle-on" if on else ""} {tog_cls}"{st}><i></i></span></div>'

admin = f'''<div class="win" style="position: relative; width: 100%">
<div class="bw-top"><span class="ui-dot"></span><span class="ui-dot"></span><span class="ui-dot"></span><span class="bw-url">jouwbedrijf.nl/<b>admin</b></span></div>
<div class="adm">
<div class="adm-side"><span>Pagina's · zichtbaar</span>
{adm_page("Home", cur=True)}{adm_page("Menukaart")}{adm_page("Reserveren")}{adm_page("Zomeractie", tog_cls="s-tog", rng="cover 30% cover 33%")}{adm_page("Vacatures", on=False)}
</div>
<div class="adm-main">
<div class="adm-f"><span>Openingstijden</span><div class="adm-in"><span class="strike s-strike" style="animation-range: cover 14% cover 19%">Di t/m za 11–22</span><b class="s-pop" style="font-weight: 500; animation-range: cover 18% cover 22%">Di t/m zo 11–23</b></div></div>
<div class="adm-f"><span>Foto bovenaan</span><div class="adm-in"><span class="s-pop" style="width: 46px; height: 30px; border-radius: 6px; overflow: hidden; position: relative; animation-range: cover 22% cover 26%"><img src="assets/ember.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover"></span><span class="muted" style="font-size: 11.5px">terras-zomer.jpg</span></div></div>
<div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap">
<span class="s-press" style="padding: 8px 14px; border-radius: 999px; background: #EEEAE3; color: #0C0C0A; font-size: 12px; font-weight: 500; animation-range: cover 34% cover 37%">Publiceren</span>
<span class="pill pill-ember s-pop" style="animation-range: cover 37% cover 40%">{CHECK}Live op jouwbedrijf.nl</span>
</div>
</div>
</div>
</div>'''

scene3 = f'''<div class="scene" style="position: relative; min-height: 480px; background: #0C0C0A; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; color: #EEEAE3; padding: 32px 22px">
<img class="plx" src="assets/d4.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .55">
<div style="position: relative; width: min(560px, 100%)">{admin}</div>
<span class="scribble s-pop" style="position: relative; font-size: 22px; animation-range: cover 40% cover 44%">zelf aanpassen, de lay-out blijft strak</span>
</div>'''

scene4 = f'''<div class="scene" style="position: relative; height: 440px; background: #0C0C0A; overflow: hidden; display: flex; align-items: center; justify-content: center; color: #EEEAE3; padding: 28px 20px">
<img class="plx" src="assets/d2.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .7">
<div style="position: relative; width: min(500px, 100%); height: 340px">
<div class="s-in" style="position: absolute; left: 0; top: 0; width: 76%; animation-range: cover 12% cover 18%">{browser('<b>jouwbedrijf.nl</b>', minisite('Vers van de <em class="serif-i">zaak.</em>', 'd2.webp'), style="position: relative")}</div>
<div class="phone s-from" style="position: absolute; right: 0; bottom: 0; --fx: 40px; --fy: 30px; animation-range: cover 18% cover 26%"><div class="phone-in">{minisite('Vers van de <em class="serif-i">zaak.</em>', 'd2.webp', buttons=("Reserveer", "Menu"))}</div></div>
<span class="scribble s-pop s4-scrib" style="position: absolute; left: 4%; bottom: -6px; font-size: 22px; animation-range: cover 26% cover 30%">op elk scherm even strak</span>
</div>
</div>'''

def hcard(num, title, text, img, inner):
    return f'''<a href="diensten.html" class="card zoom" style="flex: none; width: clamp(270px, 24vw, 340px); display: flex; flex-direction: column">
<div class="media" style="height: 220px; display: flex; align-items: center; justify-content: center; padding: 18px"><img src="assets/{img}" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .45">
{inner}</div>
<div style="padding: 22px 24px 24px; display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; justify-content: space-between; align-items: center"><span class="label">{num}</span><span class="tile-arrow" style="width: 34px; height: 34px; border-radius: 50%; border: 1px solid rgba(238,234,227,.2); display: inline-flex; align-items: center; justify-content: center">{ARR14}</span></div>
<span class="h3" style="font-size: 26px">{title}</span>
<span class="body muted" style="font-size: 14.5px; line-height: 1.5">{text}</span>
</div>
</a>'''

def rows(items, delay0=.1):
    return "".join(f'<div class="cell-in" style="display: flex; justify-content: space-between; gap: 10px; padding: 8px 12px;{" border-top: 1px solid rgba(238,234,227,.1);" if i else ""} animation-delay: {delay0 + i * .25:.2f}s"><span>{a}</span><span style="color: {c}">{b}</span></div>' for i, (a, b, c) in enumerate(items))

M = "#A19C93"; E = "#FF6A2B"
hcards = "\n".join([
    hcard("01", "Horeca", "Menukaart en reserveren op één plek, ook op de telefoon.", "d3.webp",
          '<div class="win" style="position: relative; width: 100%; font-size: 11.5px">' + rows([("Voorgerechten", "bekijk", M), ("Hoofdgerechten", "bekijk", M), ("Tafel reserveren", "vanavond", E)]) + '</div>'),
    hcard("02", "Sport &amp; vrije tijd", "Zalen, activiteiten en agenda overzichtelijk bij elkaar.", "d4.webp",
          '<div class="win" style="position: relative; width: 100%; font-size: 11.5px">' + rows([("Zaal 1", "bezet", M), ("Zaal 2", "vrij", E), ("Agenda", "deze week", M)]) + '</div>'),
    hcard("03", "Praktijken &amp; wellness", "Behandelingen helder uitgelegd, met een knop om te boeken.", "d6.webp",
          '<div class="win" style="position: relative; width: 100%; font-size: 11.5px">' + rows([("Behandelingen", "bekijk", M), ("Tarieven", "bekijk", M), ("Afspraak maken", "online", E)]) + '</div>'),
    hcard("04", "Winkels", "Openingstijden, assortiment en route altijd actueel.", "d1.webp",
          '<div class="win" style="position: relative; width: 100%; font-size: 11.5px">' + rows([("Maandag", "gesloten", M), ("Di t/m za", "open", M), ("Vandaag", "open", E)]) + '</div>'),
    hcard("05", "Dienstverleners", "Diensten, werkgebied en een offerte in twee klikken.", "d5.webp",
          '<div class="win" style="position: relative; width: 100%; padding: 12px; display: flex; flex-direction: column; gap: 8px"><span class="cell-in" style="font-size: 11.5px; animation-delay: .1s">Offerte aanvragen</span><div class="doc-line" style="width: 100%"></div><div class="doc-line" style="width: 72%; animation-delay: .3s"></div><span class="cell-in" style="align-self: flex-start; padding: 5px 10px; border-radius: 999px; background: #FF6A2B; color: #0C0C0A; font-size: 10.5px; animation-delay: .9s">Versturen</span></div>'),
    hcard("06", "Verenigingen", "Nieuws en agenda, zelf bij te houden via het beheerscherm.", "d2.webp",
          '<div class="win" style="position: relative; width: 100%; font-size: 11.5px">' + rows([("Nieuw bericht", "vandaag", E), ("Ledenvergadering", "agenda", M), ("Toernooi", "agenda", M)]) + '</div>'),
])

orbit_groups = [
    ("Domein", "D", -60, [("Jouw domein", "D"), ("DNS", "D"), ("HTTPS", "H"), ("E-mail blijft", "E")]),
    ("Livegang", "L", 30, [("Online zetten", "O"), ("Beheerscherm", "B"), ("Veilige login", "V"), ("Eigen lettertypes", "L")]),
    ("Koppelingen", "K", 120, [("Reserveren", "R"), ("Google Maps", "G"), ("Agenda", "A"), ("Social media", "S")]),
    ("Vindbaarheid", "V", 210, [("Oude adressen", "O"), ("Doorverwijzingen", "D"), ("Search Console", "S"), ("Paginatitels", "P")]),
]
import math
orbit_html = ""
for name, l, a, subs in orbit_groups:
    r = math.radians(a)
    sub_html = ""
    for j, (sn, sl) in enumerate(subs):
        b = j / len(subs) * math.pi * 2 - math.pi / 2
        sub_html += f'<div class="sub-pos" style="left:{50 + 50 * math.cos(b):.2f}%;top:{50 + 50 * math.sin(b):.2f}%"><div class="sub-chip"><span class="sys sys-small"><span class="sys-logo">{sl}</span>{sn}</span></div></div>'
    orbit_html += f'<div class="orb-node" style="left:{50 + 34 * math.cos(r):.2f}%;top:{50 + 34 * math.sin(r):.2f}%"><div class="orb-up"><div class="sub-ring">{sub_html}</div><span class="sys sys-main"><span class="sys-logo">{l}</span>{name}</span></div></div>'

steps = [("01", "Kennismaking", "Het bedrijf, de huidige site en de wensen op een rij."),
         ("02", "Ontwerp", "Een ontwerp dat past bij het merk, op basis van wat er al is."),
         ("03", "Samen doorlopen", "Samen bijschaven tot alles klopt."),
         ("04", "Livegang", "Online op het eigen domein, met een eigen beheerscherm."),
         ("05", "Beheer", "Optioneel: per maand of per jaar. Zonder beheer kan ook.")]
steps_html = "".join(f'''<div style="display: flex; flex-direction: column; gap: 18px"><div class="rule line-in"></div><span class="count" style="font-size: clamp(64px, 6.4vw, 104px); font-weight: 500; letter-spacing: -.06em; line-height: 1">{n}</span><span style="font-size: 22px; font-weight: 500; letter-spacing: -.02em">{t}</span><span class="body muted" style="font-size: 15px">{d}</span></div>''' for n, t, d in steps)

promises = [("01", "Domein op eigen naam", "Het domein blijft van de eigenaar."),
            ("02", "Eerst zien", "Een eerste ontwerp op maat, gemaakt voor uw zaak. Bekijken, bespreken en pas dan beslissen."),
            ("03", "Veilig inloggen", "Met eigen e-mailadres en wachtwoord, via een vaste loginpagina."),
            ("04", "Overdracht bij opzegging", "Stoppen met beheer? Dan wordt de site overgedragen."),
            ("05", "Afspraken op papier", "Duidelijke afspraken over kosten en beheer, vastgelegd in een overeenkomst.")]
prom_html = "".join(f'''<div class="reveal" style="display: flex; flex-direction: column; gap: 14px; padding-block: 28px; border-top: 1px solid rgba(238,234,227,.14)"><span class="label">{n}</span><span style="font-size: 22px; font-weight: 500; letter-spacing: -.02em">{t}</span><span class="body muted" style="font-size: 15px">{d}</span></div>''' for n, t, d in promises)

audience = ["Restaurants", "Cafés", "Kapsalons", "Sportcentra", "Praktijken", "Winkels", "Hoveniers", "Bouwbedrijven", "Verenigingen", "Massagesalons", "Rijscholen", "Fotografen"]
marq = "".join(f'<span style="font-size: 26px; font-weight: 500; letter-spacing: -.03em; color: rgba(238,234,227,.38); white-space: nowrap">{a}</span>' for a in audience * 2)

home = head(f"{FULL} – Webdesign en websites voor ondernemers",
            "Websites ontwerpen, bouwen en beheren voor ondernemers. Eerst samen het ontwerp doorlopen, daarna zelf aanpassen via een eenvoudig beheerscherm.") + nav("index.html") + f'''
<!-- HERO -->
<section style="position: relative; height: min(calc(100svh - 72px), 900px); min-height: 680px; overflow: hidden">
<div class="media hero-out" style="position: absolute; inset: 0">
<img class="kb" src="assets/hero.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover">
<img class="kb-2" src="assets/hero.webp" alt="" style="width: 100%; height: 100%; object-fit: cover">
<div class="scrim"></div>
</div>
{hero_site}
<div class="wrap text-out" style="position: relative; height: 100%; display: flex; flex-direction: column; justify-content: center; gap: 36px; padding-block: 48px">
<h1 class="display hero-h">
<span class="line"><span style="animation-delay: .15s">Jouw website,</span></span>
<span class="line"><span style="animation-delay: .3s">maar dan <em class="serif-i">beter.</em></span></span>
</h1>
<div class="hero-copy" style="display: flex; flex-direction: column; gap: 32px">
<p class="lead fade-up" style="max-width: 34rem; animation-delay: .6s; color: rgba(238,234,227,.82)">Websites voor ondernemers die strak ogen, snel laden en op elk scherm kloppen. Eerst een ontwerp op maat zien, daarna zelf de inhoud bijhouden via een eenvoudig beheerscherm.</p>
<div class="fade-up" style="display: flex; flex-wrap: wrap; gap: 10px; animation-delay: .75s">
{btn("kennismaking.html", "Plan een kennismaking")}
<a class="btn btn-ghost" href="werkwijze.html">Zo werkt het</a>
</div>
</div>
</div>
</section>

<!-- 01 VAN OUD NAAR NIEUW -->
<section class="wrap" style="padding-top: 140px; padding-bottom: 56px">
<div class="reveal" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 24px 64px">
<p class="h2" style="max-width: 18ch">Alles gaat mee. Behalve de <em class="serif-i">verouderde</em> uitstraling.</p>
<p class="lead muted" style="max-width: 30rem">Alle benodigde pagina's, foto's en links verhuizen naar een nieuw ontwerp dat bij het merk past. Teksten kunnen meeverhuizen, indien gewenst. Oude links blijven gewoon werken.</p>
</div>
</section>
<div class="expand media band" style="height: 640px">
<img class="plx" src="assets/ember.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover">
<div style="position: absolute; inset: 0; background: rgba(12,12,10,.3)"></div>
<div class="float band-old" style="position: absolute; left: 6%; top: 12%; width: min(420px, 40%)">
<span class="pill" style="margin-bottom: 12px; background: rgba(12,12,10,.55)">Voor</span>
<div style="position: relative; filter: saturate(.7)">{old_win}<div class="scan"></div></div>
</div>
<div class="float band-new" style="position: absolute; right: 6%; bottom: 9%; width: min(400px, 40%); animation-delay: -4.5s">
<span class="pill pill-ember" style="margin-bottom: 12px">Na</span>
{new_win}
</div>
<svg class="hand band-arrow" viewBox="0 0 220 80" aria-hidden="true" style="left: 41%; top: 44%; width: 17%; height: 80px"><path class="draw" d="M 6 20 C 60 70, 140 70, 200 34 M 186 26 L 202 33 L 192 47" style="stroke-dasharray: 600"></path></svg>
</div>

<!-- DOELGROEP -->
<section style="padding-block: 96px; border-bottom: 1px solid rgba(238,234,227,.12)">
<div class="marquee"><div class="marquee-track">{marq}</div></div>
</section>

<!-- 02 STATEMENT -->
<section class="words-scope" style="height: 2200px; position: relative">
<div style="position: sticky; top: 0; height: min(100svh, 920px); display: flex; align-items: center">
<div class="wrap" style="width: 100%">
<p style="margin: 0; max-width: 24ch; font-weight: 500; font-size: clamp(34px, 4.8vw, 76px); line-height: 1.03; letter-spacing: -.04em">{words(statement)}</p>
</div>
</div>
</section>

<!-- 03 WAT IK DOE -->
<section class="light">
<div class="wrap" style="padding-block: 160px; display: flex; flex-wrap: wrap; gap: 64px 80px">
<div style="flex: 1 1 340px; min-width: 0">
<div style="position: sticky; top: 140px; display: flex; flex-direction: column; gap: 28px">
<h2 class="h2">Van eerste ontwerp tot <em class="serif-i">eigen</em> beheer.</h2>
<p class="body muted" style="max-width: 26rem">Een website die er goed uitziet, is pas het begin. Het moet kloppen, werken op elk scherm en makkelijk bij te houden zijn.</p>
<a class="ulink" href="diensten.html" style="align-self: flex-start">Bekijk alle diensten {ARR}</a>
</div>
</div>
<div style="flex: 2 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 24px">
{card("01", "Ontwerp vanuit de huidige site", "Alle benodigde pagina's, knoppen en links gaan mee, net als reserveringen, formulieren en downloads. Teksten kunnen meeverhuizen, indien gewenst.", scene1)}
{card("02", "Samen doorlopen, tot alles klopt", "Het ontwerp wordt samen doorgelopen en bijgeschaafd. Pas als alles klopt, volgt de oplevering.", scene2)}
{card("03", "Zelf aanpassen via een beheerscherm", "Teksten, foto's en openingstijden zelf bijwerken, binnen de vaste lay-out. Een pagina tijdelijk niet nodig? Uitzetten, en hij verdwijnt uit menu en links.", scene3, ("diensten.html#beheerscherm", "Meer over het beheerscherm"))}
{card("04", "Op elk scherm even strak", "Ontworpen voor telefoon, tablet en laptop. Vloeiende beweging bij het scrollen, alles netjes in beeld.", scene4)}
</div>
</div>
</section>

<!-- 04 TECHNIEK (ORBIT) -->
<section class="media" style="padding-block: 140px; overflow: hidden">
<img class="plx" src="assets/d4.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover">
<div style="position: absolute; inset: 0; background: rgba(12,12,10,.5)"></div>
<div class="wrap" style="position: relative; display: flex; flex-direction: column; gap: 40px">
<div class="reveal" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 24px">
<div style="display: flex; flex-direction: column; gap: 24px">
<h2 class="h2" style="max-width: 16ch">De techniek, ook <em class="serif-i">geregeld.</em></h2>
</div>
<p class="body" style="max-width: 26rem; color: rgba(238,234,227,.75)">Domein, livegang, reserveringssysteem en de vindbaarheid van oude pagina's. Het werkt, zonder er zelf in te hoeven duiken.</p>
</div>
<div class="orbit-wrap orbit-in" role="img" aria-label="{BRAND} in het midden, verbonden met domein, livegang, koppelingen en vindbaarheid">
<div class="ring" style="inset: 16%"></div>
<div class="ring ring-dash" style="inset: 32%"></div>
<div class="orb-rot" aria-hidden="true">{orbit_html}</div>
<div aria-hidden="true" style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; gap: 14px">
<span class="ui" style="width: 120px; height: 120px; border-radius: 32px; display: flex; align-items: center; justify-content: center">{ICON_D.format(s=50)}</span>
<span style="font-size: 15px; font-weight: 500; letter-spacing: -.02em">Jouw site</span>
</div>
</div>
</div>
</section>

<!-- 05 VOOR ELKE ZAAK -->
<section class="hs-section">
<div class="hs-sticky">
<div class="wrap" style="width: 100%; padding-block: 40px">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 20px; margin-bottom: 36px">
<div style="display: flex; flex-direction: column; gap: 16px">
<h2 class="h2" style="font-size: clamp(36px, 4.4vw, 64px)">Voor <em class="serif-i">elke</em> zaak.</h2>
</div>
<a class="ulink" href="diensten.html">Bekijk de diensten {ARR}</a>
</div>
<div class="hs-track">
{hcards}
</div>
</div>
</div>
</section>

<!-- 06 WERKWIJZE -->
<section class="wrap" style="padding-block: 56px 160px; display: flex; flex-direction: column; gap: 80px">
<div class="reveal" style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 24px 64px; align-items: flex-end">
<div style="display: flex; flex-direction: column; gap: 24px">
<h2 class="h2" style="max-width: 14ch">In vijf stappen <em class="serif-i">online.</em></h2>
</div>
<a class="ulink" href="werkwijze.html">Lees de werkwijze {ARR}</a>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px 32px">{steps_html}</div>
</section>

<!-- 08 AFSPRAKEN -->
<section class="wrap" style="padding-block: 140px; display: flex; flex-direction: column; gap: 56px">
<div class="reveal" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 24px">
<h2 class="h2" style="max-width: 16ch">Afspraken die <em class="serif-i">kloppen.</em></h2>
<a class="ulink" href="werkwijze.html#vragen">Veelgestelde vragen {ARR}</a>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0 28px">{prom_html}</div>
</section>
''' + cta_block('Begin met <em class="serif-i">één</em> gesprek.', "Een korte kennismaking, met de link van de huidige site erbij. Daarna volgt een eerlijk advies over wat beter kan.") + footer() + tail(height=11000)
pages["index.html"] = home

# =====================================================================
# DIENSTEN
# =====================================================================
def svc(id_, num, title, text, ticks, vis, light=False):
    t = "".join(f"<li>{x}</li>" for x in ticks)
    return f'''<div id="{id_}" class="svc">
<div class="svc-txt reveal">
<h2 class="h2" style="font-size: clamp(34px, 3.8vw, 58px)">{title}</h2>
<p class="body muted" style="font-size: 17px; max-width: 34rem">{text}</p>
<ul class="ticks">{t}</ul>
</div>
<div class="svc-vis scene reveal">{vis}</div>
</div>'''

wire = f'''<img class="plx" src="assets/d5.webp" alt="">
<div style="position: relative; width: min(400px, 100%)">{browser('<b>nieuw</b>.jouwbedrijf.nl', """<div class="ms">
<div class="ms-nav s-in" style="animation-range: cover 12% cover 16%"><span>Jouw zaak</span><span><i></i><i></i><i></i></span></div>
<div class="ms-title s-in" style="animation-range: cover 15% cover 20%">Een eerste <em class="serif-i">indruk.</em></div>
<div class="ms-img s-gx" style="animation-range: cover 19% cover 25%"><img src="assets/d5.webp" alt=""></div>
<div class="ms-line s-gx" style="width: 90%; animation-range: cover 24% cover 28%"></div>
<div class="ms-line s-gx" style="width: 64%; animation-range: cover 26% cover 30%"></div>
<div class="ms-row s-in" style="animation-range: cover 29% cover 33%"><span class="ms-btn">Neem contact op</span></div></div>""", style="position: relative")}</div>'''

redesign_vis = f'''<img class="plx" src="assets/ember.webp" alt="">
<div style="position: relative; width: min(470px, 100%); height: 330px">
<div style="position: absolute; left: 0; top: 0; width: 64%; filter: saturate(.7)">{old_win}</div>
<div class="s-from" style="position: absolute; right: 0; bottom: 0; width: 62%; --fx: 30px; --fy: 20px; animation-range: cover 15% cover 26%">{new_win}</div>
</div>'''

admin_vis = f'''<img class="plx" src="assets/d4.webp" alt="">
<div style="position: relative; width: min(540px, 100%)">{admin}</div>'''

dns_rows = [("jouwbedrijf.nl gekoppeld", 14), ("HTTPS actief", 18), ("E-mail ongewijzigd", 22), ("Oude adressen doorverwezen", 26), ("Lettertypes zelf gehost", 30)]
live_vis = f'''<img class="plx" src="assets/d2.webp" alt="">
<div class="win" style="position: relative; width: min(420px, 100%); text-align: left">
<div class="bw-top"><span class="ui-dot"></span><span class="ui-dot"></span><span class="ui-dot"></span><span class="bw-url">Livegang · checklist</span></div>
{"".join(f'<div class="s-in" style="display: flex; align-items: center; gap: 12px; padding: 13px 16px;{" border-top: 1px solid rgba(238,234,227,.1);" if i else ""} font-size: 13.5px; animation-range: cover {r}% cover {r + 4}%">{CHECK}<span>{t}</span></div>' for i, (t, r) in enumerate(dns_rows))}
<div style="padding: 14px 16px; border-top: 1px solid rgba(238,234,227,.1)"><span class="pill pill-ember s-pop" style="animation-range: cover 34% cover 38%"><span class="pulse-dot"></span>Online</span></div>
</div>'''

plan_vis = f'''<img class="plx" src="assets/d6.webp" alt="">
<div class="win" style="position: relative; width: min(400px, 100%); padding: 22px; display: flex; flex-direction: column; gap: 16px; text-align: left">
<span style="font-weight: 500; font-size: 15px">Beheer</span>
<div style="display: inline-flex; align-self: flex-start; padding: 4px; border-radius: 999px; background: rgba(238,234,227,.07); font-size: 12.5px"><span class="s-pop" style="padding: 7px 14px; border-radius: 999px; background: #EEEAE3; color: #0C0C0A; font-weight: 500; animation-range: cover 14% cover 18%">Per maand</span><span style="padding: 7px 14px; border-radius: 999px; color: #A19C93">Per jaar</span><span style="padding: 7px 14px; border-radius: 999px; color: #A19C93">Zonder beheer</span></div>
{"".join(f'<div class="s-in" style="display: flex; align-items: center; gap: 10px; font-size: 13.5px; animation-range: cover {r}% cover {r + 4}%">{CHECK}<span>{t}</span></div>' for t, r in [("Login-dienst en hosting geregeld", 18), ("Hulp als er iets niet werkt", 21), ("Losse aanpassingen mogelijk", 24)])}
<span class="muted" style="font-size: 12.5px">Prijzen op aanvraag</span>
</div>'''

diensten = head(f"{FULL} – Diensten", "Nieuwe website, redesign van je huidige site, beheerscherm, livegang op je eigen domein en beheer.") + nav("diensten.html") + page_hero(
    ["Alles voor een site", 'die <em class="serif-i">werkt.</em>'],
    "Van nieuw ontwerp tot livegang op het eigen domein. Daarna een beheerscherm om alles zelf bij te houden.", "d1.webp", visual=DIENSTEN_VIS) + f'''
<section class="wrap" style="padding-top: 40px; padding-bottom: 80px">
{svc("nieuw", "01 — Nieuwe website", 'Een nieuwe <em class="serif-i">website.</em>', "Nog geen site, of één die niet meer past? Een ontwerp vanaf de basis, afgestemd op merk en klanten.", ["Ontwerp in de eigen huisstijl", "Eigen teksten en foto's, geen stockbeeld", "Werkt op telefoon, tablet en laptop"], wire)}
{svc("redesign", "02 — Redesign", 'De huidige site, <em class="serif-i">vernieuwd.</em>', "De bestaande site is de basis. Alles wat nodig is gaat mee, in een moderne lay-out met rustige beweging.", ["Alle benodigde pagina's, foto's en links mee, teksten indien gewenst", "Reserverings- en boekingsmodules overgenomen", "Oude adressen blijven werken of worden doorverwezen"], redesign_vis)}
{svc("beheerscherm", "03 — Beheerscherm", 'Zelf aanpassen, <em class="serif-i">zonder</em> gedoe.', "Na akkoord krijgt de site een beheerscherm. De lay-out blijft precies zoals ontworpen; alleen de inhoud is aan te passen.", ["Alle pagina's bewerkbaar: teksten, foto's, openingstijden", "Pagina's verbergen of weer tonen", "Inloggen met eigen e-mailadres en wachtwoord", "Een proefversie om eerst rustig te oefenen"], admin_vis)}
{svc("livegang", "04 — Livegang", 'Online op het <em class="serif-i">eigen</em> domein.', "De site gaat online en het domein wordt gekoppeld. E-mail op dat domein blijft gewoon werken.", ["Domein blijft op eigen naam", "Beveiligde verbinding (HTTPS)", "Lettertypes zelf gehost, netjes voor de privacy"], live_vis)}
{svc("beheer", "05 — Beheer", 'Daarna, alles <em class="serif-i">geregeld.</em>', "Beheer per maand of per jaar, met hulp bij het aanpassen, opstellen en toevoegen van pagina's en functies. Liever alles zelf doen? Dan kan ook alleen de website met beheerscherm, zonder maand- of jaarkosten.", ["Beheer per maand of per jaar", "Hulp bij nieuwe pagina's, functies en aanpassingen", "Of alleen website en beheerscherm, zonder vaste kosten", "Bij opzegging wordt de site overgedragen"], plan_vis)}
</section>
''' + cta_block('Welke aanpak past bij <em class="serif-i">jou?</em>', "Een kort gesprek maakt duidelijk wat er nodig is. Daarna volgt een voorstel én eerste ontwerp op maat.") + footer() + tail(height=7000)
pages["diensten.html"] = diensten

# =====================================================================
# WERKWIJZE
# =====================================================================
wsteps = [
    ("01", "Kennismaking", "Een gesprek over het bedrijf, de klanten en de huidige site. Wat werkt goed, wat mist er, en wat moet zelf aan te passen zijn?", "kennismaking.html", "Plan een kennismaking"),
    ("02", "Ontwerp", "Een ontwerp op basis van de huidige site en huisstijl: kleuren, lettertypes, eigen foto's en eigen teksten. Alle benodigde pagina's en links gaan mee.", None, None),
    ("03", "Samen doorlopen", "Het ontwerp wordt samen doorgelopen en bijgeschaafd tot alles naar wens is. Pas dan volgt het akkoord.", None, None),
    ("04", "Beheerscherm en livegang", "Na akkoord krijgt de site een beheerscherm in dezelfde lay-out. Daarna gaat hij online op het eigen domein, met de afspraken vastgelegd in een overeenkomst.", "diensten.html#beheerscherm", "Over het beheerscherm"),
    ("05", "Beheer", "Beheer per maand of per jaar, met hulp bij aanpassingen, nieuwe pagina's en functies. Zonder beheer kan ook: dan is het de website met beheerscherm, zonder maand- of jaarkosten.", "diensten.html#beheer", "Over beheer"),
]
wsteps_html = "".join(f'''<div class="reveal" style="display: flex; flex-wrap: wrap; gap: 20px 64px; padding-block: 48px; border-top: 1px solid rgba(238,234,227,.14)">
<span class="count" style="flex: 0 0 160px; font-size: clamp(56px, 6vw, 96px); font-weight: 500; letter-spacing: -.06em; line-height: 1">{n}</span>
<div style="flex: 1 1 420px; min-width: 0; display: flex; flex-direction: column; gap: 14px">
<h3 class="h3">{t}</h3>
<p class="body muted" style="font-size: 17px; max-width: 40rem">{d}</p>
{f'<a class="ulink" href="{h}" style="align-self: flex-start">{lt} {ARR}</a>' if h else ""}
</div></div>''' for n, t, d, h, lt in wsteps)

faqs = [
    ("Wat kost een website?", "Dat hangt af van het aantal pagina's en wat erin moet. Na de kennismaking volgt een voorstel met een prijs op maat."),
    ("Hoe lang duurt het?", "Dat hangt af van de omvang en van het samen doorlopen van het ontwerp. Doorgaans staat een website binnen twee weken online. De planning wordt in de kennismaking afgesproken."),
    ("Is beheer verplicht?", "Nee. Alleen de website met beheerscherm afnemen kan ook, zonder maand- of jaarkosten. Met beheer helpt Tagent bij het aanpassen, opstellen en toevoegen van pagina's en functies."),
    ("Wat is er nodig om te starten?", "De link van de huidige site (als die er is), het logo, foto's en de wensen. Teksten van de huidige site kunnen meeverhuizen, indien gewenst."),
    ("Is de site zelf aan te passen?", "Ja. Via het beheerscherm zijn teksten, foto's en openingstijden aan te passen en pagina's aan of uit te zetten. De lay-out blijft vast, zodat alles strak blijft."),
    ("Van wie is het domein?", "Van het bedrijf zelf. Het domein blijft op eigen naam, en de kosten daarvan ook. Vaak is er al een domein."),
    ("Wat gebeurt er bij stoppen met beheer?", "Dan wordt de site overgedragen."),
    ("Blijft het reserveringssysteem werken?", "Bestaande reserverings- en boekingsmodules worden overgenomen met dezelfde koppeling. Niets hoeft opnieuw te worden ingericht."),
    ("Werken oude links nog?", "Ja. Oude adressen blijven gelijk of worden doorgestuurd naar de nieuwe pagina. Links vanuit Google, social media en flyers blijven werken."),
    ("Werkt de site op een telefoon?", "Ja, elke pagina is ontworpen voor telefoon, tablet en laptop."),
]
faq_html = "".join(f'<details class="faq"><summary>{q}<span class="plus"></span></summary><p>{a}</p></details>' for q, a in faqs)

werkwijze = head(f"{FULL} – Werkwijze", "Zo werkt het: kennismaking, ontwerp, samen doorlopen, beheerscherm en livegang, beheer. Plus veelgestelde vragen.") + nav("werkwijze.html") + page_hero(
    ["Eerst zien,", 'dan <em class="serif-i">beslissen.</em>'],
    "Een eerste ontwerp op maat, gemaakt voor uw zaak. Bekijken, bespreken en pas dan beslissen.", "d3.webp", visual=WERKWIJZE_VIS) + f'''
<section class="wrap" style="padding-block: 24px 140px">
<div class="reveal" style="display: flex; flex-direction: column; gap: 24px; margin-bottom: 56px">
<h2 class="h2" style="max-width: 16ch">Van gesprek tot <em class="serif-i">live.</em></h2>
</div>
{wsteps_html}
</section>
<section id="vragen" class="light">
<div class="wrap" style="padding-block: 140px; display: flex; flex-wrap: wrap; gap: 48px 80px">
<div style="flex: 1 1 300px; min-width: 0"><div style="position: sticky; top: 120px; display: flex; flex-direction: column; gap: 24px">
<h2 class="h2">Goed om te <em class="serif-i">weten.</em></h2>
<p class="body muted" style="max-width: 24rem">Staat een vraag er niet tussen? Stel hem gerust in de kennismaking.</p>
</div></div>
<div class="faq-list" style="flex: 2 1 520px; min-width: 0; border-bottom: 1px solid rgba(12,12,10,.12)">{faq_html}</div>
</div>
</section>
''' + cta_block('Klaar voor een nieuwe <em class="serif-i">site?</em>', "Stuur bij de aanvraag de link van de huidige site mee. Dan wordt er vooraf al even meegekeken.", second=("diensten.html", "Bekijk de diensten")) + footer() + tail(height=6000)
werkwijze = werkwijze.replace('<details class="faq">', '<details class="faq" style="border-color: rgba(12,12,10,.12)">').replace('<p>', '<p>', 0)
pages["werkwijze.html"] = werkwijze

# =====================================================================
# OVER ONS
# =====================================================================
over_words = ("Een goede website voelt vanzelfsprekend. Alles is snel te vinden, alles klopt, en de ondernemer houdt hem zelf bij. "
              "Dat is de maatstaf voor elke site.")
vals = [("Eerst zien", "Een eerste ontwerp op maat, gemaakt voor uw zaak. Bekijken, bespreken en pas dan beslissen.", "d1.webp",
         '<div class="win" style="padding: 10px 14px; display: flex; gap: 10px; align-items: center; font-size: 12.5px"><span style="padding: 6px 12px; border-radius: 999px; background: #EEEAE3; color: #0C0C0A; font-weight: 500">Akkoord</span><span class="muted">ontwerp op maat bekeken</span></div>'),
        ("Eerlijk", "Echte foto's, echte openingstijden, echte reviews. Wat nog niet duidelijk is, wordt samen afgestemd.", "d3.webp",
         '<div class="win" style="width: 100%; font-size: 12.5px">' + "".join(f'<div style="display: flex; gap: 10px; align-items: center; padding: 9px 14px;{" border-top: 1px solid rgba(238,234,227,.1);" if i else ""}">{ic}<span>{a}</span><span style="margin-left: auto; color: {c}">{b}</span></div>' for i, (ic, a, b, c) in enumerate([(CHECK, "Foto's", "eigen beeld", "#A19C93"), (CHECK, "Openingstijden", "huidige site", "#A19C93"), ('<span style="width: 14px; height: 14px; border-radius: 50%; border: 1.5px dashed #FF6A2B; flex: none"></span>', "Klantreview", "samen afstemmen", "#FF6A2B")])) + '</div>'),
        ("Zelf in de hand", "De inhoud zelf aanpassen, en het domein blijft op eigen naam.", "d4.webp",
         '<div class="win" style="padding: 10px 14px; display: flex; gap: 10px; align-items: center; font-size: 12.5px"><span class="toggle toggle-on"><i></i></span><span>jouwbedrijf.nl</span><span class="muted">op eigen naam</span></div>')]
vals_html = "".join(f'''<div class="card reveal" style="display: flex; flex-direction: column">
<div class="media" style="aspect-ratio: 4 / 3"><img class="plx" src="assets/{img}" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .75"><div style="position: absolute; left: 24px; top: 24px; right: 24px; display: flex">{ui}</div><span class="h3" style="position: absolute; left: 28px; bottom: 24px; font-size: clamp(30px, 2.8vw, 40px)">{t}</span></div>
<p class="body muted" style="padding: 26px 28px 30px; font-size: 16px">{d}</p></div>''' for t, d, img, ui in vals)

info_rows = [("Specialisme", "Websiteontwerp, -beheer en -optimalisatie"), ("Werkgebied", "Utrecht en omstreken"), ("Contact", f'<a href="mailto:{EMAIL}" style="color: inherit">{EMAIL}</a>'), ("Telefoon", f'<a href="{TEL_HREF}" style="color: inherit">{TEL}</a>')]
info_card = '<div class="win" style="position: relative; width: min(420px, 100%); font-size: 14px">' + "".join(f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 18px 22px;{" border-top: 1px solid rgba(238,234,227,.1);" if i else ""}"><span style="font-size: 13px; color: #FF6A2B">{a}</span><span style="font-size: 17px">{b}</span></div>' for i, (a, b) in enumerate(info_rows)) + '</div>'

over = head(f"{FULL} – Over ons", "Tagent ontwerpt, bouwt en beheert websites voor ondernemers in Utrecht en omstreken: met een eerste ontwerp op maat en een beheerscherm om zelf aan te passen.") + nav("over-ons.html") + page_hero(
    ["Gemaakt met oog", 'voor <em class="serif-i">detail.</em>'],
    "Tagent ontwerpt, bouwt en beheert websites voor ondernemers in Utrecht en omstreken. Met een eerste ontwerp op maat en een beheerscherm om zelf aan te passen.", "d5.webp", visual=OVER_VIS) + f'''
<section class="words-scope" style="height: 2000px; position: relative">
<div style="position: sticky; top: 0; height: min(100svh, 920px); display: flex; align-items: center">
<div class="wrap" style="width: 100%">
<p style="margin: 0; max-width: 26ch; font-weight: 500; font-size: clamp(34px, 4.6vw, 74px); line-height: 1.04; letter-spacing: -.04em">{words(over_words)}</p>
</div>
</div>
</section>
<section class="light">
<div class="wrap" style="padding-block: 160px; display: flex; flex-wrap: wrap; gap: 64px 96px; align-items: center">
<div class="reveal" style="flex: 1 1 460px; min-width: 0; display: flex; flex-direction: column; gap: 26px">
<h2 class="h2">Waarom <em class="serif-i">Tagent?</em></h2>
<p class="body muted" style="font-size: 17px; max-width: 36rem">Voor veel ondernemers is de website de eerste kennismaking met hun zaak. Toch is die site vaak verouderd, lastig te bekijken op een telefoon of niet zelf bij te werken.</p>
<p class="body muted" style="font-size: 17px; max-width: 36rem">Tagent maakt daar een site van die strak oogt, op elk scherm klopt en die de ondernemer zelf kan bijhouden. Zonder ingewikkelde techniek, met heldere afspraken.</p>
</div>
<div class="svc-vis scene reveal" style="flex: 1 1 420px; min-width: 0; min-height: 460px">{redesign_vis}</div>
</div>
</section>
<section class="wrap" style="padding-block: 160px; display: flex; flex-direction: column; gap: 72px">
<div class="reveal" style="display: flex; flex-direction: column; gap: 24px; max-width: 44rem">
<h2 class="h2">Drie vaste <em class="serif-i">uitgangspunten.</em></h2>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px">{vals_html}</div>
</section>
<section class="light">
<div class="wrap" style="padding-block: 160px; display: flex; flex-wrap: wrap; gap: 64px 96px; align-items: center">
<div class="reveal" style="flex: 1 1 460px; min-width: 0; display: flex; flex-direction: column; gap: 26px">
<h2 class="h2">Achter <em class="serif-i">Tagent.</em></h2>
<p class="body muted" style="font-size: 17px; max-width: 36rem">Tagent is opgericht door Tygo Brunenberg. Hij studeert Ondernemerschap &amp; Retailmanagement aan de HAN en heeft een achtergrond in retail en marketing. Daar zag hij hoe belangrijk een sterke eerste indruk is, en hoe vaak een website daarin tekortschiet.</p>
</div>
<div class="media reveal" style="flex: 1 1 380px; min-width: 0; border-radius: 28px; padding: clamp(24px, 4vw, 48px); display: flex; align-items: center; justify-content: center; min-height: 420px">
<img class="plx" src="assets/d6.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .7">
{info_card}
</div>
</div>
</section>
''' + cta_block('Laten we <em class="serif-i">kennismaken.</em>', "Een kort gesprek over het bedrijf, met eerlijk advies over wat de site nodig heeft.") + footer() + tail(height=7200)
pages["over-ons.html"] = over
pages["over-mij.html"] = f'''<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8"><title>{FULL} – Over ons</title><meta name="robots" content="noindex"><link rel="canonical" href="https://tagent.nl/over-ons.html"><meta http-equiv="refresh" content="0; url=over-ons.html"></head>
<body><p>Deze pagina is verhuisd naar <a href="over-ons.html">Over ons</a>.</p></body></html>'''

# =====================================================================
# KENNISMAKING
# =====================================================================
ken_logic = r"""
  constructor(props) {
    super(props);
    this.state = { step: 1, picked: {}, sent: false, err: '', busy: false, naam: '' };
  }
  val(id) { var el = document.getElementById(id); return el ? (el.value || '').trim() : ''; }
  renderVals() {
    var self = this, st = this.state;
    var on = 'background:#0C0C0A;color:#EEEAE3;border:0;box-shadow:inset 0 0 0 1px #0C0C0A';
    var off = 'background:transparent;color:#0C0C0A;border:0;box-shadow:inset 0 0 0 1px rgba(12,12,10,.2)';
    var opts = ['Nieuwe website', 'Redesign van de website', 'Beheer van de website', 'Advies', 'Weet ik nog niet', 'Overig'];
    var needs = opts.map(function (l) {
      var sel = !!st.picked[l];
      return { label: l, pressed: sel ? 'true' : 'false', style: sel ? on : off,
        toggle: function () { var p = Object.assign({}, self.state.picked); p[l] = !p[l]; self.setState({ picked: p, err: '' }); } };
    });
    var show = 'opacity:1;transform:none;filter:none;visibility:visible';
    var hideF = 'opacity:0;transform:translateY(-16px);filter:blur(8px);pointer-events:none;visibility:hidden';
    var hideB = 'opacity:0;transform:translateY(24px);filter:blur(8px);pointer-events:none;visibility:hidden';
    function ps(n) { if (st.sent) return hideF; return st.step === n ? show : (st.step > n ? hideF : hideB); }
    function go(n) {
      self.setState({ step: n, err: '' });
      setTimeout(function () { var f = document.querySelector('[data-step="' + n + '"] input:not([tabindex]), [data-step="' + n + '"] textarea'); if (f && n > 1) { try { f.focus({ preventScroll: true }); } catch (e) {} } }, 500);
    }
    return {
      needs: needs, s1: ps(1), s2: ps(2), s3: ps(3),
      doneStyle: st.sent ? show : hideB,
      headStyle: st.sent ? 'opacity:0;visibility:hidden' : 'opacity:1;visibility:visible',
      prog: 'transform:scaleX(' + (st.step / 3) + ')',
      stepTxt: 'Vraag ' + st.step + ' van 3',
      err: st.err, errStyle: st.err ? 'display:block' : 'display:none',
      naam: st.naam,
      sendTxt: st.busy ? 'Bezig met versturen…' : 'Verstuur',
      next1: function () {
        var any = Object.keys(st.picked).some(function (k) { return st.picked[k]; }) || self.val('q-anders');
        if (!any) { self.setState({ err: 'Kies een onderwerp, of omschrijf het kort.' }); return; }
        go(2);
      },
      next2: function () {
        if (!self.val('q-doel')) { self.setState({ err: 'Omschrijf kort wat het doel is.' }); return; }
        go(3);
      },
      back: function () { go(Math.max(1, st.step - 1)); },
      submit: function () {
        if (st.busy) return;
        var naam = self.val('q-naam'), tel = self.val('q-tel'), mail = self.val('q-mail');
        if (!naam) { self.setState({ err: 'Vul een naam in.' }); return; }
        if (!tel && !mail) { self.setState({ err: 'Vul een telefoonnummer of e-mailadres in.' }); return; }
        if (mail && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)) { self.setState({ err: 'Controleer het e-mailadres.' }); return; }
        if (self.val('q-bot')) { self.setState({ sent: true, naam: naam }); return; }
        var hulp = Object.keys(st.picked).filter(function (k) { return st.picked[k]; }).join(', ');
        var anders = self.val('q-anders'), doel = self.val('q-doel'), site = self.val('q-site');
        var body = 'Hulp nodig bij: ' + (hulp || '-') + (anders ? ' (' + anders + ')' : '') + '\n\nDoel: ' + doel + '\n\nHuidige website: ' + (site || '-') +
                   '\n\nNaam: ' + naam + '\nTelefoon: ' + (tel || '-') + '\nE-mail: ' + (mail || '-');
        var KEY = '__KEY__';
        if (!KEY) {
          window.location.href = 'mailto:__EMAIL__?subject=' + encodeURIComponent('Kennismaking via tagent.nl – ' + naam) + '&body=' + encodeURIComponent(body);
          self.setState({ sent: true, naam: naam });
          return;
        }
        self.setState({ busy: true, err: '' });
        var data = { access_key: KEY, subject: 'Nieuwe aanvraag via tagent.nl – ' + naam, from_name: 'Website Tagent', name: naam, phone: tel, message: body, botcheck: '' };
        if (mail) { data.email = mail; data.replyto = mail; }
        fetch('https://api.web3forms.com/submit', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
          .then(function (r) { return r.json(); })
          .then(function (j) { if (j && j.success) { self.setState({ busy: false, sent: true, naam: naam }); } else { throw new Error('mislukt'); } })
          .catch(function () { self.setState({ busy: false, err: 'Versturen lukte niet. Mail gerust naar __EMAIL__ of bel __TEL__.' }); });
      },
      reset: function () {
        ['q-anders', 'q-doel', 'q-site', 'q-naam', 'q-tel', 'q-mail'].forEach(function (id) { var el = document.getElementById(id); if (el) el.value = ''; });
        self.setState({ step: 1, picked: {}, sent: false, err: '', busy: false, naam: '' });
      }
    };
  }""".replace('__KEY__', WEB3FORMS_KEY).replace('__EMAIL__', EMAIL).replace('__TEL__', TEL)
gets = ["Een kort gesprek over het bedrijf en de huidige site", "Eerlijk advies over wat beter kan", "Een voorstel én eerste ontwerp op maat"]
gets_html = "".join(f'<div style="display: flex; gap: 14px; align-items: center; padding: 16px 0; border-top: 1px solid rgba(238,234,227,.2)">{CHECK}<span style="font-size: 16px">{t}</span></div>' for t in gets)
def qbtn(txt, fn, kind="dark", arrow=True):
    arr = f'<span class="arr">{ARR}</span>' if arrow else ""
    return f'<button type="button" class="btn btn-{kind}" onClick="{{{{{fn}}}}}">{txt}{arr}</button>'
qpanel = 'position: absolute; inset: 0; display: flex; flex-direction: column; gap: 32px'

ken = head(f"{FULL} – Plan een kennismaking", "Plan een kennismaking over een nieuwe website, redesign of beheer. Drie korte vragen, daarna neemt Tagent contact op.") + nav("kennismaking.html") + f"""
<section style="display: flex; flex-wrap: wrap; min-height: calc(100svh - 72px)">
<div class="media" style="flex: 1 1 520px; min-width: 0; min-height: 640px">
<div style="position: absolute; inset: 0; background: radial-gradient(120% 75% at 85% 112%, rgba(255,106,43,.32), transparent 62%), radial-gradient(90% 60% at 0% 0%, rgba(238,234,227,.06), transparent 60%), #0C0C0A"></div>
<div style="position: relative; padding: clamp(32px, 5vw, 72px); display: flex; flex-direction: column; gap: 48px; min-height: 100%; justify-content: space-between">
<div style="display: flex; flex-direction: column; gap: 32px">
<h1 class="h1"><span class="line"><span style="animation-delay: .2s">Laten we</span></span><span class="line"><span style="animation-delay: .32s"><em class="serif-i">kennismaken.</em></span></span></h1>
<p class="lead fade-up" style="max-width: 30rem; animation-delay: .55s; color: rgba(238,234,227,.82)">Een kort gesprek over het bedrijf en de wensen. Is er al een website? Stuur de link mee, dan wordt er vooraf al meegekeken.</p>
</div>
<div class="fade-up" style="display: flex; flex-direction: column; animation-delay: .8s; max-width: 30rem">
{gets_html}
<div style="display: flex; flex-wrap: wrap; gap: 8px 24px; padding-top: 22px; border-top: 1px solid rgba(238,234,227,.2); color: rgba(238,234,227,.82)"><a href="mailto:{EMAIL}" style="color: inherit">{EMAIL}</a><a href="{TEL_HREF}" style="color: inherit">{TEL}</a></div>
</div>
</div>
</div>
<div class="light" style="flex: 1 1 520px; min-width: 0; position: relative; padding: clamp(32px, 5vw, 80px); display: flex; flex-direction: column; gap: 36px">
<div style="{{{{headStyle}}}}; display: flex; flex-direction: column; gap: 12px; max-width: 560px; transition: opacity .6s var(--ease)">
<span style="font-size: 14px; font-weight: 500; color: #A8410F">{{{{stepTxt}}}}</span>
<div class="step-bar"><i style="{{{{prog}}}}; transition: transform .8s var(--ease)"></i></div>
</div>
<form onsubmit="return false" style="position: relative; flex: 1; min-height: 600px; max-width: 560px; margin: 0">
<div class="panel" data-step="1" style="{{{{s1}}}}; {qpanel}">
<h2 class="h3" style="font-size: clamp(30px, 2.8vw, 42px)">Waar kan Tagent bij <em class="serif-i">helpen?</em></h2>
<div style="display: flex; flex-wrap: wrap; gap: 8px">
<sc-for list="{{{{needs}}}}" as="d" hint-placeholder-count="6">
<button type="button" class="chip" aria-pressed="{{{{d.pressed}}}}" onClick="{{{{d.toggle}}}}" style="{{{{d.style}}}}">{{{{d.label}}}}</button>
</sc-for>
</div>
<div class="field"><label for="q-anders">Of omschrijf het kort</label><input id="q-anders" type="text" placeholder="Bijv. een extra pagina of een webshop"></div>
<div style="display: flex; gap: 10px">{qbtn("Volgende", "next1")}</div>
</div>
<div class="panel" data-step="2" style="{{{{s2}}}}; {qpanel}">
<h2 class="h3" style="font-size: clamp(30px, 2.8vw, 42px)">Wat is het <em class="serif-i">doel?</em></h2>
<div class="field"><label for="q-doel">Wat moet de website straks opleveren of makkelijker maken?</label><textarea id="q-doel" rows="3" placeholder="Bijv. meer reserveringen via de site, of zelf de openingstijden kunnen aanpassen"></textarea></div>
<div class="field"><label for="q-site">Huidige website (als die er is)</label><input id="q-site" type="url" inputmode="url" placeholder="www.jouwbedrijf.nl"></div>
<div style="display: flex; flex-wrap: wrap; gap: 10px">{qbtn("Terug", "back", "ghost", False)}{qbtn("Volgende", "next2")}</div>
</div>
<div class="panel" data-step="3" style="{{{{s3}}}}; {qpanel}">
<h2 class="h3" style="font-size: clamp(30px, 2.8vw, 42px)">Hoe is er contact <em class="serif-i">mogelijk?</em></h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px">
<div class="field" style="grid-column: 1 / -1"><label for="q-naam">Naam</label><input id="q-naam" type="text" autocomplete="name" placeholder="Voor- en achternaam"></div>
<div class="field"><label for="q-tel">Telefoonnummer</label><input id="q-tel" type="tel" autocomplete="tel" placeholder="06 12345678"></div>
<div class="field"><label for="q-mail">E-mailadres</label><input id="q-mail" type="email" autocomplete="email" placeholder="naam@bedrijf.nl"></div>
</div>
<input id="q-bot" name="botcheck" type="text" tabindex="-1" autocomplete="off" aria-hidden="true" style="position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0">
<span style="font-size: 13px; color: #5A5650; max-width: 26rem">Telefoon of e-mail is genoeg. Gegevens worden alleen gebruikt om contact op te nemen. Lees de <a href="privacy.html" style="color: #0C0C0A; text-decoration: underline">privacyverklaring</a>.</span>
<div style="display: flex; flex-wrap: wrap; gap: 10px">{qbtn("Terug", "back", "ghost", False)}<button type="button" class="btn btn-dark" onClick="{{{{submit}}}}">{{{{sendTxt}}}}<span class="arr">{ARR}</span></button></div>
</div>
<div class="panel" role="status" style="{{{{doneStyle}}}}; display: flex; flex-direction: column; justify-content: center; gap: 28px">
<span style="width: 64px; height: 64px; border-radius: 50%; background: #0C0C0A; color: #EEEAE3; display: inline-flex; align-items: center; justify-content: center"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>
<h2 class="h2" style="max-width: 14ch">Bedankt, <em class="serif-i">{{{{naam}}}}.</em></h2>
<p class="body muted" style="max-width: 28rem; font-size: 17px">Dit is alle informatie die nodig is. Tagent neemt zo snel mogelijk contact op.</p>
<div style="display: flex; flex-wrap: wrap; gap: 10px">
{btn("index.html", "Terug naar home", kind="dark")}
{qbtn("Nieuwe aanvraag", "reset", "ghost", False)}
</div>
</div>
</form>
<p role="alert" style="{{{{errStyle}}}}; margin: -12px 0 0; color: #A8410F; font-size: 14px; font-weight: 500">{{{{err}}}}</p>
</div>
</section>
""" + footer() + tail(ken_logic, height=1700)
pages["kennismaking.html"] = ken

# =====================================================================
# PRIVACY
# =====================================================================
priv_items = [
    ("Wie we zijn", f"{FULL} ontwerpt, bouwt en beheert websites voor ondernemers in Utrecht en omstreken. Vragen over privacy? Mail naar {EMAIL} of bel {TEL}."),
    ("Welke gegevens", "Bij een aanvraag via het kennismakingsformulier: naam, telefoonnummer en/of e-mailadres, het onderwerp, het doel en (als ingevuld) de link van de huidige website. Bij contact per e-mail of telefoon: de gegevens die daarin worden gedeeld."),
    ("Waarvoor", "Alleen om contact op te nemen over de aanvraag en, bij een samenwerking, om de afspraken uit te voeren en te factureren. Gegevens worden niet gebruikt voor nieuwsbrieven of reclame."),
    ("Grondslag", "Het verwerken gebeurt op basis van de aanvraag zelf (het voorbereiden van een overeenkomst) en, bij een samenwerking, de uitvoering van die overeenkomst en wettelijke verplichtingen zoals de administratie."),
    ("Hoe lang", "Aanvragen zonder samenwerking worden na 12 maanden verwijderd. Bij een samenwerking blijven gegevens bewaard zolang dat nodig is voor de afspraken. Gegevens voor de administratie worden 7 jaar bewaard, zoals de wet voorschrijft."),
    ("Delen met anderen", "Gegevens worden niet verkocht. Het formulier wordt verstuurd via Web3Forms, dat de aanvraag doorstuurt naar " + EMAIL + ". De website draait op GitHub Pages. Met deze diensten worden alleen de gegevens gedeeld die daarvoor nodig zijn."),
    ("Cookies", "De website gebruikt geen tracking- of advertentiecookies en houdt geen bezoekersstatistieken bij."),
    ("Lettertypes", "De lettertypes worden vanaf de eigen website geladen. Daarbij gaan er geen gegevens naar Google Fonts of andere partijen."),
    ("Rechten", "Gegevens zijn altijd in te zien, aan te passen of te laten verwijderen via " + EMAIL + ". Een klacht kan ook worden ingediend bij de Autoriteit Persoonsgegevens."),
]
priv_html = "".join(f'<div style="display: flex; flex-wrap: wrap; gap: 12px 64px; padding-block: 36px; border-top: 1px solid rgba(12,12,10,.12)"><h2 class="h3" style="flex: 0 0 280px; font-size: 26px">{t}</h2><p class="body" style="flex: 1 1 380px; font-size: 17px; color: #5A5650">{d}</p></div>' for t, d in priv_items)
privacy = head(f"{FULL} – Privacyverklaring", f"Hoe {FULL} omgaat met je gegevens.") + nav("privacy.html") + f'''
<section class="wrap" style="padding-block: 120px 80px; display: flex; flex-direction: column; gap: 28px">
<h1 class="h1"><span class="line"><span style="animation-delay: .15s">Privacy<em class="serif-i">verklaring.</em></span></span></h1>
<p class="lead fade-up muted" style="max-width: 36rem; animation-delay: .45s">Hoe Tagent omgaat met gegevens van bezoekers en klanten. Laatst bijgewerkt: 22 november 2026.</p>
</section>
<section class="light"><div class="wrap" style="padding-block: 80px 140px">{priv_html}</div></section>
''' + footer() + tail(height=3000)
pages["privacy.html"] = privacy

# =====================================================================
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT + "/assets")
for f in ["site.css", "runtime.js", "cta.webp", "d1.webp", "d2.webp", "d3.webp", "d4.webp", "d5.webp", "d6.webp", "ember.webp", "hero.webp", "stone.webp"]:
    shutil.copy(f"{ROOT}/assets/{f}", f"{OUT}/assets/{f}")
shutil.copy(os.path.join(ROOT, "web.css"), f"{OUT}/assets/web.css")
with open(f"{OUT}/assets/favicon.svg", "w") as fh:
    fh.write(ICON_D.format(s=64).replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ').replace('currentColor','#EEEAE3').replace('<rect x="4"','<rect x="4" fill-opacity="1"',0).replace('viewBox="0 0 64 64"','viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#0C0C0A"/',0) if False else '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#0C0C0A"/>' + ICON_D.format(s=64).split('>',1)[1].replace('currentColor','#EEEAE3'))
import json as _json, re as _re
SITE = "https://tagent.nl"
os.makedirs(f"{OUT}/assets/fonts", exist_ok=True)
for f in os.listdir(os.path.join(ROOT, "assets", "fonts")):
    shutil.copy(f"{ROOT}/assets/fonts/{f}", f"{OUT}/assets/fonts/{f}")
for f in ["og.png", "logo-512.png"]:
    shutil.copy(f"{ROOT}/assets/{f}", f"{OUT}/assets/{f}")

ORG = {"@type": "Organization", "@id": SITE + "/#organisatie", "name": FULL, "url": SITE + "/",
       "logo": SITE + "/assets/logo-512.png", "image": SITE + "/assets/og.png",
       "description": "Tagent ontwerpt, bouwt en beheert websites voor ondernemers in Utrecht en omstreken, met een eerste ontwerp op maat en een beheerscherm om zelf aan te passen.",
       "email": EMAIL, "telephone": "+31615541022", "areaServed": "Utrecht en omstreken",
       "knowsAbout": ["Websiteontwerp", "Websitebeheer", "Website-optimalisatie", "Redesign van websites"],
       "founder": {"@type": "Person", "name": "Tygo Brunenberg"},
       "contactPoint": {"@type": "ContactPoint", "contactType": "klantenservice", "email": EMAIL, "telephone": "+31615541022", "availableLanguage": "nl"},
       "sameAs": ["https://www.instagram.com/tagent.nl/"]}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "name": FULL, "url": SITE + "/", "inLanguage": "nl-NL", "publisher": {"@id": SITE + "/#organisatie"}}
CRUMB = {"index.html": None, "diensten.html": "Diensten", "werkwijze.html": "Werkwijze", "over-ons.html": "Over ons", "kennismaking.html": "Kennismaking", "privacy.html": "Privacyverklaring", "404.html": None}
SERVICES = [("Nieuwe website", "Een website vanaf de basis, met een eerste ontwerp op maat en een beheerscherm om de inhoud zelf aan te passen."),
            ("Redesign van een website", "Een bestaande website opnieuw ontworpen: alle benodigde pagina's, foto's en links gaan mee naar een modern ontwerp."),
            ("Beheerscherm", "Een eenvoudig beheerscherm om teksten, foto's en openingstijden zelf aan te passen, binnen de vaste lay-out."),
            ("Websitebeheer", "Optioneel beheer per maand of per jaar, met hulp bij aanpassingen, nieuwe pagina's en functies.")]

def url_of(name):
    return SITE + "/" if name == "index.html" else f"{SITE}/{name}"

def seo_block(name, html):
    title = _re.search(r"<title>(.*?)</title>", html).group(1)
    desc = _re.search(r'<meta name="description" content="(.*?)">', html).group(1)
    u = url_of(name)
    graph = [ORG, WEBSITE]
    page = {"@type": "WebPage", "@id": u + "#pagina", "url": u, "name": title, "description": desc, "inLanguage": "nl-NL",
            "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organisatie"}}
    if CRUMB.get(name):
        page["breadcrumb"] = {"@id": u + "#kruimelpad"}
        graph.append({"@type": "BreadcrumbList", "@id": u + "#kruimelpad", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": CRUMB[name], "item": u}]})
    if name == "over-ons.html": page["@type"] = "AboutPage"
    if name == "kennismaking.html": page["@type"] = "ContactPage"
    graph.append(page)
    if name == "diensten.html":
        for n, d in SERVICES:
            graph.append({"@type": "Service", "name": n, "description": d, "serviceType": n, "provider": {"@id": SITE + "/#organisatie"}, "areaServed": "Utrecht en omstreken"})
    if name == "werkwijze.html":
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    ld = _json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    return (f'<link rel="canonical" href="{u}">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="nl_NL">\n<meta property="og:site_name" content="{FULL}">\n'
            f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{u}">\n'
            f'<meta property="og:image" content="{SITE}/assets/og.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{FULL}: jouw website, maar dan beter.">\n<meta name="twitter:card" content="summary_large_image">\n'
            f'<script type="application/ld+json">{ld}</script>')

def render_tpl(tpl, vals):
    """Zelfde uitkomst als runtime.js bij de eerste weergave (alleen {{x}}, {{a.b}} en <sc-for>)."""
    def look(path, ctx):
        v = ctx
        for k in path.strip().split("."):
            v = v.get(k) if isinstance(v, dict) else None
        return v
    def interp(txt, ctx):
        return _re.sub(r"\{\{([^{}]+)\}\}", lambda m: "" if look(m.group(1), ctx) is None else str(look(m.group(1), ctx)), txt)
    def do_for(m):
        lst = look(m.group(1).strip("{} "), vals) or []
        return "".join(interp(m.group(3), dict(vals, **{m.group(2): it})) for it in lst)
    out = _re.sub(r'<sc-for list="([^"]+)" as="([^"]+)"[^>]*>(.*?)</sc-for>', do_for, tpl, flags=_re.S)
    out = _re.sub(r'\s+on[A-Za-z]+="\{\{[^}]*\}\}"', "", out)
    out = _re.sub(r'\s+hint-[a-z-]+="[^"]*"', "", out)
    return interp(out, vals)

SHOW = 'opacity:1;transform:none;filter:none;visibility:visible'
HIDEB = 'opacity:0;transform:translateY(24px);filter:blur(8px);pointer-events:none;visibility:hidden'
OFF = 'background:transparent;color:#0C0C0A;border:0;box-shadow:inset 0 0 0 1px rgba(12,12,10,.2)'
INIT = {"kennismaking.html": {
    "needs": [{"label": l, "pressed": "false", "style": OFF} for l in ['Nieuwe website', 'Redesign van de website', 'Beheer van de website', 'Advies', 'Weet ik nog niet', 'Overig']],
    "s1": SHOW, "s2": HIDEB, "s3": HIDEB, "doneStyle": HIDEB, "headStyle": "opacity:1;visibility:visible",
    "prog": "transform:scaleX(" + repr(1 / 3) + ")", "stepTxt": "Vraag 1 van 3", "err": "", "errStyle": "display:none", "naam": "", "sendTxt": "Verstuur"}}

SEO_META = {
    "index.html": ("Webdesign Utrecht: website laten maken voor ondernemers | Tagent",
                   "Tagent ontwerpt, bouwt en beheert websites voor ondernemers in Utrecht en omstreken. Eerst een ontwerp op maat bekijken, daarna zelf de inhoud bijhouden."),
    "diensten.html": ("Nieuwe website, redesign en websitebeheer in Utrecht | Tagent",
                      "Een nieuwe website, een redesign van de huidige site, een beheerscherm om zelf aan te passen en optioneel beheer. Voor ondernemers in Utrecht en omstreken."),
    "werkwijze.html": ("Werkwijze en veelgestelde vragen | Tagent webdesign Utrecht",
                       "Van kennismaking tot livegang in vijf stappen: eerst een ontwerp op maat, samen bijschaven, dan pas akkoord. Met antwoorden op veelgestelde vragen."),
    "over-ons.html": ("Over ons | Tagent, webdesign in Utrecht en omstreken",
                      "Tagent ontwerpt, bouwt en beheert websites voor ondernemers in Utrecht en omstreken, met een eerste ontwerp op maat en een beheerscherm om zelf aan te passen."),
    "kennismaking.html": ("Kennismaking plannen | Tagent webdesign Utrecht",
                          "Plan een kennismaking over een nieuwe website, redesign, websitebeheer of advies. Drie korte vragen, daarna neemt Tagent contact op."),
    "privacy.html": ("Privacyverklaring | Tagent", "Hoe Tagent omgaat met gegevens van bezoekers en klanten: welke gegevens, waarvoor, hoe lang en welke rechten er zijn."),
}

def finish(name, html):
    if name in SEO_META:
        t, d = SEO_META[name]
        html = _re.sub(r"<title>.*?</title>", f"<title>{t}</title>", html, count=1)
        html = _re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{d}">', html, count=1)
    if "<!--PRE-->" not in html:
        return html
    m = _re.search(r'<template id="dc-tpl">(.*?)</template>', html, _re.S)
    tpl = m.group(1)
    # semantiek: <main> rond de inhoud, skiplink
    tpl = tpl.replace("</header>\n", '</header>\n<main id="inhoud">\n', 1)
    tpl = tpl.replace("<footer ", "</main>\n<footer ", 1)
    assert tpl.count("<main") == 1 and tpl.count("</main>") == 1, name
    # lazy loading voor afbeeldingen buiten de eerste schermhoogte
    n = [0]
    def lazy(mm):
        n[0] += 1
        tag = mm.group(0)
        return tag if (n[0] <= 2 or "loading=" in tag) else tag.replace("<img ", '<img loading="lazy" decoding="async" ', 1)
    tpl = _re.sub(r"<img [^>]*>", lazy, tpl)
    if "{{" in tpl:
        pre = render_tpl(tpl, INIT[name])
        html = html[:m.start(1)] + tpl + html[m.end(1):]
        html = html.replace("<!--PRE-->", pre)
    else:
        html = html[:m.start(1)] + html[m.end(1):]
        html = html.replace('<div id="dc-root"><!--PRE--></div>', '<div id="dc-root" data-static>' + tpl + '</div>')
    html = html.replace("<body>\n", '<body>\n<a class="skip" href="#inhoud">Naar de inhoud</a>\n<div class="tr" id="tr" aria-hidden="true"><div class="tr-mark">' + ICON_D.format(s=52) + '<span class="tr-name"><span>' + BRAND + '</span></span></div></div>\n', 1)
    return html.replace("<!--SEO-->", seo_block(name, html))

pages["404.html"] = head(f"{FULL} – Pagina niet gevonden", "Deze pagina bestaat niet (meer). Ga terug naar de homepage van Tagent.") + nav("") + f"""
<section class="wrap" style="padding-block: 160px; min-height: 60svh; display: flex; flex-direction: column; gap: 28px; justify-content: center">
<h1 class="h1"><span class="line"><span style="animation-delay: .15s">Deze pagina bestaat</span></span><span class="line"><span style="animation-delay: .27s"><em class="serif-i">niet.</em></span></span></h1>
<p class="lead fade-up muted" style="max-width: 32rem; animation-delay: .45s">De link klopt niet meer, of de pagina is verhuisd.</p>
<div class="fade-up" style="display: flex; flex-wrap: wrap; gap: 10px; animation-delay: .6s">{btn("index.html", "Naar de homepage", kind="light")}{btn("kennismaking.html", "Plan een kennismaking", kind="ghost")}</div>
</section>
""" + footer() + tail(height=2000)

for name, html in pages.items():
    html = finish(name, html)
    if name == "404.html":
        html = html.replace('<link rel="canonical" href="https://tagent.nl/404.html">\n', '').replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
        html = html.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('url(assets/', 'url(/assets/')
    with open(f"{OUT}/{name}", "w", encoding="utf-8") as fh:
        fh.write(html)

INDEX = ["index.html", "diensten.html", "werkwijze.html", "over-ons.html", "kennismaking.html", "privacy.html"]
PRIO = {"index.html": "1.0", "diensten.html": "0.9", "werkwijze.html": "0.8", "over-ons.html": "0.7", "kennismaking.html": "0.8", "privacy.html": "0.3"}
with open(f"{OUT}/sitemap.xml", "w", encoding="utf-8") as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
             "".join(f"  <url><loc>{url_of(n)}</loc><lastmod>{LASTMOD}</lastmod><priority>{PRIO[n]}</priority></url>\n" for n in INDEX) + "</urlset>\n")
with open(f"{OUT}/robots.txt", "w", encoding="utf-8") as fh:
    fh.write(f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {SITE}/sitemap.xml\n")
with open(f"{OUT}/CNAME", "w") as fh:
    fh.write("tagent.nl\n")
llms = f"""# {FULL}

> {FULL} ontwerpt, bouwt en beheert websites voor ondernemers in Utrecht en omstreken. Elk traject begint met een eerste ontwerp op maat: bekijken, bespreken en pas dan beslissen. Elke site krijgt een beheerscherm om teksten, foto's en openingstijden zelf aan te passen.

## Contact
- E-mail: {EMAIL}
- Telefoon: {TEL}
- Werkgebied: Utrecht en omstreken
- Kennismaking plannen: {SITE}/kennismaking.html

## Diensten
""" + "".join(f"- {n}: {d}\n" for n, d in SERVICES) + f"""
## Werkwijze
1. Kennismaking: over het bedrijf, de klanten en de huidige site.
2. Ontwerp: een eerste ontwerp op maat, in de eigen huisstijl.
3. Samen doorlopen en bijschaven tot alles naar wens is; pas dan akkoord.
4. Beheerscherm en livegang op het eigen domein.
5. Beheer (optioneel): per maand of per jaar. Zonder beheer kan ook: website met beheerscherm, zonder maand- of jaarkosten.

## Veelgestelde vragen
""" + "".join(f"- {q} {a}\n" for q, a in faqs) + f"""
## Pagina's
- [Home]({SITE}/)
- [Diensten]({SITE}/diensten.html)
- [Werkwijze en veelgestelde vragen]({SITE}/werkwijze.html)
- [Over ons]({SITE}/over-ons.html)
- [Kennismaking]({SITE}/kennismaking.html)
- [Privacyverklaring]({SITE}/privacy.html)
"""
with open(f"{OUT}/llms.txt", "w", encoding="utf-8") as fh:
    fh.write(llms)
print("ok", list(pages))
