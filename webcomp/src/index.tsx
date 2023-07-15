import React from "react"
import ReactDOM from "react-dom/client"
import { LiveBashPanel, useLiveBashPanelHandle } from "./LiveBashPanel"
import {JssProvider, SheetsRegistry } from "react-jss"
import {LiveBashPanelRenderer as _LiveBashPanelRenderer} from "./LiveBashPanelRenderer";

export const LiveBashPanelRenderer = _LiveBashPanelRenderer;

interface Delegate {
    methods?: ReturnType<typeof useLiveBashPanelHandle>["methods"];
    onReady: () => void;
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
        this.setStyle(this.toString());
    }

    remove(...args) {
        this.registry.remove(...args);
        this.setStyle(this.toString());
    }

    reset(...args) {
        this.registry.reset(...args);
        this.setStyle(this.toString());
    }

    toString() {
        return this.registry.toString({attached: true});
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
    shadowRoot: ShadowRoot;
    delegate: Delegate,
}

function Controller(props: ControllerProps) {
    const {
        delegate,
        shadowRoot
    } = props;

    const onEvent = React.useCallback((event: any) => {
        shadowRoot.dispatchEvent(new CustomEvent('response', {
            detail: event,
            bubbles: true, 
            composed: true
        }));
    }, [shadowRoot]);

    const {
        props: liveBashPanelProps,
        methods: liveBashPanelMethods
    } = useLiveBashPanelHandle({onEvent});

    delegate.methods = liveBashPanelMethods;

    const {
        registry,
        style,
    } = useSheetRegistry();

    React.useEffect(() => {
        delegate.onReady();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <>
            <style>{style}</style>
            <JssProvider registry={registry}>
                <LiveBashPanel {...liveBashPanelProps} onEvent={onEvent}/>
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
        const delegate = {
            onReady: () => {
                const isRunning = this.getAttribute("is-running") === "true";
                const heightInLines = parseInt(this.getAttribute("height-in-lines") || "0");
                const confirmationRequired = this.getAttribute("confirmation-required");
                const {
                    methods
                } = delegate as Delegate;

                methods?.setIsRunning(isRunning);
                methods?.setHeightInLines(heightInLines);
                methods?.setConfirmationRequired(confirmationRequired === "true");
            }
        };

        this.delegate = delegate as Delegate;

        root.render(
            <Controller
                shadowRoot={shadowRoot}
                delegate={this.delegate}
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
        if (this.delegate === undefined || this.delegate.methods === undefined) {
            return;
        }

        if (name === "messages") {
            const messages = newValue;
            this.delegate.methods.log(messages.split("\n").slice(1).join("\n"));
        } else if (name === "status-header") {
            this.delegate.methods.setStatusHeader(newValue as string);
        } else if (name === "status") {
            this.delegate.methods.setStatus((newValue as string).split("\n"));
        } else if (name === "is-running") {
            this.delegate.methods.setIsRunning(newValue === "true");
        } else if (name === "height-in-lines") {
            this.delegate.methods.setHeightInLines(parseInt(newValue));
        } else if (name === "action") {
            this.delegate.methods.sendAction(newValue);
        } else if (name === "confirmation-required") {
            this.delegate.methods.setConfirmationRequired(newValue === "true");
        }
    }

    static get observedAttributes() {
        return ["messages", 
            "status-header", 
            "status","is-running", "height-in-lines", 
            "action", "confirmation-required"];
    }
}
    
if (!customElements.get("live-bash-panel")) {
    customElements.define("live-bash-panel", LiveBashPanelElm);
}
