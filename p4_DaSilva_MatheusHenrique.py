# -*- coding: utf-8 -*-
"""
Matheus Henrique Bijos Da Silva
"""

import math
import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):

    xmin, xmax = domain

    step = (xmax - xmin) / (ns - 1)
    xs = [xmin + i * step for i in range(ns)]

    ys = []
    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    print("{:>10s}{:>10s}".format("x", "y"))
    print("-" * 20)
    for x, y in zip(xs, ys):
        print("{:+10.4f}{:+10.4f}".format(x, y))

    plt.figure()
    plt.plot(xs, ys, "o-", color="blue")
    plt.title(fun_str)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()



fun_str = input("Enter function with variable x: ")
ns = int(input("Enter number of samples: "))
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))

plot_function(fun_str, (xmin, xmax), ns)