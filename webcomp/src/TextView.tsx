import React from "react";
import { createUseStyles } from 'react-jss'

interface TextViewProps {
    children: React.ReactNode
}

const useStyles = createUseStyles({
    container: {
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
});

export function TextView(props: TextViewProps) {
    const {
        children
    } = props;
    const classes = useStyles();

    return (
        <div className={classes.container}>
            {children}
        </div>
    )
}