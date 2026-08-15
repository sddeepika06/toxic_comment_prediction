const commentText = document.getElementById('commentText');
const charCounter = document.getElementById('charCounter');
const scanButton = document.getElementById('scanButton');
const buttonIcon = document.getElementById('buttonIcon');
const buttonText = document.getElementById('buttonText');
const statusMessage = document.getElementById('statusMessage');
const resultsPanel = document.getElementById('resultsPanel');
const resultBadge = document.getElementById('resultBadge');

const labels = ['Toxic', 'Severe Toxic', 'Hate Speech', 'Offensive'];

function updateCharacterCount() {
  const count = commentText.value.length;
  charCounter.textContent = `${count} / 500`;
}

function setLoadingState(isLoading) {
  scanButton.disabled = isLoading;
  scanButton.classList.toggle('opacity-70', isLoading);
  buttonIcon.innerHTML = isLoading ? '<span class="loading-spinner"></span>' : 'search';
  buttonText.textContent = isLoading ? 'Scanning...' : 'Scan Comment';
  statusMessage.textContent = isLoading ? 'Analyzing the comment...' : 'Ready to analyze your comment.';
}

function renderResults(payload) {
  resultsPanel.innerHTML = '';

  labels.forEach((label) => {
    const percent = payload[label] ?? 0;
    const card = document.createElement('div');
    card.className = 'progress-card result-animate';
    card.innerHTML = `
      <div class="progress-label">
        <span>${label}</span>
        <span class="result-value">${percent.toFixed(2)}%</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill" style="width: 0%"></div>
      </div>
    `;
    resultsPanel.appendChild(card);
  });

  requestAnimationFrame(() => {
    const fills = resultsPanel.querySelectorAll('.progress-fill');
    fills.forEach((fill, index) => {
      const value = payload[labels[index]] ?? 0;
      fill.style.width = `${Math.max(value, 2)}%`;
    });
  });

  resultBadge.textContent = 'Scanned';
  resultBadge.className = 'rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300';
}

function showError(message) {
  resultsPanel.innerHTML = `
    <div class="rounded-2xl border border-rose-400/30 bg-rose-500/10 p-4 text-sm text-rose-200">
      ${message}
    </div>
  `;
  resultBadge.textContent = 'Error';
  resultBadge.className = 'rounded-full border border-rose-400/30 bg-rose-500/10 px-3 py-1 text-xs font-medium text-rose-300';
}

async function scanComment() {
  const text = commentText.value.trim();

  if (!text) {
    showError('Please enter a comment before scanning.');
    return;
  }

  setLoadingState(true);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || 'Unable to analyze the comment right now.');
    }

    renderResults(payload);
    statusMessage.textContent = 'Analysis complete.';
  } catch (error) {
    showError(error.message || 'A network error occurred. Please try again.');
    statusMessage.textContent = 'Analysis failed.';
  } finally {
    setLoadingState(false);
  }
}

commentText.addEventListener('input', updateCharacterCount);
scanButton.addEventListener('click', scanComment);
updateCharacterCount();
