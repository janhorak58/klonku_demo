# Klonku — Přehled stránek frontendu

> Flask frontend volá FastAPI backend přes `api_client.py`. Landing page běží samostatně jinde.

---

## Legenda

- **Auth:** `public` / `login_required` / `admin_required`
- **API calls:** funkce z `api_client.py`

---

## 1. Login

**Route:** `GET/POST /login`  
**Auth:** public (přihlášeného redirectuje na dashboard)

### Účel
Přihlášení existujícího uživatele.

### UI elementy
- Logo Klonku (odkaz na landing page)
- Formulář: email + heslo + tlačítko "Přihlásit se"
- Odkaz "Přihlásit se přes Google" (OAuth redirect)
- Odkaz "Zapomněl/a jsem heslo" → `/forgot-password`
- Odkaz "Nemáš účet? Zaregistruj se" → `/register`
- Chybová hláška při špatných přihlašovacích údajích (inline, ne flash)

### API calls
- `POST /auth/login` → uloží `access_token` do session, `refresh_token` do httpOnly cookie
- `POST /auth/google` → po OAuth callbacku

### Poznámky
- Po úspěšném přihlášení redirect na `/dashboard`
- Google OAuth: Flask generuje `state` token, uloží do session, ověří v callbacku

---

## 2. Registrace

**Route:** `GET/POST /register`  
**Auth:** public

### Účel
Vytvoření nového účtu.

### UI elementy
- Formulář: email + heslo + potvrzení hesla + tlačítko "Zaregistrovat se"
- Tlačítko "Registrovat přes Google"
- Odkaz "Už máš účet? Přihlaš se" → `/login`
- Inline validace (hesla se shodují, email formát)

### API calls
- `POST /auth/register`

### Poznámky
- Po úspěšné registraci redirect na `/verify-email` (čekání na email)
- Backend automaticky rozpozná doménu emailu a nastaví tier (`institutional_free` vs. `unverified`)

---

## 3. Ověření emailu

**Route:** `GET /verify-email`  
**Auth:** public

### Účel
Informační stránka — uživatel čeká na klik z verifikačního emailu.

### UI elementy
- Ikona obálky / emailu
- Text: "Poslali jsme ti odkaz na [email]. Klikni na odkaz pro potvrzení."
- Tlačítko "Znovu odeslat email" (rate-limitováno)
- Odkaz "Přihlásit se jiným účtem" → `/login`

### API calls
- `POST /auth/resend-verification` (při znovu odeslání)

### Poznámky
- `GET /auth/verify-email/{token}` zpracuje backend sám; Flask jen zobrazí výsledek
- Po ověření backend nastaví `email_verified = true` a aktivuje tier
- Uživatel s `email_verified = false` nemůže spouštět analýzy

---

## 4. Zapomenuté heslo

**Route:** `GET/POST /forgot-password`  
**Auth:** public

### UI elementy
- Formulář: email + tlačítko "Odeslat odkaz"
- Po odeslání: potvrzovací zpráva (vždy stejná — neodhalujeme existenci emailu)

### API calls
- `POST /auth/forgot-password`

---

## 5. Reset hesla

**Route:** `GET/POST /reset-password`  
**Auth:** public (token v query parametru)

### UI elementy
- Formulář: nové heslo + potvrzení + tlačítko "Nastavit heslo"
- Chyba při neplatném / prošlém tokenu

### API calls
- `POST /auth/reset-password` (s tokenem z URL a novým heslem)

---

## 6. Onboarding

**Route:** `GET/POST /onboarding`  
**Auth:** `login_required` (přeskočí, pokud onboarding už proběhl)

### Účel
Jednorázový průvodce po registraci. Uživatel nastaví výchozí pipeline pro svůj účet.

### UI elementy
- Nadpis: "Jak chceš kontrolovat svou práci?"
- **Karta A — Doporučená pipeline** (pre-selected)
  - Label: "Doporučeno"
  - Popis: "Kompletní kontrola dle směrnic fakulty — citace, typografie, struktura, jazyk."
  - Zobrazí seznam kroků (read-only chips)
- **Karta B — Vlastní pipeline**
  - Checkbox list kroků pipeline (načtených ze všech fakult)
  - Uživatel zaškrtne, co chce
- Tlačítko "Pokračovat na dashboard"

