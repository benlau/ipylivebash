import React from "react";
import stopIcon from "./assets/stop-solid.svg";
import {IconButton} from "./IconButton";
import {createUseStyles} from "react-jss";

const useStyles = createUseStyles({
    container: {
        display: "flex",
        flexDirection: "row",
        justifyContent: "flex-start",
        alignItems: "center",
        height: "30px",
        backgroundColor: "#f5f5f5",
        borderBottom: "1px solid #e0e0e0",
    },
});

interface Props {
    isRunning: boolean;
    onStopClick: () => void;
}

export function Toolbar(props: Props) {
    const classes = useStyles();
    const {isRunning, onStopClick} = props;

    return (
        <div className={classes.container}>
            <IconButton icon={stopIcon} onClick={onStopClick} isDisabled={!isRunning}/>
        </div>
    )
}
