
export enum Page {
    TerminalPage,
    CodePage,
    SessionPage
}

export interface Session {
    id: string;
    state: string;
}

export enum EventType {
    RequestToStop = "RequestToStop",
    ConfirmedToRun = "ConfirmedToRun",
    CancelledToRun = "CancelledToRun"
}