### API calls
- `GET /faculties` → seznam fakult (pro načtení dostupných kroků)
- `GET /faculties/{faculty_id}/pipeline-steps` → kroky pipeline
- Preference se ukládá do Flask session (není endpoint pro "user default pipeline" — nastaví se při vytváření projektu)

### Poznámky
- Onboarding stránka se zobrazí jen jednou; po dokončení se uloží do session `onboarding_done = true`
- Výběr z onboardingu se použije jako výchozí hodnota v modalu "Nový projekt"

---

## 7. Dashboard

**Route:** `GET /dashboard`  
**Auth:** `login_required`

### Účel
Přehled všech projektů uživatele. Vstupní bod po přihlášení.

### UI elementy
- Navbar (logo, jméno uživatele, tier badge, odkaz na profil, odhlášení)
- Nadpis "Moje projekty"
- Tlačítko "+ Nový projekt" → otevře modal (viz stránka 8)
- **Grid projektových karet**, každá karta obsahuje:
  - Název projektu
  - Fakulta + typ práce (DOCX/LaTeX)
  - Počet verzí
  - Status poslední verze (badge: `pending` / `processing` / `completed` / `failed`)
  - Datum poslední aktivity
  - Tlačítko "Otevřít"
- Prázdný stav: ilustrace + text "Zatím žádné projekty. Vytvořte první."
- Pagination (limit 20, offset)

### API calls
- `GET /projects?limit=20&offset=0`

---

## 8. Modal — Nový projekt

**Trigger:** tlačítko "+ Nový projekt" na dashboardu  
**Auth:** `login_required`

### Účel
Vytvoření nového projektu. Vybírá se fakulta, typ práce a pipeline.

### UI elementy
- Pole: Název projektu (text input)
- Select: Fakulta (dropdown ze seznamu fakult)
- Select: Typ souboru — DOCX nebo LaTeX (radio)
- Sekce pipeline:
  - **Možnost A: Doporučená** (výchozí, pre-selected dle onboardingu)
    - Chips s kroky pipeline (read-only)
  - **Možnost B: Vlastní**
    - Checkbox list kroků pro vybranou fakultu
- Tlačítko "Vytvořit projekt"
- Tlačítko "Zrušit"

### API calls
- `GET /admin/faculties` nebo `GET /faculties` → seznam fakult
- `GET /faculties/{faculty_id}/pipeline-steps` → kroky pro zvolenou fakultu (volá se při změně faculty selectu)
- `POST /projects`

### Poznámky
- Po vytvoření projektu: modal se zavře, dashboard se refreshne, nový projekt je nahoře

---

## 9. Detail projektu

**Route:** `GET /projects/<project_id>`  
**Auth:** `login_required` (403 pokud projekt nepatří uživateli)

### Účel
Přehled verzí dokumentu, upload nové verze.

### UI elementy
- Breadcrumb: Dashboard → [Název projektu]
- Hlavička: název projektu, fakulta, typ, tlačítko "Nahrát novou verzi" → modal upload
- **Seznam verzí** (chronologicky, nejnovější nahoře):
  - Číslo verze (V1, V2, …)
  - Datum nahrání
  - Status badge (`pending` / `processing` / `completed` / `partial` / `failed` / `conversion_failed`)
  - Počet chyb (pokud `completed` nebo `partial`)
  - Tlačítko "Zobrazit výsledky" → `/projects/<id>/versions/<id>`
  - Tlačítko "Porovnat s předchozí" → `/projects/<id>/versions/<id>/diff` (zobrazí se od V2)
- Prázdný stav: "Nahrajte první verzi dokumentu."

### API calls
- `GET /projects/{project_id}`
- `GET /projects/{project_id}/versions`

---

## 10. Modal — Upload nové verze

**Trigger:** tlačítko "Nahrát novou verzi" na detailu projektu  
**Auth:** `login_required`

### Účel
Nahrání souboru → okamžité spuštění analýzy.

### UI elementy
- Dropzone: "Přetáhni soubor nebo klikni pro výběr"
- Povolené typy: `.docx`, `.tex` (max 20 MB)
- Po výběru souboru: zobrazí se název souboru + velikost
- Tlačítko "Nahrát a analyzovat"
- Progress bar při uploadu
- Tlačítko "Zrušit"

### API calls
- `POST /projects/{project_id}/versions` (multipart/form-data)

### Poznámky
- Po úspěšném uploadu: modal se zavře, redirect na `/projects/<id>/versions/<version_id>/analysis`
- Frontend nečeká na výsledek analýzy — jen nahraje soubor a přejde na polling stránku

