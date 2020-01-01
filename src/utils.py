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
    while np.absolute(z) < 5:
        if counter >= max_iter:
            break
        z = func(z, c)
        counter += 1
    return counter


def mandelbrot_figure():
    figure = go.Figure(
        data=go.Heatmap(z=get_data()), layout=go.Layout(width=800, height=700)
    )
    return figure


def get_data(N=400):
    x1, x2 = -1.666, 1  # 0.2, 0.5
    y1, y2 = -1.2, 1.2  # -0.2, 0.2
    x_interval, y_interval = np.linspace(x1, x2, N), np.linspace(y1, y2, N)
    xx, yy = np.meshgrid(x_interval, y_interval)
    zz = np.zeros_like(xx)

    for i in range(N):
        for k in range(N):
            c = np.complex(xx[i, k], yy[i, k])
            zz[i, k] = recursive_color(c)

    return zz
