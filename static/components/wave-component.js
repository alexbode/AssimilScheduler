class WaveComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.language = this.capitalCase(window.location.pathname.slice(1));
    }

    async connectedCallback() {
        await this.render(null);
        await this.fetchData();
    }

    async fetchData() {
        try {
            const response = await fetch(`/api/v1/get_course/${this.language.replace(" ", "")}`);
            const data = await response.json();
            await this.render(data.response);
        } catch (error) {
            this.render(null);
            console.error(error);
        }
    }

    processData(data) {
        if (!data.waves) return;
        let maxWeight = 0;
        data.waves.flatMap(wave => wave.weights_list).forEach(w => {
            if (Math.max(w.weight) > maxWeight) {
                maxWeight = Math.max(w.weight);
            }
        });
        this.maxWeight = maxWeight;
    }

    createWaveBar(wave) {
        let waveMap = new Map();
        console.log(wave)
        for (let w of wave.weights_list) {
            waveMap.set(Math.floor(w.weight), [w.lesson, w.completed, w.skip]);
        }
        let html = "";
        for (let i = 1; i <= Math.floor(this.maxWeight); i++) {
            const waveValue = waveMap.get(i) || [null, null, null];
            const lesson = waveValue[0];
            const completed = waveValue[1];
            const skip = waveValue[2];
            let state = "exclude";
            if (skip == true) {
                state = "skip";
            } else if (completed == true) {
                state = "completed";
            } else if (completed == false) {
                state = "not-completed";
            }
            html += `<div class="bar ${state}" title="${lesson}"></div>`;
        }
        return html;
    }

    createWaveBars(waves) {
        let html = "";
        for (let i = 0; i < waves.length; i++) {
            const reviewType = waves[i].review_type;
            const offset = waves[i].weights.offset || 0;
            const multiplier = waves[i].weights.multiplier || 1;
        html += `<p>${reviewType} - offset: ${offset} - multipler: ${multiplier}</p>
                <div class="uptime-bars">
                    ${this.createWaveBar(waves[i])}
                </div>`
        }
        return html;
    }

    async render(data) {
        if (data == null) {
            this.shadowRoot.innerHTML = ``;
            return 
        }
        this.processData(data);
        let listHtml = "";
        for (let i = 0; i < 250; i++) {
            listHtml += `<div class="bar operational" title="May ${i + 1}: No downtime"></div>`;
        }
        this.shadowRoot.innerHTML = `
            <style>
            .uptime-widget {
                width: 100%;
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }

            .uptime-header {
                display: flex;
                justify-content: space-between;
                margin-bottom: 8px;
                font-size: 14px;
                color: var(--bg-color-3);
            }

            .uptime-percent {
                font-weight: 600;
                color: #10b981; /* Green text to match operational status */
            }

            .uptime-bars {
                display: flex;
                gap: 1px; 
                height: 40px; /* Set the height of your bars */
                width: 100%;
            }
            .bar {
                flex: 1;
                border-radius: 3px;
                min-width: 2px; /* Prevents bars from disappearing entirely on tiny screens */
                transition: opacity 0.2s ease, transform 0.2s ease;
                cursor: pointer;
            }

            .bar:hover {
                opacity: 0.8;
                transform: scaleY(1.1); /* Slight vertical pop on hover */
            }

            .bar.completed {
                background-color: #10b981; /* Instatus Green */
            }

            .bar.exclude {
                background-color: #505050; /* Instatus Red */
            }

            .bar.skip {
                background-color: #707070; /* Instatus Red */
            }

            .bar.not-completed {
                background-color: #909090; /* Instatus Red */
            }

            </style>
            <div class="uptime-widget">
                ${this.createWaveBars(data.waves)}
            </div>
        `;
    }

    capitalCase(str){
        return str.replace(/(^|-)\w/g, (match) => match.toUpperCase().replace("-", " "));
    }
}

customElements.define('wave-component', WaveComponent);