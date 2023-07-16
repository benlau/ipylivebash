import React from 'react';
import {createUseStyles} from "react-jss";
import {Session} from "./types";

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
        fontSize: '10px',
        padding: "2px",

    },
    row: {
        display: "contents",
        fontSize: '10px',
        lineHeight: '20px',
        "& > div": {
            padding: "2px",
            backgroundColor: '#fff',    
        },
        "&:hover > div": {
            padding: "2px",
            backgroundColor: '#ffffff1f',
        },
    },
    activeRow: {
        display: "contents",
        fontSize: '10px',
        lineHeight: '20px',
        "& > div": {
            padding: "2px",
            backgroundColor: '#d9f4d7',
        },
        "&:hover > div": {
            backgroundColor: '#d9f4d77f',
        }
    }
},
{name: "SessionTable"}
);

interface RowProps {
    id: string;
    state: string;
    isActive: boolean;
}

function Row(props: RowProps) {
    const {
        id,
        state,
        isActive
    } = props;

    const classes = useStyles();

    const className = isActive ? classes.activeRow : classes.row;

    return (
        <div className={className}>
            <div> {id} </div>
            <div> {state} </div>
        </div>
    )
}

interface SessionTableProps {
    activeSessionId?: string;
    rows: Session[];
}

export function SessionTable(props: SessionTableProps) {
    const {
        rows,
        activeSessionId
    } = props;
    const classes = useStyles();

    return (
        <div className={classes.container}>
            <div className={classes.table}>
                <div className={classes.header}> ID </div>
                <div className={classes.header}> State </div>
                {rows.map((row, index) => {
                    return (
                        <Row key={`row-${index}`} id={row.id} state={row.state} isActive={row.id === activeSessionId}/>
                    )})}
            </div>
        </div>
    )

}