from math import cos, pi, sin
from matplotlib import pyplot as plt, use
import networkx as nx
import numpy as np
from pulp import LpMaximize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD


""" Cut Norm and Grothendieck's inequality
        This is an example for relationship between the cut-norm and
        Grothendieck's inequality.  """


def get_matrix(g, edges):
    a = np.zeros((2 * g.size(), g.order()), dtype=int)
    for i, (j, k) in enumerate(edges):
        a[2*i, j] = 1
        a[2*i+1, k] = 1
        a[2*i, k] = -1
        a[2*i+1, j] = -1
    return a


def matrix_to_latex(arr, matrix_type='bmatrix'):
    """Converts a 2D NumPy array into a LaTeX matrix string."""
    if len(arr.shape) != 2:
        raise ValueError("Array must be 2D")

    lines = []
    for row in arr:
        # Join elements with ' & ' and add row terminator
        lines.append(" & ".join(map(str, row)) + r" \\")

    # Join rows with newlines and wrap in the matrix environment
    in_cont = "\n  ".join(lines)
    return f"\\begin{{{matrix_type}}}\n  {in_cont}\n\\end{{{matrix_type}}}"


def maxcut(g, edges):
    z = [LpVariable(f'z_{i},{j}', cat='Binary') for i, j in edges]
    x = [LpVariable(f'x_{i}', cat='Binary') for i in g]
    lp = LpProblem(sense=LpMaximize)
    lp += lpSum(z)
    for i, (u, v) in enumerate(edges):
        lp += z[i] <= x[u] + x[v]
        lp += z[i] <= 2 - (x[u] + x[v])
    PULP_CBC_CMD(msg=0).solve(lp)
    return ([edges[i] for i in range(len(edges)) if z[i].varValue > 0],
            [i for i in g if x[i].varValue == 0])


def get_pos():
    pos, t = {}, 2 * pi / 5
    for i in range(5):
        pos[i] = (cos(t * i), sin(t * i))
    s, t, d = 0.5, 2 * pi / 3, -0.01
    for i in range(5, 8):
        pos[i] = (s * cos(t * (i+1)) + d, s * sin(t * (i+1)))
    return pos


if __name__ == '__main__':
    edges = [(0, 1), (2, 1), (2, 3), (4, 3), (0, 4), (5, 0),
             (1, 6), (7, 2), (6, 3), (4, 7), (6, 5), (5, 7)]
    g = nx.DiGraph(edges)
    print(a := get_matrix(g, edges))
    print(matrix_to_latex(a))

    # use('module://backend_ipe')
    pos = get_pos()
    nx.draw_networkx_nodes(g, pos, node_color='#ffcccc').set_edgecolor('k')
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)
    cut_edges, cut = maxcut(g, edges)
    nx.draw_networkx_nodes(g, pos, nodelist=cut, node_color='#ccccff')
    nx.draw_networkx_edges(g, pos, edgelist=cut_edges, edge_color='r')

    edge_labels = {e: i for i, e in enumerate(edges)}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    # plt.savefig('ac.ipe')
    plt.show()
