import networkx as nx
from matplotlib import pyplot as plt
import random
from tutte_pos import tutte_pos


def gen(k):
    g = nx.LCF_graph(20, [1, 3, 14], 5)
    for u, v in g.edges_iter():
        g[u][v]['cost'] = 2

    random.seed(3)
    srcs = random.sample(range(g.number_of_nodes()), k)

    return (g, srcs)


def multiway_cut(g, srcs):
    t = g.number_of_nodes()
    for s in srcs:
        g.add_edge(s, t, cost=float('inf'))

    cutset = set()
    for s in srcs:
        g.remove_edge(s, t)
        cut_val, partition = nx.minimum_cut(g, s, t, capacity='cost')

        reachable, non_reachable = partition
        for u, nbrs in ((n, g[n]) for n in reachable):
            cutset.update((u, v) for v in nbrs if v not in reachable)

        g.add_edge(s, t, cost=float('inf'))

    g.remove_node(t)
    return cutset


def draw(g, srcs, cutset):
    pos = tutte_pos(g, 1)

    nx.draw_networkx(g, pos=pos, node_color='#ffddaa', node_size=150,
                     font_size=8)
    nx.draw_networkx_nodes(g, pos=pos, nodelist=srcs, node_color='#ffcccc',
                           node_size=150, font_size=8)
    nx.draw_networkx_edges(g, pos=pos, edgelist=list(cutset), edge_color='r')

    plt.gca().set_axis_off()
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.savefig('multiway_e1.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    k = 3
    g, srcs = gen(k)

    cutset = multiway_cut(g, srcs)
    print sum(g.edge[u][v]['cost'] for (u, v) in cutset)

    draw(g, srcs, cutset)
