class ContainerComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.render();
    }

    async connectedCallback() {};

    render() {
        this.shadowRoot.innerHTML = `
        <style>
        div.grid-container {
            height: 100vh;
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 12fr) minmax(0, 1fr);
            grid-template-rows: minmax(0, 1fr) minmax(0, 12fr) minmax(0, 1fr);
            background-color: var(--bg-color-3);
        }

        div.center-cell {
            grid-column: 2;
            grid-row: 2;
            background-color: var(--bg-color-2);
            color: var(--text-color-3);
            border-radius: 8px;
            padding: 1rem;
            overflow: scroll;
            scrollbar-width: none;
        }

        .div.center-cell::-webkit-scrollbar {
            display: none;
        }
        </style>
        <div class="grid-container">
            <div class="center-cell">
                <slot></slot>
            </div>
        </div>
        `;
    }
}

customElements.define('container-component', ContainerComponent);