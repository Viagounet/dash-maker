from abc import ABC
from dash import html


class Structure(ABC):
    def __init__(self, children, line_number):
        self.children = children
        self.line_number = line_number
        self.id = {"type": self.__class__.__name__.lower(),
                   "index": line_number}
        self.className = "flex-grow-2 m-1"

    def id_field(self, field):
        return {"type": field + "-" + self.__class__.__name__.lower(),
                "index": self.line_number}

    def construct(self):
        return html.Div()

    @property
    def component(self):
        return None


class Tile(Structure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)

    def construct(self):
        for child in self.children:
            setattr(self, child.arg, child.value)

        return html.Div(style={c.arg: c.value for c in self.children})

    @property
    def component(self):
        return None


class NoneStruct:
    def __init__(self):
        self.component = html.Div()

    def construct(self):
        return html.Div()


class Field:
    def __init__(self, arg_name, arg_value):
        self.variable = {arg_name: arg_value}

    def construct(self):
        pass

    @property
    def component(self):
        return None


