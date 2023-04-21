import { LoadingSpinner } from '../../src/LoadingSpinner';
import React from 'react';

export default {
    title: 'LoadingSpinner',
    component: LoadingSpinner,
    tags: ['autodocs'],
    parameters: {
        layout: 'fullscreen',
    },
};

export const LoadingSpinnerStory = (args) => (
    <LoadingSpinner {...args} />
)

LoadingSpinnerStory.storyName = "LoadingSpinner";
LoadingSpinnerStory.args = {
    isRunning: true
}

