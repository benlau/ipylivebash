import { Toolbar } from '../../src/Toolbar';
import React from 'react';
import { Page } from '../../src/types';

export default {
    title: 'Toolbar',
    component: Toolbar,
    tags: ['autodocs'],
    parameters: {
        layout: 'fullscreen',
    },
};

export const ToolbarStory = (args) => {
    const onStopClick = () => {
        // Do nothing
    }

    const [page, setPage] = React.useState(Page.TerminalPage);

    return (
        <Toolbar onStopClick={onStopClick} 
            page={page}
            setPage={setPage}
            {...args} />
    );
}

ToolbarStory.storyName = "Toolbar";
ToolbarStory.args = {
    isRunning: true
}

