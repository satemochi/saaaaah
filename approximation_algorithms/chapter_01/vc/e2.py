from lpsolve55 import lpsolve, IMPORTANT
from matplotlib import pyplot as plt
from matplotlib.colors import CSS4_COLORS
import networkx as nx
from networkx.algorithms import bipartite
from tutte_embedding import fix_outer_cycle_pos, fix_all_pos


class vc_mat:
    def __init__(self, g):
        self.nv = nx.number_of_nodes(g)
        self.ne = nx.number_of_edges(g)
        self.__e = g.edges()
        self.__s = [[(v, w) if v < w else (w, v) for w in g[v]]
                    for v in g.nodes_iter()]

    def __is_contained(self, v, e):
        return 1 if e in self.__s[v] else 0

    def cover_constraints(self):
        for e in self.__e:
            yield [self.__is_contained(v, e) for v in range(self.nv)]

    def matching_constraints(self):
        for v in range(self.nv):
            yield [self.__is_contained(v, e) for e in self.__e]

    def draw(self, I=None, ax=None, title=None):
        if I is None:
            I = range(self.nv)
        if ax is None:
            ax = plt.gca()
        cnames = CSS4_COLORS.values()[59:]
        for y in I:
            c = cnames[y]
            for x in range(self.ne):
                if self.__is_contained(y, self.__e[x]):
                    rect = plt.Rectangle((x-0.5, y-0.5), 1, 1, alpha=0.75,
                                         color=c)
                    ax.add_patch(rect)
        ax.set_xlim([-0.5, self.ne-0.5])
        ax.set_ylim([-0.5, self.nv-0.5])
        ax.set_xticks(range(self.ne))
        ax.set_yticks(range(self.nv))
        ax.set_xticklabels([str(e) for e in self.__e], rotation=90)
        ax.set_axisbelow(True)
        ax.grid(color='#cccccc')
        if title:
            ax.set_title(title)


def vc(ip):
    lp = lpsolve('make_lp', 0, ip.nv)
    lpsolve('set_obj_fn', lp, [1] * ip.nv)
    for c in ip.cover_constraints():
        lpsolve('add_constraint', lp, c, 'GE', 1)
    lpsolve('set_binary', lp, [1] * ip.nv)
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('solve', lp)
    return [v for v, b in enumerate(lpsolve('get_variables', lp)[0]) if b > 0]


def mat(ip):
    lp = lpsolve('make_lp', 0, ip.ne)
    lpsolve('set_maxim', lp)
    lpsolve('set_obj_fn', lp, [1] * ip.ne)
    for c in ip.matching_constraints():
        lpsolve('add_constraint', lp, c, 'LE', 1)
    lpsolve('set_binary', lp, [1] * ip.ne)
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('solve', lp)
    ans = lpsolve('get_variables', lp)[0]
    E = g.edges()
    return [E[e] for e, b in enumerate(ans) if b > 0]


def draw(g, ax=None, title=None, vl=None, el=None):
    if not ax:
        ax = plt.gca()
#    pos = nx.get_node_attributes(g, 'coord')
    pos = nx.circular_layout(g)
    nx.draw_networkx(g, pos=pos, ax=ax, node_color='g', with_labels=False,
                     node_size=150)
    nx.draw_networkx_labels(g, pos=pos, ax=ax, font_size=6,
                            font_color='gold', font_weight='bold')
    if vl:
        nx.draw_networkx_nodes(g, pos=pos, ax=ax, node_color='r',
                               node_size=170, node_shape='s', nodelist=vl)
    if el:
        nx.draw_networkx_edges(g, pos=pos, ax=ax, edge_color='r', width=3,
                               edgelist=el)
    ax.set_title(title)
    ax.set_axis_off()
    ax.set_aspect('equal')


if __name__ == '__main__':
#    g = nx.petersen_graph()
    g = bipartite.random_graph(5, 5, 0.7, seed=1)
    fix_outer_cycle_pos(g, nx.cycle_basis(g)[3])
    fix_all_pos(g)

    gs_kw = {'height_ratios':[2, 1]}
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 6),
                                                 gridspec_kw=gs_kw)
    ip = vc_mat(g)
    vl = vc(ip)
    draw(g, ax1, 'vertex cover', vl=vl)
    draw(g, ax2, 'matching', el=mat(ip))
    ip.draw(ax=ax3, title='input')
    ip.draw(ax=ax4, I=vl, title='set cover')

#    plt.savefig('vc_mat_on_petersen.png', bbox_inches='tight')
    plt.savefig('vc_mat_on_random_bipartite.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
