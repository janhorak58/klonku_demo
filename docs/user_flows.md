# Klonku — Uživatelské toky (User Flows)

---

## Flow 1: Registrace + Onboarding

```
[Landing page] → klik "Zaregistrovat se"
    ↓
[/register] → vyplní email + heslo (nebo Google)
    ↓
POST /auth/register
    ↓
[/verify-email] → "Zkontroluj inbox"
    ↓
Klik na odkaz v emailu → backend ověří token
    ↓
Redirect na [/onboarding]
    ↓
Uživatel vybere pipeline (doporučená / vlastní)
    ↓
Uloží se do session: onboarding_done = true, pipeline_preference
    ↓
[/dashboard]
```

**Větev: Google OAuth**
```
[/register] → klik "Registrovat přes Google"
    ↓
Flask generuje state token → uloží do session
    ↓
Redirect na Google OAuth
    ↓
Google callback → Flask ověří state token
    ↓
POST /auth/google {code}
    ↓
Backend vrátí tokeny + user data
    ↓
[/onboarding] (pokud nový uživatel) nebo [/dashboard]
```

---

## Flow 2: Přihlášení

```
[/login] → email + heslo
    ↓
POST /auth/login
    ↓
Uloží: access_token → Flask session
        refresh_token → httpOnly cookie
    ↓
[/dashboard]
```

**Automatický refresh (middleware `before_request`):**
```
Request přijde → chybí access_token v session?
    ↓ ano
Existuje refresh_token cookie?
    ↓ ano
POST /auth/refresh
    ↓
Nový access_token → session
    ↓
Požadavek pokračuje normálně
    ↓ (pokud refresh selže)
Redirect na /login
```

---

## Flow 3: Zapomenuté heslo

```
[/login] → klik "Zapomněl/a jsem heslo"
    ↓
[/forgot-password] → zadá email
    ↓
POST /auth/forgot-password
    ↓
Zobrazí: "Pokud účet existuje, pošleme odkaz."
    ↓
Klik na odkaz v emailu → [/reset-password?token=...]
    ↓
Zadá nové heslo → POST /auth/reset-password
    ↓
Úspěch → redirect na [/login]
```

---

## Flow 4: Vytvoření projektu + Upload

```
[/dashboard] → klik "+ Nový projekt"
    ↓
[Modal: Nový projekt]
  - Vyplní název
  - Vybere fakultu → načtou se kroky pipeline pro tuto fakultu
  - Vybere typ souboru (DOCX / LaTeX)
  - Potvrdí / upraví pipeline (default z onboardingu nebo vlastní)
    ↓
POST /projects
    ↓
Modal se zavře, dashboard se refreshne
Nový projekt je nahoře v seznamu
    ↓
Uživatel klikne na projekt → [/projects/<id>]
    ↓
Klik "Nahrát novou verzi"
    ↓
[Modal: Upload]
  - Vybere soubor (drag & drop nebo klik)
  - Klik "Nahrát a analyzovat"
    ↓
POST /projects/{id}/versions (multipart)
    ↓
Modal se zavře
Redirect na [/projects/<id>/versions/<vid>/analysis]
```

**Zkrácený flow (od V2):**
```
[/projects/<id>] → klik "Nahrát novou verzi"
    ↓
[Modal: Upload] → vybere soubor → automaticky se nahraje
    ↓
Redirect na [/projects/<id>/versions/<new_vid>/analysis]
```

---

## Flow 5: Sledování průběhu analýzy (Polling)

```
[/projects/<id>/versions/<vid>/analysis]
    ↓
JavaScript spustí polling:
  - 0–30 s: každé 3 s volá GET /api/analysis-status/<id>/<vid>
  - 30 s+: každých 10 s
    ↓
Aktualizuje UI:
  - Progress bar (percent)
  - Aktuální krok ("Kontrola citací...")
  - "X / Y kroků dokončeno"
    ↓
Terminální stav:
  completed / partial → redirect na /projects/<id>/versions/<vid>
  failed              → zobrazí chybu + tlačítko "Zkusit znovu"
  conversion_failed   → zobrazí chybu "Nepodařilo se převést soubor"
    ↓
Timeout (15 min bez terminálního stavu) → chybová zpráva
```

---

## Flow 6: Prohlížení výsledků

```
[/projects/<id>/versions/<vid>]
    ↓
Načte se: metadata verze + markdown obsah + seznam chyb
    ↓
Markdown viewer (vlevo):
  - Renderuje HTML z markdownu
  - Vloží <mark> tagy na pozice char_start–char_end každé chyby
  - Barevné kódování dle severity
    ↓
Sidebar (vpravo):
  - Zobrazí seznam chyb
  - Free tier: 3 chyby + teaser "a X dalších — odemkni Pro"
    ↓
Uživatel klikne na chybu v sidebaru:
  → Markdown viewer scrolluje na příslušný highlight
  → Chybová karta se rozbalí (suggested_fix pro Pro tier)
    ↓
Uživatel klikne na highlight v textu:
  → Sidebar se scrolluje na příslušnou chybu
  → Chybová karta se zvýrazní
```

---

## Flow 7: Porovnání verzí (Diff)

```
[/projects/<id>] → klik "Porovnat s předchozí" u verze ≥ V2
    ↓
[/projects/<id>/versions/<vid>/diff]
    ↓
Zobrazí 3 sekce:
  Nové chyby (X)      — přibyly v této verzi
  Neopravené (X)      — přešly z předchozí verze
  Opravené (X) ✅     — v předchozí verzi byly, teď nejsou
    ↓
Klik na záložku "Výsledky" → přejde na /projects/<id>/versions/<vid>
```

---

## Flow 8: Odhlášení

```
Klik "Odhlásit se" (navbar nebo profil)
    ↓
POST /auth/logout (pošle refresh_token z cookie)
    ↓
Session se vymaže
Cookie se smaže
    ↓
Redirect na /login
```

---

## Flow 9: Admin — Správa pipeline

```
[/admin] → Fakulty
    ↓
[/admin/faculties] → vybere fakultu
    ↓
[/admin/faculties/<id>/pipeline]
    ↓
Klik "Přidat krok"
  - Zadá název, prompt template
  - Uloží → POST /admin/faculties/<id>/pipeline-steps
    ↓
Klik "Upravit" u existujícího kroku
  - Změní prompt → PUT /admin/pipeline-steps/<step_id>
  - Backend automaticky verzionuje (PIPELINE_STEP_VERSION)
    ↓
Klik "Smazat" → potvrzovací dialog → DELETE /admin/pipeline-steps/<step_id>
```

---

## Chybové stavy (globální)

| HTTP kód | Co se stane na frontendu |
|---|---|
| 401 | Smazat session + redirect na /login |
| 403 | Zobrazit stránku "Nemáš přístup" |
| 404 | Zobrazit stránku "Nenalezeno" |
| 429 | Zobrazit "Příliš mnoho pokusů, zkus za chvíli" |
| 503 | Zobrazit "Služba dočasně nedostupná" |
| Síťová chyba | Toast "Zkontroluj připojení" + retry tlačítko |
