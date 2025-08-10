function startCountdown(seconds) {
    let timerElement = document.getElementById("timer");
    let statusElement = document.getElementById("status");
    let timeLeft = seconds;

    let interval = setInterval(function() {
        if (timeLeft <= 0) {
            clearInterval(interval);
            timerElement.textContent = "Done!";
            statusElement.textContent = "Enjoy your coffee! ☕";
        } else {
            timerElement.textContent = timeLeft;
        }
        timeLeft--;
    }, 1000);
}

