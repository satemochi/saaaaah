from scpgen import scpgen
from lpsolve55 import lpsolve, IMPORTANT


def solve_lp(scp_gen):
    print "--- SOLVE LINEAR PROGRAMMING ---"
    lp = lpsolve('make_lp', 0, scp_gen.covering_set_num)
    lpsolve('set_obj_fn', lp, scp_gen.cost)
    for v in scp_gen.get_rows():
        lpsolve('add_constraint', lp, v, 'GE', 1)
    for i in range(1, scp_gen.covering_set_num+1):
        lpsolve('set_lowbo', lp, i, 0)
    lpsolve('write_lp', lp, 'a.lp')
    lpsolve('set_verbose', lp, IMPORTANT)

    lpsolve('solve', lp)
    res = lpsolve('get_objective', lp)
    print "solution of lp:", res
    V = lpsolve('get_variables', lp)[0]
    print "solution vector:", V
    _, f = scp_gen.get_f()
    print "f:", f, "1/f", 1.0 / float(f)
    AV = [1 if v >= 1.0/float(f) else 0 for v in V]
    print "deterministic rounding:", AV
    ares = sum([c * v for c, v in zip(scp_gen.cost, AV)])
    print "result of linear relaxation:", ares
    print "alpha: ", ares / res, "\n"
    lpsolve('delete_lp', lp)

if __name__ == '__main__':
    scp_gen = scpgen(10, 100, 0.5, 0)
    solve_lp(scp_gen)
