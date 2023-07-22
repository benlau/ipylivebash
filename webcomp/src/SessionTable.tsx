import React from 'react';
import {createUseStyles} from "react-jss";
import {Session, SessionState} from "./types";
import stopIcon from "./assets/stop-solid.svg";
import {IconButton} from "./IconButton";

const useStyles = createUseStyles({
    container: {
        display: 'block',
        padding: "4px"
    },
    table: {
        display: 'grid',
        gap: '1px',
        backgroundColor: '#d3d3d3',
        gridTemplateColumns: 'auto 2fr',
        border: '1px solid #d3d3d3',
    },
    header: {
        backgroundColor: '#edebe9',
        fontWeight: 600,
        fontSize: '14px',
        padding: "4px 8px",

    },
    row: {
        display: "contents",
        fontSize: '14px',
        lineHeight: '20px',
        "& > div": {
            padding: "4px 4px",
            backgroundColor: '#fff',    
        },
        "&:hover > div": {
            backgroundColor: '#ffffff1f',
        },
    },
    activeRow: {
        display: "contents",
        fontSize: '14px',
        lineHeight: '20px',
        "& > div": {
            padding: "4px 4px",
            backgroundColor: '#d9f4d7',
        },
        "&:hover > div": {
            backgroundColor: '#d9f4d77f',
        }
    },
    spaceBetween: {
        display: "flex",
        justifyContent: "space-between",
        flexDisplay: "row"
    }
},
{name: "SessionTable"}
);

interface RowProps {
    id: string;
    state: string;
    isActive: boolean;
    killSession: (sessionId: string) => void;
}

function Row(props: RowProps) {
    const {
        id,
        state,
        isActive,
        killSession
    } = props;

    const classes = useStyles();

    const className = isActive ? classes.activeRow : classes.row;
    const onClick= React.useCallback(() => {
        killSession(id);
    }, [id, killSession]);

    return (
        <div className={className}>
            <div> {id} </div>
            <div className={classes.spaceBetween}> 
                <div>{state}</div>
                {
                    state === SessionState.Running && (
                        <div> <IconButton icon={stopIcon} onClick={onClick}/> </div>
                    )
                }
            </div>
        </div>
    )
}

interface SessionTableProps {
    activeSessionId?: string;
    rows: Session[];
    killSession: (sessionId: string) => void;
}

export function SessionTable(props: SessionTableProps) {
    const {
        rows,
        activeSessionId,
        killSession
    } = props;
    const classes = useStyles();

    return (
        <div className={classes.container}>
            <div className={classes.table}>
                <div className={classes.header}> ID </div>
                <div className={classes.header}> State </div>
                {rows.map((row, index) => {
                    return (
                        <Row key={`row-${index}`} id={row.id} state={row.state} isActive={row.id === activeSessionId}
                            killSession={killSession}/>
                    )})}
            </div>
        </div>
    )

}