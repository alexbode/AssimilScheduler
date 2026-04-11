
class LanguageComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    async connectedCallback() {
        this.language = this.capitalCase(window.location.pathname.slice(1));
        console.log("Language path:", this.language);
        await this.fetchData();
    }

    click = async () => {
        console.log("Complete review button clicked");
        await this.completeReview();
        await this.fetchData()
    }

    async fetchData() {
        try {
            const response = await fetch(`/api/v1/next_review/${this.language.replace(" ", "")}`);
            const data = await response.json();
            this.render(data.response);
            console.log(data.response);
        } catch (error) {
            this.render('Error fetching data.');
            console.error(error);
        }
    }

    async completeReview() {
        const response = await fetch(`/api/v1/complete_review/${this.language.replace(" ", "")}`);
        const data = await response.json();
        console.log("complete review response:", data);
    }

    render(data) {
        this.shadowRoot.innerHTML = `
            <div class="cardchinese" style="background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
                <h1>${this.language}</h2>
                <div style="display: flex; flex-direction: row; justify-content: space-between;">
                    <h3>${data.lesson} ${data.review_type}</h3> 
                    <button id="review-complete-btn" type="button">Complete</button>
                </div>
            </div>
        `;
        this.shadowRoot.querySelector('#review-complete-btn').addEventListener('click', this.click);
    }

    capitalCase(str){
        return str.replace(/(^|-)\w/g, (match) => match.toUpperCase().replace("-", " "));
    }
}

customElements.define('language-component', LanguageComponent);