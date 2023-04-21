import React from 'react';
import {createUseStyles} from 'react-jss'

const useStyles = createUseStyles({
    "background": {
        "height": "4px",
        "width": "100%",
        "margin-bottom": "4px"
    },
    "linearActivity": {
        "overflow": "hidden",
        "width": "100%",
        "height": "4px",
        "backgroundColor": "#cccccccc",
        "margin-bottom": "4px"
    },
    "determinate": {
        "position": "relative",
        "maxWidth": "100%",
        "height": "100%",
        "webkitTransition": "width 500ms ease-out 1s",
        "mozTransition": "width 500ms ease-out 1s",
        "oTransition": "width 500ms ease-out 1s",
        "transition": "width 500ms ease-out 1s",
        "backgroundColor": "#03A9F4"
    },
    "indeterminate": {
        "position": "relative",
        "width": "100%",
        "height": "100%",
        "&:before": {
            "content": "''",
            "position": "absolute",
            "height": "100%",
            "backgroundColor": "#0000007f",
            "animation": "$indeterminate_first 1.5s infinite ease-out"    
        },
        "&:after": {
            "content": "''",
            "position": "absolute",
            "height": "100%",
            "backgroundColor": "#00000050",
            "animation": "$indeterminate_second 1.5s infinite ease-in"    
        }
    },
    "@keyframes indeterminate_first": {
        "0%": {
            "left": "-100%",
            "width": "100%"
        },
        "100%": {
            "left": "100%",
            "width": "10%"
        }
    },
    "@keyframes indeterminate_second": {
        "0%": {
            "left": "-150%",
            "width": "100%"
        },
        "100%": {
            "left": "100%",
            "width": "10%"
        }
    }
});

interface Props {
    isRunning: boolean;
}

export function LoadingSpinner(props: Props) {
    const {
        isRunning,
    } = props;
    const classes = useStyles();

    return (
        <>
            {
                isRunning && (
                    <div className={classes.linearActivity}>
                        <div className={classes.indeterminate}></div>
                    </div>
                )
            }
            {
                !isRunning && (
                    <div className={classes.background}></div>
                )
            }        
        </>
    )
}

