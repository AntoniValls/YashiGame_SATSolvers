"""
### Main code

This is the code which merges all the constraints defined above.
"""

def SAT_const(G, lines, pts, pts2line):
    phi = WCNF()
    k = len(pts) - 1 # number of lines

    phi_constraint_nocross = constraint_nocross(lines, pts)
    phi_no_cycles = no_cycles(G, pts2line)
    phi_tree = constraint_exactlyk(lines.keys(), k)

    phi.extend(phi_constraint_nocross.hard)
    phi.extend(phi_no_cycles.hard)
    phi.extend(phi_tree.hard)

    return phi
