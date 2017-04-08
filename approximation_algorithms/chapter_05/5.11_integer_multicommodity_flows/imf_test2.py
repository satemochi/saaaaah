import networkx as nx
import matplotlib.pyplot as plt
from lpsolve55 import lpsolve, IMPORTANT
from pprint import pprint
import random


class integer_multicommodity_flows:
    def __init__(self, digraph, flows):
        assert nx.is_directed(digraph), '[digraph error]'
        self.__g = digraph
        self.__edges = g.edges()
        self.__flows = flows
        self.__nv = len(g.nodes())
        self.__ne = len(g.edges())
        self.__nf = len(flows)
        self.__n = self.__ne * self.__nf
        self.__nvar = self.__n + 1 + self.__nf
        self.__ncon = (self.__ne / 2) + (self.__nv * self.__nf) + (self.__nf)
        self.__lp = lpsolve('make_lp', 0, self.__nvar)

    def __repr__(self):
        s = "=== Integer multicommodity flows === \n"
        s += "number of nodes:\t" + str(self.__nv) + '\n'
        s += "number of edges:\t" + str(self.__ne) + '\n'
        s += "number of flows:\t" + str(self.__nf) + '\n'
        s += "number of variables:\t" + str(self.__nvar) + '\n'
        s += "number of constraints:\t" + str(self.__ncon) + '\n'
        return s

    def __set_objective(self):
        lpsolve('set_obj_fn', self.__lp,
                [0] * (self.__n) + [self.__n] + [1] * self.__nf)

    def __overwrap_constraints(self):
        checked = [False] * self.__ne
        for ei, e in enumerate(self.__edges):
            reverse = self.__edges.index((e[1], e[0]))
            if checked[ei]:
                continue
            v = [0] * self.__nvar
            v[self.__n] = 1
            for i in range(self.__nf):
                v[ei + self.__ne * i] = -1
                v[reverse + self.__ne * i] = -1
            lpsolve('add_constraint', self.__lp, v, 'GE', 0)
            checked[ei] = True
            checked[reverse] = True

    def __flow_constraints(self):
        for u in range(self.__nv):
            outgoing = [self.__edges.index(e) for e in self.__g.out_edges(u)]
            incoming = [self.__edges.index(e) for e in self.__g.in_edges(u)]

            for fi in range(self.__nf):
                v = [0] * self.__nvar
                for i in outgoing:
                    v[i + self.__ne * fi] = 1
                for i in incoming:
                    v[i + self.__ne * fi] = -1

                if u not in self.__flows[fi]:
                    lpsolve('add_constraint', self.__lp, v, 'EQ', 0)
                elif u == self.__flows[fi][0]:
                    lpsolve('add_constraint', self.__lp, v, 'EQ', 1)
                else:
                    lpsolve('add_constraint', self.__lp, v, 'EQ', -1)

    def __edge_constraints(self):
        checked = [False] * self.__ne
        for ei, e in enumerate(self.__edges):
            if checked[ei]:
                continue
            ri = self.__edges.index((e[1], e[0]))
            for fi in range(self.__nf):
                v = [0] * self.__nvar
                v[ei + self.__ne * fi] = 1
                v[ri + self.__ne * fi] = 1
                lpsolve('add_constraint', self.__lp, v, 'LE', 1)
            checked[ei] = True
            checked[ri] = True

    def __flow_size_constraints(self):
        bias = self.__n + 1
        for fi in range(self.__nf):
            v = [0] * self.__nvar
            v[bias + fi] = 1
            for ei in range(self.__ne):
                v[ei + self.__ne * fi] = -1
            lpsolve('add_constraint', self.__lp, v, 'GE', 0)

    def __set_constraints(self):
        self.__overwrap_constraints()
        self.__flow_constraints()
        self.__flow_size_constraints()

    def __set_bin(self, flag=True):
        if flag:
            lpsolve('set_binary', self.__lp,
                    [1] * (self.__n) + [0] * (1 + self.__nf))
        else:
            lpsolve('set_binary', self.__lp, [0] * self.__nvar)

    def __set_bounds(self):
        lpsolve('set_lowbo', self.__lp, [0] * self.__nvar)

    def __config(self):
        lpsolve('set_verbose', self.__lp, IMPORTANT)
        lpsolve('write_lp', self.__lp, 'imf.lp')

    def __lp_setting(self, flag=True):
        self.__set_objective()
        self.__set_constraints()
        self.__set_bounds()
        self.__set_bin(flag)
        self.__config()
        assert self.__ncon == lpsolve('get_Nrows', self.__lp), '[N constraint]'

    def __get(self, bin=True):
        if lpsolve('get_Nrows', self.__lp) == 0:
            self.__lp_setting(bin)
            lpsolve('solve', self.__lp)
        elif bin and lpsolve('is_binary', self.__lp, 1) == 0:
            self.__set_bin(bin)
            lpsolve('solve', self.__lp)
        elif not bin and lpsolve('is_binary', self.__lp, 1) == 1:
            self.__set_bin(bin)
            lpsolve('solve', self.__lp)

        var = lpsolve('get_variables', self.__lp)[0][:self.__n + 1]
        return (var[self.__n], var[:-1])

    def get(self, type='int'):
        if type in ['i', 'int']:
            return self.__get(True)
        elif type in ['f', 'float']:
            return self.__get(False)
        else:
            return (0.0, [])


