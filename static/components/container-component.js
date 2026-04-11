import sharedStyles from '../css/shared.css' with { type: 'css' };

class ContainerComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.render();
    }

    async connectedCallback() {};

    render() {
        this.shadowRoot.innerHTML = `
            <div class="grid-container">
                <div class="center-cell">
                    <slot></slot>
                </div>
            </div>
        `;
        this.shadowRoot.adoptedStyleSheets = [sharedStyles];
    }
}

customElements.define('container-component', ContainerComponent);