from fgg import fgg
import itertools
import os
from zipfile import ZipFile, ZIP_DEFLATED
import matplotlib.pyplot as plt
import networkx as nx


def calc_pos(sp):
    pos = {}
    pos[sp[0][0]], pos[sp[0][-1]] = [0, 0], [len(sp[0]) - 1, 0]
    h = [0] * (len(sp[0]) - 1)
    for p in sp:
        for i, v in enumerate(p[1:-1], 1):
            if v not in pos:
                pos[v] = [i, h[i]]
                h[i] += 0.5
    return pos


def common_diag(se, te):
    sd = [s for s in se[1:-1] if s[0] - s[1] != 1]
    td = [t for t in te[1:-1] if t[0] - t[1] != 1]
    return [x for x in sd if x in td]


def draw_each_triang(f, g, pos, t, scalefactor=0.2):
    ttf = f.get_triangulation_edges(t)
    for v in g.nodes():
        tg = nx.Graph()
        tf = f.get_triangulation_edges(v)
        tg.add_edges_from(tf)
        poss = nx.circular_layout(tg)
        for node in tg.nodes():
            poss[node] = poss[node] * scalefactor + pos[v]
        nx.draw_networkx_edges(tg, pos=poss)
        if v == t:
            continue
        nx.draw_networkx_edges(tg, pos=poss, edgelist=common_diag(tf, ttf),
                               edge_color='r', width=1.5)


def path_plotter(f, fg, sp):
    el = list(set(itertools.chain.from_iterable([zip(p, p[1:]) for p in sp])))
    g = nx.Graph()
    g.add_edges_from(el)

    pos = calc_pos(sp)
    nx.draw_networkx_edges(g, pos, alpha=0.2)
    draw_each_triang(f, g, pos, sp[0][-1])

    title = "(%d, %d)" % (sp[0][0], sp[0][-1])
    title += ", distance: %d" % (len(sp[0]) - 1)
    title += ", #-of paths: %d" % len(sp)
    return title


def save_all(f, fg):
    plt.figure(figsize=(10, 8))
    pvc = f.get_polygon_vertex_count()
    files = []
    for s, t in itertools.combinations(range(f.get_vertex_count()), 2):
        plt.cla()
        plt.hold(True)
        sp = [p for p in nx.all_shortest_paths(fg, source=s, target=t)]
        if len(sp[0]) - 1 <= pvc - 3:
            continue
        title = path_plotter(f, fg, sp)
        fname = "path_plotter-%d-output-(%d, %d).png" % (pvc, s, t)
        plt.axis('equal')
        plt.title(title)
        plt.savefig(fname)
        files.append(fname)
    with ZipFile('path_plotter-output-%d.zip' % (pvc), 'w', ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f)
    for f in files:
        os.remove(f)


if __name__ == '__main__':
    f = fgg(6)
    f.gen()
    fg = nx.Graph()
    fg.add_edges_from(f.get_edges())
    save_all(f, fg)
