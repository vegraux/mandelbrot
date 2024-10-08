# -*- coding: utf-8 -*-

"""

"""

__author__ = "Vegard Ulriksen Solberg"
__email__ = "vegardsolberg@hotmail.com"

import plotly.graph_objects as go
import numpy as np
from numba import jit, guvectorize, int32, int64, complex128
import dash_bootstrap_components as dbc
from dash import dcc

from dash import html


def func(z, c):
    return z ** 2 + c


def recursive_color(c, max_iter=100, z0=0):
    z, counter = z0, 0
    while True:
        if counter >= max_iter:
            break

        if counter % 10 == 0:
            if np.absolute(z) > 2:
                break

        z = func(z, c)
        counter += 1
    return counter


def array_to_rgb(array):
    rgb_string = "rgb("
    for value in array:
        rgb_string += str(int(value * 255)) + ","
    return rgb_string[:-1] + ")"


def create_colorscale(max_iter, switch_nr):
    """
    Creates colorscale for plotting of the Mandelbrot set
    :param max_iter: Iterations before loop breaks when calculating if z is in
    the mandelbrot
    :param switch_nr: Color shifts every switch_nr integer.
    :return: colorscale to use in plotly heatmap
    """
    color_list = [
        "rgb(60, 30, 15)",
        "rgb(25, 7, 26)",
        "rgb(9, 1, 47)",
        "rgb(4, 4, 73)",
        "rgb(12, 44, 138)",
        "rgb(57, 125, 209)",
        "rgb(211, 236, 248)",
        "rgb(248, 201, 95)",
        "rgb(255, 170, 0)",
    ]

    dx = (1 / max_iter) * switch_nr
    colorscale = [[0, "rgb(0, 0, 0)"], [dx, "rgb(0 ,0, 0)"]]

    for i in range(1, int(np.ceil(1 / dx))):
        colorscale.append([i * dx, color_list[i % len(color_list)]])
        if (i + 1) * dx < 1:
            colorscale.append([(i + 1) * dx, color_list[(i) % len(color_list)]])
        else:
            colorscale.append([1, color_list[(i) % len(color_list)]])

    return colorscale


def mandelbrot_figure(
    x1=-2, x2=1, y1=-1.2, y2=1.2, resolution=500, max_iter=300, switch_nr=5
):
    xrange, yrange, data = get_data_numba(
        x1=x1, x2=x2, y1=y1, y2=y2, resolution=resolution, max_iter=max_iter
    )
    figure = go.Figure(
        data=go.Heatmap(
            x=xrange,
            y=yrange,
            z=data,
            hoverinfo="none",
            showscale=False,
            colorscale=create_colorscale(max_iter=max_iter, switch_nr=switch_nr),
        ),
        layout=go.Layout(
            margin=dict(l=20, r=20, t=20, b=20), height=650
        ),  # width=800, height=700
    )
    return figure


@jit(int64(complex128, int32))
def mandelbrot(c, maxiter):
    real = 0
    imag = 0
    for n in range(maxiter):
        nreal = real * real - imag * imag + c.real
        imag = 2 * real * imag + c.imag
        real = nreal
        if real * real + imag * imag > 4.0:
            return n
    return 0


@guvectorize([(complex128[:], int32[:], int32[:])], "(n),()->(n)", target="parallel")
def mandelbrot_numpy(c, maxit, output):
    maxiter = maxit[0]
    for i in range(c.shape[0]):
        output[i] = mandelbrot(c[i], maxiter)


def get_data_numba(x1=-1.666, x2=1, y1=-1.2, y2=1.2, resolution=200, max_iter=100):
    xrange = np.linspace(x1, x2, resolution, dtype=np.float64)
    yrange = np.linspace(y1, y2, resolution, dtype=np.float64)
    c = xrange + yrange[:, None] * 1j
    data = mandelbrot_numpy(c, max_iter)
    return (xrange, yrange, data)


card_color = [
    dbc.CardBody(
        [
            html.H5("Select color range", className="card-title"),
            html.P(
                "Try pulling the slider to the right to see shapes when zoomed in",
                className="card-text",
            ),
            dcc.Slider(
                id="color-slider",
                min=4,
                max=60,
                step=1,
                value=5,
                marks={k: str(k) for k in range(5, 61, 5)},
            ),
        ]
    )
]

card_max_iter = [
    dbc.CardBody(
        [
            html.H5("Select number of iterations", className="card-title"),
            html.P(
                "Number of iteration before a number is said to be in the Mandelbrot set",
                className="card-text",
            ),
            dcc.Slider(
                id="max-iter-slider",
                min=10,
                max=1000,
                step=30,
                value=300,
                marks={k: str(k) for k in range(100, 1001, 100)},
            ),
        ]
    )
]

card_resolution = [
    dbc.CardBody(
        [
            html.H5("Select resolution", className="card-title"),
            html.P("Number of pixels in width and height", className="card-text"),
            dcc.Slider(
                id="resolution-slider",
                min=100,
                max=1000,
                step=100,
                value=500,
                marks={k: str(k) for k in range(100, 1001, 100)},
            ),
        ]
    )
]

coordinates = {"x1": -2, "x2": 1, "y1": -1.2, "y2": 1.2}
relayout_map = {
    "xaxis.range[0]": "x1",
    "xaxis.range[1]": "x2",
    "yaxis.range[0]": "y1",
    "yaxis.range[1]": "y2",
}
