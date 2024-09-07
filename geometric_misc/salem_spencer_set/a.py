from functools import reduce
import numpy as np


def larger_salem_spencer_set_with_ternary_numbers(n):
    return [i for i in range(1, n+1) if '2' not in str(np.base_repr(i, base=3))]

def larger_salem_spencer_set_with_behrend(n, d=2, k=3):
    boad = reduce(lambda x, i: x+str(i), range(d), '')
    print(boad)
    for i in range(1, n+1):
        print(i, str(np.base_repr(i, base=2*d-1)))
    return [i for i in range(1, n+1)
            if all(c in boad for c in str(np.base_repr(i, base=2*d-1)))]


if __name__ == '__main__':
    print(larger_salem_spencer_set_with_ternary_numbers(14))
    print(larger_salem_spencer_set_with_behrend(14, 3))
