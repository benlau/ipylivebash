import React from "react";
import {createUseStyles} from "react-jss";

const useStyles = createUseStyles({
    container: {
        "overflow-y": "auto",
    },
}, {name: "ScrollablePane"});

interface HandleArgs {
    height?: string;
}

export function useScrollablePaneHandle(args: HandleArgs) {
    const {
        height
    } = args;

    const containerRef = React.useRef<HTMLDivElement>(null);
    const childRef = React.useRef<HTMLDivElement>(null);

    const scrollToEnd = React.useCallback(() => {
        if (!containerRef.current || !childRef.current) {
            return;
        }
        containerRef.current.scrollTop = childRef.current?.scrollHeight;
    }, [containerRef, childRef]);

    const containerStyle = React.useMemo(() => ({
        height
    }), [height]);

    const props = React.useMemo(() => ({
        containerStyle,
        containerRef,
        childRef
    }), [containerRef, childRef, containerStyle]);

    const methods = React.useMemo(() => ({
        scrollToEnd
    }), [scrollToEnd]);

    return React.useMemo(() => ({
        props, methods
    }), [props, methods]);
}

type ScrollablePaneProps = {
    children: React.ReactNode
} & ReturnType<typeof useScrollablePaneHandle>["props"];

export function ScrollablePane(props: ScrollablePaneProps) {
    const {
        children,
        containerRef,
        childRef,
        containerStyle
    } = props;
    const classes = useStyles();

    return (
        <div style={containerStyle} className={classes.container} ref={containerRef}>
            <div ref={childRef}>
                {children}
            </div>
        </div>
    )
}