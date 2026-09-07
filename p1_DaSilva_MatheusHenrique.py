# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 20:42:11 2026

@author: Matheus Henrique Da Silva
"""


import math
import matplotlib.pyplot as plt


while True:

    a_str = input("Enter a: ")
    if a_str == "":
        break
    a = float(a_str)

    b = float(input("Enter b: "))
    c = float(input("Enter c: "))

    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        print("No real solutions")
    elif discriminant == 0:
        x1 = -b / (2 * a)
        print("One solution: {:.5f}".format(x1))
    else:
        sqrt_disc = math.sqrt(discriminant)
        x1 = (-b + sqrt_disc) / (2 * a)
        x2 = (-b - sqrt_disc) / (2 * a)
        print("Two solutions: x1={:.5f} x2={:.5f}".format(x1, x2))

    if discriminant >= 0:
        if discriminant == 0:
            x_left = x1
            x_right = x1
        else:
            x_left = min(x1, x2)
            x_right = max(x1, x2)

        margin = max(1.0, (x_right - x_left))  # extra room around roots
        x_min = x_left - margin
        x_max = x_right + margin
    else:
        x_opt = -b / (2 * a)
        half_width = 5.0
        x_min = x_opt - half_width
        x_max = x_opt + half_width

    n_points = 150
    step = (x_max - x_min) / (n_points - 1)
    x_values = [x_min + i * step for i in range(n_points)]
    y_values = [a * x ** 2 + b * x + c for x in x_values]

    plt.figure()
    plt.plot(x_values, y_values)
    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.title("y = {}x^2 + {}x + {}".format(a, b, c))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

print("Program ended.")