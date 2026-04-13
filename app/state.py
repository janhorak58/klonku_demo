from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any


def _now() -> datetime:
    return datetime(2026, 4, 3, 10, 0)


def _timestamp(days: int = 0, hours: int = 0, minutes: int = 0) -> str:
    return (_now() + timedelta(days=days, hours=hours, minutes=minutes)).strftime("%Y-%m-%d %H:%M")


def _demo_economics_document_html() -> str:
    return """
<h1>Vliv inflace na spotřebitelské chování domácností v ČR</h1>
<p>Tato bakalářská práce analyzuje, jak se v letech 2021 až 2023 proměnila struktura výdajů českých domácností v reakci na růst cen potravin, energií a služeb. Zaměřuje se na domácnosti s čistým příjmem do 45 000 Kč měsíčně a porovnává jejich spotřební rozhodování s domácnostmi středněpříjmovými.</p>
<div class="demo-kpi-grid">
  <div class="demo-kpi-card">
    <span>Průměrná inflace</span>
    <strong><span class="error-hl hl-medium" data-error="error-13">17,2%</span></strong>
    <small>vrchol sledovaného období</small>
  </div>
  <div class="demo-kpi-card">
    <span>Domácnosti ve vzorku</span>
    <strong>1 248</strong>
    <small>kombinace ČSÚ, STEM/MARK a vlastního dotazníku</small>
  </div>
  <div class="demo-kpi-card">
    <span>Pokles diskreční spotřeby</span>
    <strong>14,6 %</strong>
    <small>volný čas, kultura a drobné služby</small>
  </div>
</div>

<h2>1. Úvod</h2>
<p><span class="error-hl hl-critical" data-error="error-1">Cílem práce je popsat, jak inflace změnila výdaje domácností.</span> Text ale v této části výslovně neformuluje výzkumnou otázku, podle které by bylo možné později jednoznačně posoudit naplnění cíle a interpretovat zjištěné výsledky.</p>
<p>Podle ČNB a Eurostatu se česká ekonomika v roce 2022 dostala do období výrazné cenové nestability. <span class="error-hl hl-high" data-error="error-7">Inflace byla v ČR jedna z nejvyšších v celé EU a domácnosti proto změnily své nákupy napříč všemi kategoriemi.</span> Tvrzení je nosné pro celý úvod, ale není zde uveden přesný zdroj ani konkrétní statistika.</p>
<p>V běžné veřejné debatě se často opakuje, že <span class="error-hl hl-low" data-error="error-19">domácnosti prostě začaly šetřit skoro na všem</span>, což je ale zjednodušující interpretace. Ve skutečnosti byl pokles spotřeby rozdílný mezi jednotlivými příjmovými skupinami, regiony i typy výdajů.</p>

<h2>2. Teoretická východiska</h2>
<p>Teorie spotřebitelského chování vychází z předpokladu, že domácnost maximalizuje užitek při daném rozpočtovém omezení. V textu je však patrné, že <span class="error-hl hl-critical" data-error="error-2">hypotézy nejsou v práci formulovány samostatně a nejsou navázány na analytickou část</span>, přestože struktura práce později pracuje s testováním předpokladů o poklesu reálné spotřeby.</p>
<p>Pro makroekonomické zasazení je využit komentář Evropské centrální banky, podle nějž se inflační vlna šířila zejména přes energetické a potravinové vstupy. Citace je uvedena jen jako <span class="error-hl hl-high" data-error="error-8">ECB (2024)</span>, bez názvu dokumentu, URL, data citace nebo stránky, což znemožňuje přesné dohledání originálního zdroje.</p>
<p>Podobně problematicky působí věta, že inflace dlouhodobě mění očekávání <span class="error-hl hl-low" data-error="error-20">domacnosti</span> o budoucí kupní síle. Vedle pravopisné chyby je zde použita formulace bez opory v bezprostředně uvedené literatuře.</p>
<p>Rešeršní část dále cituje sekundární interpretaci OECD vývoje cen, když uvádí, že <span class="error-hl hl-high" data-error="error-9">jak uvádí Novotná (2023) podle OECD, české domácnosti reagovaly na inflaci rychleji než domácnosti v Polsku</span>. Není ale jasné, který dokument OECD je původním zdrojem a zda autorka cituje přímo nebo zprostředkovaně.</p>
<p>Definice inflace je v jedné pasáži převzata z obecné encyklopedie, konkrétně z formulace <span class="error-hl hl-high" data-error="error-10">„Inflace je všeobecný růst cenové hladiny v ekonomice“ (Wikipedie, 2024)</span>, což neodpovídá požadavkům na akademický zdroj použitý v teoretické kapitole.</p>
<p>V další části se autorka opírá o publikaci z období před pandemií a tvrdí, že strukturální změny spotřeby domácností lze vysvětlit již podle práce <span class="error-hl hl-medium" data-error="error-12">Jandová (2012)</span>. Vzhledem k mimořádné povaze inflace po roce 2021 je použití takto starého zdroje bez novější korekce metodicky slabé.</p>

<h2>3. Data a metodika</h2>
<p>Analytická část kombinuje sekundární data a vlastní dotazníkové šetření. Hned v úvodu metodiky se ale píše, že <span class="error-hl hl-high" data-error="error-25">zpracovaná data pokrývají období 2020 až 2023</span>, ačkoli zadání práce i úvod výslovně vymezují sledované období jen na roky 2021 až 2023.</p>
<p>Výzkumný soubor je jednou popsán jako soubor o velikosti 1 248 respondentů, zatímco o odstavec níže autorka uvádí, že <span class="error-hl hl-high" data-error="error-26">do finální analýzy vstoupilo 1 182 domácností</span>, aniž by vysvětlila, jaké případy byly ze vzorku vyřazeny a proč.</p>
<p>V části s operacionalizací proměnných se současně pracuje s nominálními výdaji a reálně očištěnými příjmy. Věta <span class="error-hl hl-high" data-error="error-27">výdaje byly porovnávány v běžných cenách, zatímco příjmy byly převedeny do cen roku 2021</span> vytváří metodický nesoulad, který ztěžuje interpretaci elasticity spotřeby.</p>
<p>Metodika dále uvádí, že model používá vícerozměrnou regresi, ale jen ve formě stručného konstatování <span class="error-hl hl-medium" data-error="error-28">vztahy mezi proměnnými byly testovány pomocí regresního modelu</span>. Chybí specifikace závislé proměnné, kontrolních proměnných i základní odhadovací rovnice.</p>
<p>Ve stejné kapitole není popsáno, jak byl sestaven výběr respondentů podle regionů a typu domácnosti. Pasáž <span class="error-hl hl-critical" data-error="error-4">respondenti byli osloveni prostřednictvím online panelu a doporučení studentů</span> neobsahuje informaci o kritériích zařazení, stratifikaci ani reprezentativnosti souboru.</p>
<p>Chybí také vysvětlení, zda byly časové řady sezonně očištěny. Formulace <span class="error-hl hl-critical" data-error="error-5">měsíční data byla použita v původní podobě bez dalších úprav</span> je problematická, protože srovnává spotřebu za období s odlišnou sezonností a může zkreslovat meziroční závěry.</p>

<div class="demo-chart-card">
  <div class="demo-chart-header">
    <strong>Vývoj inflace a maloobchodních tržeb</strong>
    <span>ČR, 2021–2023</span>
  </div>
  <svg class="demo-chart-svg" viewBox="0 0 640 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Vývoj inflace a maloobchodních tržeb">
    <rect x="0" y="0" width="640" height="240" rx="18" fill="#fff8f4"/>
    <line x1="70" y1="190" x2="590" y2="190" stroke="#d7c6bb" stroke-width="2"/>
    <line x1="70" y1="45" x2="70" y2="190" stroke="#d7c6bb" stroke-width="2"/>
    <polyline fill="none" stroke="#d95f3b" stroke-width="4" points="90,160 180,138 270,108 360,72 450,88 540,126"/>
    <polyline fill="none" stroke="#3b8c6e" stroke-width="4" points="90,128 180,132 270,142 360,158 450,150 540,138"/>
    <g fill="#6b4f3f" font-family="Inter, sans-serif" font-size="12">
      <text x="90" y="210">2021 Q1</text>
      <text x="180" y="210">2021 Q4</text>
      <text x="270" y="210">2022 Q2</text>
      <text x="360" y="210">2022 Q4</text>
      <text x="450" y="210">2023 Q2</text>
      <text x="540" y="210">2023 Q4</text>
    </g>
  </svg>
  <p class="demo-chart-caption"><span class="error-hl hl-medium" data-error="error-14">Graf 1: Inflace a tržby maloobchodu</span></p>
</div>

<h2>4. Analýza výsledků</h2>
<p>V datech je patrný pokles výdajů na volnočasové aktivity a růst podílu výdajů na potraviny, bydlení a energie. Při popisu vývoje spotřeby ale autorka přechází mezi meziroční inflací a ročním průměrem a uvádí, že <span class="error-hl hl-medium" data-error="error-29">vysoká inflace v roce 2022 byla srovnána s průměrem za celé období 2021–2023</span>, aniž by vysvětlila, proč jsou porovnávány odlišně konstruované ukazatele.</p>
<p>Pro doplnění textu je zařazena informace, že <span class="error-hl hl-high" data-error="error-11">index spotřebitelské důvěry se v období vysoké inflace propadl na historické minimum</span>, ale tvrzení není doplněno datovým zdrojem, metodikou indexu ani konkrétní hodnotou.</p>
<p>Část věnovaná spotřebě potravin pracuje se zápisem <span class="error-hl hl-low" data-error="error-16">1.8; 2,4; 3.1</span> v jedné větě, tedy s promíchanými desetinnými oddělovači. Tento formát je v českém odborném textu nekonzistentní a zhoršuje čitelnost datové interpretace.</p>

<div class="demo-chart-card">
  <div class="demo-chart-header">
    <strong>Změna výdajů podle kategorií</strong>
    <span>porovnání 2021 a 2023</span>
  </div>
  <svg class="demo-chart-svg" viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Změna výdajů podle kategorií">
    <rect x="0" y="0" width="640" height="250" rx="18" fill="#fff8f4"/>
    <line x1="90" y1="200" x2="590" y2="200" stroke="#d7c6bb" stroke-width="2"/>
    <rect x="110" y="82" width="48" height="118" rx="10" fill="#d95f3b"/>
    <rect x="190" y="64" width="48" height="136" rx="10" fill="#f1a37f"/>
    <rect x="270" y="136" width="48" height="64" rx="10" fill="#3b8c6e"/>
    <rect x="350" y="152" width="48" height="48" rx="10" fill="#7bb49f"/>
    <rect x="430" y="120" width="48" height="80" rx="10" fill="#d97706"/>
    <rect x="510" y="166" width="48" height="34" rx="10" fill="#f2bb63"/>
    <g fill="#6b4f3f" font-family="Inter, sans-serif" font-size="12">
      <text x="96" y="220">Potraviny</text>
      <text x="180" y="220">Bydlení</text>
      <text x="272" y="220">Doprava</text>
      <text x="348" y="220">Kultura</text>
      <text x="431" y="220">Zdraví</text>
      <text x="500" y="220">Vzdělání</text>
    </g>
  </svg>
  <p class="demo-chart-caption">Graf 2: Meziroční změna výdajů domácností podle kategorií</p>
  <p class="demo-chart-note"><span class="error-hl hl-medium" data-error="error-18">Osa grafu a legenda neuvádějí jednotku ani informaci, zda se jedná o procenta nebo procentní body.</span></p>
</div>

<p>Na výsledky navazuje tabulkový přehled mediánových a průměrných výdajů, jenže odkaz v textu uvádí <span class="error-hl hl-low" data-error="error-15">Tabulka 4</span>, přestože jde o první a jedinou tabulku této kapitoly. Nekonzistentní číslování komplikuje orientaci čtenáře.</p>
<p>V interpretaci nákladů na bydlení se objevuje hodnota <span class="error-hl hl-low" data-error="error-17">12 500, 9250 a 8.750 Kč</span>, tedy kombinace různých oddělovačů tisíců a desetinných míst. U jednoho datového přehledu by měl být použit jednotný zápis.</p>
<p>Text současně uvádí, že domácnosti s nižšími příjmy reagovaly na zdražování rychleji, protože sledovaly <span class="error-hl hl-low" data-error="error-22">consumer confidence</span> a častěji odkládaly nákupy zbytného zboží. Nečeský termín zde není vysvětlen ani přeložen.</p>
<p>V navazujícím souvětí se objevuje formulace <span class="error-hl hl-medium" data-error="error-21">výdaje domácností se v analyzovaném období snížily a spotřební koš se zároveň proměnily</span>, kde není zachována správná shoda přísudku s podmětem.</p>
<p>Ve zhodnocení výsledků se dále píše, že <span class="error-hl hl-low" data-error="error-23">pokles spotřeby byl byl nejsilnější</span> ve skupině samoživitelek. Jde o zjevné zdvojení slova, které by mělo být zachyceno korekturou.</p>
<p>Jedna z interpretačních vět zní, že <span class="error-hl hl-medium" data-error="error-24">inflace tlačí domácnosti do rozhodnutí, která jsou svou podstatou více obranná než růstově-konzumní</span>. Formulace je stylisticky neobratná a bez dalšího vysvětlení působí nejasně.</p>

<h2>5. Doplňkové modely a regionální srovnání</h2>
<p>Regresní model má prokázat vztah mezi růstem cen a změnou struktury spotřeby, ale věta <span class="error-hl hl-medium" data-error="error-28">do modelu byly zahrnuty socioekonomické proměnné a regionální efekty</span> nepřináší informaci o tom, které proměnné byly skutečně použity a v jaké specifikaci.</p>
<p>Regionální srovnání dále konstatuje, že domácnosti v Praze a Brně měly vyšší nominální výdaje, zatímco domácnosti v Moravskoslezském kraji zaznamenaly prudší pokles reálné spotřeby. Bez vysvětlení ale zůstává, proč je v jedné tabulce porovnán <span class="error-hl hl-high" data-error="error-27">nominální růst výdajů na bydlení s reálně očištěným vývojem mezd</span>.</p>

<div class="demo-chart-card">
  <div class="demo-chart-header">
    <strong>Rozdělení rozpočtu domácností</strong>
    <span>nízkopříjmové vs. středněpříjmové skupiny</span>
  </div>
  <svg class="demo-chart-svg" viewBox="0 0 640 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Rozdělení rozpočtu domácností">
    <rect x="0" y="0" width="640" height="240" rx="18" fill="#fff8f4"/>
    <circle cx="190" cy="120" r="72" fill="#f5d2c5"/>
    <path d="M190 120 L190 48 A72 72 0 0 1 256 153 Z" fill="#d95f3b"/>
    <path d="M190 120 L256 153 A72 72 0 0 1 154 184 Z" fill="#3b8c6e"/>
    <path d="M190 120 L154 184 A72 72 0 1 1 190 48 Z" fill="#d97706"/>
    <circle cx="450" cy="120" r="72" fill="#f5d2c5"/>
    <path d="M450 120 L450 48 A72 72 0 0 1 518 132 Z" fill="#d95f3b"/>
    <path d="M450 120 L518 132 A72 72 0 0 1 430 189 Z" fill="#3b8c6e"/>
    <path d="M450 120 L430 189 A72 72 0 1 1 450 48 Z" fill="#d97706"/>
    <g fill="#6b4f3f" font-family="Inter, sans-serif" font-size="13">
      <text x="140" y="28">Nízkopříjmové domácnosti</text>
      <text x="404" y="28">Středněpříjmové domácnosti</text>
    </g>
  </svg>
  <p class="demo-chart-caption">Graf 3: Struktura výdajů podle příjmové skupiny</p>
</div>

<p>Ve vysvětlující poznámce je uvedeno, že nízkopříjmové domácnosti utratily za bydlení mediánově 12 400 Kč, přičemž v závěrečném shrnutí autorka vyvozuje, že <span class="error-hl hl-medium" data-error="error-30">průměrná domácnost ze zkoumaného souboru vydávala na bydlení stejně jako mediánová domácnost</span>. Záměna průměru a mediánu zde vede ke zkreslení interpretace.</p>

<h2>6. Diskuse a implikace</h2>
<p>Diskusní část vhodně shrnuje, že inflace se neprojevovala rovnoměrně, ale nejvíce zasahovala výdaje na bydlení a potraviny. Přesto zde chybí explicitní pasáž, která by systematicky popsala omezení výzkumu. Problém je patrný v místě, kde text přechází rovnou k interpretaci a <span class="error-hl hl-critical" data-error="error-3">neobsahuje samostatné vymezení limitů použitého vzorku, délky časové řady ani rizika samovýběru respondentů</span>.</p>
<p>V navazující části autorka konstatuje, že výsledky mohou být důležité pro banky, obchodní řetězce i veřejnou správu. Kapitola ale končí obecnou formulací a <span class="error-hl hl-critical" data-error="error-6">nepřináší konkrétní doporučení pro firmy, obce ani sociální politiku</span>, přestože název práce slibuje dopady na spotřebitelské chování v praxi.</p>
<p>Závěrečný odstavec znovu odkazuje na inflační vývoj po roce 2021 a přitom shrnuje, že růst cen byl „bezprecedentní od počátku transformace“. Tuto formulaci by bylo vhodné opřít o novější datovou základnu i přesnější metodiku srovnání.</p>
""".strip()


