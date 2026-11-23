# VOORTGANG – Tagent website

Compacte stand van zaken, zodat een volgende sessie direct verder kan. Lees eerst `TAGENT_PROJECT_CONTEXT.md` en `TAGENT_BRAND_GUIDELINES.md`.

## Gedaan (22-11-2026)
- [x] Fase 1 inventarisatie + plan (goedgekeurd).
- [x] Backup `backup/tagent-website-backup-2026-11-22.zip`.
- [x] Batch A: alle feedback (contactgegevens, kernzin, werkwijze, diensten, home, over ons, afspraken, contactformulier vraag voor vraag, privacy).
- [x] Batch B: pre-render, lettertypes zelf gehost, SEO/GEO (canonical, OG, JSON-LD, sitemap, robots, llms.txt), semantiek, lazy loading, Lighthouse.
- [x] Paginaovergang in Tagent-stijl.
- [x] Documentatie (brand guidelines, projectcontext, changelog, voortgang).

## Open
- [ ] **Web3Forms-sleutel** (Tygo, zodra info@tagent.nl werkt) → `WEB3FORMS_KEY` in build.py, daarna formulier live testen.
- [x] GitHub-repo TBrunenberg/tagent-website + GitHub Pages (Actions). Tijdelijk adres: https://tbrunenberg.github.io/tagent-website/ (custom domain tijdelijk verwijderd tot tagent.nl actief is).
- [x] Beheerscherm (Decap CMS) met alle teksten, foto's, plaatsing, pagina's verbergen, SEO; proefversie /admin/demo; identiek-check + wijzigtest geslaagd.
- [ ] Zodra tagent.nl actief is (± 22-11 20:00): DNS bij Strato (Tygo), daarna in GitHub → Settings → Pages custom domain tagent.nl opnieuw invullen en HTTPS afdwingen; daarna PageSpeed Insights + Search Console.
- [ ] DecapBridge-site aanmaken (Tygo) + GitHub-token → identity/gateway-URL in build.py → inlog- en opslagtest.
- [x] Instagram bijgewerkt in de editor + `TAGENT_INSTAGRAM_UPDATE_BRIEF.md`.
- [ ] **PageSpeed Insights** op de live site (home en diensten konden lokaal niet volledig gemeten worden).
- [ ] Google Search Console: domein verifiëren, sitemap indienen.
- [ ] Projectdocument `claude/werkwijze-websites.md` bijwerken (Tagent i.p.v. Koppl/Werknaam).

## Aandachtspunten
- Aanspreekvorm: kernzin gebruikt "uw", diensten-CTA "jou"; rest neutraal. Bewuste keuze van Tygo.
- Na livegang is `content/` van de klant (ook bij de eigen site): nooit standaardinhoud terugschrijven.

## Cloudflare Web Analytics (22-11)
- [x] Code voorbereid, privacyverklaring bijgewerkt, handleiding in docs/CLOUDFLARE_ANALYTICS.md
- [x] Site tagent.nl in Cloudflare (aangemaakt door Tygo), token opgehaald
- [x] Token ingevuld en gepubliceerd
- [ ] Na livegang tagent.nl: eerste bezoek controleren in Cloudflare

## Livegang (23-11)
- [x] DNS bij Strato (A, AAAA, CNAME www; MX ongewijzigd)
- [x] Custom domain tagent.nl in GitHub Pages, DNS-check geslaagd, Enforce HTTPS aan
- [x] Alle pagina's, admin, sitemap, robots, llms.txt 200; 404 werkt; www → tagent.nl
- [x] Cloudflare Web Analytics telt bezoeken
- [x] Web3Forms-formulier werkt; DecapBridge gekoppeld
- [ ] DecapBridge login-URL → https://tagent.nl/admin/index.html
- [ ] Web3Forms domeinbeperking op tagent.nl
- [ ] Search Console + sitemap, PageSpeed live
