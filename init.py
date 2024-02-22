"""
## Initialization

Firstly, we install `python-sat` and import all the needed libraries.
"""

!pip install python-sat

from pysat.formula import WCNF
from pysat.solvers import Minisat22
from pysat.examples.fm import FM

import pandas
import itertools
from itertools import chain
from collections import defaultdict, deque
from io import StringIO
from typing import List, Set, Dict, NewType, Tuple
import math
import matplotlib.pyplot as plt

"""Prior to discussing the key components that can resolve the game, it's necessary to initialize the game from the csv file. `initialize_yashi` yields the following outputs:

* **lines**: a dictionary associating the line identifier with itself;
* **pts**: a dictionary associating the point identifier with itself;
* **pts2line**: a dictionary associating a pair of points with the line they form.

Each line that originates from a point A and terminates at a point B is constructed based on this invariant: the line connecting A and B is singular and B is the nearest point reachable from A in a non-diagonal direction. By doing so, I address the second constraint.

**Line identifiers are the literals of the propositional formulas.**
"""

def initialize_yashi(df, dimension):
    size = len(df)
    grid = defaultdict(dict) # Doesn't raise errors if we search for unexisting points
    pts = dict()
    lines = dict()
    addedLines = defaultdict(bool)
    pts2line = defaultdict(dict)
    j = 1 # Line identifier

    # Creating the points and setting them to the grid
    for _, row in df.iterrows():
        p, x, y = row["point"], row["x"], row["y"]
        if x <= (dimension - 1) and y <= (dimension - 1): # Checking if all points are inside the grid (first constraint)
            pts[p] = (x, y)
            grid[x][y] = p
        else:
            raise ValueError("Point "+str(p)+" outside the grid")

    # Function to create lines
    def create_lines(reference, v, range_values, dim): # Inner function that creates the lines
        """ Reference can be the row or the column of a node depending on which dimension we are searching for lines"""
        nonlocal j
        if dim == "Horitzontal":
          for i in range_values:
              u = grid[reference].get(i, None)
              if u is not None:
                  u_v = (u, v) if u <= v else (v, u)
                  if not addedLines[u_v]:
                      lines[j] = (v, u)
                      pts2line[v][u] = j
                      pts2line[u][v] = j
                      addedLines[u_v] = True
                      j += 1
                  break # If we found a point we do not need to look farther as lines cannot overlap!

        elif dim == "Vertical":
          for i in range_values:
              u = grid[i].get(reference, None)
              if u is not None:
                  u_v = (u, v) if u <= v else (v, u)
                  if not addedLines[u_v]:
                      lines[j] = (v, u)
                      pts2line[v][u] = j
                      pts2line[u][v] = j
                      addedLines[u_v] = True
                      j += 1

                  break # If we found a point we do not need to look farther as lines cannot overlap!

        else:
          raise ValueError("The given dimension is wrong!")

    # Creating the lines from a point v
    for v, (r, c) in pts.items():
        create_lines(c, v, range(r + 1, size), dim = "Vertical") # to the closest point above
        create_lines(c, v, range(r - 1, -1, -1), dim = "Vertical") # to the closest point below
        create_lines(r, v, range(c + 1, size), dim = "Horitzontal") # to the closest point to its right
        create_lines(r, v, range(c - 1, -1, -1), dim = "Horitzontal") # to the closest point to its left

    return lines, pts, pts2line
