# CHANGELOG – Tagent website

## 2026-11-22 · Batch A – feedback Tygo verwerkt
Backup vooraf: `backup/tagent-website-backup-2026-11-22.zip`.

| Wat | Waar | Bestanden | Getest |
|---|---|---|---|
| E-mail info@tagent.nl en telefoon +31 (0)6 1554 1022 (klikbaar) | footer, contactpagina, Over ons, privacy | build.py | screenshots desktop/mobiel |
| "De complete site eerst bekijken" overal vervangen door "Een eerste ontwerp op maat, gemaakt voor uw zaak. Bekijken, bespreken en pas dan beslissen." (ook hero home "complete ontwerp") | werkwijze-hero, home (afspraken, hero), Over ons | build.py | grep: 0 keer "complete site/ontwerp" |
| Werkwijze: kleinere ruimte header → "Van gesprek tot live"; planning-graphic completed / in progress / scheduled, balk Beheer leeg; teksten Ontwerp, Samen doorlopen, Beheer; FAQ's (2 weken, indien gewenst, overeenkomst-zin weg) + nieuwe FAQ "Is beheer verplicht?" | werkwijze.html | build.py | screenshot |
| Beheer zonder vaste kosten als optie | diensten (tekst, punten, graphic "Zonder beheer"), werkwijze stap 5, home stap 5, FAQ | build.py | screenshot |
| "Daarna, alles *geregeld.*"; CTA "Welke aanpak past bij *jou?*" + nieuwe ondertekst | diensten.html | build.py | screenshot |
| Home: "indien gewenst"-teksten, infographic zonder "alle links mee", ondertekst infographic, quote + portretfoto weg, kleinere ruimte "Voor elke zaak" → "In vijf stappen" (padding + korter naloop horizontale kaarten) | index.html | build.py, web.css | screenshot |
| Afspraken die kloppen: 4 zinnen aangepast | home | build.py | screenshot |
| Over mij → Over ons (bedrijf centraal, kort stuk over Tygo zonder foto, nieuwe hero-graphic, "Waarom Tagent?" met voor/na-graphic, info-kaart specialisme/werkgebied/contact). Maatstaf-tekst met oplichtende woorden behouden. `over-mij.html` verwijst door. | over-ons.html, over-mij.html, menu, footer | build.py | screenshot |
| Werkgebied "Utrecht en omstreken", specialisme "Websiteontwerp, -beheer en -optimalisatie"; "Eerlijk" zonder "in plaats van verzonnen" | Over ons | build.py | screenshot |
| Contactformulier vraag voor vraag (hulp → doel → contact → "Bedankt, [naam]"), foto en 01/02/03 weg, validatie, spam-honeypot, verzending via Web3Forms naar info@tagent.nl (zonder sleutel: via e-mailprogramma) | kennismaking.html | build.py | Playwright-doorloop incl. foutmeldingen |
| Privacyverklaring volledig (12 maanden bewaren, 7 jaar administratie, Web3Forms, GitHub Pages, geen tracking, AP) | privacy.html | build.py | screenshot |

Open: Web3Forms-sleutel (WEB3FORMS_KEY in build.py), batch B (SEO/GEO/performance), paginaovergang, beheerscherm, Instagram.

## 2026-11-22 · Batch B – techniek, SEO/GEO, performance
| Wat | Waar | Bestanden | Getest | Akkoord nodig |
|---|---|---|---|---|
| Inhoud vooraf in de HTML (pre-render): zonder JavaScript leesbaar voor zoekmachines en AI-crawlers (home: 7 → 829 woorden). Runtime koppelt alleen gedrag (statisch) of werkt de vooraf opgebouwde DOM bij (contactformulier). | alle pagina's | build.py, assets/runtime.js | pixelvergelijking pre-render vs. oude JS-weergave (desktop + mobiel): opmaak identiek; formulier opnieuw doorlopen | nee |
| Lettertypes zelf gehost (Geist 400/500/600, Instrument Serif italic), Google Fonts verwijderd, preload van 2 gewichten | alle pagina's | build.py, assets/fonts/ | geen verzoeken meer naar fonts.googleapis.com | nee |
| Canonical, Open Graph + deelafbeelding (og.png), JSON-LD: Organization, WebSite, WebPage/AboutPage/ContactPage, BreadcrumbList, Service (diensten), FAQPage (werkwijze) | alle pagina's | build.py, assets/og.png, assets/logo-512.png | JSON-LD geparset, types gecontroleerd | nee |
| Titels en descriptions met natuurlijke lokale zoektermen (webdesign Utrecht, website laten maken, websitebeheer) | alle pagina's (alleen zichtbaar in Google) | build.py | grep | nee |
| sitemap.xml, robots.txt (admin uitgesloten), llms.txt, CNAME tagent.nl, 404-pagina (noindex) | root | build.py | bestanden gecontroleerd | nee |
| Semantiek en toegankelijkheid: `<main>`, skiplink "Naar de inhoud", lazy loading op afbeeldingen buiten beeld, contrast formulierlabel verbeterd | alle pagina's | build.py | Lighthouse toegankelijkheid 100 | nee |

Metingen (Lighthouse mobiel, lokaal): werkwijze 99/100/100/100, privacy 99/100/100/100, over ons 98/100/100/100, kennismaking 98/100/100/100 (prestaties/toegankelijkheid/best practices/SEO); LCP 2,0-2,1 s, CLS 0, TBT 0-90 ms. Home: toegankelijkheid/best practices/SEO 100, LCP niet bepaalbaar (hero verschijnt met fade-in). Diensten: geen volledige meting in deze omgeving. Vóór de ombouw gaf Lighthouse op elke pagina "geen inhoud getekend". Opnieuw meten met PageSpeed Insights zodra de site live staat.

## 2026-11-22 · Paginaovergang + documentatie
| Wat | Waar | Bestanden | Getest | Akkoord nodig |
|---|---|---|---|---|
| Paginaovergang (techniek Massage Woudenberg, Tagent-stijl): Ink-scherm met logo + naam komt van boven, schuift na laden naar beneden weg; animaties nieuwe pagina starten daarna. Alleen bij interne navigatie; reduced-motion: uit; bfcache en vangnet na 4 s. | alle pagina's | build.py (head, tail, finish) | frames + positie-log per 100 ms, klikflow, directe bezoeken zonder scherm, regressie pixelvergelijking + formuliertest | akkoord gegeven (22-11) |
| TAGENT_BRAND_GUIDELINES.md, TAGENT_PROJECT_CONTEXT.md, VOORTGANG.md | projectmap | docs/ | – | nee |
