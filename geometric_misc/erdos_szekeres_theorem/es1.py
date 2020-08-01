from bisect import bisect_left


def longest_increasing_subsequence(seq):
    n, pred, mid = len(seq), {}, [0]
    for i in range(n):
        pred[i] = mid[(lo:=bisect_left([seq[j] for j in mid], seq[i], lo=1))-1]
        if lo < len(mid):
            mid[lo] = i
        else:
            mid.append(i)
    idx, subseq, k = [0] * (m:=(len(mid)-1)), [0] * m, mid[-1]
    for i in reversed(range(m)):
        idx[i], subseq[i], k = k, seq[k], pred[k]
    return idx, subseq, pred



def gen(n, s):
    from random import sample, seed
    seed(s)
    return sample(range(n), n)


if __name__ == '__main__':
    seq = gen(n:=100, s:=0)
    x, y, p = longest_increasing_subsequence(seq)

    from matplotlib import pyplot as plt
    plt.scatter(range(n), seq)
    plt.plot(x, y, 'ro-')
    for k, v in p.items():
        if k != v and seq[v] <= seq[k]:
            plt.plot([k, v], [seq[k],seq[v]], 'g--', alpha=0.5, zorder=-10)

    plt.gca().set_aspect('equal')
    plt.tight_layout()
    # plt.savefig('longest_increasing_subsequence_1.png', bbox_inches='tight',
    #             dpi=200)
    plt.show()
