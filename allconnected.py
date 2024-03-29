"""

## All points must be connected

Now we work on the third constraint: **All points must be connected**. The verification of whether the game's points form a connected graph doesn't depend on SAT but on a Depth-First Search (DFS) that counts the number of connected components.

A connected component is a subset of the graph where every pair of nodes is linked through a path. A graph is considered connected if it has precisely one connected component. Therefore, if executing DFS on the graph once doesn't traverse all the vertices, then the graph is not connected. Utilizing a SAT approach would be less efficient due to the enormous quantity of constraints we would need to incorporate.

Below, you'll find the function that constructs a graph based on the lines generated during initialization. Each line represents an edge, and each point signifies a vertex, identified by its unique identifier.
"""

def init_graph(lines):
    g = Graph()
    for (u, v) in lines.values():
        g.add_edge(u, v)
    return g

"""While here you there is the DFS code."""

def DFS(G, v, parent, visited):
    visited[v] = True
    for u in G.get_adj_list_vertex(v):
        if u != parent:
            if not visited[u]:
                # Go on with DFS iff the vertex to visit isn't the parent
                # and hasn't been visited yet
                DFS(G, u, v, visited)


def connected_graph(G):
    '''Returns True if the first run of DFS visits all the vertices and therefore
    the number of components hasn't been incremented more than once'''
    visited = {v: False for v in G.get_vertices()}
    k = 0 # Number of connected components
    for v in G.get_vertices():
        if not visited[v]:
            k += 1
            if k != 1: # Returns False if the first DFS haven't visited all the nodes
                return False
            DFS(G, v, None, visited)

    return True
