import React from "react";
import { createUseStyles } from "react-jss";

const useStyles = createUseStyles({
    container: {
        width: 24,
        height: 24,
        position: "relative",
        borderRadius: 4,
        cursor: "pointer",
        userSelect: "none",
        "&:hover" : {
            backgroundColor: "#e7e7e7",
            color: "#a4262c"
        },
        "&:active": {
            backgroundColor: "#e7e7e77f",
            color: "#a4262c"
        },
        "&[disabled]": {
            pointerEvents: "none",
            opacity: 0.5,
        },
        "& img": {
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
        },
    },
    selectedBar: {
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height: 2,
        opacity: 1,
        margin: "0px 2px",
        backgroundColor: "#000",
        zIndex: 1,
    }
}, {name: "IconButton"});

export function IconButton(props: {
    icon: any;
    isDisabled?: boolean;
    isSelected?: boolean;
    onClick?: () => void;
}) {
    const classes = useStyles();

    const src = React.useMemo(() => {
        return "data:image/svg+xml;charset=utf8," + encodeURIComponent(props.icon);
    }, [props.icon])

    const callback = React.useCallback(
        (ev: React.MouseEvent<HTMLDivElement>) => {
            if (props.isDisabled) {
                return;
            }
            ev.stopPropagation();
            props?.onClick();
        },
        [props]
    );

    const isSelected = props.isSelected ?? false;

    return (
        <div
            className={classes.container}
            onClick={callback}
            disabled={props.isDisabled ?? false}
        >
            <img src={src} alt="" width={12} height={12} />
            {
                isSelected && (<div className={classes.selectedBar}></div>)
            }
        </div>
    );
}