def my_grid(m, n):
    r, c = range(m), range(n)
    g = nx.DiGraph()
    g.add_edges_from((n*i+j, n*(i-1)+j) for i in r for j in c if i > 0)
    g.add_edges_from((n*i+j, n*i+j-1) for i in r for j in c if j > 0)
    g.add_edges_from((n*i+j, n*(i+1)+j) for i in r for j in c if i < m-1)
    g.add_edges_from((n*i+j, n*i+j+1) for i in r for j in c if j < n-1)
    return g, {n*i+j: (j, i) for i in r for j in c}


def get_paths(g, var):
    ne = len(g.edges())
    flows = [var[i:i + ne] for i in range(0, len(var), ne)]
    paths, weights = [], []
    for f in flows:
        p, w = [], []
        for i, e in enumerate(f):
            if e > 0.0:
                p.append(g.edges()[i])
                w.append(e)
        paths.append(p)
        weights.append(w)
    return paths, weights


def integer_path(imf):
    o, var = imf.get()
    paths, weights = get_paths(g, var)
    return paths


def get_simple_paths(paths, s, t):
    sg = nx.DiGraph()
    sg.add_edges_from(paths)
    return [sp for sp in nx.all_simple_paths(sg, source=s, target=t)]


def cumulative_distribution(p, w, sp_list):
    pr = [0]
    for sp in sp_list:
        pr.append(pr[-1] + min(w[p.index(e)] for e in zip(sp[:-1], sp[1:])))
    return pr[1:]


def path_selection(pr, sp_list):
    r = random.random()
    """ This loop is needed by arithmetic precisions. """
    while pr[-1] < r:
        r = random.random()
    for i, val in enumerate(pr):
        if r < val:
            return zip(sp_list[i][:-1], sp_list[i][1:])


def float_path(flows, imf):
    o, var = imf.get('float')
    paths, weights = get_paths(g, var)
    selected_paths = []

    for k, (p, w) in enumerate(zip(paths, weights)):
        simple_paths = get_simple_paths(p, flows[k][0], flows[k][1])
        pr = cumulative_distribution(p, w, simple_paths)
        selected_paths.append(path_selection(pr, simple_paths))

    return selected_paths


def overwrap(paths):
    mg = nx.MultiGraph()
    for p in paths:
        mg.add_edges_from(p)
    return max(mg.number_of_edges(e[0], e[1]) for e in mg.edges())


def draw_paths(g, pos, paths, ax):
    col = "bgrcmy"
    nx.draw_networkx_edges(g, pos=pos, ax=ax, alpha=0.125, arrows=False)
    nx.draw_networkx_nodes(g, pos=pos, ax=ax, node_color='#ffaaff')
    for i, p in enumerate(paths):
        nx.draw_networkx_edges(g, pos=pos, ax=ax, edgelist=p, alpha=0.5,
                               edge_color=col[i % len(col)], width=2.0)
        nx.draw_networkx_nodes(g, pos=pos, ax=ax, node_color=col[i % len(col)],
                               nodelist=[flows[i][0], flows[i][1]])
    nx.draw_networkx_labels(g, pos=pos, ax=ax, font_size=10)


if __name__ == '__main__':
    g, pos = my_grid(3, 4)
    flows = [(0, 11), (3, 8), (4, 7), (5, 7)]

    imf = integer_multicommodity_flows(g, flows)
    print imf

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ipaths = integer_path(imf)
    draw_paths(g, pos, ipaths, ax1)
    ax1.title.set_text('Integer programing')
    print
    print '====== integer ======'
    print overwrap(ipaths), "overwrap(s).\nThe flows:", flows
    print "path(s):"
    pprint(ipaths)

    random.seed(0)
    fpaths = float_path(flows, imf)
    draw_paths(g, pos, fpaths, ax2)
    ax2.title.set_text('Randomized Rounding')
    print
    print '====== float ======'
    print overwrap(fpaths), "overwrap(s).\nThe flows:", flows
    print "path(s):"
    pprint(fpaths)

    ax1.axis('off')
    ax2.axis('off')
    plt.savefig('imf_ex_fig.png', bbox_inches='tight', dpi=120)
#    plt.tight_layout()
#    plt.show()
