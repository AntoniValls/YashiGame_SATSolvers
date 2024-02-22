"""
## V3: Minimum cost solution

The last version is the more complex one as it requires to add a soft constraint regarding to the length of the spanning tree.

 I used the negative euclidean distance because to find the solution with the minimum cost exploiting the Fu&Malik MaxSAT algorithm, we need to maximize the negative cost of them. Due to the use of negative weights, the cost solution is obtained by summing the negated total soft constraints cost and the solution found cost, which will be negative.

$$\infty: \phi_{no\_crossing} \\
\infty: \phi_{n-1\_lines} \\
\infty: \phi_{no\_cycles} \\
-d(l_{ip_1}, l_{ip_2}): l_i = (l_{ip_1}, l_{ip_2}) \,\, \forall l_i$$
"""

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def minimum_cost_solution_constraints(lines, pts, pts2line):
    phi = WCNF()
    for (u, v) in lines.values():
        phi.append([pts2line[u][v]], weight=-distance(pts[u], pts[v]))
    return phi


def version_three(file, dimension):
    y_csv = pandas.read_csv(file)
    lines, pts, pts2line = initialize_yashi(y_csv, dimension)
    G = init_graph(lines)

    yashi_plot({}, pts, dimension, "Yashi Game")

    if connected_graph(G):
      phi_hard = SAT_const(G, lines, pts, pts2line)
      phi_soft = minimum_cost_solution_constraints(lines, pts, pts2line)

      phi = WCNF()
      phi.extend(phi_hard.hard)
      phi.extend(phi_soft.soft, weights=phi_soft.wght)

      solver = FM(phi, verbose=0)

      solution = solver.compute()

      if solution:
          model = solver.model
          cost = -sum(phi_soft.wght) + solver.cost
          model_lines = {x: lines[x] for x in model if x > 0}
          yashi_plot(model_lines, pts, dimension, "The best solution: Cost = "+str(int(cost)))

      else:
          print("No solution")
    else:
        print("No solution")
