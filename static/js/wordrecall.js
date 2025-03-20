document.addEventListener("DOMContentLoaded", function () {
  let startButton = document.getElementById("startButton");
  let inputSection = document.getElementById("inputSection");
  let userInput = document.getElementById("userInput");
  let submitButton = document.getElementById("submitAnswer");
  let feedback = document.getElementById("feedback");
  let feedbackText = document.getElementById("feedbackText");
  let wordDisplay = document.getElementById("wordDisplay");

  let currentIndex = 0;
  let correctAnswers = 0;

  async function fetchWords() {
    let response = await fetch("/get_words", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ current_index: currentIndex })
    });

    let data = await response.json();
    if (data.game_over) {
      feedbackText.innerHTML = `🎉 Game Over! You got ${correctAnswers} out of ${currentIndex} correct.`;
      feedback.style.display = "block";
      return;
    }

    wordDisplay.innerHTML = data.words.join(" ");
    waitForEnterKey();
  }

  function waitForEnterKey() {
    document.addEventListener("keydown", function enterKeyHandler(event) {
      if (event.key === "Enter" && document.activeElement !== userInput) {
        wordDisplay.innerHTML = "";
        inputSection.style.display = "block";
        userInput.focus();
        document.removeEventListener("keydown", enterKeyHandler);
      }
    });
  }

  submitButton.addEventListener("click", async function () {
    let userAnswer = userInput.value.trim();
    if (!userAnswer) {
      feedbackText.innerHTML = "Please enter your answer before submitting.";
      feedback.style.display = "block";
      return;
    }

    let response = await fetch("/check_words", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ current_index: currentIndex, user_words: userAnswer })
    });

    let result = await response.json();
    if (result.correct) {
      correctAnswers++;
    }

    userInput.value = "";
    inputSection.style.display = "none";
    currentIndex++;
    fetchWords();
  });

  startButton.addEventListener("click", function () {
    startButton.style.display = "none";
    fetchWords();
  });
});
