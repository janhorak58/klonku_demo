# Klonku — Plán implementace frontendu

> Každá fáze je samostatná a testovatelná. Mock backend běží paralelně po celou dobu vývoje.
> Backend URL se přepíná přes env proměnnou `BACKEND_URL`.

---

## Příprava před implementací

- [ ] Dohodnout s backend týmem: kdy bude dostupné staging prostředí?
- [ ] Ověřit finální URL strukturu endpointů (shoduje se s `index.html`?)
- [ ] Domluvit formát chybových odpovědí (detail, kód)

---

## Fáze 0 — Základ projektu

**Výstup:** Spustitelná Flask aplikace, přepínaná mezi mock a real backendem.

- [ ] Inicializace Flask projektu (app factory pattern: `create_app()`)
- [ ] `config.py` — načítání `BACKEND_URL`, `SECRET_KEY` z env
- [ ] `.env.example` se všemi proměnnými
- [ ] `api_client.py` — kostra s prázdnými funkcemi pro každý endpoint
- [ ] `mock_backend/server.py` — mock Flask server se statickými odpověďmi pro všechny endpointy
- [ ] `templates/base.html` — základní layout (navbar slot, content slot, footer)
- [ ] Statické soubory: brand CSS (proměnné, fonty, reset), `marked.js`
- [ ] `run.py` + `requirements.txt`

---

## Fáze 1 — Autentizace

**Stránky:** Login, Registrace, Ověření emailu, Forgot password, Reset password  
**Prerekvizity:** Fáze 0

- [ ] `auth/routes.py` — routy: `/login`, `/register`, `/verify-email`, `/forgot-password`, `/reset-password`, `/logout`
- [ ] `auth/decorators.py` — `@login_required`, `@admin_required`, `@onboarding_required`
- [ ] Middleware `before_request` — automatický refresh access tokenu
- [ ] Google OAuth flow — generování state tokenu, callback route, ověření
- [ ] `api_client.py` — implementace: `login()`, `register()`, `logout()`, `refresh_token()`, `forgot_password()`, `reset_password()`
- [ ] Šablony: `auth/login.html`, `auth/register.html`, `auth/verify_email.html`, `auth/forgot_password.html`, `auth/reset_password.html`
- [ ] Komponenta: auth layout (logo + formulář, bez navbaru)
- [ ] Session handling: uložení `access_token`, `user`, httpOnly cookie pro refresh

**Testování:**
- Login s mock backendem → session je nastavena
- Chybné heslo → inline chybová hláška
- Logout → session smazána, redirect na login
- Neautentizovaný přístup na `/dashboard` → redirect na `/login`

---

## Fáze 2 — Onboarding

**Stránky:** Onboarding  
**Prerekvizity:** Fáze 1

- [ ] `onboarding/routes.py` — route `/onboarding`
- [ ] Načtení fakult a kroků pipeline z API
- [ ] UI: dvě karty (Doporučená / Vlastní pipeline), toggle
- [ ] Vlastní pipeline: checkbox list kroků
- [ ] Uložení preference do Flask session: `pipeline_preference`
- [ ] Přeskočení onboardingu pro již onboardované uživatele (session flag)
- [ ] `api_client.py` — `get_faculties()`, `get_faculty_pipeline_steps(faculty_id)`

**Testování:**
- Po registraci je uživatel redirectován na onboarding
- Po onboardingu je redirectován na dashboard
- Přihlášený uživatel s `onboarding_done` přeskočí onboarding

---

## Fáze 3 — Dashboard + Modal nový projekt

**Stránky:** Dashboard, Modal nový projekt  
**Prerekvizity:** Fáze 1, 2

- [ ] `projects/routes.py` — route `/dashboard`
- [ ] Komponenta: `project_card.html`
- [ ] Komponenta: `status_badge.html`
- [ ] Načítání projektů s pagination (`limit`, `offset`)
- [ ] Prázdný stav (žádné projekty)
- [ ] Modal "Nový projekt":
  - [ ] Formulář: název, fakulta (select), typ souboru (radio), pipeline
  - [ ] Dynamické načítání kroků pipeline při změně fakulty (AJAX)
  - [ ] Toggle: doporučená (z onboarding preference) vs. vlastní
  - [ ] Submit → `POST /projects` → refresh dashboard
