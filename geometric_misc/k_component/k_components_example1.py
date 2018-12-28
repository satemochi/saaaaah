import operator
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import networkx as nx
from networkx.algorithms import approximation as apxa
import numpy as np


if __name__ == '__main__':
    n, radius, seed = 700, 0.05, 0
    g = nx.random_geometric_graph(n, radius, seed=seed)
    k_components = apxa.k_components(g)

    result = {}
    for k, comps in sorted(k_components.items(), key=operator.itemgetter(0)):
        for comp in comps:
            for node in comp:
                result[node] = k

    plt.figure(figsize=(10, 10))
    pos = nx.get_node_attributes(g, 'pos')
    _max = max(k_components.keys()) + 1
    sizes = [2.0**result[v] + 20 if v in result else 10 for v in g.nodes()]
    cmap = cm.rainbow
    colors = cmap(map(lambda c: float(c) / _max,
                      [result[v] if v in result else 0 for v in g.nodes()]))
    nx.draw_networkx(g, pos=pos, node_size=1, alpha=0.2, with_labels=False)
    nx.draw_networkx_nodes(g, pos=pos, node_size=sizes, node_color=colors)
    plt.gca().collections[2].set_edgecolor('#000000')

    plt.gca().set_aspect('equal')
    plt.axis('off')
    sm = cm.ScalarMappable(cmap=cmap)
    sm._A = []
    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes('right', size='2%', pad='1%')

    cbar = plt.colorbar(sm, cax=cax, ticks=np.linspace(0, 1, _max+1))
    cbar.ax.set_yticklabels(range(_max))
    plt.tight_layout()
    plt.savefig('k_components_1.png', bbox_inches='tight')
    plt.show()