def _demo_economics_errors() -> list[dict[str, Any]]:
    return [
        {
            "id": "error-1",
            "type": "Výzkumná otázka",
            "category": "Chybějící části",
            "severity": "critical",
            "location": "Úvod, odstavec 1",
            "impact": "Bez jasné výzkumné otázky není možné přesně posoudit naplnění cíle práce.",
            "description": "Úvod formuluje cíl pouze obecně. Chybí explicitní výzkumná otázka, ke které by se mohla vracet analytická i závěrečná část.",
            "suggested_fix": "Doplňte samostatnou větu typu: „Jak ovlivnila inflace v letech 2021–2023 strukturu výdajů českých domácností podle příjmových skupin?“",
        },
        {
            "id": "error-2",
            "type": "Hypotézy",
            "category": "Chybějící části",
            "severity": "critical",
            "location": "Kapitola 2, odstavec 1",
            "impact": "Analytická část pracuje s předpoklady, které ale nejsou nikde formálně vymezeny.",
            "description": "Práce neobsahuje samostatně formulované hypotézy, přesto později interpretuje výsledky tak, jako by byly předem definovány.",
            "suggested_fix": "Vložte podkapitolu s 2–3 hypotézami, například o růstu podílu výdajů na bydlení a poklesu diskreční spotřeby.",
        },
        {
            "id": "error-3",
            "type": "Limity výzkumu",
            "category": "Chybějící části",
            "severity": "critical",
            "location": "Diskuse, odstavec 1",
            "impact": "Bez limitů výzkumu působí závěry silněji, než kolik skutečně dovolují data.",
            "description": "Diskuse nepopsala omezení vzorku, časové řady ani riziko samovýběru respondentů.",
            "suggested_fix": "Doplňte odstavec o limitech výzkumu a vysvětlete, jak mohou ovlivnit zobecnitelnost výsledků.",
        },
        {
            "id": "error-4",
            "type": "Výběr vzorku",
            "category": "Chybějící části",
            "severity": "high",
            "location": "Metodika, odstavec 5",
            "impact": "Není zřejmé, zda byl výzkumný soubor reprezentativní nebo pouze příležitostný.",
            "description": "Popis výběru respondentů neobsahuje kritéria zařazení, stratifikaci ani způsob kontroly reprezentativnosti.",
            "suggested_fix": "Uveďte, podle jakých kritérií byli respondenti zařazeni a zda byl soubor kvótně nebo jinak strukturován.",
        },
        {
            "id": "error-5",
            "type": "Úprava časových řad",
            "category": "Chybějící části",
            "severity": "high",
            "location": "Metodika, odstavec 6",
            "impact": "Bez sezonného očištění mohou být některé změny spotřeby interpretovány chybně.",
            "description": "Metodika neřeší sezonní očištění měsíčních dat, přesto je používá pro meziroční srovnání.",
            "suggested_fix": "Doplňte informaci, zda byla data sezonně očištěna, případně proč k očištění nedošlo.",
        },
        {
            "id": "error-6",
            "type": "Doporučení pro praxi",
            "category": "Chybějící části",
            "severity": "critical",
            "location": "Diskuse, odstavec 2",
            "impact": "Práce slibuje praktické implikace, ale čtenář nedostane konkrétní doporučení.",
            "description": "Text neobsahuje závěrečná doporučení pro firmy, obce nebo tvůrce veřejných politik.",
            "suggested_fix": "Doplňte 3–4 stručná doporučení pro retail, obce a sociální politiku vycházející z datových zjištění.",
        },
        {
            "id": "error-7",
            "type": "Neozdrojované tvrzení",
            "category": "Citace a zdroje",
            "severity": "high",
            "location": "Úvod, odstavec 2",
            "impact": "Silné tvrzení bez zdroje snižuje důvěryhodnost celé argumentace.",
            "description": "Tvrzení o mimořádném dopadu české inflace na celé spotřební chování není doplněno konkrétním statistickým zdrojem.",
            "suggested_fix": "Doplňte odkaz na zprávu ČNB, Eurostatu nebo ČSÚ a uveďte přesnou hodnotu inflace i srovnávané období.",
        },
        {
            "id": "error-8",
            "type": "Neúplná citace",
            "category": "Citace a zdroje",
            "severity": "high",
            "location": "Teoretická část, odstavec 2",
            "impact": "Čtenář nemůže dohledat citovaný dokument Evropské centrální banky.",
            "description": "Citace „ECB (2024)“ neobsahuje název dokumentu, vydavatele, stránku ani URL.",
            "suggested_fix": "Uveďte plnou bibliografickou citaci zdroje včetně názvu reportu a data citace, pokud jde o online dokument.",
        },
        {
            "id": "error-9",
            "type": "Sekundární citace",
            "category": "Citace a zdroje",
            "severity": "medium",
            "location": "Teoretická část, odstavec 4",
            "impact": "Sekundární citace oslabuje přesnost interpretace zahraničního zdroje.",
            "description": "Pasáž odkazuje na OECD prostřednictvím sekundárního autora, aniž by bylo označeno, že jde o zprostředkovanou citaci.",
            "suggested_fix": "Citujte přímo dokument OECD nebo zřetelně označte sekundární citaci podle zvolené citační normy.",
        },
        {
            "id": "error-10",
            "type": "Encyklopedický zdroj",
            "category": "Citace a zdroje",
            "severity": "high",
            "location": "Teoretická část, odstavec 5",
            "impact": "Použití Wikipedie v teoretické kapitole působí neakademicky.",
            "description": "Definice inflace je převzata z otevřené encyklopedie místo z odborné literatury nebo institucionálního zdroje.",
            "suggested_fix": "Nahraďte encyklopedický zdroj učebnicí makroekonomie, zprávou ČNB nebo odborným článkem.",
        },
        {
            "id": "error-11",
            "type": "Nepodložený ukazatel",
            "category": "Citace a zdroje",
            "severity": "medium",
            "location": "Analýza výsledků, odstavec 2",
            "impact": "Index důvěry je použit jako argument bez vysvětlení metodiky a zdroje.",
            "description": "Text pracuje s tvrzením o historickém minimu spotřebitelské důvěry bez uvedení datové řady nebo zdroje ukazatele.",
            "suggested_fix": "Doplňte zdroj ukazatele, jeho hodnotu a stručně vysvětlete, co přesně index měří.",
        },
        {
            "id": "error-12",
            "type": "Zastaralý zdroj",
            "category": "Citace a zdroje",
            "severity": "medium",
            "location": "Teoretická část, odstavec 6",
            "impact": "Starší literatura sama o sobě nestačí pro výklad postpandemické inflační epizody.",
            "description": "Práce se opírá o zdroj z roku 2012 bez doplnění novější literatury reflektující období po roce 2021.",
            "suggested_fix": "Rozšiřte rešerši o minimálně 2–3 aktuální zdroje z let 2022–2024.",
        },
        {
            "id": "error-13",
            "type": "Zápis procent",
            "category": "Typografie",
            "severity": "low",
            "location": "KPI blok, karta 1",
            "impact": "Nekorektní typografie zhoršuje profesionální dojem dokumentu.",
            "description": "V českém textu chybí mezera mezi číslem a symbolem procenta.",
            "suggested_fix": "Použijte zápis „17,2 %“ a sjednoťte typografii všech procentních údajů v práci.",
        },
        {
            "id": "error-14",
            "type": "Popisek grafu",
            "category": "Typografie",
            "severity": "medium",
            "location": "Graf 1, popisek",
            "impact": "Graf bez úplného popisku a zdroje nelze správně citovat ani interpretovat.",
            "description": "Popisek grafu neobsahuje informaci o zdroji ani standardní formát označení obrázku.",
            "suggested_fix": "Převeďte popisek na formát „Graf 1: Vývoj inflace a maloobchodních tržeb (Zdroj: ČSÚ, vlastní zpracování)“.",
        },
        {
            "id": "error-15",
            "type": "Číslování tabulek",
            "category": "Typografie",
            "severity": "low",
            "location": "Analýza výsledků, odstavec 5",
            "impact": "Nekonzistentní číslování komplikuje orientaci v textu.",
            "description": "Text odkazuje na Tabulku 4, přestože jde o první tabulku kapitoly.",
            "suggested_fix": "Zkontrolujte automatické číslování tabulek a odkazy na ně v celé práci.",
        },
        {
            "id": "error-16",
            "type": "Desetinné oddělovače",
            "category": "Typografie",
            "severity": "low",
            "location": "Analýza výsledků, odstavec 3",
            "impact": "Smíšený zápis čísel snižuje čitelnost analytické části.",
            "description": "V jedné větě jsou kombinovány české i anglické desetinné oddělovače.",
            "suggested_fix": "Použijte konzistentně český zápis s desetinnou čárkou.",
        },
        {
            "id": "error-17",
            "type": "Oddělovače tisíců",
            "category": "Typografie",
            "severity": "low",
            "location": "Analýza výsledků, odstavec 6",
            "impact": "Nejednotný zápis částek působí neprofesionálně.",
            "description": "Částky používají různé oddělovače tisíců a desetinných míst.",
            "suggested_fix": "Sjednoťte peněžní údaje na formát např. „12 500 Kč“ v celé práci.",
        },
        {
            "id": "error-18",
            "type": "Osy a jednotky",
            "category": "Typografie",
            "severity": "medium",
            "location": "Graf 2, poznámka pod grafem",
            "impact": "Bez jednotek nelze správně interpretovat velikost změny.",
            "description": "Graf neuvádí, zda hodnoty představují procenta, procentní body nebo absolutní změnu.",
            "suggested_fix": "Doplňte jednotky na osu nebo do legendy a explicitně popište datový formát v popisku grafu.",
        },
        {
            "id": "error-19",
            "type": "Hovorový styl",
            "category": "Jazyk a pravopis",
            "severity": "low",
            "location": "Úvod, odstavec 3",
            "impact": "Hovorový jazyk snižuje odborný tón textu.",
            "description": "Formulace „domácnosti prostě začaly šetřit skoro na všem“ je stylově neakademická.",
            "suggested_fix": "Nahraďte ji přesnější větou popisující změnu spotřebních preferencí a opřete ji o zdroj nebo data.",
        },
        {
            "id": "error-20",
            "type": "Překlep",
            "category": "Jazyk a pravopis",
            "severity": "low",
            "location": "Teoretická část, odstavec 3",
            "impact": "I drobný překlep v odborné práci kazí celkový dojem.",
            "description": "V textu je slovo „domacnosti“ bez diakritiky.",
            "suggested_fix": "Opravte na „domácnosti“ a před finálním odevzdáním proveďte korekturu celého dokumentu.",
        },
        {
            "id": "error-21",
            "type": "Shoda přísudku",
            "category": "Jazyk a pravopis",
            "severity": "medium",
            "location": "Analytická část, pozdější odstavec",
            "impact": "Gramatická chyba snižuje jazykovou kvalitu textu.",
            "description": "Ve větě o změně spotřebního koše není správně zachována shoda přísudku s podmětem.",
            "suggested_fix": "Zkontrolujte větnou shodu a upravte problematickou část na jazykově správný tvar.",
        },
        {
            "id": "error-22",
            "type": "Anglicismus",
            "category": "Jazyk a pravopis",
            "severity": "low",
            "location": "Analýza výsledků, odstavec 7",
            "impact": "Nevysvětlený anglický termín ztěžuje srozumitelnost textu.",
            "description": "V českém textu je použit termín „consumer confidence“ bez překladu nebo vysvětlení.",
            "suggested_fix": "Použijte český ekvivalent „spotřebitelská důvěra“ a anglický termín případně připojte do závorky.",
        },
        {
            "id": "error-23",
            "type": "Zdvojené slovo",
            "category": "Jazyk a pravopis",
            "severity": "low",
            "location": "Analýza výsledků, odstavec 8",
            "impact": "Zdvojené slovo působí jako nedokončená korektura.",
            "description": "Ve větě se opakuje slovo „byl“, což vytváří zjevnou jazykovou chybu.",
            "suggested_fix": "Odstraňte zdvojené slovo a projděte text ještě jednou korekturou.",
        },
        {
            "id": "error-24",
            "type": "Neobratná formulace",
            "category": "Jazyk a pravopis",
            "severity": "medium",
            "location": "Analýza výsledků, odstavec 9",
            "impact": "Nepřesná formulace zhoršuje srozumitelnost závěru.",
            "description": "Věta o „obranných rozhodnutích“ je stylisticky neobratná a významově nejasná.",
            "suggested_fix": "Přeformulujte větu jednodušeji a konkrétněji, ideálně s vazbou na data nebo teorii.",
        },
        {
            "id": "error-25",
            "type": "Rozsah dat",
            "category": "Data a metodika",
            "severity": "high",
            "location": "Metodika, odstavec 1",
            "impact": "Nesoulad v časovém vymezení zpochybňuje konzistenci celé datové základny.",
            "description": "Práce jednou uvádí data za období 2020–2023, jinde ale pracuje jen s roky 2021–2023.",
            "suggested_fix": "Sjednoťte časový rozsah dat v úvodu, metodice i výsledcích a vysvětlete případné rozdíly.",
        },
        {
            "id": "error-26",
            "type": "Velikost vzorku",
            "category": "Data a metodika",
            "severity": "high",
            "location": "Metodika, odstavec 2",
            "impact": "Bez vysvětlení rozdílu ve velikosti vzorku není analýza transparentní.",
            "description": "V textu se objevují dvě různé hodnoty počtu respondentů bez vysvětlení důvodu vyřazení části souboru.",
            "suggested_fix": "Přidejte informaci o čištění dat a přesně popište, kolik respondentů a proč bylo vyloučeno.",
        },
        {
            "id": "error-27",
            "type": "Nominální a reálné veličiny",
            "category": "Data a metodika",
            "severity": "high",
            "location": "Metodika a regionální srovnání",
            "impact": "Smíchání nominálních a reálných hodnot může vést k chybným závěrům.",
            "description": "Práce porovnává nominální výdaje s reálně očištěnými příjmy bez metodického zdůvodnění.",
            "suggested_fix": "Používejte konzistentně nominální nebo reálné veličiny a jasně popište použitý deflátor.",
        },
        {
            "id": "error-28",
            "type": "Specifikace modelu",
            "category": "Data a metodika",
            "severity": "medium",
            "location": "Kapitola 5, odstavec 1",
            "impact": "Bez specifikace modelu nelze regresní výsledky ověřit ani reprodukovat.",
            "description": "Pasáž o regresním modelu neuvádí jeho rovnici, proměnné ani způsob odhadu.",
            "suggested_fix": "Doplňte formální specifikaci modelu, definice proměnných a základní odhadovací postup.",
        },
        {
            "id": "error-29",
            "type": "Srovnání ukazatelů",
            "category": "Data a metodika",
            "severity": "medium",
            "location": "Analýza výsledků, odstavec 1",
            "impact": "Porovnání nesouměřitelných ukazatelů zkresluje interpretaci trendu.",
            "description": "Text míchá meziroční inflaci s průměrem za celé období bez vysvětlení metodiky srovnání.",
            "suggested_fix": "Srovnávejte stejné typy ukazatelů nebo vysvětlete, proč jsou použity různé konstrukce.",
        },
        {
            "id": "error-30",
            "type": "Průměr vs. medián",
            "category": "Data a metodika",
            "severity": "medium",
            "location": "Kapitola 5, závěrečný odstavec",
            "impact": "Záměna průměru a mediánu zkresluje závěrečné shrnutí práce.",
            "description": "Závěrečná interpretace zaměňuje průměrnou domácnost s mediánovou domácností.",
            "suggested_fix": "Opravte interpretaci a vždy explicitně rozlišujte, zda komentujete průměr nebo medián.",
        },
    ]