- [ ] `api_client.py` — `list_projects()`, `create_project()`
- [ ] Komponenta: `modal.html` (reusable)
- [ ] `static/js/modal.js` — otevření/zavření modalu

**Testování:**
- Dashboard zobrazí projekty z mock backendu
- Vytvoření projektu → karta se objeví na dashboardu
- Prázdný stav se zobrazí správně

---

## Fáze 4 — Detail projektu + Upload

**Stránky:** Detail projektu, Modal upload  
**Prerekvizity:** Fáze 3

- [ ] Route `/projects/<project_id>`
- [ ] Seznam verzí (chronologicky, nejnovější nahoře)
- [ ] Status badge pro každou verzi
- [ ] Tlačítko "Porovnat s předchozí" (zobrazí se od V2)
- [ ] Modal "Upload nové verze":
  - [ ] Komponenta: `upload_dropzone.html`
  - [ ] `static/js/upload.js` — drag & drop, validace přípony a velikosti
  - [ ] Po výběru souboru: auto-submit (ne čekání na tlačítko) nebo tlačítko "Nahrát"
  - [ ] Progress bar při uploadu
  - [ ] Po úspěchu: redirect na `/projects/<id>/versions/<vid>/analysis`
- [ ] `api_client.py` — `get_project()`, `list_versions()`, `upload_version()`
- [ ] Cascade delete: tlačítko "Smazat projekt" + `confirm_dialog.html`

**Testování:**
- Detail projektu zobrazí verze z mock backendu
- Upload souboru → redirect na polling stránku
- Validace: špatná přípona zobrazí chybu
- Validace: soubor > 20 MB zobrazí chybu

---

## Fáze 5 — Polling analýzy

**Stránky:** Analýza probíhá  
**Prerekvizity:** Fáze 4

- [ ] Route `/projects/<project_id>/versions/<version_id>/analysis`
- [ ] Flask proxy endpoint: `GET /api/analysis-status/<project_id>/<version_id>`
- [ ] `static/js/poll.js`:
  - [ ] Polling interval 3 s / 10 s (backoff po 30 s)
  - [ ] Timeout 15 min
  - [ ] Terminální stavy → redirect nebo chybový stav
- [ ] UI: progress bar, aktuální krok, počet kroků
- [ ] Animovaný indikátor (CSS animace)
- [ ] Chybový stav + tlačítko "Zkusit znovu" → `POST /analysis/retry`
- [ ] `api_client.py` — `get_analysis_status()`, `retry_analysis()`

**Testování:**
- Mock vrátí `status: processing` 3× → pak `completed` → redirect na výsledky
- Mock vrátí `failed` → zobrazí chybový stav
- Timeout simulace (mock neodpoví terminálním stavem)

---

## Fáze 6 — Výsledky verze

**Stránky:** Výsledky verze  
**Prerekvizity:** Fáze 5

- [ ] Route `/projects/<project_id>/versions/<version_id>`
- [ ] Dvousloupcový layout: markdown viewer (65 %) + sidebar (35 %)
- [ ] `static/js/markdown_viewer.js`:
  - [ ] Renderování markdownu přes `marked.js`
  - [ ] Injekce `<mark>` tagů dle `char_start` / `char_end`
  - [ ] Klik na highlight → focus v sidebaru
- [ ] `static/css/markdown_viewer.css` — styly pro highlight, severity barvy
- [ ] Sidebar: `error_card.html`
  - [ ] Klik na kartu → scroll v markdown vieweru
  - [ ] Severity badge, typ chyby, popis
  - [ ] `suggested_fix` jen pro Pro tier
