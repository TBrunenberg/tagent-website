"""Tagent – inhoudslaag voor het beheerscherm (Decap CMS).

Werking
- build.py maakt de pagina's zoals ontworpen (de standaardinhoud).
- cms.py haalt daar alle zichtbare teksten, foto's en graphics uit en geeft elk een vaste sleutel
  (op basis van de standaardtekst, dus onafhankelijk van wat de klant later invult).
- Waarden in content/ die afwijken van de standaard worden toegepast. Zonder afwijkingen blijft
  de HTML byte voor byte gelijk.
- `python build.py --init` vult content/ aan met nieuwe velden (bestaande waarden blijven staan).

Opmaak in tekstvelden: *woord* = cursief slotwoord, **woord** = vet, nieuwe regel = regelafbreking.
"""
import hashlib, html as _html, json, os, re
import yaml
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
TXT = os.path.join(CONTENT, "teksten")

PAGE_LABEL = {"index.html": "Home", "diensten.html": "Diensten", "werkwijze.html": "Werkwijze", "over-ons.html": "Over ons",
              "kennismaking.html": "Kennismaking", "privacy.html": "Privacyverklaring", "404.html": "Pagina niet gevonden"}
PAGE_FILE = {k: k.replace(".html", "").replace("index", "home") for k in PAGE_LABEL}
HIDEABLE = ["diensten.html", "werkwijze.html", "over-ons.html", "kennismaking.html", "privacy.html"]
INLINE = {"em", "strong", "b", "i", "br"}
SKIP = {"script", "style", "svg", "noscript", "template", "head", "title"}
PLAATS = [("hero-site", "Graphic in de header"), ("scene", "Graphic"), ("orbit-wrap", "Graphic"), ("pin", "Bolletje")]


def h(s, n=10):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:n]


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


# ---------- opmaak <-> tekst ----------
def to_markup(el):
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            out.append(str(c))
        elif c.name == "br":
            out.append("\n")
        elif c.name == "em":
            out.append("*" + c.get_text() + "*")
        elif c.name in ("strong", "b"):
            out.append("**" + c.get_text() + "**")
        elif c.name == "i":
            out.append("_" + c.get_text() + "_")
    txt = "".join(out)
    return "\n".join(norm(line) for line in txt.split("\n")).strip()


