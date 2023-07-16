import ReactDOM from "react-dom/client"
import { LiveBashPanel, useLiveBashPanelHandle } from "./LiveBashPanel";
import React from "react";


interface Delegate {
    methods?: ReturnType<typeof useLiveBashPanelHandle>["methods"];
    onEvent: (event: any) => void;
    onReady: () => void;
}

interface ControllerProps {
    delegate: Delegate;
}

function Controller(props: ControllerProps) {
    const {
        delegate,
    } = props;

    const {
        onEvent,
        onReady
    } = delegate

    const {
        props: liveBashPanelProps,
        methods: liveBashPanelMethods
    } = useLiveBashPanelHandle({onEvent});

    delegate.methods = liveBashPanelMethods;

    React.useEffect(() => {
        onReady?.();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <>
            <LiveBashPanel {...liveBashPanelProps} onEvent={onEvent}/>
        </>
    )
}


export class LiveBashPanelRenderer {

    dom: HTMLElement;
    delegate: Delegate;

    constructor(dom: HTMLElement, onEvent: (event: any) => void, onReady: () => void) {
        this.dom = dom;
        this.delegate = {
            onEvent,
            onReady,
        }
    }

    render() {
        const root = ReactDOM.createRoot(this.dom);
        return root.render(<Controller delegate={this.delegate}/>);
    }

    setAttribute(name: string, newValue:any) {
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
            this.delegate.methods.setIsRunning(newValue);
        } else if (name === "height-in-lines") {
            this.delegate.methods.setHeightInLines(parseInt(newValue));
        } else if (name === "action") {
            this.delegate.methods.sendAction(newValue);
        } else if (name === "confirmation-required") {
            this.delegate.methods.setConfirmationRequired(newValue);
        } else if (name === "script") {
            this.delegate.methods.setScript(newValue);
        } else if (name === "sessions") {
            this.delegate.methods.setSessions(newValue);
        } else if (name === "session-id") {
            this.delegate.methods.setSessionId(newValue)
        }
    }
}