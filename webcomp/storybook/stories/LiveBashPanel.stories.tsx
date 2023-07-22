import { LiveBashPanel, useLiveBashPanelHandle } from '../../src/LiveBashPanel';
import React from 'react';
import { Page } from '../../src/types';

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
    } = useLiveBashPanelHandle();

    return <LiveBashPanel {...props} {...args} />
}

LiveBashPanelDefaultStory.storyName = "LiveBashPanel(default)";
LiveBashPanelDefaultStory.args = {
}

export const LiveBashPanelMessageOnlyStory = (args) => {
    const {
        props,
    } = useLiveBashPanelHandle();

    return <LiveBashPanel {...props} {...args} />
}

LiveBashPanelMessageOnlyStory.storyName = "LiveBashPanel(Plan Text)";
LiveBashPanelMessageOnlyStory.args = {
    messages: ["Hello",  "World"],
    statusHeader: "=== Divider ===",
    status: ["Status: OK", "End"],
    isRunning: false
}

export const LiveBashPanelMaxHeightStory = (args) => {
    const {
        props,
    } = useLiveBashPanelHandle();

    return <LiveBashPanel {...props} {...args} />
}

LiveBashPanelMaxHeightStory.storyName = "LiveBashPanel(HeightInLines)";
LiveBashPanelMaxHeightStory.args = {
    messages: Array.from(Array(20).keys()).map((i) => `Message ${i}`),
    isRunning: false,
    heightInLines: 10
}
    
export const LiveBashPanelLongMessageStory = (args) => {
    const {
        props,
    } = useLiveBashPanelHandle();

    return <LiveBashPanel {...props} {...args}/>
}

LiveBashPanelLongMessageStory.storyName = "LiveBashPanel(Long Message)";
LiveBashPanelLongMessageStory.args = {
    messages: [
        Array.from(Array(50).keys()).map((i) => `${i}`).join(".") + "\n" +
        Array.from(Array(50).keys()).map((i) => `${i}`).join("."),  
        "World"
    ],
    isRunning: false
}

export const LiveBashPanelConfirmationStory = (args) => {
    const {
        props,
    } = useLiveBashPanelHandle();

    return <LiveBashPanel {...props} {...args}/>
}

LiveBashPanelConfirmationStory.storyName = "LiveBashPanel(Confirmation Dialog Visible)";
LiveBashPanelConfirmationStory.args = {
    confirmationRequired: true
}


export const LiveBashPanelScriptPageStory = (args) => {
    const {
        props,
    } = useLiveBashPanelHandle();

    return <LiveBashPanel {...props} {...args} page={Page.CodePage}/>
}

LiveBashPanelScriptPageStory.storyName = "LiveBashPanel(Script)";
LiveBashPanelScriptPageStory.args = {
    script: `
    echo 123;
    `
}


export const LiveBashPanelSessionPageStory = (args) => {
    const {
        props,
    } = useLiveBashPanelHandle();

    return <LiveBashPanel {...props} {...args} page={Page.SessionPage}/>
}

LiveBashPanelSessionPageStory.storyName = "LiveBashPanel(Session)";
LiveBashPanelSessionPageStory.args = {
    sessions: [
        {
            id: "instance0001",
            state: "Completed"
        },
        {
            id: "instance0002",
            state: "Running"
        },
    ]
}