def from_markup(txt, em_attrs):
    s = _html.escape(txt, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    em = "<em" + "".join(f' {k}="{" ".join(v) if isinstance(v, list) else v}"' for k, v in em_attrs.items()) + ">"
    s = re.sub(r"\*(.+?)\*", lambda m: em + m.group(1) + "</em>", s)
    s = re.sub(r"(?<![\w])_(.+?)_(?![\w])", r"<i>\1</i>", s)
    return s.replace("\n", "<br>")


def simple_inline(el):
    """Alleen tekst + eenvoudige opmaak (em/strong/br), geen geneste structuur."""
    for c in el.children:
        if isinstance(c, Tag):
            if c.name not in INLINE or any(isinstance(g, Tag) for g in c.children):
                return False
    return True


def is_words(el):
    kids = [c for c in el.children if isinstance(c, Tag)]
    return bool(kids) and all(c.name == "br" or "w" in (c.get("class") or []) for c in kids) and any("w" in (c.get("class") or []) for c in kids)


def words_html(text, first_style, step):
    parts = [p for p in text.replace("\n", " <br> ").split(" ") if p]
    words = [p for p in parts if p != "<br>"]
    n = len(words)
    m = re.search(r"contain ([\d.]+)%", first_style or "")
    start = float(m.group(1)) if m else 8.0
    rng = step * max(n, 1)
    out, i = [], 0
    for p in parts:
        if p == "<br>":
            out.append("<br>"); continue
        s = start + i * rng / n
        out.append(f'<span class="w" style="animation-range:contain {s:.1f}% contain {s + rng / n + 4:.1f}%">{_html.escape(p, quote=False)} </span>')
        i += 1
    return "".join(out)


# ---------- structuur van een pagina uitlezen ----------
class Field:
    def __init__(self, kind, key, default, label, group, gkey, node=None, extra=None):
        self.kind, self.key, self.default, self.label, self.group, self.gkey, self.node, self.extra = kind, key, default, label, group, gkey, node, extra or {}


def scope_of(el):
    for p in el.parents:
        if p.name in ("header", "footer") or (p.name == "div" and "tr" in (p.get("class") or [])):
            return "alg"
    return None


def group_of(el, page):
    sec = None
    for p in el.parents:
        if p.name in ("section", "header", "footer"):
            sec = p
            break
    if sec is None:
        return ("Overige onderdelen", "overig")
    if sec.name == "header":
        return ("Menu (bovenaan)", "menu")
    if sec.name == "footer":
        return ("Footer (onderaan)", "footer")
    hd = sec.find(["h1", "h2", "h3"])
    title = norm(hd.get_text()) if hd else "Sectie"
    return (title[:48], "s_" + h(page + "|" + title, 8))


def label_for(txt):
    t = norm(txt.replace("*", ""))
    return (t[:58] + "…") if len(t) > 60 else t


CONSTS = {}


def canon(t):
    for k, v in CONSTS.items():
        if v:
            t = t.replace(v, "{" + k + "}")
    return t


def uncanon(t):
    for k, v in CONSTS.items():
        t = t.replace("{" + k + "}", v)
    return t


def collect(soup, page, consts):
    """Geeft (fields, nodes) voor één opgebouwde pagina-boom."""
    fields, seen = [], set()
    body_roots = [soup.find(id="dc-root")] + [soup.find(id="tr")]
    roots = [r for r in body_roots if r is not None]

    CONSTS.update(consts)

    def add(kind, default, el, extra=None, label=None):
        if kind == "text" and canon(default).strip() in ("{email}", "{telefoon}"):
            return None  # staat bij Bedrijfsgegevens
        sc = scope_of(el) or page
        g, gk = group_of(el, page) if sc != "alg" else (("Menu en footer", "alg"))
        key = {"text": "t_", "img": "i_", "plaats": "p_"}[kind] + h(sc + "|" + kind + "|" + canon(default) + "|" + (extra or {}).get("salt", ""))
        f = Field(kind, key, default, label or label_for(default), g, gk, el, extra)
        f.scope = sc
        fields.append(f)
        return key

    occ = {}
    for root in roots:
        for el in root.find_all(True):
            if el.name in SKIP or any(p.name in SKIP for p in el.parents):
                continue
            # plaatsing
            cls = el.get("class") or []
            for c, lab in PLAATS:
                if c in cls:
                    n = occ.get(("p", c), 0); occ[("p", c)] = n + 1
                    add("plaats", f"{c}#{n}", el, {"salt": str(n), "cls": c}, label=f"{lab} {n + 1}")
            if el.name == "img" and el.get("src"):
                src = el["src"]
                n = occ.get(("i", src), 0); occ[("i", src)] = n + 1
                add("img", src, el, {"salt": str(n), "alt": el.get("alt", "")}, label=f"Foto: {os.path.basename(src)}" + (f" ({n + 1})" if n else ""))
            for attr in ("placeholder",):
                if el.get(attr) and "{{" not in el[attr]:
                    add("text", el[attr], el, {"attr": attr}, label=f"Voorbeeldtekst: {el[attr][:40]}")
            # tekst
            direct = [c for c in el.children if isinstance(c, NavigableString) and not isinstance(c, Comment) and norm(str(c))]
            if is_words(el):
                toks = ["\n" if c.name == "br" else norm(c.get_text()) for c in el.children if isinstance(c, Tag)]
                txt = "\n".join(norm(line) for line in " ".join(toks).split("\n")).strip()
                ws = [c for c in el.children if isinstance(c, Tag) and c.name != "br"]
                st = [float(x) for x in re.findall(r"contain ([\d.]+)%", ws[0].get("style", ""))] if ws else []
                st2 = [float(x) for x in re.findall(r"contain ([\d.]+)%", ws[1].get("style", ""))] if len(ws) > 1 else []
                step = (st2[0] - st[0]) if st and st2 else 4.0
                add("text", txt, el, {"words": True, "style": ws[0].get("style", "") if ws else "", "step": step})
                continue
            if any(p for p in el.parents if p is not None and getattr(p, "_cms_done", False)):
                continue
            if not direct:
                continue
            if any("{{" in str(c) for c in direct):
                continue
            if simple_inline(el) and el.name not in ("html", "body"):
                mk = to_markup(el)
                if mk:
                    ems = el.find("em")
                    add("text", mk, el, {"em": dict(ems.attrs) if ems else {"class": ["serif-i"]}, "block": True})
                    el._cms_done = True
            else:
                for i, c in enumerate(direct):
                    t = norm(str(c))
                    add("text", t, el, {"node_index": i, "raw": str(c)})
    return fields


# ---------- content laden ----------
def load(name):
    p = os.path.join(CONTENT, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return {}


def save(name, data):
    p = os.path.join(CONTENT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False, width=10000)


def flat(data):
    out = {}
    for k, v in (data or {}).items():
        if isinstance(v, dict) and not k.startswith(("i_", "p_")) and k != "seo":
            out.update(flat(v))
        else:
            out[k] = v
    return out


# ---------- toepassen ----------
def apply_field(f, val):
    el = f.node
    if f.kind == "text":
        if val is None:
            return False
        val = uncanon(str(val))
        if val.strip() == f.default.strip():
            return False
        if f.extra.get("attr"):
            el[f.extra["attr"]] = val
        elif f.extra.get("words"):
            el.clear()
            el.append(BeautifulSoup(words_html(val, f.extra["style"], f.extra["step"]), "html.parser"))
        elif f.extra.get("block"):
            el.clear()
            el.append(BeautifulSoup(from_markup(val, f.extra["em"]), "html.parser"))
        else:
            direct = [c for c in el.children if isinstance(c, NavigableString) and not isinstance(c, Comment) and norm(str(c))]
            c = direct[f.extra["node_index"]]
            raw = f.extra["raw"]
            lead = raw[:len(raw) - len(raw.lstrip())]
            trail = raw[len(raw.rstrip()):]
            c.replace_with(lead + val + trail)
        return True
    if f.kind == "img":
        if not isinstance(val, dict):
            return False
        ch = False
        src = (val.get("foto") or "").lstrip("/")
        if src and src != f.default:
            el["src"] = src; ch = True
        alt = val.get("alt")
        if alt is not None and alt != f.extra.get("alt", ""):
            el["alt"] = alt; ch = True
        fp = val.get("focus")
        if fp:
            el["style"] = (el.get("style", "").rstrip("; ") + f"; object-position: {fp}").strip("; ")
            ch = True
        return ch
    if f.kind == "plaats":
        if not isinstance(val, dict):
            return False
        g, x, y, r = val.get("grootte"), val.get("x"), val.get("y"), val.get("afronding")
        add = []
        if g not in (None, "", 100):
            add.append(f"scale: {float(g) / 100:g}")
        if (x not in (None, "", 0)) or (y not in (None, "", 0)):
            add.append(f"translate: {int(x or 0)}px {int(y or 0)}px")
        if r not in (None, ""):
            add.append(f"border-radius: {int(r)}px")
        if not add:
            return False
        el["style"] = (el.get("style", "").rstrip("; ") + "; " + "; ".join(add)).strip("; ")
        return True
    return False


def apply(name, html, consts, hidden):
    """Past content/ toe op één gebouwde pagina. Geeft de (eventueel ongewijzigde) HTML terug."""
    if name not in PAGE_FILE:
        return html
    soup = BeautifulSoup(html, "html.parser")
    fields = collect(soup, name, consts)
    vals = flat(load("teksten/algemeen.yml"))
    vals.update(flat(load(f"teksten/{PAGE_FILE[name]}.yml")))
    changed = False
    for f in fields:
        if f.key in vals and apply_field(f, vals[f.key]):
            changed = True
    # verborgen pagina's: links weghalen
    for a in soup.find_all("a", href=True):
        tgt = a["href"].split("#")[0]
        if tgt in hidden:
            a.decompose(); changed = True
    # SEO
    seo = load(f"teksten/{PAGE_FILE[name]}.yml").get("seo") or {}
    out = str(soup) if changed else html
    if seo.get("titel"):
        out = re.sub(r"<title>.*?</title>", "<title>" + _html.escape(seo["titel"], quote=False) + "</title>", out, count=1)
        out = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + _html.escape(seo["titel"]), out, count=1)
    if seo.get("omschrijving"):
        out = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + _html.escape(seo["omschrijving"]), out, count=1)
        out = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + _html.escape(seo["omschrijving"]), out, count=1)
    return out


