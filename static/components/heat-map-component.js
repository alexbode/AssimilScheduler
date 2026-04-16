class HeatMapComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    async connectedCallback() {
        await this.render(null);
        await this.fetchData();
    }

    async fetchData() {
        try {
            const response = await fetch(`/api/v1/review_counts`);
            const data = await response.json();
            await this.render(data.response);
        } catch (error) {
            this.render(null);
            console.error(error);
        }
    }

    async render(data) {
        if (data == null) {
            this.shadowRoot.innerHTML = ``;
            return 
        };
        let reviewCountMap = new Map();
        let maxReviewCount = 0;
        for (let i = 0; i < data.length; i++) {
            const dateString = data[i][0]
            const reviewCount = data[i][1];
            if (reviewCount > maxReviewCount) {
                maxReviewCount = reviewCount;
            }
            reviewCountMap.set(dateString, reviewCount);
        }

        const now = new Date();
        const offset = now.getTimezoneOffset() * 60000;
        const date = new Date(now - offset);
        const dayIndex = date.getDay();
        let html = ""
        for (let i = 364 + (dayIndex % 7); i >= 0; i--) {
            const n = new Date()
            const date = new Date(n - offset);
            date.setDate(now.getDate() - i);
            const dateString = date.toISOString().split('T')[0] + "T00:00:00";
            const reviewCount = reviewCountMap.get(dateString) || -1;
            const activityLevel = reviewCount == -1 ? 0 : (Math.floor(reviewCount / maxReviewCount * 4) + 1);
            html += `<div class="cell level-${activityLevel}" title="${date.toDateString()}: ${Math.max(0, reviewCount)} reviews"></div>`;
        this.shadowRoot.innerHTML = `
        <style>
        .heatmap {
            margin-top: 30px;
            min-width: 800px;
            display: grid;
            grid-template-rows: repeat(7, 1fr);
            grid-auto-flow: column; /* Crucial for week-by-week layout */
            column-gap: 1px;
            row-gap: 1px;
        }
        .cell {
            width: 12px;
            height: 12px;
            background-col            .bar:hover {
                opacity: 0.8;
                transform: scaleY(1.1); /* Slight vertical pop on hover */
            }or: #ebedf0;
            border-radius: 3px;
            transition: opacity 0.2s ease, transform 0.2s ease;
            cursor: pointer;
        }
        .cell:hover {
            opacity: 0.8;
            transform: scale(1.1); /* Slight vertical pop on hover */
        }

        /* Define intensity levels */
        // .level-0 { background-cologrid-auto-flow: columnr: #000000; }
        .level-0 { background-color: #202321; }
        .level-1 { background-color: #ebedf0; }
        .level-2 { background-color: #9be9a8; }
        .level-3 { background-color: #40c463; }
        .level-4 { background-color: #30a14e; }
        .level-5 { background-color: #216e39; }
        .container {
            display: flex;
            justify-content: center;
        }
        </style>
        <div class="container">
            <div class="heatmap">
                ${html}
            </div>
        </div>
        `
        };
    }
}

customElements.define('heat-map-component', HeatMapComponent);