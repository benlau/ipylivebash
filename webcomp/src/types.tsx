
export enum Page {
    TerminalPage,
    CodePage,
    SessionPage
}

export interface Session {
    id: string;
    state: string;
}

export enum SessionState {
    Running = "Running",
}

export enum EventType {
    RequestToKill = "RequestToKill",
    ConfirmedToRun = "ConfirmedToRun",
    CancelledToRun = "CancelledToRun"
}