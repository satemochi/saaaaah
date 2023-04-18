from random import choice
from matplotlib import pyplot as plt
import networkx as nx


def halin_graph():
    g = __atachment_tree()
    leaves = [v for v in nx.dfs_preorder_nodes(g) if g.degree(v) == 1]
    g.add_edges_from((u, v) for u, v in zip(leaves, leaves[1:]))
    g.add_edge(leaves[0], leaves[-1])
    return g


def __atachment_tree(n=7):
    g, nc = nx.Graph([(0, 1), (0, 2), (0, 3)]), 4
    for i in range(n):
        v = choice(range(nc))
        g.add_edges_from([(v, nc), (v, nc+1)])
        nc += 2
    return g


if __name__ == '__main__':
    g = halin_graph()
    print(f'n: {g.order()}, m: {g.size()}')

    pos = nx.spring_layout(g)
    nodes = nx.draw_networkx_nodes(g, pos, node_color='#ffcccc')
    nodes.set_edgecolor('k')
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    # plt.savefig('halin_graph_ex1.png', bbox_inches='tight')
    plt.show()
