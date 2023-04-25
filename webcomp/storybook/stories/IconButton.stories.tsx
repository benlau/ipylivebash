import { IconButton } from '../../src/IconButton';
import React from 'react';
import stopIcon from "../../src/assets/stop-solid.svg";

export default {
    title: 'IconButton',
    component: IconButton,
    tags: ['autodocs'],
    parameters: {
        layout: 'fullscreen',
    },
};

export const IconButtonStory = (args) => {
    const onClick = () => {
        // do nothing
    }

    return (
        <IconButton onClick={onClick} {...args}
            icon={stopIcon}>
        </IconButton>
    );
}

IconButtonStory.storyName = "IconButton";
IconButtonStory.args = {
    isDisabled: false
}

