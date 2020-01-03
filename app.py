# -*- coding: utf-8 -*-

"""

"""

__author__ = "Vegard Ulriksen Solberg"
__email__ = "vegardsolberg@hotmail.com"

import dash

import dash_core_components as dcc
import dash_html_components as html

from src.utils import mandelbrot_figure
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

layout = html.Div(
    children=[
        html.H1(id="header", children="Mandelbrot"),
        html.P(
            id="info-text",
            children="Explore the mandelbrot set by zooming on the figure",
        ),
        dcc.Graph(id="mandelbrot-fig", figure=mandelbrot_figure()),
    ]
)

app.layout = layout


@app.callback(
    Output(component_id="mandelbrot-fig", component_property="figure"),
    [Input(component_id="mandelbrot-fig", component_property="relayoutData")],
)
def update_data(relayoutData):
    if relayoutData is None:
        return mandelbrot_figure()
    else:
        x1 = relayoutData["xaxis.range[0]"]
        x2 = relayoutData["xaxis.range[1]"]
        y1 = relayoutData["yaxis.range[0]"]
        y2 = relayoutData["yaxis.range[1]"]
        return mandelbrot_figure(x1, x2, y1, y2)


if __name__ == "__main__":
    app.run_server(debug=True)
