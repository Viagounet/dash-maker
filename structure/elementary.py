import csv
import pandas as pd
from dash import html, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from structure.structures import Structure


class ElementaryStructure(Structure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)
        self.className = "text-white p-1 m-1 rounded",


class Variables(Structure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)
        self.variables = {c.arg: c.value for c in children}
        for var, val in self.variables.items():
            if ".csv" in val:
                self.variables[var] = pd.read_csv(val)




class StructTakingVariable(ElementaryStructure):
    def __init__(self, children, line_number, **kwargs):
        super().__init__(children, line_number)
        for k, v in kwargs.items():
            setattr(self, k, v)


class Title(StructTakingVariable):
    def __init__(self, children, line_number, **kwargs):
        super().__init__(children, line_number, **kwargs)

    def construct(self):
        return html.H1(children=self.value)

    @property
    def component(self):
        return html.Div(dbc.Input(id=self.id_field("input"), placeholder="Your title", type="text", value=self.value), id=self.id,
                        className=self.className)


class Subtitle(StructTakingVariable):
    def __init__(self, children, line_number, **kwargs):
        super().__init__(children, line_number, **kwargs)

    def construct(self):
        return html.H4(children=self.value)

    @property
    def component(self):
        return html.Div(dbc.Input(id=self.id_field("input"), placeholder="Your subtitle", type="text", value=self.value), id=self.id,
                        className=self.className)


class Author(StructTakingVariable):
    def __init__(self, children, line_number, **kwargs):
        super().__init__(children, line_number, **kwargs)

    @property
    def component(self):
        return html.Div(dbc.Input(id=self.id_field("input"), placeholder="Author", type="text", value=self.value), id=self.id,
                        className=self.className)

    def construct(self):
        return html.H6(children=self.value)


class Text(StructTakingVariable):
    def __init__(self, children, line_number, **kwargs):
        super().__init__(children, line_number, **kwargs)

    def construct(self):
        return html.P(children=self.value)

    @property
    def component(self):
        return html.Div(dbc.Textarea(id=self.id_field("text-area"), placeholder="Enter text here", value=self.value), id=self.id,
                        className=self.className)



class Scatter(ElementaryStructure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)

    def construct(self):
        for child in self.children:
            setattr(self, child.arg, child.value)
        with open(self.data, "r") as f:
            data = f.read()
            sep = csv.Sniffer().sniff(data).delimiter

        df = pd.read_csv(self.data, sep=sep)
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df[self.x],
                y=df[self.y],
                mode="markers",
            ))
        fig.update_layout(
            margin=dict(l=5, r=5, t=5, b=5))
        return dcc.Graph(figure=fig, style={"width": "100%"})

    @property
    def component(self):
        return html.Div([html.I(className="fas fa-chart-bar me-3"),
                         html.P("Scatter Plot"),
                         html.I(className="fas fa-cog ms-2 clickable")],
                        className="d-flex flex-row align-items-baseline justify-content-center p-1 bg-white border "
                                  "rounded m-1")


class Table(ElementaryStructure):
    def __init__(self, children, line_number):
        super().__init__(children, line_number)

    def construct(self):
        for child in self.children:
            setattr(self, child.arg, child.value)

        with open(self.data, "r") as f:
            data = f.read()
            sep = csv.Sniffer().sniff(data).delimiter

        df = pd.read_csv(self.data, sep=sep)
        table = html.Div([dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size="sm",
                                                   style={"overflow-x": "scroll"})],
                         style={"width": "100%", "height": "100%", "max-height": "30vh", "overflow": "scroll"})
        return table

    @property
    def component(self):
        return html.Div([html.I(className="fas fa-table me-3"),
                         html.P("Table"),
                         html.I(className="fas fa-cog ms-2 clickable")],
                        className="d-flex flex-row align-items-baseline justify-content-center p-1 bg-white border "
                                  "rounded m-1")
