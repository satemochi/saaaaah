from itertools import product
from matplotlib import pyplot as plt
import networkx as nx


def sparsest_cut_with_exhaustively(g):
    u, n = set(g), g.order()
    return min((sum(1 for e in product(s, u-s) if g.has_edge(*e))/len(s), i, s)
               for i, s in enumerate(__powerset(list(g))))[2]


def __powerset(s):
    for i in range(1 << (n := len(s))):
        if i != 0 and bin(i).count('1') <= (half := n // 2):
            yield set(s[j] for j in range(n) if i & 1 << j)


def __sparsity(g, s, t):
    assert(len(s) <= len(t))
    return sum(1 for e in product(s, t) if g.has_edge(*e)) / len(s)


def gen():
    return nx.frucht_graph()


if __name__ == '__main__':
    g = gen()
    s = sparsest_cut_with_exhaustively(g)
    c = __sparsity(g, s, set(g)-s)
    print(c)
    print(s)

    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, nodelist=s, node_color='#ffcccc')
    t = [v for v in g if v not in s]
    nx.draw_networkx_nodes(g, pos, nodelist=t, node_color='#ccffcc')

    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)

    plt.title(f'Cheeger constant: {c}')
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    # plt.savefig('sparsest_cut_on_frucht_graph.png', bbox_inches='tight')
    plt.show()
