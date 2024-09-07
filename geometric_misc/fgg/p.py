from fgg import fgg
import networkx as nx
import matplotlib.pyplot as plt


def gen(n=5):
    f = fgg(n)
    f.gen()
    g = nx.Graph()
    g.add_edges_from(f.get_edges())
#    pos = nx.spectral_layout(g)
#    pos = nx.spring_layout(g)
    pos = nx.circular_layout(g)
    return (f, g, pos)


def topo(f, g, pos):
    nx.draw_networkx_nodes(g, pos, alpha=0.09, node_size=500)
    nx.draw_networkx_edges(g, pos, alpha=0.4)


def labels(f, g, pos):
    labels = {v: f.print_dss(dss) for dss, v in f.get_ref_table().items()}
    lapos = {v: pos[v] + 0.05 for v in g.nodes()}
    nx.draw_networkx_labels(g, pos=lapos, labels=labels, font_size=7)


#def nests(f, g, pos, scalefactor=0.04):
def nests(f, g, pos, scalefactor=0.10):
    for v in g.nodes():
        tg = nx.Graph(f.get_triangulation_edges(v))
        poss = nx.circular_layout(tg)
        poss[0], poss[1] = poss[1], poss[0]
        for node in tg.nodes():
            poss[node] = poss[node] * scalefactor + pos[v]
        nx.draw_networkx_edges(tg, pos=poss)


if __name__ == '__main__':
    plt.figure(figsize=(8, 8), facecolor='white')
    plt.axis('off')
    plt.gca().autoscale(tight=True)

    f, g, pos = gen(6)
#    topo(f, g, pos)
#    labels(f, g, pos)
    nests(f, g, pos)

#    plt.savefig('basic_plot_7.png')
#    plt.autoscale()
    e = 0.1
    plt.gca().set_xlim(-1-e, 1+e)
    plt.gca().set_ylim(-1-e, 1+e)
    plt.tight_layout()
    plt.savefig('x6.png')
    plt.show()
