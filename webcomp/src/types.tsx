
export enum Page {
    TerminalPage,
    CodePage,
    SessionPage
}

export interface Session {
    id: string;
    state: string;
}