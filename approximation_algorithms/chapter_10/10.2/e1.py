import random
from matplotlib import pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from tree_decomposition import programming_for_tree_decomposition
from MIS_for_tree_decomp import max_independent_set_with_tree_decomposition
from MIS_with_ILP import max_independent_set_with_ILP


if __name__ == '__main__':
    _, (ax1, ax2) = plt.subplots(ncols=2, figsize=(11, 5))

#    g = nx.petersen_graph()
    g = nx.frucht_graph()
#    g = nx.diamond_graph()
#    g = nx.bull_graph()
#    g = nx.octahedral_graph()
#    g = nx.house_graph()

    random.seed(0)
    mean = 500.0
    for v in g.nodes():
        g.node[v]['w'] = random.expovariate(1. / mean)

    A = programming_for_tree_decomposition(g)
#    A = programming_for_tree_decomposition(g, True)
    print A.tree_width

    t = A.tree_decomposition()
    the = max_independent_set_with_tree_decomposition(g, t)
    iset = the.independent_set

    lp = max_independent_set_with_ILP(g)
    iset2 = lp.independent_set
    print list(iset), iset2

    pos = nx.spring_layout(g)
    ns = [g.node[v]['w'] for v in g.nodes()]
    nx.draw(g, pos, ax=ax1, node_color='#ffcccc',
            node_size=ns, with_labels=True)
    ns = [g.node[v]['w'] for v in iset]
    nx.draw_networkx_nodes(g, pos, ax=ax1, node_color='limegreen',
                           nodelist=iset, node_size=ns)

    pos = graphviz_layout(t, prog='twopi', args='')
    nx.draw(t, pos, ax=ax2, node_color='orange')
    nx.draw_networkx_labels(t, pos, ax=ax2,
                            labels=nx.get_node_attributes(t, 'label'))
    ax2.margins(0.2)

    plt.tight_layout()
    plt.show()
