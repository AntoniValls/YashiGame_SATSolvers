"""
## V2: Count how many solutions

In this version the program checks if the instance is solvable and it returns all the solutions.
"""

def version_two(file, dimension):
    y_csv = pandas.read_csv(file)
    solver = Minisat22()
    lines, pts, pts2line = initialize_yashi(y_csv, dimension)
    G = init_graph(lines)

    yashi_plot({}, pts, dimension, "Yashi Game")

    if connected_graph(G):
      phi = SAT_const(G, lines, pts, pts2line)
      solver.append_formula(phi.hard)

      solution = solver.solve()

      if solution:
          n_sol = 0
          for model in solver.enum_models():
              n_sol += 1
              model_lines = {x: lines[x] for x in model if x > 0}
              yashi_plot(model_lines, pts, dimension, "Solution number: " + str(n_sol))

          print("\n\nNumber of solutions: ", n_sol)
      else:
          print("No solution")
    else:
        print("No solution")
