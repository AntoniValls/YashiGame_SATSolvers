"""
## V1: Check satisfiability.

In the first version of the Yashi Game the program checks if the instance is solvable. In case it is, it returns one solution.
"""

def version_one(file, dimension, title = ""):
    y_csv = pandas.read_csv(file)
    solver = Minisat22()
    lines, pts, pts2line = initialize_yashi(y_csv, dimension)
    G = init_graph(lines)

    yashi_plot({}, pts, dimension, "Yashi Game: " +str(title))

    if connected_graph(G):
      phi = SAT_const(G, lines, pts, pts2line)
      solver.append_formula(phi.hard)

      solution = solver.solve()

      if solution:
          model = solver.get_model()
          model_lines = {x: lines[x] for x in model if x > 0}

          yashi_plot(model_lines, pts, dimension, "The solution")
          return True
      else:
          print("No solution")
          return False
    else:
        print("No solution")
        return False
