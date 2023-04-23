import { ConfirmationDialog, useConfirmationDialog } from '../../src/ConfirmationDialog';
import React from 'react';

export default {
    title: 'ConfirmationDialog',
    component: ConfirmationDialog,
    tags: ['autodocs'],
    parameters: {
        layout: 'fullscreen',
    },
};

export const ConfirmationDialogStory = (args) => {
    const {
        props,
        methods
    } = useConfirmationDialog();

    React.useEffect(() => {
        methods.show("Are you sure you want to do this?", () => {
            // do nothing
        }, () => {
            // do nothing
        })
    }, [methods]);

    return (
        <ConfirmationDialog {...props} {...args}/>
    );
}

ConfirmationDialogStory.storyName = "ConfirmationDialog";
ConfirmationDialogStory.args = {
}

