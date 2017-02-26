from lpsolve55 import lpsolve, IMPORTANT

lp = lpsolve('make_lp', 0, 4)
lpsolve('set_obj_fn', lp, [1, 3, 6.24, 0.1])

lpsolve('add_constraint', lp, [0, 78.26, 0, 2.9], 'GE', 92.3)
lpsolve('add_constraint', lp, [0.24, 0, 11.31, 0], 'LE', 14.8)
lpsolve('add_constraint', lp, [12.68, 0, 0.08, 0.9], 'GE', 4)
lpsolve('set_lowbo', lp, 1, 28.6)
lpsolve('set_lowbo', lp, 4, 18)
lpsolve('set_upbo', lp, 4, 48.98)

lpsolve('set_col_name', lp, 1, 'x1')
lpsolve('set_col_name', lp, 2, 'x2')
lpsolve('set_col_name', lp, 3, 'x3')
lpsolve('set_col_name', lp, 4, 'x4')
lpsolve('set_row_name', lp, 1, 'CONST1')
lpsolve('set_row_name', lp, 2, 'CONST2')
lpsolve('set_row_name', lp, 3, 'CONST3')
lpsolve('write_lp', lp, 'a.lp')

lpsolve('set_verbose', lp, IMPORTANT)
lpsolve('solve', lp)
print lpsolve('get_objective', lp)
print lpsolve('get_variables', lp)
print lpsolve('get_constraints', lp)[0]
