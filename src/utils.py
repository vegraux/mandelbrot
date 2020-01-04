# -*- coding: utf-8 -*-

"""

"""

__author__ = "Vegard Ulriksen Solberg"
__email__ = "vegardsolberg@hotmail.com"

import plotly.graph_objects as go
import numpy as np
from numba import jit, guvectorize, complex64, int32
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import dash_html_components as html


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
    x1=-2, x2=1, y1=-1.2, y2=1.2, resolution=900, max_iter=100, switch_nr=5
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
            margin=dict(l=20, r=20, t=20, b=20),
            # width=600,
            # height=500
        ),  # width=800, height=700
    )
    return figure


def numpy_recursive(cs, z0=0, max_iter=100):
    iters = np.zeros_like(cs, dtype=int)
    z = z0 * np.ones_like(cs)
    for i in range(max_iter):
        z = z ** 2 + cs
        a = np.abs(z)
        selection = (a >= 2) & (iters == 0)
        sel = np.where(selection)
        iters[sel] = i

    return iters


def get_data(x1=-1.666, x2=1, y1=-1.2, y2=1.2, resolution=200):
    x_interval, y_interval = (
        np.linspace(x1, x2, resolution),
        np.linspace(y1, y2, resolution),
    )
    xx, yy = np.meshgrid(x_interval, y_interval)
    zz = np.zeros_like(xx)

    for i in range(resolution):
        for k in range(resolution):
            c = np.complex(xx[i, k], yy[i, k])
            zz[i, k] = recursive_color(c)

    return zz


def get_data_numpy(x1=-1.666, x2=1, y1=-1.2, y2=1.2, resolution=200):
    x_interval = np.linspace(x1, x2, resolution)
    y_interval = np.linspace(y1, y2, resolution)
    xx, yy = np.meshgrid(x_interval, y_interval)
    cs = np.zeros_like(xx, dtype=complex)
    for i in range(resolution):
        for k in range(resolution):
            cs[i, k] = np.complex(xx[i, k], yy[i, k])
    return numpy_recursive(cs)


@jit(int32(complex64, int32))
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


@guvectorize([(complex64[:], int32[:], int32[:])], "(n),()->(n)", target="parallel")
def mandelbrot_numpy(c, maxit, output):
    maxiter = maxit[0]
    for i in range(c.shape[0]):
        output[i] = mandelbrot(c[i], maxiter)


def get_data_numba(x1=-1.666, x2=1, y1=-1.2, y2=1.2, resolution=200, max_iter=100):
    xrange = np.linspace(x1, x2, resolution, dtype=np.float32)
    yrange = np.linspace(y1, y2, resolution, dtype=np.float32)
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
            dcc.Slider(id="color-slider", min=4, max=40, step=1, value=1),
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
            dcc.Slider(id="max-iter-slider", min=10, max=500, step=30, value=300),
        ]
    )
]

card_resolution = [
    dbc.CardBody(
        [
            html.H5("Select resolution", className="card-title"),
            html.P("Number of pixels in width and height", className="card-text"),
            dcc.Slider(id="resolution-slider", min=100, max=1500, step=100, value=500),
        ]
    )
]
