document.addEventListener("DOMContentLoaded", () => {
  const app = document.querySelector(".demo-app");
  if (!app) return;

  const groups = [...document.querySelectorAll(".demo-error-group")];
  const cards = [...document.querySelectorAll(".demo-error-card")].sort(
    (left, right) => Number(left.dataset.order) - Number(right.dataset.order),
  );
  const highlights = [...document.querySelectorAll(".error-hl")];
  const chipButtons = [...document.querySelectorAll(".demo-cat-chip")];
  const startButton = document.getElementById("demo-start");
  const resetButton = document.getElementById("demo-reset");
  const foundCount = document.getElementById("demo-found-count");
  const statusText = document.getElementById("demo-status-text");
  const statusStep = document.getElementById("demo-status-step");
  const progressFill = document.getElementById("demo-progress-fill");
  const emptyState = document.getElementById("demo-empty-state");

  const total = Number(app.dataset.demoTotal || cards.length);
  const revealDelayMs = 640;
  const analysisSteps = [
    "Kontrola povinných částí",
    "Kontrola citací a zdrojů",
    "Kontrola typografie",
    "Kontrola jazyka a pravopisu",
    "Kontrola dat a metodiky",
  ];
  const stepCount = analysisSteps.length;

  let discovered = 0;
  let timerId = null;
  let running = false;
  let selectedCategory = "all";

  const pulseElement = (element) => {
    if (!element) return;
    element.classList.remove("demo-focus");
    void element.offsetWidth;
    element.classList.add("demo-focus");
  };

  const bumpCount = () => {
    foundCount.classList.remove("demo-count-bumping");
    void foundCount.offsetWidth;
    foundCount.classList.add("demo-count-bumping");
    foundCount.addEventListener("animationend", () => foundCount.classList.remove("demo-count-bumping"), { once: true });
  };

  const visibleCards = () =>
    cards.filter((card) => !card.classList.contains("hidden") && card.style.display !== "none");

  const pulseSelection = (id) => {
    pulseElement(document.querySelector(`.demo-error-card[data-error="${id}"]`));
    pulseElement(document.querySelector(`.error-hl[data-error="${id}"]`));
  };

  const setActive = (id) => {
    cards.forEach((card) => card.classList.toggle("active", card.dataset.error === id && card.style.display !== "none"));
    highlights.forEach((hl) => hl.classList.toggle("active", hl.dataset.error === id));
  };

  const updateProgress = () => {
    foundCount.textContent = String(discovered);
    emptyState.classList.toggle("hidden", discovered > 0);
  };

  const updateChipState = () => {
    chipButtons.forEach((chip) => chip.classList.toggle("active", chip.dataset.cat === selectedCategory));
  };

  const applyFilter = () => {
    groups.forEach((group) => {
      const discoveredCards = [...group.querySelectorAll(".demo-error-card")].filter(
        (card) => !card.classList.contains("hidden"),
      );
      const groupVisible =
        discoveredCards.length > 0 &&
        (selectedCategory === "all" || group.dataset.group === selectedCategory);
      group.style.display = groupVisible ? "" : "none";
    });

    const activeCard = document.querySelector(".demo-error-card.active");
    if (activeCard && activeCard.style.display === "none") {
      const fallback = visibleCards()[0];
      if (fallback) {
        setActive(fallback.dataset.error);
      }
    }
  };

  const syncGroups = () => {
    groups.forEach((group) => {
      const hasVisibleCard = [...group.querySelectorAll(".demo-error-card")].some(
        (card) => !card.classList.contains("hidden"),
      );
      group.classList.toggle("hidden", !hasVisibleCard);
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

    const currentStep = Math.min(
      stepCount,
      Math.max(1, Math.ceil((Math.max(discovered, 1) / Math.max(total, 1)) * stepCount)),
    );
    const width = 8 + (currentStep / stepCount) * 84;
    progressFill.style.width = `${Math.min(92, width)}%`;
    progressFill.classList.remove("complete");
  };

  const attachCardInteractions = () => {
    cards.forEach((card) => {
      card.addEventListener("click", () => {
        if (card.classList.contains("hidden") || card.style.display === "none") return;
        setActive(card.dataset.error);
        pulseSelection(card.dataset.error);
        const target = document.querySelector(`.error-hl[data-error="${card.dataset.error}"]`);
        target?.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });

    highlights.forEach((hl) => {
      hl.addEventListener("click", () => {
        if (!hl.classList.contains("found")) return;
        const targetCard = document.querySelector(`.demo-error-card[data-error="${hl.dataset.error}"]`);
        if (targetCard?.classList.contains("hidden")) return;
        selectedCategory = targetCard?.dataset.category || "all";
        if (selectedCategory && selectedCategory !== "all") {
          updateChipState();
        }
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

  const revealNextError = () => {
    if (discovered >= total) {
      running = false;
      timerId = null;
      statusText.textContent = "Analýza dokončena";
      statusStep.textContent = `Hotovo. Analýza odhalila ${total} problémů k opravě.`;
      setProgressForState("complete");
      startButton.disabled = false;
      startButton.textContent = "Spustit znovu";
      return;
    }

    const card = cards[discovered];
    const errorId = card.dataset.error;
    const stepLabel = analysisSteps[Math.min(analysisSteps.length - 1, Math.floor((discovered / Math.max(total, 1)) * stepCount))];

    card.classList.remove("hidden");
    card.classList.add("demo-found");

    const highlight = document.querySelector(`.error-hl[data-error="${errorId}"]`);
    highlight?.classList.add("found");

    discovered += 1;
    updateProgress();
    bumpCount();
    syncGroups();
    setProgressForState("running");
    setActive(errorId);
    pulseSelection(errorId);

    statusText.textContent = "Probíhá analýza";
    statusStep.textContent = `${stepLabel} • nalezen další problém v dokumentu`;

    card.scrollIntoView({ behavior: "smooth", block: "nearest" });
    highlight?.scrollIntoView({ behavior: "smooth", block: "center" });

    timerId = window.setTimeout(revealNextError, revealDelayMs);
  };

  const resetDemo = () => {
    if (timerId) {
      window.clearTimeout(timerId);
      timerId = null;
    }

    running = false;
    discovered = 0;
    selectedCategory = "all";

    cards.forEach((card) => {
      card.classList.add("hidden");
      card.classList.remove("active", "demo-found", "demo-focus");
      card.style.display = "";
    });

    groups.forEach((group) => {
      group.classList.add("hidden");
      group.style.display = "";
    });

    highlights.forEach((hl) => hl.classList.remove("active", "found", "demo-focus"));

    statusText.textContent = "Připraveno";
    statusStep.textContent = "Spusť analýzu.";
    startButton.disabled = false;
    startButton.textContent = "Začít analýzu";

    updateChipState();
    updateProgress();
    setProgressForState("idle");
  };

  startButton.addEventListener("click", () => {
    if (running) return;
    resetDemo();
    running = true;
    startButton.disabled = true;
    startButton.textContent = "Probíhá...";
    statusText.textContent = "Probíhá analýza";
    statusStep.textContent = "Kontrolujeme dokument.";
    setProgressForState("running");
    timerId = window.setTimeout(revealNextError, 700);
  });

  resetButton.addEventListener("click", resetDemo);

  attachCardInteractions();
  resetDemo();
});