def hidden_pages():
    z = load("paginas.yml")
    return {p for p in HIDEABLE if z.get(PAGE_FILE[p], {}).get("zichtbaar", True) is False} if isinstance(z, dict) else set()


def bedrijf(defaults):
    b = load("bedrijf.yml")
    out = dict(defaults)
    for k in ("email", "telefoon"):
        if b.get(k):
            out[k] = b[k]
    return out


# ---------- init: content/ aanvullen + Decap-config ----------
def init(pages, consts, seo_meta):
    """Vult content/ aan (nooit overschrijven) en geeft per pagina de velden terug voor de config."""
    schema = {}
    alg = load("teksten/algemeen.yml")
    alg_fields = {}
    for name, html in pages.items():
        if name not in PAGE_FILE:
            continue
        soup = BeautifulSoup(html, "html.parser")
        fields = collect(soup, name, consts)
        data = load(f"teksten/{PAGE_FILE[name]}.yml")
        groups = {}
        for f in fields:
            if f.scope == "alg":
                alg_fields.setdefault(f.key, f)
                continue
            groups.setdefault(f.gkey, {"label": f.group, "fields": {}})["fields"].setdefault(f.key, f)
        for gk, g in groups.items():
            d = data.setdefault(gk, {})
            for k, f in g["fields"].items():
                if k not in d:
                    d[k] = default_value(f)
        sm = seo_meta.get(name)
        if sm:
            data.setdefault("seo", {"titel": sm[0], "omschrijving": sm[1]})
        save(f"teksten/{PAGE_FILE[name]}.yml", data)
        schema[name] = groups
    for k, f in alg_fields.items():
        if k not in alg:
            alg[k] = default_value(f)
    save("teksten/algemeen.yml", alg)
    schema["algemeen"] = {"alg": {"label": "Menu en footer", "fields": alg_fields}}
    b = load("bedrijf.yml")
    if not b:
        save("bedrijf.yml", {"email": consts["email"], "telefoon": consts["telefoon"]})
    z = load("paginas.yml")
    for p in HIDEABLE:
        z.setdefault(PAGE_FILE[p], {"zichtbaar": True})
    save("paginas.yml", z)
    with open(os.path.join(CONTENT, ".schema.json"), "w", encoding="utf-8") as fh:
        json.dump({n: {gk: {"label": g["label"], "fields": [[f.key, f.kind, f.label, f.extra.get("block", False) or f.extra.get("words", False)] for f in g["fields"].values()]} for gk, g in gr.items()} for n, gr in schema.items()}, fh, ensure_ascii=False, indent=1)
    return schema


