from random import shuffle
from matplotlib import pyplot as plt
import networkx as nx


def randomized_mis(g):  # algorithm 1 and 2
    """ Dalirrooyfard, Makarychev, Mitrovic (2026):
        A Simple Average-case Analysis of Recursive Randomized Greedy MIS
    """
    n = __gen_nbr(g)
    return [u for u in g if __rgmis(u, n)]


def __gen_nbr(g):
    shuffle((pi := list(g)))
    n = {u: [] for u in pi}
    for u in pi:
        for v in g[u]:
            if v not in n[u]:
                n[v].append(u)
    return n


def __rgmis(u, n):
    return not any(__rgmis(v, n) for v in n[u])


if __name__ == '__main__':
    g = nx.random_geometric_graph(n=150, radius=0.15, seed=0)
    pos = nx.get_node_attributes(g, 'pos')

    nx.draw_networkx_nodes(g, pos, node_size=30, alpha=.9,
                           node_color='skyblue').set_edgecolor('darkblue')
    nx.draw_networkx_edges(g, pos, alpha=0.3)
    nx.draw_networkx_nodes(g, pos, node_color='#ffcccc', node_size=50,
                           nodelist=randomized_mis(g)).set_edgecolor('red')

    plt.axis('off')
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    # plt.savefig('rgmis_a12.png', bbox_inches='tight', dpi=200)
    plt.show()
