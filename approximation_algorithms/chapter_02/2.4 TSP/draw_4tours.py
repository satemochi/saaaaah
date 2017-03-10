import itertools
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from lpsolve55 import lpsolve, IMPORTANT, Infinite


def gen(n=2, k=3):
    P = np.random.random((n, 2)) + np.random.randint(0, 10, 2)
    for i in range(k-1):
        pts = np.random.random((n, 2)) + np.random.randint(0, 10, 2)
        P = np.concatenate((P, pts))
    return P


def get_closest_pair(P):
    closest_pair, d = (0, 1), np.linalg.norm(P[0] - P[1])
    for i, j in itertools.combinations(range(len(P)), 2):
        if d > np.linalg.norm(P[i] - P[j]):
            d = np.linalg.norm(P[i] - P[j])
            closest_pair = (i, j)
    return closest_pair


def get_nearest_addition_tour(P):
    S = range(len(P))
    i, j = get_closest_pair(P)
    del S[j]
    del S[i]
    tour = [i, j, i]
    while len(S) > 0:
        min_sid, correspond_tid = 0, 0
        mind = np.linalg.norm(P[S[0]] - P[tour[0]])
        for si, tj in itertools.product(range(len(S)), range(len(tour) - 1)):
            if mind > np.linalg.norm(P[S[si]] - P[tour[tj]]):
                mind = np.linalg.norm(P[S[si]] - P[tour[tj]])
                min_sid = si
                correspond_tid = tj
        tour.insert(correspond_tid + 1, S[min_sid])
        del S[min_sid]
    return tour


def get_complete_graph(P):
    g = nx.Graph()
    edges = []
    for i, j in itertools.combinations(range(len(P)), 2):
        edges.append((i, j, np.linalg.norm(P[i] - P[j])))
    g.add_weighted_edges_from(edges)
    return g


def draw_minimum_spanning_tree(P, Te):
    lines = []
    for u, v in Te:
        lines.append([P[u], P[v]])
    plt.gca().add_collection(mc.LineCollection(lines, colors='b',
                                               linewidth=2, zorder=1))


def extract_odd_degree_vertices(Te):
    tg = nx.Graph()
    tg.add_edges_from(Te)
    O = []
    for v in tg.nodes():
        if tg.degree(v) % 2 != 0:
            O.append(v)
    return O


def get_perfect_matching_on_subgraph_induced_by(G, O):
    sg = G.subgraph(O)
    for u, v in sg.edges_iter():
        sg[u][v]['weight'] *= (-1)
    m = nx.max_weight_matching(sg, maxcardinality=True)
    return [[u, v] for u, v in m.iteritems() if u < v]


def get_double_tree_tour(n, Te):
    Eulerian_Graph = nx.MultiGraph()
    Eulerian_Graph.add_edges_from(Te + Te)
    checked = [False] * n
    double_tree_tour = []
    for u, v in nx.eulerian_circuit(Eulerian_Graph):
        if not checked[u]:
            double_tree_tour.append(u)
            checked[u] = True
    double_tree_tour.append(double_tree_tour[0])
    return double_tree_tour


def get_christofides_tour(G, n, Te):
    O = extract_odd_degree_vertices(Te)
    pm = get_perfect_matching_on_subgraph_induced_by(G, O)
    eg = nx.MultiGraph()
    eg.add_edges_from(Te + pm)
    checked = [False] * n
    christofides_tour = []
    for u, v in nx.nx.eulerian_circuit(eg):
        if not checked[u]:
            christofides_tour.append(u)
            checked[u] = True
    christofides_tour.append(christofides_tour[0])
    return christofides_tour


def distance_matrix(P):
    return [np.linalg.norm(P[i] - P[j])
            for i, j in itertools.product(range(len(P)), range(len(P)))]

def incomming_constraints(n):
    N = n**2
    for j in range(n):
        const_vector = [0] * (N + n)
        for i in range(n):
            if i == j:
                continue
            const_vector[n * i + j] = 1
        yield const_vector

def outgoing_constraints(n):
    N = n**2
    for i in range(n):
        const_vector = [0] * (N + n)
        for j in range(n):
            if i == j:
                continue
            const_vector[n * i + j] = 1
        yield const_vector

def subtour_constraints(n):
    N = n**2
    for i in range(1, n):
        for j in range(1, n):
            if i == j:
                continue
            const_vector = [0] * (N + n)
            const_vector[n * i + j] = n
            const_vector[N + i] = 1
            const_vector[N + j] = -1
            yield const_vector

def set_bounds(lp, N, n):
    lpsolve('set_int', lp, [1] * (N + n))
    lpsolve('set_upbo', lp, [1] * N + [n - 1] * n)
    lpsolve('set_lowbo', lp, [0] * N + [1] * n)
    lpsolve('set_upbo', lp, N + 1, 0)
    lpsolve('set_lowbo', lp, N + 1, 0)

def set_constraints(lp, n):
    for v in incomming_constraints(n):
        lpsolve('add_constraint', lp, v, 'EQ', 1)
    for v in outgoing_constraints(n):
        lpsolve('add_constraint', lp, v, 'EQ', 1)
    for v in subtour_constraints(n):
        lpsolve('add_constraint', lp, v, 'LE', n - 1)

def config_lp(lp):
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('write_lp', lp, 'in_darw_tours.lp')


def get_mtz_ilp_tour(P):
    dmat = distance_matrix(P)
    n, N = len(P), len(dmat)

    lp = lpsolve('make_lp', 0, N + n)
    lpsolve('set_obj_fn', lp, dmat + [0] * len(P))
    set_constraints(lp, n)
    set_bounds(lp, N, n)
    config_lp(lp)

    lpsolve('solve', lp)

    tour = [0] * (n + 1)
    for i, v in enumerate(lpsolve('get_variables', lp)[0][N:]):
        tour[int(v)] = i
    return tour


def draw_tour(ax, P, tour, title="a: "):
    ax.scatter(P[:, 0], P[:, 1], color='r')
    lines = [[P[u], P[v]] for u, v in zip(tour[:-1], tour[1:])]
    ax.add_collection(mc.LineCollection(lines, colors='g',
                                               linewidth=3, zorder=-1))
    tour_length = 0.0
    for s, t in lines:
        tour_length += np.linalg.norm(s - t)
    ax.set_title(title + str(tour_length), fontsize=10)


def draw_tours(P):
    G = get_complete_graph(P)
    Te = [(u, v) for u, v, w in nx.minimum_spanning_edges(G)]

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')

    d_tour = get_double_tree_tour(len(P), Te)
    c_tour = get_christofides_tour(G, len(P), Te)
    a_tour = get_nearest_addition_tour(P)
    i_tour = get_mtz_ilp_tour(P)

    draw_tour(ax1, P, d_tour, "Double tree: ")
    draw_tour(ax2, P, c_tour, "Christofides': ")
    draw_tour(ax3, P, a_tour, "Nearest addition: ")
    draw_tour(ax4, P, i_tour, "MTZ formula: ")


if __name__ == '__main__':
    n, k = 5, 1
    P = gen(n, k * 1)
    draw_tours(P)
#    plt.savefig("chap02_tsp_tours.png", bbox_inches='tight')
    plt.show()
