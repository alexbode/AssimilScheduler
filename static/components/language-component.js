class LanguageComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.language = this.capitalCase(window.location.pathname.slice(1));
    }

    async connectedCallback() {
        await this.render({lesson: 0, review_type: 'N/A'});
        await this.fetchData();
    }

    async fetchData() {
        try {
            const response = await fetch(`/api/v1/next_review/${this.language.replace(" ", "")}`);
            const data = await response.json();
            this.render(data.response);
        } catch (error) {
            this.render({});
            console.error(error);
        }
    }

    async completeReview() {
        const response = await fetch(`/api/v1/complete_review/${this.language.replace(" ", "")}`);
        const data = await response.json();
    }

    async undoReview() {
        const response = await fetch(`/api/v1/undo_review/${this.language.replace(" ", "").toLowerCase()}`);
        const data = await response.json();
    }

    async render(data) {
        const percentComplete = data.percent_complete ? `${data.percent_complete.toFixed(2)}` : 'N/A';
        const lessonNumber = data.lesson ? `${data.lesson}` : 'N/A';
        const reviewType = data.review_type ? `${data.review_type}` : 'N/A';
        const reviewCount = data.review_count ? `${data.review_count}` : 'N/A';
        const totalReviewCount = data.total_review_count ? `${data.total_review_count}` : 'N/A';
        const previousReviewsCompleted = data.previous_reviews_completed ? `${data.previous_reviews_completed}` : 'N/A';
        const previousLessonReviewsCompleted = data.previous_lesson_reviews_completed ? `${data.previous_lesson_reviews_completed}` : 'N/A';
        this.shadowRoot.innerHTML = `
        <style>
        .review-info {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
        }
        #review-complete-btn, #review-undo-btn {
            cursor: pointer;
        }
        </style>
        <h1>${this.language}</h1>
        <slot name="timer"></slot>
        <div class="review-info">
            <div>
                <h5>Lesson Number: ${lessonNumber}</h5> 
                <h5>Review Type: ${reviewType}</h5> 
                <p>Review ${reviewCount} of ${totalReviewCount} (${percentComplete} % complete) | Review count: ${previousReviewsCompleted} | Lesson count: ${previousLessonReviewsCompleted}</p>
            </div>
            <div>
                <button id="review-complete-btn">Next Review</button>
                <button id="review-undo-btn">Previous Review</button>
            </div>
        </div>
        <slot name="wave"></slot>
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