import { Toolbar } from '../../src/Toolbar';
import React from 'react';

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
        <Toolbar onStopClick={onClick} onPlayClick={onClick} {...args} />
    );
}

ToolbarStory.storyName = "Toolbar";
ToolbarStory.args = {
    isRunning: true
}

