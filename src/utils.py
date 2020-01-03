# -*- coding: utf-8 -*-

"""

"""

__author__ = "Vegard Ulriksen Solberg"
__email__ = "vegardsolberg@hotmail.com"

import numpy as np
import plotly.graph_objects as go


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


def mandelbrot_figure(x1=-1.666, x2=1, y1=-1.2, y2=1.2, resolution=500):
    figure = go.Figure(
        data=go.Heatmap(
            x=np.linspace(x1, x2, resolution),
            y=np.linspace(y1, y2, resolution),
            z=get_data_numpy(x1=x1, x2=x2, y1=y1, y2=y2, resolution=resolution),
            hoverinfo="none",
            showscale=False,
            colorscale="inferno",
        ),
        layout=go.Layout(width=800, height=700),
    )
    return figure


def numpy_recursive(cs, z0=0):
    iters = np.zeros_like(cs, dtype=int)
    z = z0 * np.ones_like(cs)
    for i in range(100):
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


get_data()
