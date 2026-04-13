# Klonku — Sdílené UI komponenty

> Komponenty jsou Jinja2 makra nebo `{% include %}` bloky. Barevná paleta vychází z brandingu Klonku.

---

## Brand

```css
:root {
  --salmon:       #D95F3B;   /* primární akcent, CTA tlačítka */
  --salmon-light: #F5E8E3;   /* pozadí karet, hover stavy */
  --salmon-mid:   #EEC4B3;   /* oddělovače, borders */
  --cream:        #FDFAF7;   /* hlavní pozadí stránek */
  --dark:         #1C1410;   /* primární text */
  --mid:          #6B4F3F;   /* sekundární text, popisky */
  --light:        #B09080;   /* placeholder, disabled */
  --accent-green: #3B8C6E;   /* úspěch, ověřeno, completed */

  /* Severity chyb */
  --sev-critical: #DC2626;
  --sev-high:     #EA580C;
  --sev-medium:   #D97706;
  --sev-low:      #16A34A;
}
```

**Fonty:**
- `Libre Baskerville` — logo
- `Playfair Display` — sekční nadpisy (h2, h3)
- `DM Sans` — tělo textu, UI prvky

---

## Navbar

**Soubor:** `templates/components/navbar.html`

```
[Logo Klonku]    [Dashboard]    [Profil ▾]    [Tier badge]
                                  ↳ Můj profil
                                  ↳ Odhlásit se
```

**Variace:**
- `authenticated` — plný navbar s uživatelem
- `auth-only` — jen logo (použito na /login, /register, /onboarding)

**Tier badge:**
- `institutional_free` → zelená: "Akademický free"
- `basic` → šedá: "Basic"
- `pro` → salmon: "Pro"
- `unverified` → oranžová: "Neověřeno"

**Admin banner** (pokud `user.role == 'superadmin'`):
- Tenký pruh nad navbarem: "Admin mód — [Správa →]"

---

## Tlačítka

**Soubor:** `templates/components/button.html`

| Varianta | Použití |
|---|---|
| `btn-primary` | Hlavní CTA (salmon background, bílý text) |
| `btn-secondary` | Sekundární akce (outline, salmon border) |
| `btn-danger` | Smazání, destruktivní akce (červená) |
| `btn-ghost` | Tertiary, odkazové akce (bez borderu) |
| `btn-sm` / `btn-lg` | Velikostní modifikátory |

---

## Modal

**Soubor:** `templates/components/modal.html`

Reusable overlay. Otevírá se přes JavaScript (`data-modal="modal-id"`).

```
┌─────────────────────────────┐
│ Nadpis modalu          [✕]  │
├─────────────────────────────┤
│                             │
│    Obsah (slot)             │
│                             │
├─────────────────────────────┤
│ [Zrušit]   [Potvrdit akci] │
└─────────────────────────────┘
```

- Klik na `✕` nebo `Escape` zavře modal
- Backdrop (tmavý overlay) zavře modal při kliku mimo

---

## Projekt karta (Dashboard)

**Soubor:** `templates/components/project_card.html`

```
┌────────────────────────────────┐
│ Analýza sentimentu             │
│ FM · DOCX                      │
│                                │
│ Poslední analýza: 31. 3. 2026  │
│ 3 verze · 12 chyb              │
│                          [●] completed │
│                                │
│         [Otevřít →]            │
└────────────────────────────────┘
```

---

## Status badge

**Soubor:** `templates/components/status_badge.html`

| Status | Barva | Text |
|---|---|---|
| `pending` | šedá | Čeká ve frontě |
| `processing` | modrá (animovaná) | Analyzuji… |
| `completed` | zelená | Dokončeno |
| `partial` | oranžová | Částečně |
| `failed` | červená | Chyba |
| `conversion_failed` | červená | Nelze převést |

---

## Error karta (sidebar výsledků)

**Soubor:** `templates/components/error_card.html`

```
┌──────────────────────────────────────┐
│ [CITACE] ● high                      │
│ Chybí rok vydání u zdroje "Novák…"   │
│                                      │
│ [Přejít na místo v textu →]          │
│                                      │
│ Návrh opravy: (Pro tier)             │
│ "Doplňte: (Novák et al., 2019)."     │
└──────────────────────────────────────┘
```

**Severity indikátor:** barevný pruh vlevo (dle `--sev-*`)

