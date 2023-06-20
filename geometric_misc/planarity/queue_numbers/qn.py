from itertools import combinations, product
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
from pulp import LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD, value


def get_queue_layout(g):
    lp = LpProblem()
    q, x, y = __variable_declaration(g, nq := 2)
    lp += lpSum(q)
    __queue_prop(lp, q)
    __total_order(lp, x, g)
    __y_prop(lp, y, q, x, nq, g)
    __intersect(lp, x, y, nq, g)

    PULP_CBC_CMD(msg=0).solve(lp)
    print(LpStatus[lp.status], value(lp.objective))
    pos = {v: (sum(int(x[u, v].varValue) for u in g if u != v), 0) for v in g}
    q_assign = {(u, v): i for (i, u, v), yi in y.items() if yi.varValue > 0}
    return pos, q_assign


def __variable_declaration(g, nq=3):
    q = [LpVariable(f'q{i}', cat='Binary') for i in range(nq)]
    x = {(i, j): LpVariable(f'x_{i},{j}', cat='Binary')
         for i, j in product(g, repeat=2) if i != j}
    y = {(i, u, v): LpVariable(f'y_{i},{u},{v}', cat='Binary')
         for i, (u, v) in product(range(nq), g.edges)}
    y.update({(i, v, u): LpVariable(f'y_{i},{v},{u}', cat='Binary')
              for i, (u, v) in product(range(nq), g.edges)})
    return q, x, y


def __queue_prop(lp, q):
    for qi, qii in zip(q, q[1:]):
        lp += qii <= qi


def __total_order(lp, x, g):
    for i, j in combinations(g, 2):
        lp += x[i, j] + x[j, i] == 1
    for i, j, k in product(g, repeat=3):
        if i == j or j == k or i == k:
            continue
        lp += x[i, j] + x[j, k] - x[i, k] <= 1


def __y_prop(lp, y, q, x, nq, g):
    for u, v in g.edges:
        lp += lpSum(y[i, u, v] for i in range(nq)) == x[u, v]
        lp += lpSum(y[i, v, u] for i in range(nq)) == x[v, u]
    for i, (u, v) in product(range(nq), g.edges):
        lp += y[i, u, v] + y[i, v, u] <= q[i]


def __intersect(lp, x, y, nq, g):
    for i, ((u, v), (w, z)) in product(range(nq), combinations(g.edges, 2)):
        if any(i == j for i, j in product((u, v), (w, z))):
            continue
        lp += (y[i, u, v] + y[i, w, z] <= x[u, w] + x[w, v] + x[v, z] +
               3 * (x[w, u] + x[v, w] + x[z, v]) - 2)
        lp += (y[i, u, v] + y[i, w, z] <= x[w, u] + x[u, z] + x[z, v] +
               3 * (x[u, w] + x[z, u] + x[v, z]) - 2)
        lp += (y[i, u, v] + y[i, z, w] <= x[u, z] + x[z, v] + x[v, w] +
               3 * (x[z, u] + x[v, z] + x[w, v]) - 2)
        lp += (y[i, u, v] + y[i, z, w] <= x[z, u] + x[u, w] + x[w, v] +
               3 * (x[u, z] + x[w, u] + x[v, w]) - 2)
        lp += (y[i, v, u] + y[i, w, z] <= x[v, w] + x[w, u] + x[u, z] +
               3 * (x[w, v] + x[u, w] + x[z, u]) - 2)
        lp += (y[i, v, u] + y[i, w, z] <= x[w, v] + x[v, z] + x[z, u] +
               3 * (x[v, w] + x[z, v] + x[u, z]) - 2)
        lp += (y[i, v, u] + y[i, z, w] <= x[v, z] + x[z, u] + x[u, w] +
               3 * (x[z, v] + x[u, z] + x[w, u]) - 2)
        lp += (y[i, v, u] + y[i, z, w] <= x[z, v] + x[v, w] + x[w, u] +
               3 * (x[u, w] + x[w, v] + x[u, w]) - 2)


def __draw_edge(x1, x2, d):
    _a, _x = 0.2, np.linspace(0, (j := max(x1, x2)) - (i := min(x1, x2)), 100)
    plt.plot(i+_x, d * _a * (j - i) * np.sin(np.pi*_x/(j-i)),
             c='b', zorder=-10, alpha=0.3)


if __name__ == '__main__':
    g = nx.frucht_graph()
    pos, q_assign = get_queue_layout(g)

    nx.draw_networkx_nodes(g, pos, node_color='#ffc800').set_edgecolor('k')
    nx.draw_networkx_labels(g, pos)
    for (u, v), i in q_assign.items():
        if pos[u][0] < pos[v][0]:
            __draw_edge(pos[u][0], pos[v][0], 1-2*i)
        else:
            __draw_edge(pos[v][0], pos[u][0], 1-2*i)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    # plt.savefig('qn_frucht.png', bbox_inches='tight')
    plt.show()
