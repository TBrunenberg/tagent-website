# Tagent – Bezoekersstatistieken (Cloudflare Web Analytics)

## Wat is er geïnstalleerd
- **Dienst**: Cloudflare Web Analytics, gratis versie, zonder Cloudflare-proxy. Hosting (GitHub Pages), DNS en domein blijven ongewijzigd.
- **Techniek**: `build.py` heeft de instelling `CF_BEACON_TOKEN`. Staat daar een token, dan zet de build op alle publieke pagina's (home, diensten, werkwijze, over ons, kennismaking, privacy, 404) vlak voor `</body>`:
  `<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "…", "spa": false}'></script>`
  Niet op de doorverwijspagina over-mij en niet in het beheerscherm (/admin). `type="module"` laadt uitgesteld, dus de pagina wordt er niet door opgehouden. `spa: false` omdat elke pagina een gewone pagina-lading is.
- **Token**: geen geheim (staat altijd zichtbaar in de broncode van elke site met Cloudflare Analytics). Leeg = geen script, geen statistieken.
- **Domein**: Cloudflare telt alleen bezoeken op de hostnaam die je opgeeft (en subdomeinen). Met `tagent.nl` telt tbrunenberg.github.io dus niet mee; statistieken komen pas binnen als tagent.nl live staat.

## Welke gegevens
Paginapad (zonder zoekparameters), verwijzende website, land, apparaattype, browser, besturingssysteem, laadtijden (Core Web Vitals). Het IP-adres wordt bij het dichtstbijzijnde Cloudflare-datacenter weggegooid en niet opgeslagen. Geen cookies, geen localStorage/sessionStorage, geen fingerprinting. Gedetailleerde data 7 dagen, daarna samengevat; terugkijken tot 6 maanden.

## Privacykeuzes
- Geen advertentie- of trackingcookies, geen retargeting, geen andere statistiekenscripts.
- Geen cookiebanner nodig: er wordt niets op het apparaat van de bezoeker opgeslagen en er worden geen bezoekers gevolgd.
- Privacyverklaring vermeldt Cloudflare Web Analytics (sectie Bezoekersstatistieken, grondslag gerechtvaardigd belang).

## Handleiding voor Tygo
1. **Waar**: log in op dash.cloudflare.com → linkermenu **Analytics & Logs → Web Analytics** (heet ook wel "Web Analytics" direct in het menu) → klik op **tagent.nl**.
2. **Wat zie je**: bezoeken (visits), paginaweergaven (page views), en onder het tabblad **Core Web Vitals** de laadsnelheid (LCP, INP, CLS) van echte bezoekers.
3. **Populairste pagina's**: scroll naar het blok **Path** (of "Top paths"): de lijst staat op aantal weergaven. Klik op een pad om alles daarop te filteren.
4. **Waar bezoekers vandaan komen**: blok **Referer** (welke website of Google/Instagram) en blok **Country** (land). Ook **Device type** en **Browser**.
5. **Zelf blijven controleren**: kies rechtsboven de periode (bijv. "Last 7 days" of "Last 30 days"). Tip: kijk elke maandag even naar de afgelopen 7 dagen en vergelijk na een Instagram-post of de bezoeken stijgen en via welke referer. Nieuwe bezoeken verschijnen meestal binnen een paar minuten.

## Openstaande stappen
1. Tygo: dash.cloudflare.com → Web Analytics → **Add a site** → hostnaam `tagent.nl` → Done. Kies bij installatie de handmatige JS-snippet (geen DNS-wijziging, geen "automatic setup").
2. Tygo: kopieer uit de snippet alleen de waarde achter `"token":` en stuur die door.
3. Claude: token in `CF_BEACON_TOKEN` zetten, publiceren, controleren dat het script op alle pagina's staat en dat de console foutloos is.
4. Zodra tagent.nl live is (DNS + custom domain in GitHub Pages): één bezoek doen en na een paar minuten in Cloudflare controleren dat het binnenkomt.
