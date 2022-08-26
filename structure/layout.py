from dash import html

from structure.structures import Structure


class LayoutStructure(Structure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)
        self.className = "rounded border-start border-2 border-dark p-3 me-3",

    @property
    def component(self):
        return html.Div(
            [
                html.I(className="fas fa-minus clickable p-1 bg-danger text-white rounded",
                       style={"position": "relative", "top": "15px", "left": "96%"}),
                html.Div(
                    [html.H4(self.__class__.__name__), html.Div(children=[c.structure.component for c in self.children],
                                                                className="d-flex flex-column")],
                    className=self.className,
                    style={"width": "100%", "background-color": "rgba(100,100,100,0.18)"}
                ),
                html.Div([html.I(className="fas fa-plus m-1")],
                         style={"width": "100%", "height": "fit-content", "background-color": "#b2c1ff"},
                         className="layout-add rounded-bottom  mb-3 text-center")
            ]
        )


class Body(LayoutStructure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)

    def construct(self):
        return html.Div(children=[c.structure.construct() for c in self.children],
                        className="d-flex flex-column gap-3 p-2")

class Header(LayoutStructure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)

    def construct(self):
        return html.Div(children=[c.structure.construct() for c in self.children] + [html.Hr()],
                        className="d-flex flex-column align-items-center justify-content-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm",
                        style={"width": "100%"})


class Row(LayoutStructure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)

    def construct(self):
        return html.Div(children=[c.structure.construct() for c in self.children],
                        className="d-flex flex-row align-items-center justify-content-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm",
                        style={"width": "100%"})


class Col(LayoutStructure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)

    def construct(self):
        return html.Div(children=[c.structure.construct() for c in self.children], className="d-flex flex-column")


class Footer(LayoutStructure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)

    def construct(self):
        return html.Div(children=[c.structure.construct() for c in self.children])

