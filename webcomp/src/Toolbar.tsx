import React from "react";
import stopIcon from "./assets/stop-solid.svg";
import codeIcon from "./assets/code-solid.svg";
import terminalIcon from "./assets/terminal-solid.svg";
import listIcon from "./assets/list-solid.svg";

import {IconButton} from "./IconButton";
import {createUseStyles} from "react-jss";
import { Page } from "./types";

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
    page: Page,
    setPage: (page: Page) => void;
}

export function Toolbar(props: Props) {
    const classes = useStyles();
    const {isRunning, onStopClick, page, setPage} = props;

    const onTerminalClick = React.useCallback(() => {
        setPage(Page.TerminalPage);
    }, [setPage]);

    const onCodeClick = React.useCallback(() => {
        setPage(Page.CodePage);
    }, [setPage]);

    const onSessionClick = React.useCallback(() => {
        setPage(Page.SessionPage);
    }, [setPage]);

    return (
        <div className={classes.container}>
            <IconButton icon={stopIcon} onClick={onStopClick} isDisabled={!isRunning}/>
            <IconButton icon={terminalIcon} isSelected={page === Page.TerminalPage} onClick={onTerminalClick} />
            <IconButton icon={codeIcon} isSelected={page === Page.CodePage} onClick={onCodeClick}/>
            <IconButton icon={listIcon} isSelected={page === Page.SessionPage} onClick={onSessionClick}/>
        </div>
    )
}
