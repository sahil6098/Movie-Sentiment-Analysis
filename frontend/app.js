const form = document.getElementById("sentiment-form");
const reviewInput = document.getElementById("review");
const analyzeButton = document.getElementById("analyze-button");
const clearButton = document.getElementById("clear-button");
const resultCard = document.getElementById("result-card");
const sentimentText = document.getElementById("sentiment-text");
const sentimentDescription = document.getElementById("sentiment-description");
const statusMessage = document.getElementById("status-message");

function setStatus(message) {
  statusMessage.textContent = message;
}

function resetResult() {
  resultCard.classList.add("hidden");
  resultCard.classList.remove("positive", "negative");
  sentimentText.textContent = "Waiting for input";
  sentimentDescription.textContent = "";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const review = reviewInput.value.trim();
  if (!review) {
    resetResult();
    setStatus("Please enter a movie review before analyzing.");
    reviewInput.focus();
    return;
  }

  analyzeButton.disabled = true;
  setStatus("Analyzing sentiment...");

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ review }),
    });

    const data = await response.json();

    if (!response.ok) {
      const errorMessage = data.detail || "Something went wrong while analyzing the review.";
      throw new Error(errorMessage);
    }

    const isPositive = data.prediction === 1;
    resultCard.classList.remove("hidden", "positive", "negative");
    resultCard.classList.add(isPositive ? "positive" : "negative");
    sentimentText.textContent = data.sentiment;
    sentimentDescription.textContent = isPositive
      ? "The model found more positive language and context in this review."
      : "The model found more negative language and context in this review.";
    setStatus("Analysis complete.");
  } catch (error) {
    resetResult();
    setStatus(error.message);
  } finally {
    analyzeButton.disabled = false;
  }
});

clearButton.addEventListener("click", () => {
  reviewInput.value = "";
  resetResult();
  setStatus("");
  reviewInput.focus();
});
