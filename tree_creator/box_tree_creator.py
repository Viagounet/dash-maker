import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.html import Div

from main import code

my_code = code
code.dash_tree()

print([structure.component for structure in code.structure])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([structure.component for structure in code.structure if structure.component != None],
    className="p-3 gap-3",
    style={"width": "fit-content"}
)
if __name__ == "__main__":
    app.run_server(debug=False)
