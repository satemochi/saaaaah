from matplotlib import pyplot as plt
import networkx as nx
from pulp import LpProblem, lpSum, LpVariable, PULP_CBC_CMD


"""
Adalat Jabrayilov and Petra Mutzel: (2017)
    New Integer Linear Programming Models for the Vertex Coloring Problem

google scholar:
    https://scholar.google.co.jp/scholar?hl=ja&as_sdt=0%2C5&q=%22New+Integer+Linear+Programming+Models+for+the+Vertex+Coloring+Problem%22&btnG=

arXiv:
    https://arxiv.org/abs/1706.10191
"""


def ass(g, h=10):
    c = list(range(h))
    w = [LpVariable(f'w{j}', cat='Binary') for j in c]
    x = {i: [LpVariable(f'x{i},{j}', cat='Binary') for j in c] for i in g}
    lp = LpProblem()
    lp += lpSum(w)
    for i in g:
        lp += lpSum(x[i]) == 1
    for u, v in g.edges:
        for j in c:
            lp += x[u][j] + x[v][j] <= w[j]
    for j in c:
        lp += w[j] <= lpSum([x[i][j] for i in g])
    for j in c[1:]:
        lp += w[j] <= w[j-1]
    PULP_CBC_CMD(msg=0).solve(lp)
    return [[xi.varValue for xi in x[i]].index(1.0) for i in g]


def rep(g):
    nbar = {u: nx.induced_subgraph(g, [v for v in g if v not in g[u]])
            for u in g}

    x = {u: {v: LpVariable(f'x{u},{v}', cat='Binary') for v in nbar[u]}
         for u in g}

    lp = LpProblem()
    lp += lpSum([x[u][u] for u in g])

    for v in g:
        lp += lpSum([x[u][v] for u in nbar[v]]) >= 1

    for u in g:
        for v, w in nbar[u].edges:
            lp += x[u][v] + x[u][w] <= x[u][u]

    lp.writeLP('rep.lp')
    PULP_CBC_CMD(msg=0).solve(lp)

    reps = [u for u in g if x[u][u].varValue > 0]
    cols = [None] * g.order()
    for c, v in enumerate(reps):
        cols[v] = c
    for c, r in enumerate(reps):
        for v in [v for v, xi in x[r].items() if xi.varValue > 0]:
            if v not in reps:
                cols[v] = c
    return cols


def pop(g, H=10):
    h = list(range(H))
    y = {i: {v: LpVariable(f'y{i},{v}', cat='Binary') for v in g} for i in h}
    z = {v: {i: LpVariable(f'z{v},{i}', cat='Binary') for i in h} for v in g}

    lp = LpProblem()
    q = 0       # arbitrary fix vertex, then q = 0
    lp += 1 + lpSum([y[i][q] for i in h])   # 15

    for v in g:
        lp += z[v][1] == 0          # 16
        lp += y[h[-1]][v] == 0      # 17
    for v in g:
        for i in h[:-2]:
            lp += y[i][v] - y[i+1][v] >= 0      # 18
            lp += y[i][v] + z[v][i+1] == 1      # 19
            lp += y[i][q] - y[i][v] >= 0        # 21
    for u, v in g.edges:
        for i in h:
            lp += y[i][u] + z[u][i] + y[i][v] + z[v][i] >= 1    # 20
    PULP_CBC_CMD(msg=0).solve(lp)
    return [next(i for i in h
                 if y[i][v].varValue == 0.0 and z[v][i].varValue == 0.0)
            for v in g]


def valid_coloring(g, c):
    return all(c[u] != c[v] for u, v in g.edges)


def gen():
    return nx.petersen_graph()
#    return nx.frucht_graph()


if __name__ == '__main__':
    g = gen()
    pos = nx.spring_layout(g)
    cmap = plt.get_cmap('tab10')

    colors = [cmap(c) for c in ass(g)]
    print('valid' if valid_coloring(g, colors) else 'invalid')
    colors = [cmap(c) for c in rep(g)]
    print('valid' if valid_coloring(g, colors) else 'invalid')
    colors = [cmap(c) for c in pop(g)]
    print('valid' if valid_coloring(g, colors) else 'invalid')

    nx.draw_networkx_nodes(g, pos, node_color=colors)
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    # plt.savefig('graph_coloring_by_ILP.png', bbox_inches='tight')
    plt.show()
