from matplotlib import pyplot as plt
import networkx as nx
from abc_td import maximum_cardinality_search, min_fill, min_degree


def gen(n=100):
    while True:
        g = nx.random_geometric_graph(n, 15./n)
        if nx.number_connected_components(g) == 1:
            return g


def trial(n=100):
    a, b, c, d = [], [], [], []
    for i in xrange(n):
        g = gen()
        a.append(maximum_cardinality_search(g).tree_width)
        b.append(min_fill(g).tree_width)
        c.append(min_degree(g).tree_width)
        d.append(max(list(g.degree()), key=lambda t: t[1])[1])
    plt.plot(range(n), a, label='MCS')
    plt.plot(range(n), b, label='min-fill')
    plt.plot(range(n), c, label='min-degree')
    plt.plot(range(n), d, label='max degree')
    plt.gca().legend(loc='best')
    plt.gca().set_ylim(0, max(d)+3)


if __name__ == '__main__':
    trial()
    plt.savefig('rand_geom_graph_100.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
