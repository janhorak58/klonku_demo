const dashboardPipelines = window.__PIPELINES__ || {};

function renderPipelineSteps(facultyId) {
  const steps = dashboardPipelines[facultyId] || [];
  const chips = document.getElementById("recommended-steps");
  const custom = document.getElementById("custom-steps");
  if (!chips || !custom) return;

  chips.innerHTML = steps.map((step) => `<span class="chip active-chip">${step.name}</span>`).join("");
  custom.innerHTML = steps
    .map(
      (step) => `
      <label class="custom-step-row">
        <input type="checkbox" name="pipeline_step_ids" value="${step.id}" checked>
        ${step.name}
      </label>`,
    )
    .join("");
}

document.addEventListener("DOMContentLoaded", () => {
  const facultySelect = document.getElementById("faculty_id");
  const modeInputs = [...document.querySelectorAll('input[name="pipeline_mode"]')];
  const chips = document.getElementById("recommended-steps");
  const custom = document.getElementById("custom-steps");

  const syncMode = () => {
    const mode = modeInputs.find((input) => input.checked)?.value || "recommended";
    chips?.classList.toggle("is-hidden", mode === "custom");
    custom?.classList.toggle("is-visible", mode === "custom");
  };

  if (facultySelect) {
    renderPipelineSteps(facultySelect.value);
    facultySelect.addEventListener("change", () => renderPipelineSteps(facultySelect.value));
  }

  modeInputs.forEach((input) => input.addEventListener("change", syncMode));
  syncMode();
});
