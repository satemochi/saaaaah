from collections import OrderedDict
from matplotlib import pyplot as plt
import networkx as nx


def gen():
    g1 = nx.frucht_graph()
    g2 = nx.LCF_graph(12, [-5, -2, -4, 2, 5, -2, 2, 5, -2, -5, 4, 2], 1)
#    print(nx.is_isomorphic(g1, g2))
#    g1 = nx.cubical_graph()
#    g2 = nx.LCF_graph(8, [3, -3], 4)
    return g1, g2


def is_isomorphic(g1, g2):
    if not verify_global_properties(g1, g2):
        return False
    try:
        x = next(iterate_isomorphisms(g1, g2))
        print(dict(x))
        return True
    except StopIteration:
        return False


def verify_global_properties(g1, g2):
    return (g1.order() == g2.order() and g1.size() == g2.size()
            and is_same_degree_sequance_pair(g1.degree(), g2.degree()))


def is_same_degree_sequance_pair(deg1, deg2):
    return sorted(d for _, d in deg1()) == sorted(d for _, d in deg2())


def iterate_isomorphisms(g1, g2):
    f1, f2 = OrderedDict(), OrderedDict()
    m1, m2 = OrderedDict(), OrderedDict()
    stack = [generate_candidates(g1, g2, f1, f2, m1, m2)]
    while stack:
        try:
            v1, v2 = next(stack[-1])
            if verify_syntactic_feasibility(g1[v1], g2[v2], f1, f2, m1, m2):
                f1[v1], f2[v2] = v2, v1
                if len(f1) == g2.order():
                    yield f1
                    f1.popitem()
                    f2.popitem()
                else:
                    update_state(g1, v1, f1, m1)
                    update_state(g2, v2, f2, m2)
                    stack.append(generate_candidates(g1, g2, f1, f2, m1, m2))
        except StopIteration:
            restore_state(f1, m1)
            restore_state(f2, m2)
            stack.pop()


def generate_candidates(g1, g2, f1, f2, m1, m2):
    t1, t2 = [v for v in m1 if v not in f1], [v for v in m2 if v not in f2]
    (t, v2) = (t1, min(t2)) if t1 and t2 else \
              ([v for v in g1 if v not in f1], min(set(g2) - set(f2)))
    for v1 in t:
        yield (v1, v2)


def verify_syntactic_feasibility(n1, n2, f1, f2, m1, m2):
    if verify_neighbor_constraint(n1, n2, f1, f2):
        return False
    if verify_look_ahead_1(n1, n2, f1, f2, m1, m2):
        return False
    if verify_look_ahead_2(n1, n2, m1, m2):
        return False
    return True


def verify_neighbor_constraint(n1, n2, f1, f2):
    return any((u1 in f1 and (f1[u1] not in n2) or
                u2 in f2 and (f2[u2] not in n1))
               for u1, u2 in zip(n1, n2))


def verify_look_ahead_1(n1, n2, f1, f2, m1, m2):
    n1 = sum(1 for u in n1 if u in m1 and u not in f1)
    n2 = sum(1 for u in n2 if u in m2 and u not in f2)
    return n1 != n2


def verify_look_ahead_2(n1, n2, m1, m2):
    n1 = sum(1 for u in n1 if u not in m1)
    n2 = sum(1 for u in n2 if u not in m2)
    return n1 != n2


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


if __name__ == '__main__':
    g1, g2 = gen()
    print(is_isomorphic(g1, g2))

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    nx.draw_networkx(g1, ax=ax1, node_color='orange')
    nx.draw_networkx(g2, ax=ax2, node_color='#ffcccc')

    ax1.set_aspect('equal')
    ax2.set_aspect('equal')
    ax1.axis('off')
    ax2.axis('off')
    plt.tight_layout()
    plt.show()
