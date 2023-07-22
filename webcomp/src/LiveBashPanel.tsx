import React from 'react';
import { createUseStyles } from 'react-jss'
import { LoadingSpinner } from './LoadingSpinner';
import { Toolbar }  from './Toolbar';
import { useConfirmationDialog, ConfirmationDialog } from './ConfirmationDialog';
import { ScrollablePane, useScrollablePaneHandle } from './ScrollablePane';
import { EventType, Page, Session } from "./types";
import { TextView } from "./TextView";
import { SessionTable} from "./SessionTable";

enum ActionType {
    askRunConfirmation = "askRunConfirmation"
}

const useStyles = createUseStyles({
    container: {
    },
    statusHeader: {
        padding: {
            left: 0,
            right: 0,
            top: 8,
            bottom: 8
        }
    }
}, {name: "LiveBashPanel"});

interface useLiveBashPanelDefaults {
    onEvent?: (event: any) => void;
}

export function useLiveBashPanelHandle(defaultValues?: useLiveBashPanelDefaults) {
    const [messages, setMessages] = React.useState<string[]>([]);
    const [status, setStatus] = React.useState<string[]>([]);
    const [statusHeader, setStatusHeader] = React.useState<string>("");
    const [isRunning, setIsRunning] = React.useState<boolean>(false);
    const [heightInLines, setHeightInLines] = React.useState<number>(0);
    const [confirmationRequired, setConfirmationRequired] = React.useState<boolean>(false);
    const [script, setScript] = React.useState<string>("");
    const [page, setPage] = React.useState<Page>(Page.TerminalPage);
    const [sessions, setSessions] = React.useState<Session[]>([]);
    const [sessionId, setSessionId] = React.useState<string>("");

    const onEvent = defaultValues?.onEvent;

    const {
        props: confirmationDialogProps,
        methods: confirmationDialogMethods
    } = useConfirmationDialog();

    const mutableState = React.useRef({
        messages,
        lastTotalLines: 0
    });

    const log = React.useCallback((message: string) => {
        mutableState.current.messages.push(message);
        setMessages([...mutableState.current.messages]);
    }, []);

    const clear = React.useCallback(() => {
        mutableState.current.messages = [];
        setMessages([]);
        setStatusHeader("");
        setStatus([]);
    }, [mutableState, setMessages, setStatusHeader, setStatus]);

    const killSession = React.useCallback((targetSessionId: string) => {
        onEvent?.({type: EventType.RequestToKill,
            target_session_id: targetSessionId});
    }, [onEvent]);

    const killActiveSession = React.useCallback(() => {
        killSession(sessionId);
    }, [sessionId, killSession]);

    const askRunConfirmation = React.useCallback(() => {
        confirmationDialogMethods.show(
            "Are you sure you want to run this script?",
            () => {
                clear();
                onEvent?.({type: EventType.ConfirmedToRun});
            },() => {
                onEvent?.({type: EventType.CancelledToRun});
                log("Cancelled");
            });
    }, [confirmationDialogMethods, onEvent, clear, log]);

    const sendAction = React.useCallback((action: string) => {
        const {
            content
        } = JSON.parse(action);

        const {
            type
        } = JSON.parse(content);

        if (type === ActionType.askRunConfirmation) {
            askRunConfirmation();
        }
    }, [askRunConfirmation]);

    const props = React.useMemo(() => ({
        messages,
        status,
        statusHeader,
        isRunning,
        heightInLines,
        confirmationDialogProps,
        confirmationRequired,
        onEvent,
        askRunConfirmation,
        clear,
        mutableState,
        page,
        setPage,
        script,
        sessions,
        sessionId,
        killActiveSession,
        killSession
    }), [messages, status, statusHeader, isRunning, 
        heightInLines,
        confirmationDialogProps, onEvent,
        confirmationRequired, askRunConfirmation, clear,
        mutableState, 
        page, 
        setPage,
        sessions,
        sessionId,
        killActiveSession,
        killSession,
        script]);

    const methods = React.useMemo(() => ({
        log,
        setStatus,
        setStatusHeader,
        setIsRunning,
        setMessages,
        setHeightInLines,
        askRunConfirmation,
        sendAction,
        setConfirmationRequired,
        clear,
        setScript,
        setSessions,
        setSessionId
    }), [log, setStatus, setStatusHeader, setIsRunning,
        setMessages, setHeightInLines, askRunConfirmation, sendAction
        , setConfirmationRequired, clear, setScript, setSessions, setSessionId]);

    return React.useMemo(() => ({
        props,
        methods
    }), [
        props,
        methods
    ])
}

type Props = ReturnType<typeof useLiveBashPanelHandle>["props"]

export function LiveBashPanel(props: Props) {
    const {
        messages,
        status,
        statusHeader,
        isRunning,
        heightInLines,
        confirmationDialogProps,
        confirmationRequired,
        askRunConfirmation,
        mutableState,
        page,
        setPage,
        script,
        sessions,
        sessionId,
        killActiveSession,
        killSession
    } = props;
    const classes = useStyles();

    const textViewHeight = heightInLines > 0 ? heightInLines * 1.2 + "em" : undefined;

    const terminalOutputHandle = useScrollablePaneHandle({
        height: textViewHeight
    });

    React.useEffect(() => {
        // auto scroll to end
        const totalLines = (messages?.length ?? 0) + (status?.length ?? 0);
        if (totalLines > mutableState.current.lastTotalLines) {
            terminalOutputHandle.methods.scrollToEnd();
            mutableState.current.lastTotalLines = totalLines;
        }
    }, [messages, status, mutableState, terminalOutputHandle.methods]);

    React.useEffect(() => {
        if (!confirmationRequired) {
            return;
        }
        askRunConfirmation();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [confirmationRequired]);

    const onStopClicked = React.useCallback(() => {
        killActiveSession();
    }, [killActiveSession]);


    return (
        <div className={classes.container}>
            <Toolbar isRunning={isRunning} onStopClick={onStopClicked} page={page} setPage={setPage}/>
            {
                page === Page.TerminalPage && (
                    <ConfirmationDialog {...confirmationDialogProps}/>
                )
            }
            <LoadingSpinner isRunning={isRunning}/>
            <ScrollablePane {...terminalOutputHandle.props} key={page}>
                {                    
                    page === Page.TerminalPage ? (
                        <TextView key={page}>
                            <>
                                {
                                    messages?.map((message, index) => (
                                        <p key={`msg-${index}`}>{message}</p>
                                    )) ?? ""
                                }
                                {
                                    statusHeader && (
                                        <div className={classes.statusHeader}>{statusHeader}</div>
                                    )
                                }
                                {
                                    status?.map((message, index) => (
                                        <p key={`status-${index}`}>{message}</p>
                                    )) ?? ""
                                }
                            </>
                        </TextView>
                    ): page === Page.CodePage ? (
                        <TextView key={page}>
                            <>
                                {script}
                            </>
                        </TextView>
                    ): page === Page.SessionPage ? (
                        <SessionTable rows={sessions} activeSessionId={sessionId}
                            killSession={killSession}/>
                    ): null
                }
            </ScrollablePane>
        </div>
    );
}

