document.addEventListener("DOMContentLoaded", () => {
  const cards = [...document.querySelectorAll(".error-card")];
  const highlights = [...document.querySelectorAll(".error-hl")];
  const filters = [...document.querySelectorAll(".filter-chip")];

  const activate = (id) => {
    cards.forEach((card) => card.classList.toggle("active", card.dataset.error === id));
    highlights.forEach((hl) => hl.classList.toggle("active", hl.dataset.error === id));
  };

  cards.forEach((card) => {
    card.addEventListener("click", () => {
      activate(card.dataset.error);
      const target = document.querySelector(`.error-hl[data-error="${card.dataset.error}"]`);
      target?.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });

  highlights.forEach((hl) => {
    hl.addEventListener("click", () => {
      activate(hl.dataset.error);
      const targetCard = document.querySelector(`.error-card[data-error="${hl.dataset.error}"]`);
      targetCard?.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });

  filters.forEach((filter) => {
    filter.addEventListener("click", () => {
      filters.forEach((chip) => chip.classList.remove("active"));
      filter.classList.add("active");
      const value = filter.dataset.filter;
      cards.forEach((card) => {
        card.classList.toggle("hidden", value !== "all" && card.dataset.severity !== value);
      });
    });
  });
});
