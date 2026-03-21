from gmpy2 import mpq
from matplotlib import pyplot as plt
import networkx as nx


def stern_brocot(depth=4):
    stack = [(mpq(0, 1), mpq(1, 2), mpq(1, 1), 0)]
    g = nx.Graph()
    g.add_node(mpq(1, 2))
    while stack:
        a, b, c, i = stack.pop()
        u = mpq(a.numerator + b.numerator, a.denominator + b.denominator)
        v = mpq(b.numerator + c.numerator, b.denominator + c.denominator)
        g.add_edges_from([(b, u), (b, v)])
        if i+1 < depth:
            stack.append((a, u, b, i+1))
            stack.append((b, v, c, i+1))
    return g


if __name__ == '__main__':
    g = stern_brocot()
    pos = nx.nx_pydot.graphviz_layout(g, prog="dot")

    nx.draw_networkx_nodes(g, pos, node_color="#ffcccc")
    nx.draw_networkx_edges(g, pos)
    labels = {u: fr"$\frac{{{u.numerator}}}{{{u.denominator}}}$" for u in g}
    nx.draw_networkx_labels(g, pos, labels)

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    # plt.savefig('stern_brocot_tree_d4.png', bbox_inches='tight')
    plt.show()
