from ipylivebash.exp.scaffold.services.changedispatcher import (
    change_dispatcher,
    Listener,
)
from ..decorators import preset_iot_class_method
from ipywidgets import widgets
from ..widgetfactory import WidgetFactory
from ..processor import Processor

# SingleValueLayout is a class that creates a layout for a single input value.


class SingleValueLayout:
    @preset_iot_class_method
    def __init__(
        self,
        input=None,
        output=None,
        title=None,
        context=None,
        instant_write=False,
    ):
        self.input = input
        self.title = title
        self.output = output
        self.action_label = "Confirm"
        self.context = context
        self.instant_write = instant_write
        self.confirm_button = None
        self.widget = self._create_ipywidget()
        self.is_running = False

    def focus(self):
        self.input_widget.focus()

    def _create_ipywidget(self):
        layout = []
        factory = WidgetFactory()

        title_widget = None
        if self.title is not None:
            # TODO: Update title style
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        input_widget = factory.create_input(self.input)
        self.input_widget = input_widget

        def on_change(value):
            try:
                if self.input_widget.get_value() != value:
                    self.input_widget.set_value(value)
            except Exception as e:
                self.context.print_line(str(e))
                raise e

        listener = Listener(self.input.get_id(), on_change)
        change_dispatcher.add_listener(listener)

        def on_submit():
            def enable():
                if self.confirm_button is not None:
                    self.confirm_button.disabled = False

            processor = Processor(self.context)
            if self.confirm_button is not None:
                self.confirm_button.disabled = True
            task = processor.create_task(
                self.input, self.output, input_widget.get_value()
            )
            task.add_done_callback(lambda _: enable())

        if self.instant_write == False:
            (submit_area, confirm_button) = factory.create_submit_area(
                self.output, on_submit=on_submit, default_label=self.action_label
            )
            self.confirm_button = confirm_button
            widgets_box = widgets.VBox(layout + [input_widget.container, submit_area])
        else:

            def on_change(change):
                if change["type"] == "change" and change["name"] == "value":
                    on_submit()

            self.input_widget.widget.observe(on_change)
            widgets_box = widgets.VBox(layout + [input_widget.container])

        return widgets_box
