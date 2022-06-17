from functools import reduce
import matplotlib
from matplotlib import pyplot as plt
import networkx as nx
from pulp import LpMaximize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD


def orientation(g):
    a = {(i, j): LpVariable(f'a{i},{j}', lowBound=0) for i, j in g.edges}
    a.update({(j, i): LpVariable(f'a{j},{i}', lowBound=0) for i, j in g.edges})
    w = LpVariable('gamma')
    lp = LpProblem()
    lp += w
    for i, j in g.edges:
        lp += a[i, j] + a[j, i] >= 1
    for i in g:
        lp += w >= lpSum(a[i, j] for j in g[i])
    PULP_CBC_CMD(msg=0).solve(lp)
    print(w.varValue)
    return nx.DiGraph([(i, j) for i, j in g.edges if a[i, j].varValue > 0] +
                      [(j, i) for i, j in g.edges if a[j, i].varValue > 0])


def acyclic_matching(g):
    y = {(i, j): LpVariable(f'y{i},{j}', cat='Binary') for i, j in g.edges}
    a = {(i, j): LpVariable(f'a{i},{j}', lowBound=0) for i, j in g.edges}
    a.update({(j, i): LpVariable(f'a{j},{i}', lowBound=0) for i, j in g.edges})
    lp = LpProblem(sense=LpMaximize)
    lp += lpSum(y.values())
    for i, j in g.edges:
        lp += a[i, j] + a[j, i] >= \
            lpSum(y[i, j] if (i, j) in y else y[j, i] for j in g[i]) + \
            lpSum(y[i, j] if (i, j) in y else y[j, i] for i in g[j]) - 1
    for i in g:
        lp += lpSum(y[i, j] if (i, j) in y else y[j, i] for j in g[i]) <= 1
        lp += lpSum(a[i, j] for j in g[i]) <= 1 - 1/(n := g.order())
    PULP_CBC_CMD(msg=0).solve(lp)
    return nx.DiGraph([k for k, v in y.items() if v.varValue > 0])


def gen():
    return nx.frucht_graph()
#    return nx.random_tree(30, seed=None)
#    return nx.lollipop_graph(8, 4)
#    g =  nx.lollipop_graph(3, 3)
#    g.remove_edge(2, 3)
#    return g
#    return nx.balanced_tree(5, 2)


if __name__ == '__main__':
    g = gen()
#    matplotlib.use('module://backend_ipe')
    pos = nx.spring_layout(g)
    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffcccc')
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(g, pos, alpha=0.2)
    m = acyclic_matching(g)
    nx.draw_networkx_edges(m, pos, edge_color='r')
    s = nx.induced_subgraph(g, reduce(lambda x, e: x | set(e), m.edges, set()))
    nx.draw_networkx_edges(s, pos, edge_color='g', alpha=0.6)
    try:
        nx.find_cycle(s)
    except(nx.exception.NetworkXNoCycle):
        print('ok: passed acyclic-test')
#    o = orientation(g)
#    nx.draw_networkx_edges(o, pos)
    nx.draw_networkx_labels(g, pos)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')

#    plt.savefig('a.ipe', format='ipe')
#    plt.savefig('acyclic_matching_01.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
