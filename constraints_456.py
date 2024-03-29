"""
## Constraint 4, 5 and 6

The remaining constraints can be expressed using the formula: $$ϕ = ϕ_{no\_crossing} \land ϕ_{n-1\_lines} \land ϕ_{no\_cycles}$$ These constraints will be validated using a SAT solver.

### No crossing lines

The constraint to not have crossing lines is quite easy to state, since given two crossing lines $l_i$ and $l_j$ we don't want to use them together.

\begin{equation}
\phi_{no\_crossing} = \bigwedge_\limits{\substack{l_i,l_j, l_i \neq l_j, \\ iscrossing(l_i, l_j)}} \neg ({l_i \land l_j}) = \bigwedge_\limits{\substack{l_i,l_j, l_i \neq l_j, \\ iscrossing(l_i, l_j)}} (\neg{l_i} \lor \neg{l_j}).
\end{equation}

To determine if two lines intersect, it is necessary that they have distinct orientations (one horizontal and one vertical). Additionally, the $x$-coordinate of the vertical line must fall within the range of the $x$-coordinates of the points that constitute the horizontal line.
"""

def is_crossing(l1, l2, pts):
    l1_pts = sorted([pts[l1[0]], pts[l1[1]]])
    l2_pts = sorted([pts[l2[0]], pts[l2[1]]])

    if l1_pts[0][0] == l1_pts[1][0]:  # l1 is vertical
        if l2_pts[0][1] == l2_pts[1][1]:  # l2 is horizontal
            return (l2_pts[0][0] < l1_pts[0][0] < l2_pts[1][0]) and (l1_pts[0][1] < l2_pts[0][1] < l1_pts[1][1])
    elif l1_pts[0][1] == l1_pts[1][1]:  # l1 is horizontal
        if l2_pts[0][0] == l2_pts[1][0]:  # l2 is vertical
            return (l1_pts[0][0] < l2_pts[0][0] < l1_pts[1][0]) and (l2_pts[0][1] < l1_pts[0][1] < l2_pts[1][1])
    return False


def constraint_nocross(lines, pts):
    phi_constraint_nocross = WCNF()
    items = list(lines.items())
    for index, (l1_id, l1) in enumerate(items):
        for l2_id, l2 in items[index + 1:]:
            if is_crossing(l1, l2, pts):
                phi_constraint_nocross.append([-l1_id, -l2_id])  # the literals are the line identifiers
    return phi_constraint_nocross

"""### Exactly n-1 lines

To state the following constraint I used the formula to force the use of _exactly_ $k$ literals as the conjunction of _at least $k$_ and _at most $k$_:

\begin{equation}
\phi_{n-1\_lines} = \left(\bigwedge_\limits{\substack{I \subseteq [n] \\ \#I=n-k+1}} \bigvee_\limits{i \in I} l_i\right) \land \left(\bigwedge_\limits{\substack{I \subseteq [n] \\ \#I=k+1}} \bigvee_\limits{i \in I} \neg{l_i}\right)
\end{equation}
where:
* **n**: is the total number of literals, in our case the number of lines;
* **k**: the number of literals we want to force, in our case the number of points - 1.
"""

def constraint_exactlyk(literals, k):
    phi = WCNF()
    n = len(literals)

    # At least k
    for sub_lits in itertools.combinations(literals, n - k + 1):
        phi.append([lit for lit in sub_lits])

    # At most k
    for sub_lits in itertools.combinations(literals, k + 1):
        phi.append([-lit for lit in sub_lits])

    return phi

