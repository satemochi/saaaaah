from scpgen import scpgen
from datetime import datetime, timedelta
import sys
from matplotlib import pyplot as plt
from matplotlib.colors import CSS4_COLORS
from lpsolve55 import lpsolve, IMPORTANT


def det_rounding_dual(scp_gen):
    # linear reluxation
    n = scp_gen.universal_set_size
    lp = lpsolve('make_lp', 0, n)
    lpsolve('set_maxim', lp)
    lpsolve('set_obj_fn', lp, [1] * n)
    for i, v in enumerate(scp_gen.get_cols()):
        lpsolve('add_constraint', lp, v, 'LE', scp_gen.cost[i])
    lpsolve('set_lowbo', lp, [0] * n)
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('solve', lp)

    # deterministic rounding
    float_ans = lpsolve('get_variables', lp)[0]
    lpsolve('delete_lp', lp)
    I = []
    for i, v in enumerate(scp_gen.get_cols()):
        s = sum(float_ans[j] for j, e in enumerate(v) if e != 0)
        if  s == scp_gen.cost[i]:
            I.append(1)
        else:
            I.append(0)
    return I


def primal_dual(scp_gen):
    n = scp_gen.universal_set_size
    S = set([])     # for checking whether the universal set is covered
    y = [0] * n
    I = [0] * scp_gen.covering_set_num
    for i in range(n):
        if len(S) == n: break
        if i in S: continue
        min_w, ell = sys.maxint, 0
        for j in scp_gen.get_sets(i):
            diff = scp_gen.cost[j] - sum([y[e] for e in scp_gen.sets[j]])
            if min_w > diff:
                min_w, ell = diff, j
        y[i] = min_w
        I[ell] = 1
        S |= set(scp_gen.get_sets(ell))
    return I

def experiment():
#    N = range(20, 250, 20)
    N = range(20, 100, 20)
    elp, epd = [], []
    for n in N:
        trials = 100
        et_lp, et_pd = timedelta(), timedelta()
        for seed in range(trials):
            sc = scpgen(n, n, 0.5, seed)

            start = datetime.now()
            ans_drt = det_rounding_dual(sc)
            et_lp += datetime.now() - start

            start = datetime.now()
            ans_pd = primal_dual(sc)
            et_pd += datetime.now() - start
        elp.append(et_lp.seconds + et_lp.microseconds * 1.0e-6)
        epd.append(et_pd.seconds + et_pd.microseconds * 1.0e-6)
    return (N, elp, epd)


if __name__ == '__main__':
    n, el, ep = experiment()
    print n, el, ep
    plt.plot(n, el)
    plt.plot(n, ep)
#    plt.gca().set_xticklabels(n)
    plt.show()
