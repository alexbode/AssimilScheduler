class HomeComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    async connectedCallback() {
        await this.fetchData();
    }
    async fetchData() {
        try {
            // TODO These two should probably be considated to 1 endpoint but this is fine for now
            const response = await fetch('/api/v1/courses');
            const data = await response.json();
            const perc_response = await fetch('/api/v1/percentages');
            const perc_data = await perc_response.json();
            this.render(data.response, perc_data.response);
        }
        catch (error) {
            this.render(['Error fetching data.'], []);
            console.error(error);
        }
    }
    render(courses, perc_data) {
        let text = '';
        if (!courses) {
            text = 'No courses available.';
        }
        else if (courses.length === 0) {
            text = 'No courses found.';
        }
        else {
            for (let i = 0; i < courses.length; i++) {
                text += `
                <div class="course-row">
                    <h2>
                        <a href=/${this.pascalToKebab(courses[i])} class="course-link">${courses[i]}</a>
                    </h2>
                    <p>${(perc_data[courses[i]]).toFixed(2)}% complete</p>
                </div>`;
            }
        }
        if (this.shadowRoot) {
            this.shadowRoot.innerHTML = `
            <style>
            .course-link {
                text-decoration: none;
                color: inherit;
            }
            .course-row {
                display: flex;
                align-items: center;
                width: 100%;
                justify-content: space-between;
            }
            </style>
            <h1>Assimil Scheduler</h1>
            ${text}
            <slot></slot>
            `;
        }
    }
    pascalToKebab(str) {
        return str.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();
    };
}
customElements.define('home-component', HomeComponent);