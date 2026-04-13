document.addEventListener("click", (event) => {
  const opener = event.target.closest("[data-modal-open]");
  if (opener) {
    const modal = document.getElementById(opener.dataset.modalOpen);
    if (modal) {
      modal.classList.add("is-open");
    }
  }

  const closer = event.target.closest("[data-modal-close]");
  if (closer) {
    closer.closest(".modal")?.classList.remove("is-open");
  }

  if (event.target.classList.contains("modal")) {
    event.target.classList.remove("is-open");
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    document.querySelectorAll(".modal.is-open").forEach((modal) => modal.classList.remove("is-open"));
  }
});
