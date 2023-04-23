import { Toolbar } from '../../src/Toolbar';
import React from 'react';
import stopIcon from "../../src/assets/stop-solid.svg";

export default {
    title: 'Toolbar',
    component: Toolbar,
    tags: ['autodocs'],
    parameters: {
        layout: 'fullscreen',
    },
};

export const ToolbarStory = (args) => {
    const onClick = () => {
        // do nothing
    }

    return (
        <Toolbar onStopClick={onClick} {...args} 
            icon={stopIcon}>
        </Toolbar>
    );
}

ToolbarStory.storyName = "Toolbar";
ToolbarStory.args = {
    isRunning: true
}

