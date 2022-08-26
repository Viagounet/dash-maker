from __future__ import annotations

from dash import html, Output, Input

from structure.correspondance import CORRESPONDANCE
from structure.structures import Structure, NoneStruct


def seen(sorted_line, seen_struct):
    if sorted_line.children == []:
        return seen_struct + [sorted_line.line_number]
    seen_struct.append(sorted_line.line_number)
    for child in sorted_line.children:
        seen_struct += seen(child, seen_struct)

    return seen_struct


class SortedLine:
    def __init__(self, string_line: str, line_number: int, previous_sorted_line: SortedLine) -> None:
        self.line_number = line_number
        self.string_line = string_line
        self.priority = self.string_line.count("    ")
        self.clean_line = self.string_line.replace("    ", "").replace("\n", "")
        self.arg = self.clean_line.split(":")[0]
        try:
            self.value = self.clean_line.split(":")[1]
        except IndexError:
            self.value = None

        self.previous_sorted_line = previous_sorted_line
        self.parent = self.search_parent(self.previous_sorted_line, self.priority)
        self.children = []

    @property
    def structure(self):
        if self.clean_line != "":
            if self.value:
                return CORRESPONDANCE[self.arg](self.children, self.line_number, value=self.value)
            elif len(self.children) > 0:
                return CORRESPONDANCE[self.arg](self.children, self.line_number)
        return NoneStruct()

    def search_parent(self, previous_sorted_line: SortedLine, original_priority: int) -> SortedLine:
        """
        Recursive search for the parent of the current sorted_line
        :param previous_sorted_line:
        :param original_priority:
        :return: SortedLine
        """
        if self.line_number == 0:
            return None
        elif previous_sorted_line.priority < original_priority:
            return previous_sorted_line
        else:
            return previous_sorted_line.search_parent(previous_sorted_line.previous_sorted_line, original_priority)

    def __repr__(self) -> str:
        return f"SortedLine(l={self.line_number}, p={self.priority}, a={self.arg}, v={self.value}, children={self.children})"


class Code:
    def __init__(self, code_str: str) -> None:
        self.code_str = code_str
        self.string_lines = self.code_str.split("\n")
        self.string_lines.remove("")

        self.sorted_lines = {}
        self.structure = []

    def gen_sorted_line(self, string_line: str, line_number: int, previous_sorted_line: SortedLine) -> SortedLine:
        priority = string_line.count("    ")
        return SortedLine(string_line, line_number, previous_sorted_line)

    def parse(self):
        for i, code_line in enumerate(self.string_lines):
            if i == 0:
                sorted_line = code.gen_sorted_line(code_line, i, previous_sorted_line=None)
            else:
                sorted_line = code.gen_sorted_line(code_line, i, previous_sorted_line=old_sorted_line)
            self.sorted_lines[sorted_line.line_number] = sorted_line
            old_sorted_line = sorted_line
        for line, sorted_line in self.sorted_lines.items():
            if sorted_line.parent is not None:
                sorted_line.parent.children.append(sorted_line)

    def dash_tree(self):
        seen_ids = []
        tree = []
        for line, sorted_line in self.sorted_lines.items():
            if line not in seen_ids and isinstance(sorted_line.structure, Structure):
                self.structure.append(sorted_line.structure)
                seen_ids += seen(sorted_line, seen_ids)

                tree.append(sorted_line.structure.construct())

        return html.Div(children=tree)

    def __str__(self) -> str:
        str_return = ""
        for i, string in enumerate(self.string_lines):
            str_return += "{}\n".format(string)
        return str_return


with open("dash.txt", "r", encoding="utf-8") as f:
    code_str = f.read()

code = Code(code_str)
code.parse()
code_tree = code.dash_tree()

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, "style.css"])

app.layout = html.Div(children=[
    html.Div([structure.component for structure in code.structure if structure.component != None],
             className="p-3 gap-3",
             style={"width": "40vw", "overflow-y": "scroll", "height": "95vh", "border": "2px solid black"}
             ),

    html.Div([code_tree], style={"width": "60vw", "height": "60vh", "border": "2px solid black", "float": "left",
                                 "overflow-y": "scroll"},
             id="code-output")
],
    className="d-flex flex-row gap-3 p-3"
)


@app.callback(
    Output("code-output", "children"),
    Input("code-input", "value")
)
def update_output(input_value):
    code = Code(input_value)
    code.parse()
    return code.dash_tree()


if __name__ == "__main__":
    app.run_server()
