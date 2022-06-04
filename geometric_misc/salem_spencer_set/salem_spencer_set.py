from itertools import combinations
from pulp import LpMaximize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD


def salem_spencer_set(n):
    x = [LpVariable(f'x_{i}', cat='Binary') for i in range(n)]
    lp = LpProblem(sense=LpMaximize)
    lp += lpSum(x)
    for i, j, k in combinations(range(1, n+1), 3):
        if 2*j == i+k:
            lp += x[i-1] + x[j-1] + x[k-1] <= 2
    PULP_CBC_CMD(msg=0).solve(lp)
    return [i+1 for i, xi in enumerate(x) if xi.varValue > 0]


if __name__ == '__main__':
    print(salem_spencer_set(14))
