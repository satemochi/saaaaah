from scpgen import scpgen
from matplotlib import pyplot as plt
from matplotlib.colors import CSS4_COLORS
from lpsolve55 import lpsolve, IMPORTANT


def det_rounding(scp_gen):
    # linear reluxation
    lp = lpsolve('make_lp', 0, scp_gen.covering_set_num)
    lpsolve('set_obj_fn', lp, scp_gen.cost)
    for v in scp_gen.get_rows():
        lpsolve('add_constraint', lp, v, 'GE', 1)
    for i in range(1, scp_gen.covering_set_num+1):
        lpsolve('set_lowbo', lp, i, 0)
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('solve', lp)

    # deterministic rounding
    float_ans = lpsolve('get_variables', lp)[0]
    _, f = scp_gen.get_f()
    return [1 if x >= 1.0/float(f) else 0 for x in float_ans]


def draw(sc, I=None, ax=None):
    n, m = sc.universal_set_size, sc.covering_set_num
    if I is None:
        I = [1] * m
    if ax is None:
        ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(color="#cccccc")
    cnames = CSS4_COLORS.values()[59:]
    for y, val in enumerate(I):
        if val == 0:
            continue
        c = cnames[y]
        for e in range(sc.sizes[y]):
            x = sc.sets[y][e]
            rect = plt.Rectangle((x-0.5, y-0.5), 1, 1, alpha=0.75, color=c)
            ax.add_patch(rect)

if __name__ == '__main__':
    sc = scpgen(10, 20, 0.5, 0)
    f, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True,
                                 figsize=(13, 3))
    n, m = sc.universal_set_size, sc.covering_set_num
    plt.xlim([-0.5, n - 0.5])
    plt.ylim([-0.5, m - 0.5])
    plt.xticks(range(n), range(n))
    plt.yticks(range(m), range(m))

    draw(sc, ax=ax1)
    ans = det_rounding(sc)
    draw(sc, I=ans, ax=ax2)

    plt.tight_layout()
    plt.savefig('lp_rounding_example.png', bbox_inches='tight')
    plt.show()
