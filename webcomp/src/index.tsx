import React from "react"
import ReactDOM from "react-dom/client"
import { LiveBashPanel, useLiveBashPanel } from "./LiveBashPanel"
import {JssProvider, SheetsRegistry } from 'react-jss'

interface Delegate {
    methods?: ReturnType<typeof useLiveBashPanel>["methods"];
}

class SheetsRegistryWrapper {
    registry: any;
    setStyle: (style: string) => void;

    constructor(registry, setStyle) {
        this.registry = registry;
        this.setStyle = setStyle;
    }

    get index() {
        return this.registry.index;
    }

    add(...args) {
        this.registry.add(...args);
        this.setStyle(this.registry.toString());
    }

    remove(...args) {
        this.registry.remove(...args);
        this.setStyle(this.registry.toString());
    }

    reset(...args) {
        this.registry.reset(...args);
        this.setStyle(this.registry.toString());
    }

    toString() {
        return this.registry.toString();
    }

}

function useSheetRegistry() {
    const [style, setStyle] = React.useState("");
    const registry = React.useMemo(() => {
        const reg = new SheetsRegistry();
        const wrapper = new SheetsRegistryWrapper(reg, setStyle);
        return wrapper;
    }, []);

    return React.useMemo(() => {
        return {
            registry,
            style,
        }
    }, [registry, style]);
}

interface ControllerProps {
    delegate: Delegate,
    defaultHeightInLines: string | null,
}

function Controller(props: ControllerProps) {
    const {
        delegate,
        defaultHeightInLines
    } = props;

    const {
        props: liveBashPanelProps,
        methods: liveBashPanelMethods
    } = useLiveBashPanel();

    delegate.methods = liveBashPanelMethods;

    const {
        registry,
        style
    } = useSheetRegistry();

    React.useEffect(() => {
        if (defaultHeightInLines !== null) {
            liveBashPanelMethods.setHeightInLines(
                parseInt(defaultHeightInLines));
        }
    }, [defaultHeightInLines]);

    return (
        <>
            <style>{style}</style>
            <JssProvider registry={registry}>
                <LiveBashPanel {...liveBashPanelProps} />
            </JssProvider>
        </>
    )
}


class LiveBashPanelElm extends HTMLElement {
    delegate: Delegate;

    connectedCallback() {
        const mountPoint = document.createElement('span');

        const shadowRoot = this.attachShadow({ mode: 'open' });
        shadowRoot.appendChild(mountPoint);
        const root = ReactDOM.createRoot(mountPoint);
        const delegate: Delegate = {}
        this.delegate = delegate;
        const defaultHeightInLines = this.getAttribute("height-in-lines");

        root.render(
            <Controller
                defaultHeightInLines={defaultHeightInLines}
                delegate={delegate}
            />
        );
    }
    
    attachedListener(root) {
        for (const elm of root.querySelectorAll("ul li")) {
            elm.addEventListener("click", ({ target: { textContent } }) =>
                alert(`You have clicked on ${textContent}`)
            );
        }
    }
    
    attributeChangedCallback(name: string, oldValue: any, newValue: any) {
        if (name === "messages") {
            const messages = (newValue as string).split("\n").slice(1);
            this.delegate.methods?.log(messages.join("\n"));
        } else if (name === "status-header") {
            this.delegate.methods?.setStatusHeader(newValue as string);
        } else if (name === "status") {
            this.delegate.methods?.setStatus((newValue as string).split("\n"));
        } else if (name === "loading-spinner-running") {
            this.delegate.methods?.setIsLoadingSpinnerRunning(newValue === "true");
        } else if (name === "height-in-lines") {
            this.delegate.methods?.setHeightInLines(parseInt(newValue));
        }
    }

    static get observedAttributes() {
        return ["messages", "status-header", "status","loading-spinner-running", "height-in-lines"];
    }
}
    
if (!customElements.get("live-bash-panel")) {
    customElements.define("live-bash-panel", LiveBashPanelElm);
}
