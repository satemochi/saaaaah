from pulp import lpDot, LpProblem, lpSum, LpVariable, PULP_CBC_CMD
import numpy as np


def col_player(a):
    (m, n), lpc = a.shape, LpProblem()
    lpc += (r := LpVariable('R'))
    lpc += lpSum(y := [LpVariable(f'y_{j}', 0, 1) for j in range(n)]) == 1
    for i in range(m):
        lpc += lpDot(a[i, :], y) <= r
    PULP_CBC_CMD(msg=0).solve(lpc)
    return r, y


def row_player(a):
    (m, n), lpr = a.shape, LpProblem(sense=-1)
    lpr += (c := LpVariable('L'))
    lpr += lpSum(x := [LpVariable(f'x_{i}', 0, 1) for i in range(m)]) == 1
    for j in range(n):
        lpr += lpDot(a[:, j], x) >= c
    PULP_CBC_CMD(msg=0).solve(lpr)
    return c, x


if __name__ == '__main__':
    a = np.random.randint(low=-10, high=10, size=(m:=5, n:=4))
    print(a)
    # print(a[2, :])  # i-th row (i = 2)
    # print(a[:, 2])  # j-th column (j = 2)
    r, y = col_player(a)
    print(r.varValue)
    print([yi.varValue for yi in y])
    c, x = row_player(a)
    print(c.varValue)
    print([xi.varValue for xi in x])
