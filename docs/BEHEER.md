# BEHEER – tagent.nl

## Overzicht
- **Repository**: https://github.com/TBrunenberg/tagent-website (openbaar, branch `main`).
- **Publiceren**: elke push op `main` → GitHub Actions (`.github/workflows/publiceren.yml`) → `pip install -r requirements.txt && python build.py` → GitHub Pages.
- **Live**: https://tagent.nl (na DNS bij Strato) · tijdelijk https://tbrunenberg.github.io/tagent-website/
- **Beheerscherm**: `/admin/` (login via DecapBridge) · **proefversie**: `/admin/demo/` (niets wordt opgeslagen).

## Hoe het beheerscherm werkt
- `build.py` bouwt de site zoals ontworpen. `cms.py` haalt alle zichtbare teksten, foto's en graphics uit de gebouwde pagina's en geeft elk een vaste sleutel (op basis van de standaardtekst in de code).
- De inhoud staat in `content/`:
  - `bedrijf.yml` – e-mail en telefoon (overal tegelijk; belknop wordt automatisch aangepast)
  - `paginas.yml` – pagina's tonen of verbergen (verborgen = niet gebouwd en alle links weg)
  - `teksten/algemeen.yml` – menu en footer
  - `teksten/<pagina>.yml` – per sectie: teksten, foto's (foto, alt-tekst, focuspunt), plaatsing van graphics (grootte, horizontaal, verticaal, afronding) en SEO (titel, omschrijving)
- Alleen waarden die afwijken van de standaard worden toegepast; zonder wijzigingen is de gebouwde HTML byte voor byte gelijk aan het ontwerp.
- Opmaak in tekstvelden: `*woord*` = cursief slotwoord, `**woord**` = vet, nieuwe regel = regelafbreking.
- Uploads komen in `assets/img/uploads/` (als commit in de repository) en worden bij het bouwen verkleind tot max. 2000 px breed.
- `admin/config.yml` wordt bij elke build gegenereerd uit `content/.schema.json` (niet met de hand aanpassen).

## Regels bij aanpassingen aan de code (belangrijk)
- **`content/` en `assets/img/uploads/` zijn van de eigenaar.** Eerst `git pull`, nooit `content/` overschrijven of opnieuw genereren vanaf nul.
- Nieuwe onderdelen in het ontwerp? `python build.py --init` voegt nieuwe velden toe met de standaardwaarde; bestaande waarden blijven staan.
- Wordt een standaardtekst in de code veranderd, dan krijgt dat veld een nieuwe sleutel. Een eerder aangepaste waarde van dat veld geldt dan niet meer: controleer met `git diff content/` en zet zo nodig de waarde over.
- Na elke wijziging: identiek-check (zonder content-wijzigingen moet de HTML gelijk blijven), screenshots desktop/mobiel, formuliertest.

## Login (DecapBridge)
- Account op naam van Tygo; alle Tagent-sites in één account (gratis t/m 3 sites).
- Per site: fine-grained GitHub-token met alleen toegang tot deze repository (Contents: read/write, Pull requests: read/write). Vervaldatum: `{{invullen}}`.
- In `build.py`: `DECAP_IDENTITY_URL` en `DECAP_GATEWAY_URL` uit het DecapBridge-dashboard.
- Gebruikers uitnodigen via DecapBridge (e-mail); zij kiezen zelf een wachtwoord.

## Domein en e-mail
- tagent.nl bij Strato. DNS: A-records naar GitHub Pages (185.199.108-111.153), AAAA 2606:50c0:8000::153. MX/SPF van Strato niet aanraken (info@tagent.nl).
- GitHub → Settings → Pages: custom domain `tagent.nl`, daarna "Enforce HTTPS" aan.

## Contactformulier
- Web3Forms naar info@tagent.nl; sleutel in `WEB3FORMS_KEY` (build.py). Leeg = verzenden via het e-mailprogramma van de bezoeker.

## Terugzetten
- Elke opslag in het beheerscherm is een commit. Terugzetten: GitHub → History van het bestand → vorige versie herstellen (of `git revert`).

## Wat de eigenaar niet zelf aanpast
- Opbouw en volgorde van secties, animaties, nieuwe pagina's of functies, de teksten in het formulier-script (keuzes en foutmeldingen), structured data.
