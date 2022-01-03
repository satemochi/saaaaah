from random import sample, seed
from pulp import LpProblem, lpSum, LpVariable, PULP_CBC_CMD
import networkx as nx


def steiner_tree(g, term):
    lp, x = __get_formulae(g, term)
    lp.writeLP('steiner_tree.lp')
    PULP_CBC_CMD(msg=0).solve(lp)
    return nx.Graph((e for e in x if x[e].varValue > 0))


def __get_formulae(g, term):
    x = {e: LpVariable(f'x_{e}', cat='Binary') for e in g.edges}
    lp = LpProblem()
    lp += lpSum(x.values())
    f = {}
    for t in term[1:]:
        f[t] = {(u, v): LpVariable(f'f^{t}_{u},{v}', cat='Binary')
                for u, v in g.edges}
        f[t].update({(v, u): LpVariable(f'f^{t}_{v},{u}', cat='Binary')
                     for u, v in g.edges})
    for t in term[1:]:
        for u in g:
            if u == term[0]:    # term[0] is as a root of steiner arborescence
                lp += lpSum(f[t][(u, v)] - f[t][(v, u)] for v in g[u]) == 1
            elif u == t:
                lp += lpSum(f[t][(u, v)] - f[t][(v, u)] for v in g[u]) == -1
            else:
                lp += lpSum(f[t][(u, v)] - f[t][(v, u)] for v in g[u]) == 0
    for e in g.edges:
        for t in term[1:]:
            lp += x[e] >= f[t][e] + f[t][e[::-1]]
    return lp, x


def gen(n):
    from random import sample, seed
    return (g := nx.frucht_graph()), sample(g.nodes, n)


if __name__ == '__main__':
    seed(9)
    g, t = gen(3)
    st = steiner_tree(g, t)

    from matplotlib import pyplot as plt
    pos = nx.spring_layout(g)

    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffffcc')
    nodes.set_edgecolor('black')

    nx.draw_networkx_edges(g, pos, alpha=0.2)
    nx.draw_networkx_labels(g, pos)

    nodes = nx.draw_networkx_nodes(g, pos, nodelist=t, node_color='#33cc33')
    nodes.set_edgecolor('black')
    nx.draw_networkx_edges(st, pos, edge_color='brown', width=2)

    plt.gca().axis('off')
    plt.savefig('steiner_tree_lp_ex1.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
