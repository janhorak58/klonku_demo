const onboardingPipelines = window.__PIPELINE_MAP__ || {};

function renderOnboardingSteps(facultyId) {
  const steps = onboardingPipelines[facultyId] || [];
  const recommended = document.querySelector("[data-recommended-steps]");
  const custom = document.querySelector("[data-custom-steps]");
  if (!recommended || !custom) return;

  recommended.innerHTML = steps.map((step) => `<span class="chip active-chip">${step.name}</span>`).join("");
  custom.innerHTML = steps
    .map(
      (step) => `
      <label class="custom-step-row">
        <input type="checkbox" name="step_ids" value="${step.id}" checked>
        ${step.name}
      </label>`,
    )
    .join("");
}

document.addEventListener("DOMContentLoaded", () => {
  const facultySelect = document.getElementById("faculty_id");
  const cards = [...document.querySelectorAll("[data-pipeline-card]")];

  cards.forEach((card) => {
    card.addEventListener("click", () => {
      cards.forEach((item) => item.classList.remove("selected"));
      card.classList.add("selected");
      card.querySelector('input[type="radio"]').checked = true;
    });
  });

  if (facultySelect) {
    renderOnboardingSteps(facultySelect.value);
    facultySelect.addEventListener("change", () => renderOnboardingSteps(facultySelect.value));
  }
});
