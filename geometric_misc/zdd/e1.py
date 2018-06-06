import networkx as nx
from matplotlib import pyplot as plt
from simple_path import simple_path
from zdd import zdd


def a(z, pos, ax):
    plt.cla()
    E = z.v.universe
    for i, p in enumerate(z.all_paths()):
        edges = []
        for u, v in zip(p[:-1], p[1:]):
            if z.dd[u][v]['sign'] == 1:
                edges.append(E[z.dd.node[u]['label']])
        nx.draw_networkx(z.v.g, pos, ax=ax, alpha=0.3)
        nx.draw_networkx_edges(z.v.g, pos, ax=ax, edgelist=edges,
                               edge_color='g', width=2)
        plt.tight_layout()
        plt.savefig(str(i).zfill(3) + '.png', bbox_inches='tight')
        plt.cla()


if __name__ == '__main__':
    n = 3
    g = nx.grid_graph([n, n])
    s, t = (0, 0), (n-1, n-1)

    _, (ax1, ax2) = plt.subplots(ncols=2, figsize=(11, 3))
    pos = nx.spring_layout(g)
    nx.draw_networkx(g, pos, ax=ax1)
    nx.draw_networkx_nodes(g, pos, ax=ax1, nodelist=[s, t], node_color='g')

    z = zdd(simple_path(g, s, t))
    a(z, pos, ax2)

    z.draw(ax=ax2)
    nx.draw_networkx_edge_labels(g, pos, ax=ax1,
                                 edge_labels=z.element_labels())
    plt.tight_layout()
    plt.show()
