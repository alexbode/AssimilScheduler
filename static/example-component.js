class DataFetcher extends HTMLElement {
    constructor() {
        super();
        // Attach a shadow DOM tree to this instance
        this.attachShadow({ mode: 'open' });
    }

    // Called when the element is added to the document
    async connectedCallback() {
        this.render('Loading...');
        await this.fetchData();
    }

    async fetchData() {
        try {
            // Call the FastAPI endpoint
            const response = await fetch('/api/v1/message');
            const data = await response.json();
            
            // Render the returned data
            this.render(data.message);
        } catch (error) {
            this.render('Error fetching data.');
            console.error(error);
        }
    }

    render(text) {
        // Update the Shadow DOM's HTML
        this.shadowRoot.innerHTML = `
            <style>
                .card {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    text-align: center;
                }
                h2 { color: #333; }
                p { color: #009688; font-weight: bold; }
            </style>
            
            <div class="card">
                <h2>Web Component</h2>
                <p>${text}</p>
            </div>
        `;
    }
}

// Register the custom element with the browser
customElements.define('data-fetcher', DataFetcher);