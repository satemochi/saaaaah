from matplotlib import pyplot as plt
import networkx as nx
from pulp import LpMaximize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD


def _get_density(g):
    x = {(i, j): LpVariable(f'x_{i},{j}', lowBound=0) for i, j in g.edges}
    y = {i: LpVariable(f'y_{i}', lowBound=0) for i in g}
    lp = LpProblem(sense=LpMaximize)
    lp += lpSum(x.values())
    for i, j in g.edges:
        lp += x[(i, j)] <= y[i]
        lp += x[(i, j)] <= y[j]
    lp += lpSum(y.values()) <= 1
    PULP_CBC_CMD(msg=0).solve(lp)
    return __find(g, y)


def __find(g, y):
    return max((__dens(g, s := [j for j in g if y[j].varValue >= yi.varValue]),
                i, s) for i, yi in y.items())[2]


def __dens(g, s):
    return 0 if not s else g.subgraph(s).size() / len(s)


if __name__ == '__main__':
    g = nx.random_geometric_graph(50, 0.20, seed=1)
    ver = _get_density(g)
    print(ver)
    print(__dens(g, ver))

    pos = nx.get_node_attributes(g, 'pos')
    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffcccc', node_size=14)
    nodes.set_edgecolor('k')
    nodes = nx.draw_networkx_nodes(g, pos, nodelist=ver, node_color='r',
                                   node_size=34)
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(g, pos, alpha=0.3)
    # nx.draw_networkx_labels(g, pos)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.savefig('dense_component_01.png', bbox_inches='tight')
    plt.show()
