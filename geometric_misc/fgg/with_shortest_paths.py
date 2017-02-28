from fgg import fgg
import networkx as nx
import matplotlib.pyplot as plt


def gen(n=6):
    f = fgg(n)
    f.gen()
    g = nx.Graph()
    g.add_edges_from(f.get_edges())
#    pos = nx.spectral_layout(g)
    pos = nx.spring_layout(g)
#    pos = nx.circular_layout(g)
    return (f, g, pos)


def topo(f, g, pos):
    nx.draw_networkx_nodes(g, pos, alpha=0.09, node_size=500)
    nx.draw_networkx_edges(g, pos, alpha=0.4)


def labels(f, g, pos):
    labels = {v: f.print_dss(dss) for dss, v in f.get_ref_table().items()}
    lapos = {v: pos[v] + 0.05 for v in g.nodes()}
    nx.draw_networkx_labels(g, pos=lapos, labels=labels, font_size=7)


def nests(f, g, pos, scalefactor=0.04):
    for v in g.nodes():
        tg = nx.Graph()
        tg.add_edges_from(f.get_triangulation_edges(v))
        poss = nx.circular_layout(tg)
        for node in tg.nodes():
            poss[node] = poss[node] * scalefactor + pos[v]
        nx.draw_networkx_edges(tg, pos=poss)


def paths(g, pos):
    st = [1, 10]
    plist = [p for p in nx.all_shortest_paths(g, source=st[0], target=st[1])]
    for p in plist:
        nx.draw_networkx_edges(g, pos, edgelist=zip(p, p[1:]), width=5,
                               alpha=0.3, edge_color='g')
    nx.draw_networkx_nodes(g, pos, nodelist=st, alpha=0.4, node_size=500)
    title = 'distance: ' + str(len(plist[0]) - 1)
    title += ',  variation: ' + str(len(plist))
    plt.title(title)


if __name__ == '__main__':
    plt.figure(figsize=(8, 8), facecolor='white')
    plt.axis('off')
    plt.gca().autoscale(tight=True)

    f, g, pos = gen()
    topo(f, g, pos)
    nests(f, g, pos)
    paths(g, pos)

    plt.savefig('7.png')
    plt.show()
