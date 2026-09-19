from matplotlib import pyplot as plt
import networkx as nx
import numpy as np


""" Yufei Zhao (2023): Graph Theory and Additive Combinatorics
        section 3.6 Second Eigenvalue: Alon-Boppana Bound   """


def get_test_vector(g):
    root = next(iter(g))
    d = g.degree(root)
    delta = {root: 0}
    stack, i = set(g[root]), 1
    while stack:
        _stack = set()
        dd = (d - 1)**(-i/2)
        for u in stack:
            delta[u] = dd
            _stack |= set([w for w in g[u] if w not in delta])
        i += 1
        stack = _stack
    return np.array([delta[v] for v in g])


if __name__ == '__main__':
    d, n = 3, 12
    g = nx.random_regular_graph(d, n)
    x = get_test_vector(g)
    L = nx.laplacian_matrix(g)
    A = nx.adjacency_matrix(g)
    print(L.todense())
    print(A.todense().astype(int))
    print(f"#-of edges: {np.trace((A @ A).todense())}, {2 * g.size()}")

    eigval, _ = np.linalg.eig(A.todense())
    from pprint import pprint
    pprint(eigval)
    pprint([c.real for c in eigval])
    lambdas = list(reversed(sorted([c.real for c in eigval])))
    print(sum(e * e for e in lambdas))
    print(d * d + (n - 1) * (max(lambdas[1], lambdas[n - 1])**2))

    print(x @ (L @ x))
    print(sum([(x[u] - x[v])**2 for u, v in g.edges]))

    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color='#ffcccc').set_edgecolor('k')
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)
    plt.tight_layout()
    plt.show()