INITIAL_STATE: dict[str, Any] = {
    "users": {
        "user-jan": {
            "id": "user-jan",
            "first_name": "Jan",
            "last_name": "Novák",
            "email": "jan.novak@tul.cz",
            "password": "demo12345",
            "role": "student",
            "tier": "institutional_free",
            "email_verified": True,
            "onboarding_done": True,
            "university_name": "Technická univerzita v Liberci",
            "faculty_id": "fm",
            "faculty_label": "FM TUL",
            "faculty_name": "Fakulta mechatroniky, informatiky a mezioborových studií",
            "monthly_scan_budget": 5,
            "monthly_scan_count": 3,
            "joined_at": "03/2026",
            "notifications": {
                "analysis_complete": True,
                "project_reminder": True,
                "product_news": False,
            },
        },
        "user-admin": {
            "id": "user-admin",
            "first_name": "Petra",
            "last_name": "Svobodová",
            "email": "petra.svobodova@klonku.cz",
            "password": "admin12345",
            "role": "superadmin",
            "tier": "pro",
            "email_verified": True,
            "onboarding_done": True,
            "university_name": "Klonku",
            "faculty_id": "fm",
            "faculty_label": "FM TUL",
            "faculty_name": "Fakulta mechatroniky",
            "monthly_scan_budget": 50,
            "monthly_scan_count": 8,
            "joined_at": "02/2026",
            "notifications": {
                "analysis_complete": True,
                "project_reminder": True,
                "product_news": True,
            },
        },
        "user-tereza": {
            "id": "user-tereza",
            "first_name": "Tereza",
            "last_name": "Králová",
            "email": "tereza.kralova@tul.cz",
            "password": "demo12345",
            "role": "student",
            "tier": "institutional_free",
            "email_verified": True,
            "onboarding_done": True,
            "university_name": "Technická univerzita v Liberci",
            "faculty_id": "fe",
            "faculty_label": "FE TUL",
            "faculty_name": "Ekonomická fakulta",
            "monthly_scan_budget": 5,
            "monthly_scan_count": 1,
            "joined_at": "04/2026",
            "notifications": {
                "analysis_complete": True,
                "project_reminder": False,
                "product_news": False,
            },
        },
        "user-eva": {
            "id": "user-eva",
            "first_name": "Eva",
            "last_name": "Malá",
            "email": "eva.mala@tul.cz",
            "password": "demo12345",
            "role": "student",
            "tier": "basic",
            "email_verified": True,
            "onboarding_done": True,
            "university_name": "Technická univerzita v Liberci",
            "faculty_id": "fp",
            "faculty_label": "FP TUL",
            "faculty_name": "Fakulta přírodovědně-humanitní a pedagogická",
            "monthly_scan_budget": 10,
            "monthly_scan_count": 6,
            "joined_at": "03/2026",
            "notifications": {
                "analysis_complete": True,
                "project_reminder": True,
                "product_news": True,
            },
        },
    },
    "faculties": {
        "fm": {
            "id": "fm",
            "code": "FM TUL",
            "name": "Fakulta mechatroniky",
            "short_name": "FM",
            "university_name": "Technická univerzita v Liberci",
        },
        "fe": {
            "id": "fe",
            "code": "FE TUL",
            "name": "Ekonomická fakulta",
            "short_name": "FE",
            "university_name": "Technická univerzita v Liberci",
        },
        "fp": {
            "id": "fp",
            "code": "FP TUL",
            "name": "Fakulta přírodovědně-humanitní a pedagogická",
            "short_name": "FP",
            "university_name": "Technická univerzita v Liberci",
        },
    },
    "pipeline_steps": {
        "step-fm-missing": {
            "id": "step-fm-missing",
            "faculty_id": "fm",
            "name": "Chybějící části",
            "description": "Obsah, abstrakt, závěr a povinné deklarace.",
            "prompt_version": 4,
            "active": True,
            "order": 1,
        },
        "step-fm-citations": {
            "id": "step-fm-citations",
            "faculty_id": "fm",
            "name": "Citace a zdroje",
            "description": "Kontrola citační normy a bibliografických údajů.",
            "prompt_version": 6,
            "active": True,
            "order": 2,
        },
        "step-fm-typography": {
            "id": "step-fm-typography",
            "faculty_id": "fm",
            "name": "Typografie",
            "description": "Mezery, nadpisy, tabulky, obrázky a sazba.",
            "prompt_version": 3,
            "active": True,
            "order": 3,
        },
        "step-fm-language": {
            "id": "step-fm-language",
            "faculty_id": "fm",
            "name": "Jazyk a pravopis",
            "description": "Styl, terminologie a gramatické chyby.",
            "prompt_version": 5,
            "active": True,
            "order": 4,
        },
        "step-fm-structure": {
            "id": "step-fm-structure",
            "faculty_id": "fm",
            "name": "Struktura a koherence",
            "description": "Návaznost kapitol a vnitřní konzistence textu.",
            "prompt_version": 2,
            "active": True,
            "order": 5,
        },
        "step-fe-citations": {
            "id": "step-fe-citations",
            "faculty_id": "fe",
            "name": "Citace a zdroje",
            "description": "Ekonomické citace a reference.",
            "prompt_version": 3,
            "active": True,
            "order": 1,
        },
        "step-fe-structure": {
            "id": "step-fe-structure",
            "faculty_id": "fe",
            "name": "Struktura práce",
            "description": "Logika a návaznost argumentace.",
            "prompt_version": 2,
            "active": True,
            "order": 2,
        },
        "step-fe-tables": {
            "id": "step-fe-tables",
            "faculty_id": "fe",
            "name": "Grafy a tabulky",
            "description": "Popisky, legendy a reference na obrázky.",
            "prompt_version": 1,
            "active": True,
            "order": 3,
        },
        "step-fp-language": {
            "id": "step-fp-language",
            "faculty_id": "fp",
            "name": "Jazyk a stylistika",
            "description": "Jazyková kvalita a citační disciplína.",
            "prompt_version": 2,
            "active": True,
            "order": 1,
        },
        "step-fp-appendix": {
            "id": "step-fp-appendix",
            "faculty_id": "fp",
            "name": "Přílohy a metodika",
            "description": "Povinné přílohy a metodický aparát.",
            "prompt_version": 1,
            "active": True,
            "order": 2,
        },
    },
    "error_types": {
        "citation": {
            "id": "citation",
            "slug": "citation",
            "label": "Citace",
            "description": "Chyby v citacích a zdrojích.",
            "system": True,
        },
        "style": {
            "id": "style",
            "slug": "style",
            "label": "Styl",
            "description": "Styl a formulace textu.",
            "system": True,
        },
        "missing-section": {
            "id": "missing-section",
            "slug": "missing-section",
            "label": "Chybějící část",
            "description": "Povinné kapitoly nebo části práce.",
            "system": True,
        },
        "typography": {
            "id": "typography",
            "slug": "typography",
            "label": "Typografie",
            "description": "Sazba, mezery a vizuální konzistence.",
            "system": True,
        },
    },
    "allowed_domains": {
        "domain-tul": {
            "id": "domain-tul",
            "domain": "tul.cz",
            "university_name": "Technická univerzita v Liberci",
            "free_analyses_per_month": 5,
            "active": True,
        },
        "domain-cvut": {
            "id": "domain-cvut",
            "domain": "cvut.cz",
            "university_name": "ČVUT",
            "free_analyses_per_month": 3,
            "active": True,
        },
        "domain-muni": {
            "id": "domain-muni",
            "domain": "muni.cz",
            "university_name": "Masarykova univerzita",
            "free_analyses_per_month": 3,
            "active": True,
        },
    },
    "projects": {
        "proj-sentiment": {
            "id": "proj-sentiment",
            "user_id": "user-jan",
            "title": "Vliv inflace na spotřebitelské chování domácností v ČR",
            "faculty_id": "fm",
            "file_format": "DOCX",
            "thesis_type": "Bakalářská práce",
            "created_at": "28. 3. 2026",
            "pipeline_step_ids": [
                "step-fm-missing",
                "step-fm-citations",
                "step-fm-typography",
                "step-fm-language",
            ],
            "version_ids": [
                "ver-sentiment-1",
                "ver-sentiment-2",
                "ver-sentiment-3",
            ],
        },
        "proj-logistics": {
            "id": "proj-logistics",
            "user_id": "user-jan",
            "title": "Optimalizace logistických řetězců",
            "faculty_id": "fe",
            "file_format": "LaTeX",
            "thesis_type": "Diplomová práce",
            "created_at": "2. 4. 2026",
            "pipeline_step_ids": ["step-fe-citations", "step-fe-structure", "step-fe-tables"],
            "version_ids": ["ver-logistics-1"],
        },
        "proj-generation-z": {
            "id": "proj-generation-z",
            "user_id": "user-jan",
            "title": "Vliv sociálních médií na nákupní chování generace Z",
            "faculty_id": "fp",
            "file_format": "DOCX",
            "thesis_type": "Bakalářská práce",
            "created_at": "1. 4. 2026",
            "pipeline_step_ids": ["step-fp-language", "step-fp-appendix"],
            "version_ids": [],
        },
        "proj-small-business": {
            "id": "proj-small-business",
            "user_id": "user-jan",
            "title": "Návrh informačního systému pro malý podnik",
            "faculty_id": "fm",
            "file_format": "DOCX",
            "thesis_type": "Bakalářská práce",
            "created_at": "18. 3. 2026",
            "pipeline_step_ids": [
                "step-fm-missing",
                "step-fm-citations",
                "step-fm-typography",
            ],
            "version_ids": [
                "ver-business-1",
                "ver-business-2",
                "ver-business-3",
                "ver-business-4",
                "ver-business-5",
            ],
        },
        "proj-legislation": {
            "id": "proj-legislation",
            "user_id": "user-jan",
            "title": "Srovnání účetní legislativy ČR a Německa",
            "faculty_id": "fe",
            "file_format": "DOCX",
            "thesis_type": "Diplomová práce",
            "created_at": "23. 3. 2026",
            "pipeline_step_ids": ["step-fe-citations", "step-fe-structure"],
            "version_ids": ["ver-legislation-1"],
        },
    },
    "versions": {
        "ver-sentiment-1": {
            "id": "ver-sentiment-1",
            "project_id": "proj-sentiment",
            "version_number": 1,
            "status": "completed",
            "error_count": 20,
            "unresolved_from_previous": 0,
            "created_at": "28. 3. 2026, 16:40",
            "analysis_steps": [
                "Chybějící části",
                "Typografie a formát",
                "Citace a zdroje",
                "Jazyk a pravopis",
            ],
            "poll_count": 0,
        },
        "ver-sentiment-2": {
            "id": "ver-sentiment-2",
            "project_id": "proj-sentiment",
            "version_number": 2,
            "status": "completed",
            "error_count": 12,
            "unresolved_from_previous": 4,
            "created_at": "31. 3. 2026, 09:15",
            "analysis_steps": [
                "Chybějící části",
                "Typografie a formát",
                "Citace a zdroje",
                "Jazyk a pravopis",
            ],
            "poll_count": 0,
        },
        "ver-sentiment-3": {
            "id": "ver-sentiment-3",
            "project_id": "proj-sentiment",
            "version_number": 3,
            "status": "completed",
            "error_count": 30,
            "unresolved_from_previous": 3,
            "created_at": "2. 4. 2026, 14:22",
            "analysis_steps": [
                "Chybějící části",
                "Citace a zdroje",
                "Typografie a formát",
                "Jazyk a pravopis",
                "Data a metodika",
            ],
            "poll_count": 0,
        },
        "ver-logistics-1": {
            "id": "ver-logistics-1",
            "project_id": "proj-logistics",
            "version_number": 1,
            "status": "processing",
            "error_count": None,
            "unresolved_from_previous": 0,
            "created_at": "2. 4. 2026, 11:05",
            "analysis_steps": [
                "Chybějící části",
                "Typografie a formát",
                "Citace a zdroje",
                "Jazyk a pravopis",
                "Struktura a koherence",
            ],
            "poll_count": 2,
        },
        "ver-business-1": {
            "id": "ver-business-1",
            "project_id": "proj-small-business",
            "version_number": 1,
            "status": "completed",
            "error_count": 42,
            "unresolved_from_previous": 0,
            "created_at": "19. 3. 2026, 09:10",
            "analysis_steps": [],
            "poll_count": 0,
        },
        "ver-business-2": {
            "id": "ver-business-2",
            "project_id": "proj-small-business",
            "version_number": 2,
            "status": "completed",
            "error_count": 33,
            "unresolved_from_previous": 21,
            "created_at": "21. 3. 2026, 13:20",
            "analysis_steps": [],
            "poll_count": 0,
        },
        "ver-business-3": {
            "id": "ver-business-3",
            "project_id": "proj-small-business",
            "version_number": 3,
            "status": "completed",
            "error_count": 29,
            "unresolved_from_previous": 18,
            "created_at": "24. 3. 2026, 12:05",
            "analysis_steps": [],
            "poll_count": 0,
        },
        "ver-business-4": {
            "id": "ver-business-4",
            "project_id": "proj-small-business",
            "version_number": 4,
            "status": "completed",
            "error_count": 24,
            "unresolved_from_previous": 12,
            "created_at": "26. 3. 2026, 15:10",
            "analysis_steps": [],
            "poll_count": 0,
        },
        "ver-business-5": {
            "id": "ver-business-5",
            "project_id": "proj-small-business",
            "version_number": 5,
            "status": "completed",
            "error_count": 24,
            "unresolved_from_previous": 8,
            "created_at": "28. 3. 2026, 10:44",
            "analysis_steps": [],
            "poll_count": 0,
        },
        "ver-legislation-1": {
            "id": "ver-legislation-1",
            "project_id": "proj-legislation",
            "version_number": 1,
            "status": "failed",
            "error_count": None,
            "unresolved_from_previous": 0,
            "created_at": "30. 3. 2026, 16:20",
            "analysis_steps": ["Citace a zdroje", "Struktura práce"],
            "poll_count": 0,
        },
    },
    "documents": {
        "ver-sentiment-3": _demo_economics_document_html(),
        "ver-sentiment-2": """
<h3>3. Praktická část</h3>
<p><span class="line">Na základě teoretické analýzy jsme zvolili přístup založený na doladění modelu Czech BERT.</span>
<span class="line removed">Dataset byl sestaven z veřejně dostupných příspěvků bez bližší specifikace filtrace.</span>
<span class="line">Model byl následně evaluován na oddělené testovací sadě.</span>
<span class="line updated">Přesnost modelu dosáhla F1-skóre 0.847, což je srovnatelné s publikovanými výsledky.</span></p>
<h3>2.1 Strojové učení v NLP</h3>
<p><span class="line removed">Dominují transformer modely, především BERT a jeho varianty.</span>
<span class="line">Předtrénované jazykové modely umožňují transfer learning pro specifické úlohy.</span></p>
""",
        "ver-logistics-1": """
<h2>Optimalizace logistických řetězců</h2>
<p>Analýza nově nahrané verze probíhá. Po dokončení se zde zobrazí zvýrazněný obsah dokumentu a sidebar s chybami.</p>
""",
    },
    "errors": {
        "ver-sentiment-3": _demo_economics_errors()
    },
    "diffs": {
        "ver-sentiment-3": {
            "summary": {"added": 14, "removed": 3, "fixed": 5, "open": 7},
            "changes": [
                {
                    "kind": "added",
                    "label": "Přidáno",
                    "description": "Byla doplněna metodická část k výběru datasetu a jeho čištění.",
                    "location": "Kapitola 3.1, řádky 88–112",
                },
                {
                    "kind": "updated",
                    "label": "Upraveno",
                    "description": "Citace zdroje [12] byla rozšířena o rok vydání a úplný název publikace.",
                    "location": "Úvod, řádek 26",
                },
                {
                    "kind": "removed",
                    "label": "Odebráno",
                    "description": "Bylo odstraněno nejednoznačné tvrzení o dominanci BERT modelů bez zdroje.",
                    "location": "Kapitola 2.1, řádek 54",
                },
                {
                    "kind": "updated",
                    "label": "Upraveno",
                    "description": "Zpřesněna formulace výsledků experimentu a metriky F1-skóre.",
                    "location": "Kapitola 3.4, řádky 142–150",
                },
            ],
            "before_html": """
<h3>3. Praktická část</h3>
<p><span class="line">Na základě teoretické analýzy jsme zvolili přístup založený na doladění modelu Czech BERT.</span>
<span class="line removed">Dataset byl sestaven z veřejně dostupných příspěvků bez bližší specifikace filtrace.</span>
<span class="line">Model byl následně evaluován na oddělené testovací sadě.</span>
<span class="line updated">Přesnost modelu dosáhla F1-skóre 0.847, což je srovnatelné s publikovanými výsledky.</span></p>
<h3>2.1 Strojové učení v NLP</h3>
<p><span class="line removed">Dominují transformer modely, především BERT a jeho varianty.</span>
<span class="line">Předtrénované jazykové modely umožňují transfer learning pro specifické úlohy.</span></p>
""",
            "after_html": """
<h3>3. Praktická část</h3>
<p><span class="line">Na základě teoretické analýzy jsme zvolili přístup založený na doladění modelu Czech BERT.</span>
<span class="line added">Dataset byl sestaven z 15 000 česky psaných příspěvků a před trénováním prošel deduplikací a základním čištěním.</span>
<span class="line added">Byla odstraněna reklamní sdělení, duplicitní příspěvky a jazykově nejednoznačné vzorky.</span>
<span class="line">Model byl následně evaluován na oddělené testovací sadě.</span>
<span class="line updated">Výsledný model dosáhl na testovací sadě F1-skóre 0,847, což odpovídá hodnotám uváděným ve srovnatelných studiích.</span></p>
<h3>2.1 Strojové učení v NLP</h3>
<p><span class="line added">V posledních letech převažují přístupy založené na transformerech, jejichž efektivita je podložena více recentními studiemi.</span>
<span class="line">Předtrénované jazykové modely umožňují transfer learning pro specifické úlohy.</span></p>
""",
        }
    },
    "admin_activity": [
        {
            "time": "09:42",
            "event": "Dokončena analýza",
            "detail": "Projekt „Analýza sentimentu“ převeden do výsledků.",
            "subject": "jan.novak@tul.cz",
            "status": "ok",
            "status_label": "OK",
        },
        {
            "time": "09:31",
            "event": "Zvýšená latence workeru",
            "detail": "Průměrná doba zpracování překročila interní limit.",
            "subject": "Worker EU-2",
            "status": "warn",
            "status_label": "Varování",
        },
        {
            "time": "09:18",
            "event": "Neúspěšné načtení dokumentu",
            "detail": "Soubor překročil maximální velikost nebo byl poškozen.",
            "subject": "eva.mala@tul.cz",
            "status": "fail",
            "status_label": "Chyba",
        },
        {
            "time": "08:57",
            "event": "Aktualizace fakultních pravidel",
            "detail": "Publikovány nové směrnice pro FM TUL.",
            "subject": "Admin pravidel",
            "status": "ok",
            "status_label": "OK",
        },
        {
            "time": "08:40",
            "event": "Nová registrace",
            "detail": "Uživatel dokončil onboarding a vytvořil první projekt.",
            "subject": "tereza.kralova@tul.cz",
            "status": "ok",
            "status_label": "OK",
        },
    ],
    "admin_queues": [
        {
            "title": "Dokumenty čekající na OCR",
            "count": "7 položek",
            "description": "Fronta se plní hlavně PDF exporty ze starších systémů. Doporučeno navýšit paralelní OCR worker.",
            "chips": ["Průměr 3:12 min", "Priorita vysoká"],
        },
        {
            "title": "Ruční kontrola pravidel",
            "count": "3 položky",
            "description": "Čekají směrnice pro FE a FP. Změny mají dopad na pravidla citací a povinné části práce.",
            "chips": ["Revize obsahu", "Termín dnes"],
        },
    ],
    "flash_messages": [],
}


