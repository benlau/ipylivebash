import React from "react";
import {createUseStyles} from "react-jss";

const useStyles = createUseStyles({
    container: {
        display: "flex",
        flexDirection: "row",
        justifyContent: "flex-start",
        alignItems: "center",
        height: "30px",
        backgroundColor: "#f5f5f57f",
        borderBottom: "1px solid #e0e0e0",
        "& button": {
            margin: "0 4px"
        }
    },
    message: {
        margin: "0 8px"
    }
}, { name: "ConfirmationDialog"});

export function useConfirmationDialog() {
    const [isVisible, setIsVisible] = React.useState(false);
    const [message, setMessage] = React.useState<string | undefined>(undefined);
    const [onYes, setOnYes] = React.useState<(() => void) | undefined>(undefined);
    const [onNo, setOnNo] = React.useState<(() => void) | undefined>(undefined);

    const show = React.useCallback(
        (message: string, onYes: () => void, onNo: () => void) => {
            setIsVisible(true);
            setMessage(message);
            setOnYes(() => {
                return onYes;
            });
            setOnNo(() => {
                return onNo;
            });
        }, [setIsVisible, setMessage, setOnYes, setOnNo]);

    const props = React.useMemo(() => {
        return {
            isVisible,
            message,
            setIsVisible,
            onYes,
            onNo
        }
    }, [isVisible,message, setIsVisible, onYes, onNo]);

    const methods = React.useMemo(() => {
        return {
            setIsVisible,
            show
        }
    }, [setIsVisible, show]);

    return React.useMemo(() => {
        return {props, methods};
    }, [props, methods]);
}

type Props = ReturnType<typeof useConfirmationDialog>["props"];

export function ConfirmationDialog(props: Props) {
    const classes = useStyles();
    const {
        isVisible,
        message,
        setIsVisible,
        onYes,
        onNo
    } = props;

    const onYesClick = React.useCallback(() => {
        setIsVisible(false);
        onYes?.();
    }, [onYes, setIsVisible]);

    const onNoClick = React.useCallback(() => {
        setIsVisible(false);
        onNo?.();
    }, [onNo, setIsVisible]);

    return (
        <>
            {
                isVisible && (
                    <div className={classes.container}>
                        <button onClick={onYesClick}>YES</button>
                        <button onClick={onNoClick}>NO</button>
                        <div className={classes.message}>{message}</div>
                    </div>
                )
            }
        </>
    )
}
