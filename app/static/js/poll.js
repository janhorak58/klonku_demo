document.addEventListener("DOMContentLoaded", () => {
  const card = document.querySelector(".analysis-card[data-status-url]");
  if (!card) return;

  const statusUrl = card.dataset.statusUrl;
  const resultsUrl = card.dataset.resultsUrl;
  const fill = document.getElementById("progress-fill");
  const percent = document.getElementById("progress-percent");
  const stepsLabel = document.getElementById("progress-steps");
  const currentStep = document.getElementById("current-step");
  const stepItems = [...document.querySelectorAll("#step-list .step-item")];
  let count = 0;

  const applyState = (payload) => {
    if (payload.status === "completed" || payload.status === "partial") {
      window.location.href = resultsUrl;
      return;
    }

    if (payload.status === "failed" || payload.status === "conversion_failed") {
      document.getElementById("polling-content")?.classList.add("hidden");
      document.getElementById("analysis-error")?.classList.remove("hidden");
      return;
    }

    fill.style.width = `${payload.progress.percent}%`;
    percent.textContent = `${payload.progress.percent} %`;
    stepsLabel.textContent = `${payload.progress.completed_steps} / ${payload.progress.total_steps} kroků`;
    currentStep.textContent = payload.progress.current_step;

    stepItems.forEach((item, index) => {
      item.classList.remove("done", "active");
      const icon = item.querySelector(".step-icon");
      icon.className = "step-icon pending-icon";
      icon.textContent = String(index + 1);
      if (index < payload.progress.completed_steps) {
        item.classList.add("done");
        icon.className = "step-icon done-icon";
        icon.textContent = "✓";
      } else if (index === payload.progress.completed_steps) {
        item.classList.add("active");
        icon.className = "step-icon active-icon";
        icon.textContent = String(index + 1);
      }
    });
  };

  const tick = async () => {
    const response = await fetch(statusUrl, { headers: { "X-Requested-With": "XMLHttpRequest" } });
    const payload = await response.json();
    applyState(payload);
    count += 1;
    const delay = count < 10 ? 3000 : 10000;
    window.setTimeout(tick, delay);
  };

  tick();
});
