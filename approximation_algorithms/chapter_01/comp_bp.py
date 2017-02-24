from scpgen import scpgen
from lpsolve55 import lpsolve, IMPORTANT


def solve_bp(scp_gen):
    print "--- SOLVE BINARY PROGRAMMING ---"
    lp = lpsolve('make_lp', 0, scp_gen.covering_set_num)
    lpsolve('set_obj_fn', lp, scp_gen.cost)
    lpsolve('set_binary', lp, range(scp_gen.covering_set_num))
    for v in scp_gen.get_rows():
        lpsolve('add_constraint', lp, v, 'GE', 1)
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('write_lp', lp, 'b.lp')

    lpsolve('solve', lp)
    print "solution of bp:", lpsolve('get_objective', lp)
    V = lpsolve('get_variables', lp)[0]
    print "solution vector:", V
    print scp_gen.is_covered([i for i, v in enumerate(V) if v != 0.0]), "\n"
    lpsolve('delete_lp', lp)


if __name__ == '__main__':
    scp_gen = scpgen(10, 100, 0.5, 3)
    solve_bp(scp_gen)
