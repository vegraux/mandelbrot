# -*- coding: utf-8 -*-

"""

"""

__author__ = "Vegard Ulriksen Solberg"
__email__ = "vegardsolberg@hotmail.com"

import dash_core_components as dcc
import dash_html_components as html

from src.utils import mandelbrot_figure


layout = html.Div(
    children=[
        html.H1(children="Mandelbrot"),
        html.Div(
            children="""
        Dashboard for exploring the Mandelbrot set.
    """
        ),
        dcc.Graph(id="mandelbrot-fig", figure=mandelbrot_figure()),
    ]
)
