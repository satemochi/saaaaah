from scpgen import scpgen
from lpsolve55 import lpsolve, IMPORTANT


def solve_lp(scp_gen):
    print "--- SOLVE LINEAR PROGRAMMING ---"
    n = scp_gen.universal_set_size

    lp = lpsolve('make_lp', 0, n)
    lpsolve('set_maxim', lp)
    lpsolve('set_obj_fn', lp, [1] * n)

    for i, v in enumerate(scp_gen.get_cols()):
        lpsolve('add_constraint', lp, v, 'LE', scp_gen.cost[i])
    lpsolve('set_lowbo', lp, [0] * n)

    lpsolve('write_lp', lp, 'd.lp')
    lpsolve('set_verbose', lp, IMPORTANT)

    lpsolve('solve', lp)
    res = lpsolve('get_objective', lp)
    print "solution of lp:", res
    V = lpsolve('get_variables', lp)[0]
    print "solution vector:", V

    ans = 0
    AV = []
    for i, v in enumerate(scp_gen.get_cols()):
        s = sum(V[j] for j, e in enumerate(v) if e != 0)
        if s == scp_gen.cost[i]:
            AV.append(1)
            ans += s
        else:
            AV.append(0)

    _, f = scp_gen.get_f()
    print "f:", f, "1/f", 1.0 / float(f)
    print "deterministic rounding:", AV
    print "result of linear relaxation:", ans
    print "alpha: ", ans / res, "\n"

    if scp_gen.is_covered([i for i, v in enumerate(AV) if v == 1]):
        print 'covered'
    else:
        print 'uncovered'

    lpsolve('delete_lp', lp)

if __name__ == '__main__':
    scp_gen = scpgen(10, 100, 0.5, 0)
    solve_lp(scp_gen)
