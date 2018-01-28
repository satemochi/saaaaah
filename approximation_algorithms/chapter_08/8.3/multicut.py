from lpsolve55 import lpsolve, IMPORTANT
from matplotlib import pyplot as plt
import networkx as nx


def gen():
    g = nx.LCF_graph(20, [1, 3, 14], 5)
    pairs = [(0, 12), (1, 5), (1, 19), (2, 11), (3, 4),
             (3, 9), (3, 18), (6, 15), (10, 14)]
    print pairs
    costs = [1] * nx.number_of_edges(g) * 2
    return (g, costs, pairs)


def solve(ug, costs, pairs):
    g = nx.to_directed(ug)
    k, n, m = len(pairs), nx.number_of_nodes(g), nx.number_of_edges(g)
    N = len(costs) + n * k
    lp = lpsolve('make_lp', 0, N)
    lpsolve('set_obj_fn', lp, costs + [0] * n * k)

    sources = [s for (s, t) in p]
    zero = [0] * N
    constraint_coefficients = [0] * N
    for i, (u, v) in enumerate(g.edges()):
        constraint_coefficients[i] = 1
        for j, s in enumerate(sources):
            constraint_coefficients[m + j * n + u] = -1
            constraint_coefficients[m + j * n + v] = 1
            lpsolve('add_constraint', lp, constraint_coefficients, 'GE', 0)
            constraint_coefficients[m + j * n + u] = 0
            constraint_coefficients[m + j * n + v] = 0
        constraint_coefficients[i] = 0
    for j, (s, t) in enumerate(pairs):
        zero[m + j * n + s] = 1
        lpsolve('add_constraint', lp, zero, 'EQ', 1)
        zero[m + j * n + s] = 0
        zero[m + j * n + t] = 1
        lpsolve('add_constraint', lp, zero, 'EQ', 0)
        zero[m + j * n + t] = 0
    lpsolve('set_int', lp, [1] * N)
    lpsolve('set_lowbo', lp, [0] * N)
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('write_lp', lp, 'multicut_lpsolve.lp')
    lpsolve('solve', lp)
    val = lpsolve('get_variables', lp)[0][:m]
    return [e for i, e in enumerate(g.edges()) if val[i] == 1]


def draw(g, pairs, cut):
    # pairs of dark and light colors
    colors = [('Yellow', '#FFdd90'), ('#888888', '#DDDDDD'),
              ('Dodgerblue', 'Aqua'), ('DarkGreen', 'GreenYellow'),
              ('DarkViolet', 'Violet'), ('SaddleBrown', 'Peru'),
              ('Red', 'Tomato'), ('DarkGoldenRod', 'Gold'),
              ('#444444', '#aaaaaa')]

    node_colors = ['w'] * nx.number_of_nodes(g)
    for i, (s, _) in enumerate(pairs):
        node_colors[s] = colors[i][0]
        for t in [t for (s0, t) in pairs if s0 == s]:
            node_colors[t] = colors[i][1]

    pos = {0: (0.07, 0.7), 1: (0.18, 0.78), 2: (0.26, 0.45),
           3: (0.27, 0.66), 4: (0.42, 0.79), 5: (0.56, 0.95),
           6: (0.6,  0.8), 7: (0.64, 0.65), 8: (0.55, 0.37),
           9: (0.65, 0.3), 10: (0.77, 0.46), 11: (0.83, 0.66),
           12: (0.90, 0.41), 13: (0.70, 0.1), 14: (0.56, 0.16),
           15: (0.40, 0.17), 16: (0.28, 0.05), 17: (0.03, 0.38),
           18: (0.01, 0.66), 19: (0, 0.95)}
    remaining_edges = [(u, v) for u, v in g.edges()
                       if (u, v) not in cut and (v, u) not in cut]
    nx.draw_networkx(g, pos, edgelist=remaining_edges,
                     node_color=node_colors)
    nx.draw_networkx_edges(g, pos, edgelist=cut, edge_color='r')

    plt.gca().axes.get_xaxis().set_ticks([])
    plt.gca().axes.get_yaxis().set_ticks([])
    plt.tight_layout()
    plt.savefig('multicut_example1.png', bbox_inches='tight')
    plt.show()


def test_connectivity(g, pairs, cut):
    remaining_edges = [(u, v) for u, v in g.edges()
                       if (u, v) not in cut and (v, u) not in cut]
    cut_graph = nx.Graph()
    cut_graph.add_edges_from(remaining_edges)
    if all(not nx.has_path(cut_graph, s, t) for s, t in pairs):
        print 'all pairs are not reachable.'
    else:
        print 'there exists at least one reachable pair.'


if __name__ == '__main__':
    g, c, p = gen()
    cut = solve(g, c, p)
    test_connectivity(g, p, cut)
    draw(g, p, cut)
