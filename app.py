# -*- coding: utf-8 -*-

"""

"""

__author__ = "Vegard Ulriksen Solberg"
__email__ = "vegardsolberg@hotmail.com"

import dash

from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

from src.utils import (
    mandelbrot_figure,
    card_color,
    card_max_iter,
    card_resolution,
    coordinates,
    relayout_map,
)
from dash.dependencies import Input, Output

MAX_ITER = 300
RESOLUTION = 500
SWITCH_NR = 5

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


def create_sliders():
    return [
        html.Br(),
        html.Br(),
        dbc.Card(card_color, color="light", inverse=False),
        dbc.Card(card_max_iter, color="light", inverse=False),
        dbc.Card(card_resolution, color="light", inverse=False),
    ]


layout = html.Div(
    [
        html.Br(),
        html.H1(id="header", children="Mandelbrot"),
        html.P(
            id="info-text",
            children="Explore the mandelbrot set by zooming in the figure",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="mandelbrot-fig",
                        figure=mandelbrot_figure(
                            max_iter=MAX_ITER,
                            resolution=RESOLUTION,
                            switch_nr=SWITCH_NR,
                        ),
                    ),
                    md=8,
                ),
                dbc.Col(create_sliders(), md=3),
            ]
        ),
    ]
)

app.layout = layout


@app.callback(
    Output("mandelbrot-fig", "figure"),
    [
        Input("mandelbrot-fig", "relayoutData"),
        Input("color-slider", "value"),
        Input("resolution-slider", "value"),
        Input("max-iter-slider", "value"),
    ],
)
def update_data(relayoutData, switch_nr, resolution, max_iter):
    kwargs = {"max_iter": max_iter, "resolution": resolution, "switch_nr": switch_nr}
    if relayoutData is None:
        kwargs.update(coordinates)
    elif any(["axis.range" in key for key in list(relayoutData.keys())]):
        new_coordinates = {relayout_map[key]: relayoutData[key] for key in relayoutData}
        coordinates.update(new_coordinates)
        kwargs.update(coordinates)
    return mandelbrot_figure(**kwargs)


if __name__ == "__main__":
    app.run_server(debug=True)
