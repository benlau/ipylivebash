import { SessionTable } from '../../src/SessionTable';
import React from 'react';

export default {
    title: 'SessionTable',
    component: SessionTable,
    tags: ['autodocs'],
    parameters: {
        layout: 'fullscreen',
    },
};

export const SessionTableStory = (args) => {
    const rows = [
        {
            id: "instance0001",
            state: "running"
        },
        {
            id: "instance0002",
            state: "stopped"
        },
        {
            id: "instance0003",
            state: "stopped"
        }
    ]

    return (
        <SessionTable
            activeSessionId="instance0003" 
            rows={rows}
            {...args} />
    );
}

SessionTableStory.storyName = "SessionTable";
SessionTableStory.args = {
}

