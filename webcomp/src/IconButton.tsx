import React from "react";
import { createUseStyles } from "react-jss";

const useStyles = createUseStyles({
    container: {
        width: 24,
        height: 24,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: 4,
        cursor: "pointer",
        userSelect: "none",
        "&:hover" : {
            backgroundColor: "#ffe7e7",
            color: "#a4262c"
        },
        "&:active": {
            backgroundColor: "#ffe7e77f",
            color: "#a4262c"
        }
    },
}, {name: "IconButton"});

export function IconButton(props: {
    icon: any;
    onClick: () => void;
}) {
    const classes = useStyles();

    const src = React.useMemo(() => {
        return "data:image/svg+xml;charset=utf8," + encodeURIComponent(props.icon);
    }, [props.icon])

    const callback = React.useCallback(
        (ev: React.MouseEvent<HTMLDivElement>) => {
            ev.stopPropagation();
            props.onClick();
        },
        [props]
    );

    return (
        <div
            className={classes.container}
            onClick={callback}
        >
            <img src={src} alt="" width={12} height={12} />
        </div>
    );
}