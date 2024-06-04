from matplotlib import pyplot as plt
import networkx as nx


def cartesian_tree(a):
    l, r = left_nearest_smaller(a), right_nearest_smaller(a)
    root, lc, rc = None, {}, {}
    for i, ai in enumerate(a):
        if i == l[i] and i == r[i]:
            root = i
        elif i == l[i]:     # and ai != r[i]:
            assert i == l[i] and i != r[i]
            lc[r[i]] = i
        elif i == r[i]:     # and ai != l[i]:
            assert i != l[i] and i == r[i]
            rc[l[i]] = i
        else:
            assert i != l[i] and i != r[i]
            if a[l[i]] > a[r[i]]:
                rc[l[i]] = i
            else:
                lc[r[i]] = i
    return root, lc, rc


def left_nearest_smaller(a):
    s, m = [], {}
    for i, ai in enumerate(a):
        while s and a[s[-1]] >= ai:
            s.pop()
        m[i] = s[-1] if s else i
        s.append(i)
    return m


def right_nearest_smaller(a):
    s, m = [], {}
    for i, ai in reversed(list(enumerate(a))):
        while s and a[s[-1]] >= ai:
            s.pop()
        m[i] = s[-1] if s else i
        s.append(i)
    return m


def draw(a, lc, rc):
    ct, pos = enc(a, lc, rc)
    nx.draw_networkx_nodes(ct, pos, node_color='#ffcccc').set_edgecolor('k')
    nx.draw_networkx_edges(ct, pos)
    nx.draw_networkx_labels(ct, pos)
    pos2, labels2 = {}, {}
    for i, ai in enumerate(a):
        pos2[ai] = (pos[ai][0]+0.0, pos[ai][1]+0.8)
        labels2[ai] = i
    nx.draw_networkx_labels(ct, pos2, labels=labels2, font_color='g')

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')


def enc(a, left, right):
    t, pos = nx.DiGraph(), {}
    for i, ai in enumerate(a):
        if i in left:
            t.add_edge(ai, a[left[i]])
        if i in right:
            t.add_edge(ai, a[right[i]])
        pos[ai] = (i, len(a)-ai)
    return t, pos


def gen(n=15):
    # return [7, 8, 1, 5, 3, 4, 2, 0, 9, 6]
    # return [4, 6, 3, 5, 1, 4, 6, 4, 5, 2, 6, 3]
    from random import seed, shuffle
    seed(0)
    shuffle(a := list(range(n)))
    return a


if __name__ == '__main__':
    a = gen()
    print('\033[1minput:\033[0m', a)
    _l = left_nearest_smaller(a)
    print('\033[1m[nearest smaller]\033[0m')
    print('\033[1mleft:\033[0m', [a[i] for i in _l.values()])
    _r = right_nearest_smaller(a)
    print('\033[1mright:\033[0m', [a[i] for i in _r.values()])

    _, _l, _r = cartesian_tree(a)
#    import matplotlib
#    matplotlib.use('module://backend_ipe')
    draw(a, _l, _r)
#    plt.savefig('ct_ex1.ipe', format='ipe')
    plt.tight_layout()
    plt.show()