def default_value(f):
    if f.kind == "text":
        return canon(f.default)
    if f.kind == "img":
        return {"foto": f.default, "alt": f.extra.get("alt", ""), "focus": ""}
    return {"grootte": 100, "x": 0, "y": 0, "afronding": None}


# ---------- Decap-config ----------
def decap_config(site_url, repo, backend):
    sch = json.load(open(os.path.join(CONTENT, ".schema.json"), encoding="utf-8"))
    tip = "Zet een woord tussen *sterretjes* voor het cursieve slotwoord. Een nieuwe regel = regelafbreking."

    def fields_for(group):
        out = []
        for key, kind, label, rich in group["fields"]:
            if kind == "text":
                out.append({"label": label or "Tekst", "name": key, "widget": "text" if rich or len(label) > 50 else "string", "required": False, "hint": tip if rich else ""})
            elif kind == "img":
                out.append({"label": label, "name": key, "widget": "object", "collapsed": True, "fields": [
                    {"label": "Foto", "name": "foto", "widget": "image", "required": False, "choose_url": False},
                    {"label": "Beschrijving (alt-tekst)", "name": "alt", "widget": "string", "required": False, "hint": "Wat staat er op de foto? Leeg laten bij decoratieve foto's."},
                    {"label": "Focuspunt", "name": "focus", "widget": "string", "required": False, "hint": "Welk deel van de foto in beeld blijft, bijv. 50% 30% (horizontaal, verticaal). Leeg = zoals ontworpen."}]})
            else:
                out.append({"label": label + " – plaatsing", "name": key, "widget": "object", "collapsed": True, "summary": "{{fields.grootte}}% · {{fields.x}}, {{fields.y}}", "fields": [
                    {"label": "Grootte (%)", "name": "grootte", "widget": "number", "value_type": "int", "min": 50, "max": 150, "step": 5, "default": 100, "required": False},
                    {"label": "Horizontaal verschuiven (px)", "name": "x", "widget": "number", "value_type": "int", "min": -300, "max": 300, "step": 5, "default": 0, "required": False},
                    {"label": "Verticaal verschuiven (px)", "name": "y", "widget": "number", "value_type": "int", "min": -300, "max": 300, "step": 5, "default": 0, "required": False},
                    {"label": "Afronding (px)", "name": "afronding", "widget": "number", "value_type": "int", "min": 0, "max": 60, "step": 2, "required": False, "hint": "Leeg = zoals ontworpen"}]})
        return out

    files = []
    for name, label in PAGE_LABEL.items():
        if name not in sch:
            continue
        flds = [{"label": g["label"], "name": gk, "widget": "object", "collapsed": True, "fields": fields_for(g)} for gk, g in sch[name].items()]
        flds.append({"label": "Vindbaarheid in Google", "name": "seo", "widget": "object", "collapsed": True, "required": False, "fields": [
            {"label": "Paginatitel", "name": "titel", "widget": "string", "required": False, "hint": "Wordt getoond in Google en in het browsertabblad (± 60 tekens)."},
            {"label": "Omschrijving", "name": "omschrijving", "widget": "text", "required": False, "hint": "Korte samenvatting onder de titel in Google (± 155 tekens)."}]})
        files.append({"label": label, "name": PAGE_FILE[name], "file": f"content/teksten/{PAGE_FILE[name]}.yml", "fields": flds})
    alg = sch.get("algemeen", {}).get("alg", {"fields": []})
    cfg = {
        "backend": backend,
        "locale": "nl",
        "site_url": site_url, "display_url": site_url, "logo_url": site_url + "/assets/logo-512.png",
        "media_folder": "assets/img/uploads", "public_folder": "assets/img/uploads",
        "editor": {"preview": False},
        "collections": [
            {"label": "Bedrijfsgegevens", "name": "bedrijf", "files": [{"label": "Contactgegevens", "name": "bedrijf", "file": "content/bedrijf.yml", "fields": [
                {"label": "E-mailadres", "name": "email", "widget": "string", "hint": "Verandert overal op de site."},
                {"label": "Telefoonnummer", "name": "telefoon", "widget": "string", "hint": "Zoals getoond, bijv. +31 (0)6 1554 1022. De belknop wordt automatisch aangepast."}]}]},
            {"label": "Pagina's tonen of verbergen", "name": "paginas", "files": [{"label": "Pagina's", "name": "paginas", "file": "content/paginas.yml", "fields": [
                {"label": PAGE_LABEL[p], "name": PAGE_FILE[p], "widget": "object", "fields": [{"label": "Zichtbaar op de site", "name": "zichtbaar", "widget": "boolean", "default": True}]} for p in HIDEABLE]}]},
            {"label": "Menu en footer", "name": "algemeen", "files": [{"label": "Menu en footer", "name": "algemeen", "file": "content/teksten/algemeen.yml", "fields": fields_for(alg)}]},
            {"label": "Pagina's: teksten, foto's en graphics", "name": "teksten", "files": files},
        ],
    }
    return cfg
