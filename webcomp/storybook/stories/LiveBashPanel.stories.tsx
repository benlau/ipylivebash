import { LiveBashPanel, useLiveBashPanel } from '../../src/LiveBashPanel';
import React from 'react';

export default {
    title: 'LiveBashPanel',
    component: LiveBashPanel,
    tags: ['autodocs'],
    parameters: {
        layout: 'fullscreen',
    },
};

export const LiveBashPanelDefaultStory = (args) => {
    const {
        props,
    } = useLiveBashPanel();

    return <LiveBashPanel {...props} {...args} />
}

LiveBashPanelDefaultStory.storyName = "LiveBashPanel(default)";
LiveBashPanelDefaultStory.args = {
}

export const LiveBashPanelMessageOnlyStory = (args) => {
    const {
        props,
    } = useLiveBashPanel();

    return <LiveBashPanel {...props} {...args} />
}

LiveBashPanelMessageOnlyStory.storyName = "LiveBashPanel(Plan Text)";
LiveBashPanelMessageOnlyStory.args = {
    messages: ["Hello",  "World"],
    statusHeader: "=== Divider ===",
    status: ["Status: OK", "End"],
    isLoadingSpinnerRunning: false
}

export const LiveBashPanelMaxHeightStory = (args) => {
    const {
        props,
    } = useLiveBashPanel();

    return <LiveBashPanel {...props} {...args} />
}

LiveBashPanelMaxHeightStory.storyName = "LiveBashPanel(HeightInLines)";
LiveBashPanelMaxHeightStory.args = {
    messages: Array.from(Array(20).keys()).map((i) => `Message ${i}`),
    isLoadingSpinnerRunning: false,
    heightInLines: 10
}
    
export const LiveBashPanelLongMessageStory = (args) => {
    const {
        props,
    } = useLiveBashPanel();

    return <LiveBashPanel {...props} {...args}/>
}

LiveBashPanelLongMessageStory.storyName = "LiveBashPanel(Long Message)";
LiveBashPanelLongMessageStory.args = {
    messages: [
        Array.from(Array(50).keys()).map((i) => `${i}`).join(".") + "\n" +
        Array.from(Array(50).keys()).map((i) => `${i}`).join("."),  
        "World"
    ],
    isLoadingSpinnerRunning: false
}