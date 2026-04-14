document.addEventListener("DOMContentLoaded", () => {
  const app = document.querySelector(".demo-app");
  if (!app) return;

  const groups       = [...document.querySelectorAll(".demo-error-group")];
  const highlights   = [...document.querySelectorAll(".error-hl")];
  const chipButtons  = [...document.querySelectorAll(".demo-cat-chip")];
  const startButton  = document.getElementById("demo-start");
  const resetButton  = document.getElementById("demo-reset");
  const foundCount   = document.getElementById("demo-found-count");
  const statusText   = document.getElementById("demo-status-text");
  const statusStep   = document.getElementById("demo-status-step");
  const statusDot    = document.getElementById("demo-status-dot");
  const progressFill = document.getElementById("demo-progress-fill");
  const emptyState   = document.getElementById("demo-empty-state");
  const stepItems    = [...document.querySelectorAll(".demo-step-item")];

  const pipelineStepCount = stepItems.length || 4;
  const revealDelayMs     = 1500;

  /* ── 1. Mapa: kategorie → index kroku (normalizovaně) ── */
  const stepCatOrder = {};
  stepItems.forEach((item, i) => {
    const cat = item.dataset.cat?.trim().toLowerCase();
    if (cat) stepCatOrder[cat] = i;
  });

  const getStepIdx = (category) => {
    const key = (category || "").trim().toLowerCase();
    const idx = stepCatOrder[key];
    return (idx !== undefined) ? idx : -1; // -1 = neznámá kategorie
  };

  /* ── 2. Mapa: errorId → pořadí v DOM (= shora dolů) ── */
  const hlDomOrder = {};
  document.querySelectorAll(".error-hl").forEach((hl, i) => {
    if (hl.dataset.error) hlDomOrder[hl.dataset.error] = i;
  });

  /* ── 3. Seřazení karet: krok → pozice v dokumentu ── */
  const cards = [...document.querySelectorAll(".demo-error-card")].sort((a, b) => {
    const sA = getStepIdx(a.dataset.category);
    const sB = getStepIdx(b.dataset.category);
    // Neznámé kategorie (−1) jdou na konec
    const sa = sA < 0 ? 9999 : sA;
    const sb = sB < 0 ? 9999 : sB;
    if (sa !== sb) return sa - sb;
    // Uvnitř kroku: pořadí dle pozice v dokumentu (shora dolů)
    return (hlDomOrder[a.dataset.error] ?? 9999) - (hlDomOrder[b.dataset.error] ?? 9999);
  });

  const total = Number(app.dataset.demoTotal || cards.length);

  let discovered       = 0;
  let timerId          = null;
  let running          = false;
  let selectedCategory = "all";

  /* ── Status dot ──────────────────────────────────── */
  const setStatusDot = (state) => {
    if (!statusDot) return;
    statusDot.className = `demo-status-dot ${state}`;
  };

  /* ── Indikátory kroků vlevo ──────────────────────── */
  const CHECK_SVG = `<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1.5,6 4.5,9.5 10.5,2.5"/></svg>`;
  const PULSE_DOT = `<span class="demo-step-dot-pulse"></span>`;

  const updateStepItems = (activeIdx) => {
    stepItems.forEach((item, i) => {
      const ind = item.querySelector(".demo-step-indicator");
      item.classList.remove("step-done", "step-active", "step-idle");
      if (!ind) return;
      if (activeIdx < 0) {
        item.classList.add("step-idle");
        ind.innerHTML = "";
      } else if (i < activeIdx) {
        item.classList.add("step-done");
        ind.innerHTML = CHECK_SVG;
      } else if (i === activeIdx) {
        item.classList.add("step-active");
        ind.innerHTML = PULSE_DOT;
      } else {
        item.classList.add("step-idle");
        ind.innerHTML = "";
      }
    });
  };

  /* ── Různé pomocníky ─────────────────────────────── */
  const pulseElement = (el) => {
    if (!el) return;
    el.classList.remove("demo-focus");
    void el.offsetWidth;
    el.classList.add("demo-focus");
  };

  const bumpCount = () => {
    foundCount.classList.remove("demo-count-bumping");
    void foundCount.offsetWidth;
    foundCount.classList.add("demo-count-bumping");
    foundCount.addEventListener(
      "animationend",
      () => foundCount.classList.remove("demo-count-bumping"),
      { once: true },
    );
  };

  const visibleCards = () =>
    cards.filter((c) => !c.classList.contains("hidden") && c.style.display !== "none");

  const pulseSelection = (id) => {
    pulseElement(document.querySelector(`.demo-error-card[data-error="${id}"]`));
    pulseElement(document.querySelector(`.error-hl[data-error="${id}"]`));
  };

  const setActive = (id) => {
    cards.forEach((c) =>
      c.classList.toggle("active", c.dataset.error === id && c.style.display !== "none"),
    );
    highlights.forEach((hl) => hl.classList.toggle("active", hl.dataset.error === id));
  };

  const updateProgress = () => {
    foundCount.textContent = String(discovered);
    emptyState.classList.toggle("hidden", discovered > 0);
  };

  const updateChipState = () => {
    chipButtons.forEach((chip) =>
      chip.classList.toggle("active", chip.dataset.cat === selectedCategory),
    );
  };

  const applyFilter = () => {
    groups.forEach((group) => {
      const hasDiscovered = [...group.querySelectorAll(".demo-error-card")].some(
        (c) => !c.classList.contains("hidden"),
      );
      const visible =
        hasDiscovered &&
        (selectedCategory === "all" || group.dataset.group === selectedCategory);
      group.style.display = visible ? "" : "none";
    });

    const active = document.querySelector(".demo-error-card.active");
    if (active && active.style.display === "none") {
      const fallback = visibleCards()[0];
      if (fallback) setActive(fallback.dataset.error);
    }
  };

  const syncGroups = () => {
    groups.forEach((group) => {
      const hasVisible = [...group.querySelectorAll(".demo-error-card")].some(
        (c) => !c.classList.contains("hidden"),
      );
      group.classList.toggle("hidden", !hasVisible);
    });
    applyFilter();
  };

  const setProgressForState = (state) => {
    if (state === "idle") {
      progressFill.style.width = "0%";
      progressFill.classList.remove("complete");
      return;
    }
    if (state === "complete") {
      progressFill.style.width = "100%";
      progressFill.classList.add("complete");
      return;
    }
    const pct = 8 + (Math.max(discovered, 1) / Math.max(total, 1)) * 84;
    progressFill.style.width = `${Math.min(92, pct)}%`;
    progressFill.classList.remove("complete");
  };

  /* ── Interakce s kartami / zvýrazněními ─────────── */
  const attachCardInteractions = () => {
    cards.forEach((card) => {
      card.addEventListener("click", () => {
        if (card.classList.contains("hidden") || card.style.display === "none") return;
        setActive(card.dataset.error);
        pulseSelection(card.dataset.error);
        document
          .querySelector(`.error-hl[data-error="${card.dataset.error}"]`)
          ?.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });

    highlights.forEach((hl) => {
      hl.addEventListener("click", () => {
        if (!hl.classList.contains("found")) return;
        const targetCard = document.querySelector(
          `.demo-error-card[data-error="${hl.dataset.error}"]`,
        );
        if (targetCard?.classList.contains("hidden")) return;
        selectedCategory = targetCard?.dataset.category || "all";
        if (selectedCategory !== "all") updateChipState();
        applyFilter();
        setActive(hl.dataset.error);
        pulseSelection(hl.dataset.error);
        targetCard?.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });

    chipButtons.forEach((chip) => {
      chip.addEventListener("click", () => {
        selectedCategory = chip.dataset.cat || "all";
        updateChipState();
        applyFilter();
      });
    });
  };

  /* ── Postupné odkrývání chyb ─────────────────────── */
  const revealNextError = () => {
    if (discovered >= total) {
      running = false;
      timerId  = null;
      setStatusDot("complete");
      updateStepItems(pipelineStepCount); // všechny kroky hotové
      statusText.textContent = "Analýza dokončena";
      if (statusStep) statusStep.textContent = `Celkem ${total} problémů`;
      setProgressForState("complete");
      startButton.disabled    = false;
      startButton.textContent = "Spustit znovu";
      return;
    }

    const card    = cards[discovered];
    const errorId = card.dataset.error;

    // Zjistíme, ve kterém kroku jsme — dle kategorie karty
    const stepIdx = getStepIdx(card.dataset.category);
    const activeStep = stepIdx >= 0
      ? Math.min(stepIdx, pipelineStepCount - 1)
      // Záloha: pokud kategorie neodpovídá žádnému kroku, použijeme poměr
      : Math.min(pipelineStepCount - 1, Math.floor((discovered / Math.max(total, 1)) * pipelineStepCount));

    const stepName = stepItems[activeStep]
      ?.querySelector(".demo-step-label")?.textContent?.trim() || "Probíhá analýza";

    card.classList.remove("hidden");
    card.classList.add("demo-found");
    document.querySelector(`.error-hl[data-error="${errorId}"]`)?.classList.add("found");

    discovered += 1;
    updateProgress();
    bumpCount();
    syncGroups();
    setProgressForState("running");
    updateStepItems(activeStep);
    setActive(errorId);
    pulseSelection(errorId);

    statusText.textContent = stepName;
    if (statusStep) statusStep.textContent = `Nalezeno ${discovered} / ${total}`;

    card.scrollIntoView({ behavior: "smooth", block: "nearest" });
    document
      .querySelector(`.error-hl[data-error="${errorId}"]`)
      ?.scrollIntoView({ behavior: "smooth", block: "center" });

    timerId = window.setTimeout(revealNextError, revealDelayMs);
  };

  /* ── Reset ───────────────────────────────────────── */
  const resetDemo = () => {
    if (timerId) { window.clearTimeout(timerId); timerId = null; }

    running          = false;
    discovered       = 0;
    selectedCategory = "all";

    cards.forEach((c) => {
      c.classList.add("hidden");
      c.classList.remove("active", "demo-found", "demo-focus");
      c.style.display = "";
    });
    groups.forEach((g) => { g.classList.add("hidden"); g.style.display = ""; });
    highlights.forEach((hl) => hl.classList.remove("active", "found", "demo-focus"));

    setStatusDot("idle");
    updateStepItems(-1);
    statusText.textContent  = "Připraven ke spuštění";
    if (statusStep) statusStep.textContent = "";
    startButton.disabled    = false;
    startButton.textContent = "Začít analýzu";

    updateChipState();
    updateProgress();
    setProgressForState("idle");
  };

  /* ── Tlačítka ────────────────────────────────────── */
  startButton.addEventListener("click", () => {
    if (running) return;
    resetDemo();
    running = true;
    startButton.disabled    = true;
    startButton.textContent = "Probíhá...";
    setStatusDot("running");
    updateStepItems(0);
    statusText.textContent = stepItems[0]?.querySelector(".demo-step-label")?.textContent?.trim()
      || "Probíhá analýza";
    if (statusStep) statusStep.textContent = "Kontrolujeme dokument…";
    setProgressForState("running");
    timerId = window.setTimeout(revealNextError, 700);
  });

  resetButton.addEventListener("click", resetDemo);

  attachCardInteractions();
  resetDemo();
});
