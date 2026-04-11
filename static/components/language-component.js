
class LanguageComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    async connectedCallback() {
        this.language = this.capitalCase(window.location.pathname.slice(1));
        await this.fetchData();
    }

    async fetchData() {
        try {
            const response = await fetch(`/api/v1/next_review/${this.language.replace(" ", "")}`);
            const data = await response.json();
            this.render(data.response);
        } catch (error) {
            this.render('Error fetching data.');
            console.error(error);
        }
    }

    async completeReview() {
        const response = await fetch(`/api/v1/complete_review/${this.language.replace(" ", "")}`);
        const data = await response.json();
        console.log(data);
    }

    async undoReview() {
        const response = await fetch(`/api/v1/undo_review/${this.language.replace(" ", "")}`);
        const data = await response.json();
        console.log(data);
    }

    render(data) {
        this.shadowRoot.innerHTML = `
            <h1>${this.language}</h1>
            <slot></slot>
            <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: center;">
                <div>
                    <h5>Lesson Number: ${data.lesson}</h5> 
                    <h5>Review Type: ${data.review_type}</h5> 
                </div>
                <div>
                    <button id="review-complete-btn">Next Review</button>
                    <button id="review-undo-btn">Previous Review</button>
                </div>
            </div>
        `;
        this.shadowRoot.querySelector('#review-complete-btn').addEventListener('click', async () => {
            await this.completeReview();
            await this.fetchData();
        });
        this.shadowRoot.querySelector('#review-undo-btn').addEventListener('click', async () => {
            await this.undoReview();
            await this.fetchData();
        });
    }

    capitalCase(str){
        return str.replace(/(^|-)\w/g, (match) => match.toUpperCase().replace("-", " "));
    }
}

customElements.define('language-component', LanguageComponent);