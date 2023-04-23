import React from 'react';
import { createUseStyles } from 'react-jss'
import { LoadingSpinner } from './LoadingSpinner';
import { Toolbar }  from './Toolbar';
import { useConfirmationDialog, ConfirmationDialog } from './ConfirmationDialog';

enum ActionType {
    askRunConfirmation = "askRunConfirmation"
}

const useStyles = createUseStyles({
    container: {
    },
    textViewContainer: {
        "overflow-y": "auto",
    },
    textView: {
        padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
        },
        fontFamily: "monospace",
        whiteSpace: "pre-wrap",
        lineHeight: 1.2,
        '& p': {
            marginTop: 'unset',
            marginBottom: 'unset',
            wordWrap: "break-word",
            wordBreak: "break-all"
        }
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

export function useLiveBashPanel(defaults?: useLiveBashPanelDefaults) {
    const [messages, setMessages] = React.useState<string[]>([]);
    const [status, setStatus] = React.useState<string[]>([]);
    const [statusHeader, setStatusHeader] = React.useState<string>("");
    const [isRunning, setIsRunning] = React.useState<boolean>(false);
    const [heightInLines, setHeightInLines] = React.useState<number>(0);
    const [confirmationRequired, setConfirmationRequired] = React.useState<boolean>(false);

    const textViewcontainerRef = React.useRef<HTMLDivElement>(null);
    const textViewRef = React.useRef<HTMLDivElement>(null);
    const onEvent = defaults?.onEvent;

    const {
        props: confirmationDialogProps,
        methods: confirmationDialogMethods
    } = useConfirmationDialog();

    const mutableState = React.useRef({
        messages
    });

    const log = React.useCallback((message: string) => {
        mutableState.current.messages.push(message);
        setMessages([...mutableState.current.messages]);
    }, []);

    const askRunConfirmation = React.useCallback(() => {
        confirmationDialogMethods.show(
            "Are you sure you want to run this script?",
            () => {
                onEvent?.({type: "confirmToRun"});
            },() => {
                // do nothing
            });
    }, [confirmationDialogMethods, onEvent]);

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
        textViewcontainerRef,
        textViewRef,
        confirmationDialogProps,
        confirmationRequired,
        onEvent,
        askRunConfirmation
    }), [messages, status, statusHeader, isRunning, 
        heightInLines, textViewcontainerRef, textViewRef, confirmationDialogProps, onEvent,
        confirmationRequired, askRunConfirmation]);

    const methods = React.useMemo(() => ({
        log,
        setStatus,
        setStatusHeader,
        setIsRunning,
        setMessages,
        setHeightInLines,
        askRunConfirmation,
        sendAction,
        setConfirmationRequired
    }), [log, setStatus, setStatusHeader, setIsRunning,
        setMessages, setHeightInLines, askRunConfirmation, sendAction
        , setConfirmationRequired]);

    return React.useMemo(() => ({
        props,
        methods
    }), [
        props,
        methods
    ])
}

type Props = ReturnType<typeof useLiveBashPanel>["props"]

export function LiveBashPanel(props: Props) {
    const {
        messages,
        status,
        statusHeader,
        isRunning,
        heightInLines,
        textViewcontainerRef,
        textViewRef,
        onEvent,
        confirmationDialogProps,
        confirmationRequired,
        askRunConfirmation
    } = props;
    const classes = useStyles();

    const maxHeight = heightInLines > 0 ? heightInLines * 1.2 + "em" : undefined;

    React.useEffect(() => {
        // scroll to end
        if (textViewcontainerRef.current && textViewRef.current) {
            textViewcontainerRef.current.scrollTop = textViewRef.current.scrollHeight;
        }
    }, [messages, textViewRef, textViewcontainerRef]);

    React.useEffect(() => {
        if (!confirmationRequired) {
            return;
        }
        askRunConfirmation();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [confirmationRequired]);

    const onStopClicked = React.useCallback(() => {
        onEvent?.({
            type: "requestToStop",
        });
    }, [onEvent]);

    return (
        <div className={classes.container}>
            <Toolbar isRunning={isRunning} onStopClick={onStopClicked}/>
            <ConfirmationDialog {...confirmationDialogProps}/>
            <LoadingSpinner isRunning={isRunning}/>
            <div style={{maxHeight}} className={classes.textViewContainer} ref={textViewcontainerRef}>
                <div className={classes.textView} ref={textViewRef}>
                    <>
                        {
                    messages?.map((message, index) => (
                        <p key={`msg-${index}`}>{message}</p>
                    )) ?? ""
                        }
                    </>
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
                </div>

            </div>
        </div>
    );
}

