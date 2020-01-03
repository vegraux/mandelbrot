# -*- coding: utf-8 -*-

"""

"""

__author__ = "Vegard Ulriksen Solberg"
__email__ = "vegardsolberg@hotmail.com"

import dash

import dash_core_components as dcc
import dash_html_components as html

from src.utils import mandelbrot_figure
from dash.dependencies import Input, Output, State

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout = html.Div(
    children=[
        html.H1(id="header", children="Mandelbrot"),
        dcc.Input(id="x1", value=-1.666, type="number"),
        dcc.Input(id="x2", value=1, type="number"),
        dcc.Input(id="y1", value=-1.2, type="number"),
        dcc.Input(id="y2", value=1.2, type="number"),
        html.Button(id="submit-button", n_clicks=0, children="Submit"),
        dcc.Graph(id="mandelbrot-fig"),
    ]
)

app.layout = layout


@app.callback(
    Output(component_id="mandelbrot-fig", component_property="figure"),
    [Input("submit-button", "n_clicks")],
    [
        State(component_id="x1", component_property="value"),
        State(component_id="x2", component_property="value"),
        State(component_id="y1", component_property="value"),
        State(component_id="y2", component_property="value"),
    ],
)
def update_figure(submitted, x1, x2, y1, y2):
    return mandelbrot_figure(x1=x1, x2=x2, y1=y1, y2=y2)


if __name__ == "__main__":
    app.run_server(debug=True)
