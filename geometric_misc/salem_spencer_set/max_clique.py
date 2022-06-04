from itertools import combinations
from matplotlib import pyplot as plt
import networkx as nx
from pulp import LpMaximize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD


def imax_clique(g):
    x = [LpVariable(f'x{i}', cat='Binary') for i in g]
    lp = LpProblem(sense=LpMaximize)
    lp += lpSum(x)
    for i, j in combinations(g.nodes, 2):
        if not g.has_edge(i, j):
            lp += x[i] + x[j] <= 1
    PULP_CBC_CMD(msg=0).solve(lp)
    return [i for i, xi in enumerate(x) if xi.varValue > 0]


def imax_independent_set(g):
    x = [LpVariable(f'x{i}', cat='Binary') for i in g]
    lp = LpProblem(sense=LpMaximize)
    lp += lpSum(x)
    for i, j in g.edges:
        lp += x[i] + x[j] <= 1
    PULP_CBC_CMD(msg=0).solve(lp)
    return [i for i, xi in enumerate(x) if xi.varValue > 0]


if __name__ == '__main__':
    n = 20
    g = nx.fast_gnp_random_graph(n, 8/n)
    pos = nx.circular_layout(g)
    nx.draw(g, pos, alpha=0.1)
    nx.draw(g.subgraph(imax_clique(g)), pos, node_color='r', alpha=.3, width=2)
    nx.draw_networkx_nodes(g, pos, nodelist=imax_independent_set(g), alpha=.5)
    plt.gca().set_aspect('equal')
    # plt.savefig('max_clique_01.png', bbox_inches='tight')
    plt.show()
