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
            const response = await fetch('/api/v1/courses');
            const data = await response.json();
            this.render(data.response);
        } catch (error) {
            this.render('Error fetching data.');
            console.error(error);
        }
    }

    render(courses) {
        let text = '';
        for (let i = 0; i < courses.length; i++) {
            text += `<h2><a href=/${this.pascalToKebab(courses[i])} style="text-decoration: none; color: inherit;">${courses[i]}</a></h1>`;
        }
        this.shadowRoot.innerHTML = `
            <div class="card">
                <h1>Assimil Scheduler</h2>
                ${text}
            </div>
        `;
    }

    pascalToKebab(str) {
        return str.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();                     
};
}

customElements.define('home-component', HomeComponent);