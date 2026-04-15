class TimerComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.render();
        this.originalTitle = document.title;
    }

    async connectedCallback() {};

    render() {
        this.shadowRoot.innerHTML = `
        <div id="timer">Timer: 15:00</div>
        <div class="controls">
            <button id="start-btn">Start</button>
            <button id="pause-btn">Pause</button>
            <button id="reset-btn">Reset</button>
        </div>
        `;
        let timeLeft = 15 * 60; // 15 minutes in seconds
        let timerId = null;

        const timerDisplay = this.shadowRoot.getElementById('timer');
        const startBtn = this.shadowRoot.getElementById('start-btn');
        const pauseBtn = this.shadowRoot.getElementById('pause-btn');
        const resetBtn = this.shadowRoot.getElementById('reset-btn');

        // Function to update the text on the screen
        function updateDisplay() {
            console.log("Display button clicked");
            const minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            seconds = seconds.toString().padStart(2, '0');
            timerDisplay.textContent = `Timer: ${minutes}:${seconds}`;
            document.title = `${minutes}:${seconds} - ${this.originalTitle}`;
        }

        // Logic to start the countdown using setInterval
        startBtn.addEventListener('click', () => {
            console.log("Start button clicked");
            if (timerId !== null) return; // Prevent multiple intervals
            
            timerId = setInterval(() => {
                if (timeLeft > 0) {
                    timeLeft--;
                    updateDisplay();
                } else {
                    clearInterval(timerId);
                    timerId = null;
                    document.title = this.originalTitle; // Reset title to original when timer is running
                    alert("Time is up!");
                }
            }, 1000);
        });

        // Logic to pause the timer by clearing the interval
        pauseBtn.addEventListener('click', () => {
            console.log("Pause button clicked");
            clearInterval(timerId);
            timerId = null;
            document.title = this.originalTitle; // Reset title to original when timer is running
        });

        // Logic to reset the timer to its original state
        resetBtn.addEventListener('click', () => {
            console.log("Reset button clicked");
            clearInterval(timerId);
            timerId = null;
            timeLeft = 15 * 60;
            updateDisplay();
            document.title = this.originalTitle; // Reset title to original when timer is running
        });
    }
}

customElements.define('timer-component', TimerComponent);