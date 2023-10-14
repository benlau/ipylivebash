from .formlayout import FormLayout
from .singlevaluelayout import SingleValueLayout
from .interfacebuilder import InterfaceBuilder


class Block(InterfaceBuilder):
    def __init__(self, context):
        self.context = context

    def ask(self, input=None, output=None, title=None):
        self.context.column_flow.truncate(self.context.current_block_index)
        if isinstance(input, list):
            layout = FormLayout(input, output, title, self.context)
        else:
            layout = SingleValueLayout(input, output, title, self.context)
        self.layout = layout
        self.context.column_flow.append(layout.widget)
        self.focus()

        return {
            "input": input,
            "output": output,
            "title": title,
            "layout": layout,
        }
    
    def display(self, widget):
        self.context.column_flow.append(widget)

    def focus(self):
        if self.layout is not None:
            self.layout.focus()
