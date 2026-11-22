# TAGENT – Projectcontext

Vaste referentie om de website efficiënt aan te passen zonder alles opnieuw te analyseren.
Laatst bijgewerkt: 22 november 2026.

## Locaties
- **Projectmap (laptop)**: `C:\Users\Tygo-\OneDrive\Documenten\Claude\Website\Tagent Webdesign\`
  - `website\` – gebouwde site (HTML, assets) + `build.py`, `icons.py`, `web.css`
  - `backup\` – backups vóór grote wijzigingen
  - `CHANGELOG.md`, `VOORTGANG.md`, `TAGENT_BRAND_GUIDELINES.md`, `TAGENT_PROJECT_CONTEXT.md`
  - `tagent-instagram.zip` – export Instagram-starter
- **Online preview** (privé artifact): "Tagent – website (concept)", slug `25c02475-3720-4e1b-ae48-775a0049080f`.
- **Instagram-editor** (artifact met opslag): "Tagent – Instagram-starter", slug `16278aca-2a16-4607-bf7b-906368ab73c5`; inhoud in db-document `content/main` (JSON-string). Nooit standaardinhoud terugschrijven.
- **Domein**: tagent.nl (gekocht 21-11-2026, Strato). E-mail info@tagent.nl (wordt geactiveerd).

## Techniek
- Statische site, geen framework. **`build.py`** (Python) genereert alle pagina's naar `dist/`.
- **Runtime** `assets/runtime.js`: leest `#dc-tpl` (template) en `#dc-logic` (class `Component extends DCLogic`), met `{{bindings}}`, `<sc-for>`, `<sc-if>` en een DOM-morph.
  - Pagina's zonder bindings worden **vooraf opgebouwd**: inhoud staat direct in `<div id="dc-root" data-static>`; de runtime roept alleen `componentDidMount` aan.
  - Kennismaking heeft state: template blijft, de beginstand staat vooraf in `#dc-root` (`INIT` in build.py) en de runtime werkt die bij met morph.
- Scrollen gebeurt in `#dc-root` (vast positioneringsvak), niet in het venster.
- CSS: `assets/site.css` (basis-designsysteem), `web.css` → `assets/web.css` (aanvullingen, mobiel, horizontale kaarten).
- Lettertypes zelf gehost in `assets/fonts/` (Geist 400/500/600, Instrument Serif italic), `@font-face` in de head.
- Afbeeldingen: webp (achtergronden), `og.png` (1200×630 deelafbeelding), `logo-512.png`, `favicon.svg` (uit `icons.py`).

## Pagina's
| Bestand | Inhoud |
|---|---|
| `index.html` | Hero (browsermockup), "Alles gaat mee" (voor/na), doelgroepen-marquee, statement (oplichtende woorden), diensten-kaarten met scènes, techniek-orbit, "Voor elke zaak" (horizontale kaarten), vijf stappen, afspraken die kloppen, CTA |
| `diensten.html` | Nieuwe website, redesign, beheerscherm, livegang, beheer (incl. "zonder beheer"), CTA "Welke aanpak past bij jou?" |
| `werkwijze.html` | Hero met planning-graphic (completed/in progress/scheduled), vijf stappen, FAQ (incl. "Is beheer verplicht?") |
| `over-ons.html` | Tagent-kaart, maatstaf (oplichtende woorden), Waarom Tagent (voor/na), drie uitgangspunten, Achter Tagent (Tygo, zonder foto) + infokaart |
| `over-mij.html` | Doorverwijzing naar over-ons (noindex) |
| `kennismaking.html` | Vraag-voor-vraag-formulier (hulp → doel → contact → bedankt) |
| `privacy.html` | Volledige privacyverklaring |
| `404.html` | Niet gevonden (noindex) |
| `sitemap.xml`, `robots.txt`, `llms.txt`, `CNAME` | SEO/GEO en domein |

## Gedeelde onderdelen in build.py (één plek, werkt overal door)
- **Constanten**: `BRAND`/`FULL`, `EMAIL`, `TEL`, `TEL_HREF`, `WEB3FORMS_KEY`, `LASTMOD`, `MENU`.
- **`head()`** – meta, fonts, paginaovergang-CSS + vroeg script, skiplink-stijl.
- **`nav(cur)`** – header + hoofdmenu. **`footer()`** – footerkolommen, contact, woordmerk.
- **`tail(logic, height)`** – template-einde, `#dc-root`, logica, runtime, overgangsscript.
- **`BASE_LOGIC`** – scroll naar boven, horizontale kaarten passend maken.
- **`page_hero(title_lines, lead, img, visual=)`** – paginaheaders; visuals `DIENSTEN_VIS`, `WERKWIJZE_VIS`, `OVER_VIS`.
- **`cta_block(title, text, second=)`**, **`btn()`**, **`words()`** (oplichtende woorden), **`CHECK`**, **`ARR`**.
- Mockups: `old_win`, `new_win`, `redesign_vis`, `plan_vis`, scènes `scene1-4` op home.
- **SEO** (onderaan build.py): `SEO_META` (titels/descriptions), `seo_block()` (canonical, Open Graph, JSON-LD), `finish()` (pre-render, `<main>`, lazy loading, skiplink, overgangsscherm), sitemap/robots/llms/CNAME.

## Contactformulier
- Stappen en validatie in `ken_logic` (build.py). Antwoorden: onderwerp(en), toelichting, doel, huidige website, naam, telefoon/e-mail (één van beide verplicht). Honeypot `botcheck`.
- Verzending: Web3Forms (`https://api.web3forms.com/submit`) naar info@tagent.nl met `WEB3FORMS_KEY`. Zolang de sleutel leeg is: `mailto:` met ingevulde tekst.

## Animaties
- Laden: `.line > span` (regels), `.fade-up`, `.t-pop` (graphics), met `animation-delay`.
- Scroll: view/scroll-timelines (`s-pop`, `s-in`, `s-draw`, `.w` woorden), `hscroll2` (horizontale kaarten, range 0-92 %), parallax `.plx`.
- Paginaovergang: `.tr` (zie brand guidelines), `html.tr-in` / `tr-hold` (pauzeert animaties tot het scherm wegschuift).
- `prefers-reduced-motion` uitgeschakeld in CSS.

## SEO-structuur
- Canonicals naar `https://tagent.nl/...` (home: `https://tagent.nl/`).
- JSON-LD `@graph`: Organization (`#organisatie`), WebSite (`#website`), WebPage/AboutPage/ContactPage, BreadcrumbList, Service ×4 (diensten), FAQPage (werkwijze, uit `faqs`).
- Geen LocalBusiness (geen adres bekend/gewenst); werkgebied via `areaServed`.

## Werkwijze voor wijzigingen
1. Wijzig `build.py` (of `web.css`), draai `python build.py`.
2. Controleer: screenshots desktop 1440 / mobiel 390, formuliertest, JSON-LD parse.
3. Zet bestanden in de projectmap en werk de preview bij; noteer in `CHANGELOG.md` en `VOORTGANG.md`.

## Projectstatus
Zie `VOORTGANG.md`.