---

## 11. Analýza probíhá (Polling)

**Route:** `GET /projects/<project_id>/versions/<version_id>/analysis`  
**Auth:** `login_required`

### Účel
Zobrazení průběhu analýzy. Polling dokud nedojde k finálnímu stavu.

### UI elementy
- Nadpis: "Analyzuji dokument…"
- Progress bar (plynulý) + procento
- Aktuální krok: "Kontrola citací" (textový popis)
- Počet hotových kroků: "2 / 5"
- Animovaný indikátor (spinner nebo pulzující prvek)
- Po dokončení: automatický redirect na `/projects/<id>/versions/<id>` (výsledky)
- Při `failed` / `conversion_failed`: chybová zpráva + tlačítko "Zkusit znovu"

### Polling logika (JavaScript)
- Interval: 3 s prvních 30 s, pak 10 s (backoff)
- Timeout: 15 minut → zobrazí chybu
- Terminální stavy: `completed`, `partial`, `failed`, `conversion_failed`

### API calls (přes Flask proxy endpoint)
- `GET /api/analysis-status/<project_id>/<version_id>` → proxuje `GET /projects/{id}/versions/{id}/analysis`

---

## 12. Výsledky verze

**Route:** `GET /projects/<project_id>/versions/<version_id>`  
**Auth:** `login_required`

### Účel
Zobrazení výsledků analýzy. Vlevo markdown, vpravo sidebar s chybami.

### UI elementy

**Layout: dvě kolumny**

**Levá část (markdown viewer, ~65 % šířky):**
- Markdown text dokumentu (renderovaný HTML)
- Chyby jsou zvýrazněny přímo v textu (highlight na základě `char_start` / `char_end`)
- Klik na highlight → zobrazí detail chyby v sidebaru (nebo scrolluje sidebar)
- Barevné kódování dle severity: critical (červená), high (oranžová), medium (žlutá), low (zelená)

**Pravý sidebar (~35 % šířky):**
- Záhlaví: "Nalezené chyby (X)" + filtr dle severity / typu
- Seznam chybových karet:
  - Typ chyby (label)
  - Severity badge
  - Krátký popis
  - Tlačítko "Přejít na místo v textu" → scroll v markdown vieweru
  - Pro Pro tier: také `suggested_fix`
- **Free tier teaser:** zobrazí 3 chyby + "a X dalších — odemkni Pro"
- Přepínač pohledů: "Výsledky" | "Porovnání s předchozí" (tab / toggle)

**Hlavička stránky:**
- Breadcrumb: Dashboard → Projekt → Verze 3
- Status badge verze
- Datum analýzy, počet chyb
- Tlačítko "Nahrát novou verzi" (modal)

### API calls
- `GET /projects/{project_id}/versions/{version_id}` → metadata verze
- `GET /projects/{project_id}/versions/{version_id}/document` → markdown obsah
- `GET /projects/{project_id}/versions/{version_id}/errors` → seznam chyb

### Poznámky
- Markdown se renderuje na frontendu (např. `marked.js`)
- Zvýraznění chyb přes `char_start` / `char_end` → obalení textu do `<mark>` tagu s CSS třídou dle severity
- Free tier filtrování: backend vrací všechna data, frontend zobrazí jen 3 (nebo backend vrátí omezená data — upřesnit s backendem)

---

## 13. Diff — Porovnání verzí

**Route:** `GET /projects/<project_id>/versions/<version_id>/diff`  
**Auth:** `login_required`

### Účel
Zobrazení rozdílů oproti předchozí verzi (co se opravilo, co je nové, co stále trvá).

### UI elementy
- Záhlaví: "Porovnání: Verze 2 vs. Verze 3"
- Tři sekce / záložky:
  - **Nové chyby** (X) — chyby, které v minulé verzi nebyly
  - **Neopravené** (X) — chyby, které přešly z minulé verze
  - **Opravené** (X) — chyby, které uživatel opravil ✅
- Každá chyba v kartě: stejný formát jako v sidebaru výsledků
- Přepínač: "Diff" | "Výsledky" → link zpět na výsledky verze

### API calls
- `GET /projects/{project_id}/versions/{version_id}/diff`

### Poznámky
- Tato stránka je dostupná pouze od V2 výše (předchozí verze musí existovat)

---

## 14. Profil

**Route:** `GET /profile`  
**Auth:** `login_required`