class MockStore:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.state = deepcopy(INITIAL_STATE)
        self.state["sessions"] = {"access": {}, "refresh": {}}
        self.state["verification_tokens"] = {}
        self.state["password_reset_tokens"] = {}
        self.state["session_counter"] = 0

    def _append_activity(self, event: str, detail: str, subject: str, status: str = "ok") -> None:
        labels = {"ok": "OK", "warn": "Varování", "fail": "Chyba"}
        self.state["admin_activity"].insert(
            0,
            {
                "time": _now().strftime("%H:%M"),
                "event": event,
                "detail": detail,
                "subject": subject,
                "status": status,
                "status_label": labels[status],
            },
        )

    def list_faculties(self) -> list[dict[str, Any]]:
        return list(self.state["faculties"].values())

    def get_faculty(self, faculty_id: str) -> dict[str, Any] | None:
        return self.state["faculties"].get(faculty_id)

    def get_pipeline_steps(self, faculty_id: str) -> list[dict[str, Any]]:
        steps = [
            step
            for step in self.state["pipeline_steps"].values()
            if step["faculty_id"] == faculty_id
        ]
        return sorted(steps, key=lambda item: item["order"])

    def get_user(self, user_id: str | None) -> dict[str, Any] | None:
        if not user_id:
            return None
        return self.state["users"].get(user_id)

    def get_user_by_email(self, email: str) -> dict[str, Any] | None:
        for user in self.state["users"].values():
            if user["email"].lower() == email.lower():
                return user
        return None

    def _issue_token(self, kind: str, user_id: str) -> str:
        self.state["session_counter"] += 1
        token = f"{kind}-{user_id}-{self.state['session_counter']}"
        self.state["sessions"][kind][token] = user_id
        return token

    def issue_tokens(self, user_id: str) -> dict[str, str]:
        return {
            "access_token": self._issue_token("access", user_id),
            "refresh_token": self._issue_token("refresh", user_id),
        }

    def get_user_by_access_token(self, token: str | None) -> dict[str, Any] | None:
        if not token:
            return None
        user_id = self.state["sessions"]["access"].get(token)
        return self.get_user(user_id)

    def refresh_tokens(self, refresh_token: str | None) -> dict[str, str] | None:
        if not refresh_token:
            return None
        user_id = self.state["sessions"]["refresh"].pop(refresh_token, None)
        if not user_id:
            return None
        return self.issue_tokens(user_id)

    def revoke_session(self, refresh_token: str | None) -> None:
        if not refresh_token:
            return
        self.state["sessions"]["refresh"].pop(refresh_token, None)

    def create_email_verification_token(self, user_id: str) -> str:
        token = f"verify-{user_id}"
        self.state["verification_tokens"][token] = user_id
        return token

    def verify_email_token(self, token: str) -> dict[str, Any] | None:
        user_id = self.state["verification_tokens"].pop(token, None)
        if not user_id:
            return None
        self.mark_email_verified(user_id)
        return self.get_user(user_id)

    def create_password_reset_token(self, email: str) -> str | None:
        user = self.get_user_by_email(email)
        if not user:
            return None
        token = f"reset-{user['id']}"
        self.state["password_reset_tokens"][token] = user["id"]
        return token

    def reset_password(self, token: str, password: str) -> dict[str, Any] | None:
        user_id = self.state["password_reset_tokens"].pop(token, None)
        if not user_id:
            return None
        user = self.state["users"][user_id]
        user["password"] = password
        self._append_activity("Reset hesla", "Uživatel změnil heslo přes reset token.", user["email"])
        return user

    def register_user(self, email: str, password: str) -> tuple[dict[str, Any] | None, str | None]:
        if self.get_user_by_email(email):
            return None, "Účet s tímto e-mailem už existuje."

        domain = email.split("@")[-1].lower()
        allowed_domain = next(
            (
                domain_record
                for domain_record in self.state["allowed_domains"].values()
                if domain_record["domain"] == domain and domain_record["active"]
            ),
            None,
        )
        user_id = f"user-{len(self.state['users']) + 1}"
        tier = "institutional_free" if allowed_domain else "unverified"
        budget = allowed_domain["free_analyses_per_month"] if allowed_domain else 0
        faculty = self.state["faculties"]["fm"]
        user = {
            "id": user_id,
            "first_name": "Nový",
            "last_name": "Uživatel",
            "email": email,
            "password": password,
            "role": "student",
            "tier": tier,
            "email_verified": False,
            "onboarding_done": False,
            "university_name": allowed_domain["university_name"] if allowed_domain else "Neověřená doména",
            "faculty_id": faculty["id"],
            "faculty_label": faculty["code"],
            "faculty_name": faculty["name"],
            "monthly_scan_budget": budget,
            "monthly_scan_count": 0,
            "joined_at": "04/2026",
            "notifications": {
                "analysis_complete": True,
                "project_reminder": True,
                "product_news": False,
            },
        }
        self.state["users"][user_id] = user
        self._append_activity("Nová registrace", "Vytvořen nový demo účet.", email)
        return user, None

    def authenticate(self, email: str, password: str) -> tuple[dict[str, Any] | None, str | None]:
        user = self.get_user_by_email(email)
        if not user or user["password"] != password:
            return None, "Neplatný e-mail nebo heslo."
        return user, None

    def mark_email_verified(self, user_id: str) -> None:
        user = self.state["users"][user_id]
        user["email_verified"] = True
        if user["tier"] == "unverified":
            user["tier"] = "institutional_free"
            user["monthly_scan_budget"] = 3
        self._append_activity("E-mail ověřen", "Uživatel potvrdil školní e-mail.", user["email"])

    def update_profile(
        self,
        user_id: str,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        faculty_id: str | None = None,
        onboarding_done: bool | None = None,
        pipeline_preference: dict[str, Any] | None = None,
        notifications: dict[str, bool] | None = None,
    ) -> dict[str, Any]:
        user = self.state["users"][user_id]
        if first_name:
            user["first_name"] = first_name
        if last_name:
            user["last_name"] = last_name
        if faculty_id and faculty_id in self.state["faculties"]:
            faculty = self.state["faculties"][faculty_id]
            user["faculty_id"] = faculty_id
            user["faculty_label"] = faculty["code"]
            user["faculty_name"] = faculty["name"]
            user["university_name"] = faculty["university_name"]
        if onboarding_done is not None:
            user["onboarding_done"] = onboarding_done
        if pipeline_preference:
            user["pipeline_preference"] = pipeline_preference
        if notifications:
            user["notifications"].update(notifications)
        self._append_activity("Úprava profilu", "Uživatel uložil profilové preference.", user["email"])
        return user

    def get_usage(self, user_id: str) -> dict[str, Any]:
        user = self.state["users"][user_id]
        budget = user["monthly_scan_budget"]
        used = user["monthly_scan_count"]
        percent = round((used / budget) * 100) if budget else 0
        return {
            "used": used,
            "budget": budget,
            "remaining": max(0, budget - used),
            "percent": percent,
            "renewal_date": "2026-05-01",
        }

    def complete_onboarding(self, user_id: str, faculty_id: str, pipeline_mode: str, step_ids: list[str]) -> None:
        user = self.state["users"][user_id]
        user["onboarding_done"] = True
        faculty = self.state["faculties"][faculty_id]
        user["faculty_id"] = faculty["id"]
        user["faculty_label"] = faculty["code"]
        user["faculty_name"] = faculty["name"]
        user["pipeline_preference"] = {
            "mode": pipeline_mode,
            "step_ids": step_ids or [step["id"] for step in self.get_pipeline_steps(faculty_id)],
        }
        self._append_activity("Dokončen onboarding", "Uživatel nastavil výchozí pipeline.", user["email"])

    def list_projects_for_user(self, user_id: str) -> list[dict[str, Any]]:
        projects = [
            self.project_card(project)
            for project in self.state["projects"].values()
            if project["user_id"] == user_id
        ]
        return sorted(projects, key=lambda item: item["sort_key"], reverse=True)

    def project_card(self, project: dict[str, Any]) -> dict[str, Any]:
        faculty = self.state["faculties"][project["faculty_id"]]
        versions = [self.state["versions"][version_id] for version_id in project["version_ids"]]
        latest = max(versions, key=lambda item: item["version_number"]) if versions else None
        fixed_count = 0
        if latest and latest["version_number"] > 1:
            fixed_count = max(0, latest["error_count"] or 0)
        status = latest["status"] if latest else "pending"
        return {
            **project,
            "faculty_code": faculty["short_name"],
            "version_count": len(versions),
            "status": status,
            "error_count": latest["error_count"] if latest else None,
            "resolved_count": 5 if project["id"] == "proj-sentiment" else (19 if project["id"] == "proj-small-business" else fixed_count),
            "last_activity": latest["created_at"].split(",")[0] if latest else project["created_at"],
            "sort_key": latest["version_number"] if latest else 0,
            "latest_version_id": latest["id"] if latest else None,
            "latest_version_number": latest["version_number"] if latest else None,
        }

    def get_project(self, project_id: str, user_id: str | None = None) -> dict[str, Any] | None:
        project = self.state["projects"].get(project_id)
        if not project:
            return None
        if user_id and project["user_id"] != user_id:
            return None
        return project

    def update_project(
        self,
        project_id: str,
        *,
        title: str | None = None,
        faculty_id: str | None = None,
        file_format: str | None = None,
        thesis_type: str | None = None,
    ) -> dict[str, Any]:
        project = self.state["projects"][project_id]
        if title:
            project["title"] = title
        if faculty_id and faculty_id in self.state["faculties"]:
            project["faculty_id"] = faculty_id
        if file_format:
            project["file_format"] = file_format
        if thesis_type:
            project["thesis_type"] = thesis_type
        self._append_activity("Úprava projektu", f"Projekt „{project['title']}“ byl upraven.", project["title"])
        return project

    def delete_project(self, project_id: str) -> None:
        project = self.state["projects"].get(project_id)
        if not project:
            return
        for version_id in list(project["version_ids"]):
            self.delete_version(project_id, version_id)
        self.state["projects"].pop(project_id, None)
        self._append_activity("Smazání projektu", f"Projekt „{project['title']}“ byl odstraněn.", project["title"])

    def get_versions_for_project(self, project_id: str) -> list[dict[str, Any]]:
        project = self.state["projects"][project_id]
        versions = []
        for version_id in project["version_ids"]:
            version = dict(self.state["versions"][version_id])
            version["has_diff"] = version["version_number"] > 1
            versions.append(version)
        return sorted(versions, key=lambda item: item["version_number"], reverse=True)

    def create_project(
        self,
        user_id: str,
        title: str,
        faculty_id: str,
        file_format: str,
        thesis_type: str,
        pipeline_step_ids: list[str],
    ) -> dict[str, Any]:
        project_id = f"proj-{len(self.state['projects']) + 1}"
        now = _now()
        project = {
            "id": project_id,
            "user_id": user_id,
            "title": title,
            "faculty_id": faculty_id,
            "file_format": file_format,
            "thesis_type": thesis_type,
            "created_at": f"{now.day}. {now.month}. {now.year}",
            "pipeline_step_ids": pipeline_step_ids or [step["id"] for step in self.get_pipeline_steps(faculty_id)],
            "version_ids": [],
        }
        self.state["projects"][project_id] = project
        user = self.state["users"][user_id]
        self._append_activity("Vytvořen projekt", f"Projekt „{title}“ byl založen ve standalone UI.", user["email"])
        return project

    def update_project_pipeline(self, project_id: str, step_ids: list[str]) -> None:
        project = self.state["projects"][project_id]
        project["pipeline_step_ids"] = step_ids
        self._append_activity("Aktualizace pipeline", f"Projekt „{project['title']}“ změnil kontrolní kroky.", project["title"])

    def get_project_pipeline_config(self, project_id: str) -> dict[str, Any]:
        project = self.state["projects"][project_id]
        return {
            "project_id": project_id,
            "faculty_id": project["faculty_id"],
            "step_ids": project["pipeline_step_ids"],
            "steps": self.get_pipeline_steps(project["faculty_id"]),
        }

    def create_version(self, project_id: str, filename: str) -> dict[str, Any]:
        project = self.state["projects"][project_id]
        next_number = len(project["version_ids"]) + 1
        version_id = f"{project_id}-ver-{next_number}"
        step_names = [step["name"] for step in self.get_pipeline_steps(project["faculty_id"]) if step["id"] in project["pipeline_step_ids"]]
        version = {
            "id": version_id,
            "project_id": project_id,
            "version_number": next_number,
            "status": "processing",
            "error_count": None,
            "unresolved_from_previous": 0,
            "created_at": _now().strftime("%-d. %-m. %Y, %H:%M"),
            "analysis_steps": step_names or ["Kontrola citací", "Jazyk a pravopis", "Typografie"],
            "poll_count": 0,
            "uploaded_filename": filename,
        }
        self.state["versions"][version_id] = version
        self.state["documents"][version_id] = """
<h2>Probíhá analýza nově nahrané verze</h2>
<p>Jakmile simulovaný polling doběhne, tato verze se přesune do výsledků s plným sidebar zobrazením chyb.</p>
"""
        self.state["errors"][version_id] = deepcopy(self.state["errors"]["ver-sentiment-3"])
        self.state["diffs"][version_id] = deepcopy(self.state["diffs"]["ver-sentiment-3"])
        project["version_ids"].append(version_id)
        user = self.state["users"][project["user_id"]]
        user["monthly_scan_count"] = min(user["monthly_scan_budget"], user["monthly_scan_count"] + 1)
        self._append_activity("Nahrána nová verze", f"Projekt „{project['title']}“: {filename}.", user["email"])
        return version

    def get_version(self, project_id: str, version_id: str) -> dict[str, Any] | None:
        version = self.state["versions"].get(version_id)
        if not version or version["project_id"] != project_id:
            return None
        return {**version, "has_diff": version["version_number"] > 1}

    def delete_version(self, project_id: str, version_id: str) -> None:
        project = self.state["projects"].get(project_id)
        version = self.state["versions"].pop(version_id, None)
        if not project or not version:
            return
        if version_id in project["version_ids"]:
            project["version_ids"].remove(version_id)
        self.state["documents"].pop(version_id, None)
        self.state["errors"].pop(version_id, None)
        self.state["diffs"].pop(version_id, None)
        self._append_activity(
            "Smazání verze",
            f"Projekt „{project['title']}“: odstraněna verze V{version['version_number']}.",
            project["title"],
        )

    def get_version_document(self, version_id: str) -> str:
        if version_id in self.state["documents"]:
            return self.state["documents"][version_id]

        version = self.state["versions"].get(version_id)
        project = self.state["projects"].get(version["project_id"]) if version else None
        title = project["title"] if project else "Dokument"
        return f"""
<h1>{title}</h1>
<p>Tato verze dokumentu je dostupná ve frontend mocku jako zjednodušený náhled. Pro starší verze zatím nemáme plný export původního HTML obsahu.</p>
<h2>Souhrn verze</h2>
<p>Verze V{version['version_number'] if version else '?'} byla analyzována ve stavu <strong>{version['status'] if version else 'unknown'}</strong>.</p>
<p>Počet nalezených chyb: <strong>{version['error_count'] if version and version['error_count'] is not None else '—'}</strong>.</p>
"""

    def get_version_errors(self, version_id: str) -> list[dict[str, Any]]:
        if version_id in self.state["errors"]:
            return self.state["errors"][version_id]
        version = self.state["versions"].get(version_id)
        if not version or version["status"] != "completed":
            return []
        baseline = deepcopy(self.state["errors"]["ver-sentiment-3"])
        limit = min(len(baseline), max(1, version["error_count"] or 3))
        trimmed = baseline[:limit]
        for index, item in enumerate(trimmed, start=1):
            item["id"] = f"{version_id}-error-{index}"
        return trimmed

    def get_visible_errors(self, user: dict[str, Any], version_id: str) -> list[dict[str, Any]]:
        errors = self.get_version_errors(version_id)
        if user["tier"] == "institutional_free":
            return errors[:3]
        return errors

    def get_hidden_error_count(self, user: dict[str, Any], version_id: str) -> int:
        errors = self.get_version_errors(version_id)
        if user["tier"] == "institutional_free":
            return max(0, len(errors) - 3)
        return 0

    def get_error(self, error_id: str, user_id: str | None = None) -> dict[str, Any] | None:
        for version_id, errors in self.state["errors"].items():
            for error in errors:
                if error["id"] != error_id:
                    continue
                version = self.state["versions"].get(version_id)
                project = self.state["projects"].get(version["project_id"]) if version else None
                if user_id and project and project["user_id"] != user_id:
                    return None
                return {
                    **error,
                    "version_id": version_id,
                    "project_id": version["project_id"] if version else None,
                    "project_title": project["title"] if project else None,
                }
        return None

    def get_diff(self, version_id: str) -> dict[str, Any] | None:
        if version_id in self.state["diffs"]:
            return self.state["diffs"][version_id]
        version = self.state["versions"].get(version_id)
        if not version or version["version_number"] <= 1:
            return None
        return {
            "summary": {"added": 8, "removed": 2, "fixed": max(1, (version["error_count"] or 6) // 2), "open": version["error_count"] or 6},
            "changes": [
                {
                    "kind": "added",
                    "label": "Přidáno",
                    "description": "Doplněny nové odstavce a upřesnění argumentace oproti předchozí verzi.",
                    "location": "Vybrané pasáže dokumentu",
                },
                {
                    "kind": "updated",
                    "label": "Upraveno",
                    "description": "Zpřesněna formulace některých tvrzení a doplněna terminologie.",
                    "location": "Hlavní text práce",
                },
            ],
            "before_html": """
<h3>Předchozí verze</h3>
<p><span class="line removed">Starší formulace odstavce bez doplněného zdroje a bez přesnější specifikace metodiky.</span></p>
<p><span class="line">Původní text dokumentu před poslední úpravou.</span></p>
""",
            "after_html": """
<h3>Aktuální verze</h3>
<p><span class="line added">Rozšířená formulace s doplněným zdrojem, metodikou a přesnějším vymezením výsledků.</span></p>
<p><span class="line updated">Text byl zpřesněn a lépe navazuje na ostatní části dokumentu.</span></p>
""",
        }

    def get_analysis_status(self, project_id: str, version_id: str) -> dict[str, Any]:
        version = self.get_version(project_id, version_id)
        if not version:
            return {
                "status": "failed",
                "progress": {
                    "total_steps": 0,
                    "completed_steps": 0,
                    "current_step": "Neznámá verze",
                    "percent": 0,
                },
                "reason": "version_not_found",
            }

        steps = version["analysis_steps"]
        total = max(1, len(steps))

        if version["status"] == "processing":
            version["poll_count"] += 1
            completed = min(total - 1, version["poll_count"])
            percent = int((completed / total) * 100)
            if version["poll_count"] >= total:
                version["status"] = "completed"
                version["error_count"] = len(self.get_version_errors(version_id))
                percent = 100
                completed = total
            current_step = steps[min(completed, total - 1)]
            return {
                "status": version["status"],
                "progress": {
                    "total_steps": total,
                    "completed_steps": completed,
                    "current_step": current_step,
                    "percent": percent,
                },
            }

        if version["status"] in {"failed", "conversion_failed"}:
            return {
                "status": version["status"],
                "progress": {
                    "total_steps": total,
                    "completed_steps": 0,
                    "current_step": steps[0] if steps else "Načítám",
                    "percent": 0,
                },
                "reason": "mock_failure",
            }

        return {
            "status": version["status"],
            "progress": {
                "total_steps": total,
                "completed_steps": total,
                "current_step": steps[-1] if steps else "Dokončeno",
                "percent": 100,
            },
        }

    def retry_analysis(self, project_id: str, version_id: str) -> None:
        version = self.get_version(project_id, version_id)
        if not version:
            return
        version["status"] = "processing"
        version["poll_count"] = 0
        version["error_count"] = None
        self._append_activity("Retry analýzy", f"Znovuspuštěna analýza verze {version['version_number']}.", project_id)

    def list_admin_users(self) -> list[dict[str, Any]]:
        return sorted(self.state["users"].values(), key=lambda item: item["email"])

    def update_user(self, user_id: str, role: str, tier: str, monthly_scan_budget: int) -> None:
        user = self.state["users"][user_id]
        user["role"] = role
        user["tier"] = tier
        user["monthly_scan_budget"] = monthly_scan_budget
        self._append_activity("Úprava uživatele", f"Uživatel {user['email']} byl aktualizován.", "Admin UI")

    def delete_user(self, user_id: str) -> None:
        user = self.state["users"].pop(user_id, None)
        if not user:
            return
        for project_id in [project["id"] for project in self.state["projects"].values() if project["user_id"] == user_id]:
            self.delete_project(project_id)
        self._append_activity("Smazání uživatele", f"Uživatel {user['email']} byl odstraněn.", "Admin UI")

    def list_error_types(self) -> list[dict[str, Any]]:
        return list(self.state["error_types"].values())

    def add_error_type(self, slug: str, label: str, description: str) -> None:
        self.state["error_types"][slug] = {
            "id": slug,
            "slug": slug,
            "label": label,
            "description": description,
            "system": False,
        }
        self._append_activity("Nový typ chyby", f"Přidán typ {label}.", "Admin UI")

    def update_error_type(self, type_id: str, label: str, description: str) -> None:
        error_type = self.state["error_types"][type_id]
        error_type["label"] = label
        error_type["description"] = description
        self._append_activity("Úprava typu chyby", f"Typ {label} byl upraven.", "Admin UI")

    def delete_error_type(self, type_id: str) -> None:
        error_type = self.state["error_types"].pop(type_id, None)
        if not error_type:
            return
        self._append_activity("Smazání typu chyby", f"Typ {error_type['label']} byl odstraněn.", "Admin UI")

    def list_allowed_domains(self) -> list[dict[str, Any]]:
        return list(self.state["allowed_domains"].values())

    def add_allowed_domain(self, domain: str, university_name: str, free_analyses_per_month: int) -> None:
        domain_id = f"domain-{domain.replace('.', '-')}"
        self.state["allowed_domains"][domain_id] = {
            "id": domain_id,
            "domain": domain,
            "university_name": university_name,
            "free_analyses_per_month": free_analyses_per_month,
            "active": True,
        }
        self._append_activity("Povolená doména", f"Přidána doména {domain}.", "Admin UI")

    def toggle_domain(self, domain_id: str) -> None:
        domain = self.state["allowed_domains"][domain_id]
        domain["active"] = not domain["active"]
        self._append_activity("Přepnutí domény", f"Doména {domain['domain']} změnila stav.", "Admin UI")

    def update_allowed_domain(
        self,
        domain_id: str,
        *,
        active: bool | None = None,
        free_analyses_per_month: int | None = None,
        university_name: str | None = None,
    ) -> None:
        domain = self.state["allowed_domains"][domain_id]
        if active is not None:
            domain["active"] = active
        if free_analyses_per_month is not None:
            domain["free_analyses_per_month"] = free_analyses_per_month
        if university_name:
            domain["university_name"] = university_name
        self._append_activity("Úprava domény", f"Doména {domain['domain']} byla upravena.", "Admin UI")

    def delete_allowed_domain(self, domain_id: str) -> None:
        domain = self.state["allowed_domains"].pop(domain_id, None)
        if not domain:
            return
        self._append_activity("Smazání domény", f"Doména {domain['domain']} byla odstraněna.", "Admin UI")

    def create_faculty(self, code: str, name: str, short_name: str, university_name: str) -> dict[str, Any]:
        faculty_id = code.lower().replace(" ", "-")
        faculty = {
            "id": faculty_id,
            "code": code,
            "name": name,
            "short_name": short_name,
            "university_name": university_name,
        }
        self.state["faculties"][faculty_id] = faculty
        self._append_activity("Nová fakulta", f"Přidána fakulta {code}.", "Admin UI")
        return faculty

    def add_pipeline_step(self, faculty_id: str, name: str, description: str) -> None:
        existing = self.get_pipeline_steps(faculty_id)
        next_order = len(existing) + 1
        step_id = f"{faculty_id}-step-{next_order}"
        self.state["pipeline_steps"][step_id] = {
            "id": step_id,
            "faculty_id": faculty_id,
            "name": name,
            "description": description,
            "prompt_version": 1,
            "active": True,
            "order": next_order,
        }
        self._append_activity("Přidán krok pipeline", f"Nový krok „{name}“ pro {faculty_id}.", "Admin UI")

    def update_pipeline_step(
        self,
        step_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        active: bool | None = None,
    ) -> None:
        step = self.state["pipeline_steps"][step_id]
        if name:
            step["name"] = name
        if description:
            step["description"] = description
        if active is not None:
            step["active"] = active
        self._append_activity("Úprava kroku pipeline", f"Krok „{step['name']}“ byl upraven.", "Admin UI")

    def delete_pipeline_step(self, step_id: str) -> None:
        step = self.state["pipeline_steps"].pop(step_id, None)
        if not step:
            return
        for project in self.state["projects"].values():
            if step_id in project["pipeline_step_ids"]:
                project["pipeline_step_ids"] = [item for item in project["pipeline_step_ids"] if item != step_id]
        self._append_activity("Smazání kroku pipeline", f"Krok „{step['name']}“ byl odstraněn.", "Admin UI")

    def get_admin_overview(self) -> dict[str, Any]:
        students = [user for user in self.state["users"].values() if user["role"] == "student"]
        scans_today = sum(1 for version in self.state["versions"].values() if version["created_at"].startswith("3. 4. 2026"))
        return {
            "kpis": [
                {"label": "Aktivní uživatelé", "value": "1 284", "meta": "+12,4 % oproti minulému týdnu", "alert": False},
                {"label": "Dnešní skeny", "value": str(max(347, scans_today)), "meta": "92 % dokončeno do 90 sekund", "alert": False},
                {"label": "Fronta zpracování", "value": "18", "meta": "4 úlohy čekají déle než 5 minut", "alert": True},
                {"label": "Otevřené incidenty", "value": "2", "meta": "1 kritický incident vyžaduje zásah", "alert": True},
            ],
            "activity": self.state["admin_activity"][:6],
            "queues": self.state["admin_queues"],
            "faculties": [
                {"name": faculty["code"], "subtitle": faculty["name"], "count": count, "growth": growth}
                for faculty, count, growth in [
                    (self.state["faculties"]["fm"], "482 skenů", "+18 %"),
                    (self.state["faculties"]["fe"], "291 skenů", "+9 %"),
                    (self.state["faculties"]["fp"], "173 skenů", "+6 %"),
                ]
            ],
            "student_count": len(students),
        }

    def list_audit_log(self) -> list[dict[str, Any]]:
        return self.state["admin_activity"]


store = MockStore()
