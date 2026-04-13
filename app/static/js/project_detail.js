document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("document-input");
  const selected = document.getElementById("selected-file");
  if (!input || !selected) return;

  input.addEventListener("change", () => {
    const file = input.files?.[0];
    if (!file) {
      selected.classList.add("hidden");
      selected.textContent = "";
      return;
    }
    selected.classList.remove("hidden");
    selected.innerHTML = `<h3>${file.name}</h3><p>${Math.round(file.size / 1024)} KB</p>`;
  });
});