**Stav karet:**
- `default` — standardní zobrazení
- `active` — zvýrazněná (klik z markdownu nebo sidebar)
- `locked` — free tier, rozmazaná / blur efekt

---

## Freemium teaser

**Soubor:** `templates/components/freemium_teaser.html`

Zobrazí se v sidebaru pod 3. chybou u `institutional_free` tieru.

```
┌──────────────────────────────────────┐
│  🔒  + 14 dalších chyb skryto        │
│                                      │
│  Přejdi na Pro a odhal všechny chyby │
│  bez nutnosti nového skenování.      │
│                                      │
│        [Upgradovat na Pro →]         │
└──────────────────────────────────────┘
```

---

## Markdown viewer

**Soubor:** `static/js/markdown_viewer.js` + `static/css/markdown_viewer.css`

- Renderuje markdown → HTML (knihovna `marked.js`)
- Po renderování projde seznam chyb a obalí text na pozicích `char_start`–`char_end` do:
  ```html
  <mark class="error-highlight sev-high" data-error-id="uuid">...</mark>
  ```
- Klik na `<mark>` → triggere event `error:focus` s `error_id`
- Sidebar naslouchá eventu a scrolluje/aktivuje příslušnou kartu

**CSS třídy:**
```css
.error-highlight.sev-critical { background: rgba(220, 38, 38, 0.2); }
.error-highlight.sev-high     { background: rgba(234, 88, 12, 0.2); }
.error-highlight.sev-medium   { background: rgba(217, 119, 6, 0.2); }
.error-highlight.sev-low      { background: rgba(22, 163, 74, 0.15); }
.error-highlight.active       { outline: 2px solid currentColor; }
```

---

## Polling progress bar

**Soubor:** `static/js/poll.js`

```
Analyzuji dokument…
━━━━━━━━━━━━━━━░░░░░░░░░░░░░  40 %
Krok 2 / 5 — Kontrola citací
```

- Plynulá animace progress baru
- Aktualizuje se při každém polling responsu
- Při `completed` / `partial`: přesměrování
- Při `failed` / `conversion_failed`: chybový stav + retry tlačítko

---

## Upload dropzone

**Soubor:** `templates/components/upload_dropzone.html` + `static/js/upload.js`

```
┌─────────────────────────────────────────┐
│                                         │
│    📄  Přetáhni soubor sem              │
│        nebo klikni pro výběr            │
│                                         │
│        .docx nebo .tex · max 20 MB      │
│                                         │
└─────────────────────────────────────────┘
```

**Stavy:**
- `idle` — výchozí
- `dragover` — soubor přetahován (salmon border, světlé pozadí)
- `selected` — soubor vybrán (zobrazí název + velikost)
- `uploading` — progress bar
- `error` — chybná přípona nebo velikost (inline zpráva)

---

## Toast notifikace

**Soubor:** `static/js/toast.js`

Malé notifikace v rohu obrazovky (pravý dolní roh).

| Typ | Barva | Použití |
|---|---|---|
| `success` | zelená | Projekt vytvořen, verze nahrána |
| `error` | červená | Chyba sítě, API chyba |
| `info` | modrá | Informační hláška |
| `warning` | oranžová | Limit skenů, partial status |

Auto-dismiss po 4 s. Klik zavře okamžitě.

---

## Usage bar (profil)

**Soubor:** `templates/components/usage_bar.html`

```
Skeny tento měsíc
[████████░░░░░░░░░░░░] 3 / 5
Obnoví se 1. května 2026
```

- Procento z `monthly_scan_count / monthly_scan_budget`
- Barva: zelená < 60 %, oranžová 60–90 %, červená > 90 %

---

## Pagination

**Soubor:** `templates/components/pagination.html`

```
← Předchozí   [1] [2] [3] …   Další →
```

Generuje se z `total`, `limit`, `offset`. Předává query parametry přes GET.

---

## Potvrzovací dialog

**Soubor:** `templates/components/confirm_dialog.html`

Jednoduchý modal pro destruktivní akce (smazání projektu, uživatele).

```
┌────────────────────────────────┐
│ Smazat projekt?                │
│                                │
│ Tato akce je nevratná.         │
│ Smažou se všechny verze        │
│ a nalezené chyby.              │
│                                │
│ [Zrušit]        [Smazat →]    │
└────────────────────────────────┘
```

- "Smazat" tlačítko: červené, disabled 2 s po otevření (prevence kliku omylem)
