# -*- coding: utf-8 -*-
"""yashiplot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/123WHp5YrbD5a5zKgG9Y9EI9UXpM29CH6

To plot the game given the lines and points, I implemented the function `yashi_plot`:
"""

def yashi_plot(lines, pts, dimension, title=""):
    x = []
    y = []
    plt.figure(facecolor = "palevioletred")
    # Plotting all the points
    for annot in pts:
        r, c = pts[annot]
        x.append(r)
        y.append(c)
        plt.annotate(annot, (r, c))

    plt.scatter(x, y, c = 'red', marker = "o")

    # Plotting all the lines
    for u, v in lines.values():
        (x1, y1), (x2, y2) = pts[u], pts[v]
        plt.plot([x1, x2], [y1, y2], color='green', linewidth=2)


    plt.title(title)
    plt.grid(True)
    plt.xticks(range(0, dimension + 1))
    plt.yticks(range(0, dimension + 1))
    plt.show()