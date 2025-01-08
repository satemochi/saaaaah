from collections import defaultdict
from matplotlib import pyplot as plt
import networkx as nx
from pulp import LpProblem, lpSum, LpVariable, PULP_CBC_CMD


def strong_coloring(g, k):
    ell = g.order() // k
    n_dummy = g.order() % k
    w = [LpVariable(f'w{i}', cat='Binary') for i in range(k)]
    x = {u: {i: {j: LpVariable(f'x{u},{i},{j}', cat='Binary')
                 for j in range(ell)} for i in range(k)} for u in g}
    dummy = {u: {i: {j: LpVariable(f'dummy{u},{i},{j}', cat='Binary')
                     for j in range(ell)} for i in range(k)}
             for u in range(n_dummy)}
    lp = LpProblem()
    # objective
    lp += lpSum(w)
    # a ordinary assignment constraint
    for u in g:
        lp += lpSum(lpSum(x[u][i][j] for j in range(ell))
                    for i in range(k)) == 1
    for u in range(n_dummy):
        lp += lpSum(lpSum(dummy[u][i][j] for j in range(ell))
                    for i in range(k)) <= 1
    # a ordinary coloring constraint
    for u, v in g.edges:
        for i in range(k):
            lp += lpSum(x[u][i][j] for j in range(ell)) \
                    + lpSum(x[v][i][j] for j in range(ell)) <= w[i]
    for i in range(k):
        lp += lpSum(lpSum(dummy[u][i][j] for j in range(ell)) for u in dummy) \
                <= w[i]
    # a ordinary group constraint
    for j in range(ell):
        lp += lpSum(lpSum(x[u][i][j] for i in range(k)) for u in g) + \
                lpSum(lpSum(dummy[u][i][j] for i in range(k))
                      for u in range(n_dummy)) \
            == lpSum(w)
        for i in range(k):
            lp += lpSum(x[u][i][j] for u in g) + \
                    lpSum(dummy[u][i][j] for u in range(n_dummy))  == 1
    # resolve
    PULP_CBC_CMD(msg=0).solve(lp)
    # interpretation
    c, d = {}, {}
    for u in g:
        for i in range(k):
            for j in range(ell):
                if x[u][i][j].varValue > 0:
                    c[u], d[u] = i, j
                    break
            if u in c:
                break
    return c, d


if __name__ == '__main__':
    g = nx.LCF_graph(8, [4], 4)
    c, d = strong_coloring(g, k := 4)
    from pprint import pprint
    pprint(c)
    pprint(d)
    cmap = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    nl = defaultdict(list)
    for u in g:
        nl[d[u]].append(u)
    # import matplotlib
    # matplotlib.use('module://backend_ipe')
    pos = nx.circular_layout(g)
    for j in range(max(d.keys())):
        nc = [cmap[c[u]] for u in nl[j]]
        node = nx.draw_networkx_nodes(g, pos, nodelist=nl[j], node_color=nc,
                                      linewidths=4.0)
        node.set_edgecolor(cmap[3 - j])
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    # plt.savefig('strong_coloring_for_8_mobius_ladder.ipe', format='ipe')
    plt.tight_layout()
    plt.show()
