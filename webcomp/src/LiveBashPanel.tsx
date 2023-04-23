import React from 'react';
import {createUseStyles} from 'react-jss'
import { LoadingSpinner } from './LoadingSpinner';
import { Toolbar }  from './Toolbar';

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

export function useLiveBashPanel() {
    const [messages, setMessages] = React.useState<string[]>([]);
    const [status, setStatus] = React.useState<string[]>([]);
    const [statusHeader, setStatusHeader] = React.useState<string>("");
    const [isRunning, setIsRunning] = React.useState<boolean>(false);
    const [heightInLines, setHeightInLines] = React.useState<number>(0);
    const textViewcontainerRef = React.useRef<HTMLDivElement>(null);
    const textViewRef = React.useRef<HTMLDivElement>(null);

    const mutableState = React.useRef({
        messages
    });

    const log = React.useCallback((message: string) => {
        mutableState.current.messages.push(message);
        setMessages([...mutableState.current.messages]);
    }, []);

    const props = React.useMemo(() => ({
        messages,
        status,
        statusHeader,
        isRunning,
        heightInLines,
        textViewcontainerRef,
        textViewRef,
    }), [messages, status, statusHeader, isRunning, heightInLines, textViewcontainerRef, textViewRef]);

    const methods = React.useMemo(() => ({
        log,
        setStatus,
        setStatusHeader,
        setIsRunning,
        setMessages,
        setHeightInLines
    }), [log, setStatus, setStatusHeader, setIsRunning,
        setMessages, setHeightInLines]);

    return React.useMemo(() => ({
        props,
        methods
    }), [
        props,
        methods
    ])
}

type Props = ReturnType<typeof useLiveBashPanel>["props"] & {
    onEvent?: (event: any) => void,
};

export function LiveBashPanel(props: Props) {
    const {
        messages,
        status,
        statusHeader,
        isRunning,
        heightInLines,
        textViewcontainerRef,
        textViewRef,
        onEvent
    } = props;
    const classes = useStyles();

    const maxHeight = heightInLines > 0 ? heightInLines * 1.2 + "em" : undefined;

    React.useEffect(() => {
        // scroll to end
        if (textViewcontainerRef.current && textViewRef.current) {
            textViewcontainerRef.current.scrollTop = textViewRef.current.scrollHeight;
        }
    }, [messages]);

    const onStopClicked = React.useCallback(() => {
        onEvent?.({
            type: "requestStop",
        });
    }, [onEvent]);

    return (
        <div className={classes.container}>
            <Toolbar isRunning={isRunning} onStopClick={onStopClicked}/>
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