"""### No cycles

Given a set of cycles made up by some literals, we can easily state the constraint as follows:

\begin{equation}
\phi_{no\_cycles} = \bigwedge_\limits{c \in \text{Cycles}} \neg {\bigwedge_\limits{l \in c} l} = \bigwedge_\limits{c \in \text{Cycles}} \bigvee_\limits{l \in c} \neg{l}
\end{equation}

where we force to not use all the lines in a cycle at once.

The difficult part of this constraint is how to identify all the possible cycles in the game. I relied on a famous algorithm that can be found here: https://www.codeproject.com/Articles/1158232/Enumerating-All-Cycles-in-an-Undirected-Graph.

The code that identifies all cycles in a given graph can be split into two segments: one for obtaining the fundamental cycles and another for generating all the cycles.

**Fundamental Cycles**

Fundamental cycles are the base cycles from which all other cycles can be derived. The core concept is to create a spanning tree from the undirected graph and identify all edges that exist in the graph but not in the tree. Incorporating one of these absent edges to the tree will result in a cycle, known as a **fundamental cycle**.

 It's important to note that a graph can have multiple distinct spanning trees, depending on the selected root node and the construction method of the tree. As a result, each spanning tree forms its own set of fundamental cycles. All fundamental cycles constitute a cycle basis, i.e., a basis for the cycle space of the graph. Since the basis is complete, it doesn't matter which spanning tree was used to generate the cycle basis; each basis is equally capable of constructing all possible cycles of the graph. A Depth-First Search is utilized to construct the fundamental cycles more efficiently.

To identify a fundamental cycle, we merge the path from the root to vertex i and the path from the root to vertex j using the xor operator. This is because if j is a neighbor of i and has already been visited, i.e., it's already in T, merging the two paths will result in a cycle. An example can be seen where A is the starting vertex, E and D are respectively i and j, and the outcome is the cycle <F, E, D>.
<img src="https://www.codeproject.com/KB/recipes/1158232/merging_paths.svg" width="75%" />

**Getting all the cycles**

After having got the fundamental cycles, all the cycles can be obtained by xoring all the possible combinations among the basic cycles. For instance, given a graph whose fundamental cycles are FC1, FC2 and FC3, all the cycles can be obtained as follows:

|Bitstring	|	XOR Combination	|	Cycle
|-----------|-----------------|------
|100	|	FC1	|	A-B-E-F-C-A
|010	|	FC2	|	B-D-E-B
|001	|	FC3	|	D-E-F-D
|110 	| FC1 ^ FC2	|	A-B-D-E-F-C-A
|101	|	FC1 ^ FC3	|	A-B-E-D-F-C-A
|011	|	FC2 ^ FC3	|	B-D-F-E-B
|111	|	FC1 ^ FC2 ^ FC3	|	A-B-D-F-C-A
"""

def allsubsets(iterable):
    '''returns the all possible subsets of a set'''
    s = list(iterable)
    return chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

def get_path_from_to(G, v, u, parents):
    '''returns a graph representing the path from v to u'''
    path = Graph()
    while u is not None and u != v: # While we have not reached the root v
        p = parents[u] # Parent of the current node
        path.add_edge(u, p, G.get_weight(u, p))
        u = p
    return path

def get_fundamental_cycles(G, r):
    '''returns a set of graphs represting the fundamental cycles from a root r and a graph G'''
    in_T = defaultdict(bool) # Record if a node is in a tree
    in_T[r] = True
    T = Graph()
    Q = deque([r]) # Start with the root (double ended queue)
    parents = defaultdict(lambda: None)
    cycles = set()

    while Q:
        v = Q.popleft()
        for u in G.get_adj_list_vertex(v): # get all the neighbours of the current node
            if u != parents[v]:
                if in_T[u]: # If u is already in the tree we can combine both paths to get a Fundamental Cycle
                    cycle = get_path_from_to(T, r, v, parents) ^ get_path_from_to(T, r, u, parents) # XOR Combination
                    cycle.add_edge(u, v, G.get_weight(u, v)) # Add the neighbours edge
                    cycles.add(cycle)
                else:
                    Q.append(u)
                    in_T[u] = True
                    T.add_edge(v, u, G.get_weight(v, u))
                    parents[u] = v
    return cycles

def get_cycles(G):
    '''returns a list containing all the cycles got from
    the fundamental cycles'''
    r = list(G.get_vertices())[0]
    fundamental_cycles = get_fundamental_cycles(G, r)
    cycles = []
    for subset in allsubsets(fundamental_cycles):
        if subset:
            new_cycle = Graph()
            for cycle in subset:
                new_cycle = new_cycle ^ cycle
            cycles.append(new_cycle.get_edges())

    return cycles

"""Finally, we have all the cycles and we can use the formula $\phi_{no\_cyles}$ described earlier. The function *constraint_no_cycles* is used to create the formula, while *no_cycles* is aimed to get all the cycles and get the formula to return to the caller."""

def constraint_no_cycles(cycles, pts2line):
    phi_no_cycles = WCNF()

    for cycle in cycles:
        constraint = []
        for u, v, _ in cycle:
            constraint.append(-pts2line[u][v])
        if constraint:
            phi_no_cycles.append(constraint)

    return phi_no_cycles


def no_cycles(G, pts2line):
    cycles = get_cycles(G)
    phi_no_cycles = constraint_no_cycles(cycles, pts2line)

    return phi_no_cycles