- [ ] Freemium teaser: `freemium_teaser.html` (zobrazí se po 3. chybě u free tieru)
- [ ] Filtrování v sidebaru dle severity / typu chyby
- [ ] Tab / toggle: "Výsledky" | "Porovnání" (link na diff)
- [ ] `api_client.py` — `get_version()`, `get_version_document()`, `get_errors()`

**Testování:**
- Markdown se renderuje správně
- Chyby jsou zvýrazněny na správných pozicích
- Synchronizace sidebar ↔ markdown viewer funguje
- Free tier vidí jen 3 chyby + teaser
- Pro tier vidí všechny chyby + suggested_fix

---

## Fáze 7 — Diff verzí

**Stránky:** Porovnání verzí  
**Prerekvizity:** Fáze 6

- [ ] Route `/projects/<project_id>/versions/<version_id>/diff`
- [ ] Tři sekce: Nové / Neopravené / Opravené
- [ ] Toggle mezi "Výsledky" a "Diff"
- [ ] Zobrazení jen od V2 (bez předchozí verze = diff není dostupný)
- [ ] `api_client.py` — `get_diff()`

---

## Fáze 8 — Profil

**Stránky:** Profil  
**Prerekvizity:** Fáze 1

- [ ] Route `/profile`
- [ ] `usage_bar.html` — skenů využito / budget, datum obnovy
- [ ] Tier info + upgrade CTA (placeholder)
- [ ] Odkaz na reset hesla
- [ ] Tlačítko odhlásit se
- [ ] `api_client.py` — `get_me()`, `get_usage()`

---

## Fáze 9 — Admin sekce

**Stránky:** Admin přehled, Uživatelé, Fakulty + Pipeline, Typy chyb, Domény, Audit log  
**Prerekvizity:** Fáze 1

- [ ] `admin/routes.py` — všechny admin routy
- [ ] `@admin_required` dekorátor (403 pro non-admin)
- [ ] Admin navbar varianta (banner "Admin mód")
- [ ] Uživatelé: tabulka, filtrování, detail, edit, delete
- [ ] Fakulty: CRUD, pipeline kroky (drag & drop pořadí)
- [ ] Typy chyb: CRUD (systémové read-only)
- [ ] Povolené domény: CRUD, toggle active
- [ ] Audit log: tabulka, read-only
- [ ] `api_client.py` — všechny admin funkce

---

## Fáze 10 — Polish & Error handling

**Prerekvizity:** Všechny předchozí fáze

- [ ] Globální error handlery (401, 403, 404, 500)
- [ ] `toast.js` — notifikace pro všechny API akce
- [ ] Loading stavy na všech tlačítkách (disabled + spinner při čekání)
- [ ] Responsivní layout (mobile: skrytý sidebar, accordion chyby)
- [ ] Prázdné stavy (žádné projekty, žádné chyby)
- [ ] Favicon, meta tagy
- [ ] Přepnutí z mock backendu na staging a otestování všech flows

---

## Pořadí priorit pro MVP (Květen 2026)

| Priorita | Fáze | Důvod |
|---|---|---|
| 🔴 Kritická | 0, 1, 3, 4, 5, 6 | Bez toho aplikace nefunguje |
| 🟡 Důležitá | 2 (Onboarding), 7 (Diff), 8 (Profil) | Potřebné pro UX |
| 🟢 Může počkat | 9 (Admin), 10 (Polish) | Admin může používat přímo API, polish je post-MVP |

---

## Technický stack frontendu

| Část | Technologie |
|---|---|
| Framework | Flask (Python) |
| Šablony | Jinja2 |
| CSS | Vlastní (CSS proměnné, bez frameworku) |
| JavaScript | Vanilla JS (bez frameworku) |
| Markdown rendering | `marked.js` (CDN) |
| HTTP volání backendu | `requests` (server-side, v api_client.py) |
| HTTP volání z prohlížeče | `fetch` API (jen pro polling a AJAX) |
| Env konfigurace | `python-dotenv` |
| Session | Flask server-side session (podepsaná cookie) |