### Účel
Informace o uživatelském účtu, tier a využití skenů.

### UI elementy
- Sekce "Můj účet": jméno, email, tier badge
- Sekce "Využití":
  - Progress bar: "Využito X z Y skenů tento měsíc"
  - Text "Obnoví se 1. [měsíc]"
  - (bez absolutních čísel tokenů — jen skenů)
- Sekce "Plán":
  - Aktuální tier (institutional_free / Basic / Pro)
  - Tlačítko "Upgradovat" (zatím placeholder)
- Sekce "Zabezpečení":
  - Tlačítko "Změnit heslo" (redirect na reset-password flow)
- Tlačítko "Odhlásit se"

### API calls
- `GET /users/me`
- `GET /users/me/usage`

---

## 15. Admin — Přehled

**Route:** `GET /admin`  
**Auth:** `admin_required`

### Účel
Rozcestník administrace.

### UI elementy
- Stejný navbar jako zbytek + zvýrazněný "Admin" badge
- Karty / rychlé linky:
  - Uživatelé (X celkem)
  - Fakulty (X)
  - Pipeline kroky
  - Typy chyb
  - Povolené domény
  - Audit log

---

## 16. Admin — Uživatelé

**Route:** `GET /admin/users`  
**Auth:** `admin_required`

### UI elementy
- Tabulka: email, role, tier, skenů využito/budget, datum registrace, email verified
- Filtrování dle tieru / role
- Klik na řádek → detail uživatele
- Pagination

### API calls
- `GET /admin/users?limit=20&offset=0`

---

## 17. Admin — Detail uživatele

**Route:** `GET /admin/users/<user_id>`  
**Auth:** `admin_required`

### UI elementy
- Všechny atributy uživatele
- Formulář pro úpravu: role, tier, monthly_scan_budget
- Tlačítko "Smazat uživatele" (s potvrzovacím dialogem)

### API calls
- `GET /admin/users/{user_id}`
- `PUT /admin/users/{user_id}`
- `DELETE /admin/users/{user_id}`

---

## 18. Admin — Fakulty a Pipeline

**Route:** `GET /admin/faculties`  
**Auth:** `admin_required`

### UI elementy
- Seznam fakult s tlačítkem "Přidat fakultu"
- Každá fakulta: název, kód, počet kroků pipeline, tlačítko "Spravovat kroky"

### Sub-stránka: `/admin/faculties/<faculty_id>/pipeline`
- Seznam kroků pipeline (drag & drop pro pořadí)
- Každý krok: název, zkrácený prompt, verze, status (active/inactive)
- Tlačítko "Přidat krok" / "Upravit" / "Smazat"
- Při úpravě: textarea pro prompt template, toggle active

### API calls
- `GET /admin/faculties`
- `POST /admin/faculties`
- `GET /admin/faculties/{faculty_id}/pipeline-steps`
- `POST /admin/faculties/{faculty_id}/pipeline-steps`
- `PUT /admin/pipeline-steps/{step_id}`
- `DELETE /admin/pipeline-steps/{step_id}`

---

## 19. Admin — Typy chyb

**Route:** `GET /admin/error-types`  
**Auth:** `admin_required`

### UI elementy
- Tabulka: slug, label, popis, systémový (ano/ne)
- Tlačítko "Přidat typ" (vlastní, ne systémový)
- Systémové typy: jen čtení, nelze smazat

### API calls
- `GET /admin/error-types`
- `POST /admin/error-types`
- `PUT /admin/error-types/{type_id}`
- `DELETE /admin/error-types/{type_id}`

---

## 20. Admin — Povolené domény

**Route:** `GET /admin/allowed-domains`  
**Auth:** `admin_required`

### UI elementy
- Tabulka: doména, název univerzity, skenů zdarma/měsíc, aktivní
- Tlačítko "Přidat doménu"
- Toggle pro aktivaci/deaktivaci

### API calls
- `GET /admin/allowed-domains`
- `POST /admin/allowed-domains`
- `PATCH /admin/allowed-domains/{id}`
- `DELETE /admin/allowed-domains/{id}`

---

## 21. Admin — Audit log

**Route:** `GET /admin/audit-log`  
**Auth:** `admin_required`

### UI elementy
- Tabulka: datum, admin, akce, typ objektu, ID objektu
- Filtrování dle admina / akce
- Read-only

### API calls
- `GET /admin/audit-log`
