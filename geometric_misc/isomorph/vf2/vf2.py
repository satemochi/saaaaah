from collections import OrderedDict as odict
import networkx as nx


def is_isomorphic(g1, g2):
    if has_valid_global_properties(g1, g2):
        try:
            return dict(next(iterate_isomorphisms(g1, g2)))
        except StopIteration:
            pass


def has_valid_global_properties(g1, g2):
    deg1, deg2 = dict(g1.degree()).values(), dict(g2.degree()).values()
    return (g1.order() == g2.order() and g1.size() == g2.size()
            and sorted(deg1) == sorted(deg2))


def iterate_isomorphisms(g1, g2):
    f1, f2, m1, m2 = odict(), odict(), odict(), odict()
    stack = [generate_candidates(g1, g2, f1, f2, m1, m2)]
    while stack:
        try:
            v1, v2 = next(stack[-1])
            if is_syntactic_feasible(g1[v1], g2[v2], f1, f2, m1, m2):
                f1[v1], f2[v2] = v2, v1
                if len(f1) == g2.order():
                    yield f1
                    f1.popitem(), f2.popitem()
                else:
                    update_state(g1, v1, f1, m1), update_state(g2, v2, f2, m2)
                    stack.append(generate_candidates(g1, g2, f1, f2, m1, m2))
        except StopIteration:
            restore_state(f1, m1), restore_state(f2, m2)
            stack.pop()


def generate_candidates(g1, g2, f1, f2, m1, m2):
    t1, t2 = [v for v in m1 if v not in f1], [v for v in m2 if v not in f2]
    (t, v2) = (t1, min(t2)) if t1 and t2 else \
              ([v for v in g1 if v not in f1], min(set(g2) - set(f2)))
    for v1 in t:
        yield (v1, v2)


def is_syntactic_feasible(n1, n2, f1, f2, m1, m2):
    if (is_invalid_neighbor_constraint(n1, n2, f1, f2) or
            is_invalid_look_ahead_1(n1, n2, f1, f2, m1, m2) or
            is_invalid_look_ahead_2(n1, n2, m1, m2)):
        return False
    return True


def is_invalid_neighbor_constraint(n1, n2, f1, f2):
    return (len(n1) != len(n2) or any((u1 in f1 and f1[u1] not in n2 or
            u2 in f2 and f2[u2] not in n1) for u1, u2 in zip(n1, n2)))


def is_invalid_look_ahead_1(n1, n2, f1, f2, m1, m2):
    r1 = sum(1 for u in n1 if u in m1 and u not in f1)
    r2 = sum(1 for u in n2 if u in m2 and u not in f2)
    return r1 != r2


def is_invalid_look_ahead_2(n1, n2, m1, m2):
    r1 = sum(1 for u in n1 if u not in m1)
    r2 = sum(1 for u in n2 if u not in m2)
    return r1 != r2


def update_state(g, v, f, m):
    m[v] = len(f) if v not in m else m[v]
    for u in f:
        for v in g[u]:
            if v not in f and v not in m:
                m[v] = len(f) + 1


def restore_state(f, m):
    while m:
        v, d = m.popitem()
        if d <= len(f) - 1:
            m[v] = d
            break
    if f:
        f.popitem()


def gen():
    g1 = nx.frucht_graph()
    g2 = nx.LCF_graph(12, [-5, -2, -4, 2, 5, -2, 2, 5, -2, -5, 4, 2], 1)
#    print(nx.is_isomorphic(g1, g2))
#    g1 = nx.cubical_graph()
#    g2 = nx.LCF_graph(8, [3, -3], 4)
    return g1, g2


if __name__ == '__main__':
    g1, g2 = gen()
    f = is_isomorphic(g1, g2)
    print(f)
    pos2 = nx.spring_layout(g2)
    pos1 = {v: pos2[f[v]] for v in g1}

    from matplotlib import pyplot as plt
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    nx.draw_networkx(g1, pos1, ax=ax1, node_color='orange')
    nx.draw_networkx(g2, pos2, ax=ax2, node_color='#ffcccc')

    ax1.set_aspect('equal')
    ax2.set_aspect('equal')
    ax1.axis('off')
    ax2.axis('off')
    plt.savefig('frucht_vf2_ex2.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
