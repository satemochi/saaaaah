from scpgen import scpgen
import matplotlib.pyplot as plt


def draw(sc):
    x = []
    for i in range(sc.covering_set_num):
        x.append([sc.sets[i][h]+1 for h in range(sc.sizes[i])])
    w = 10
    plt.hist(x, bins=111, range=(-5, 105), stacked=True, alpha=0.5)
    plt.gca().margins(0.1)
    plt.gcf().tight_layout()
    plt.show()

if __name__ == '__main__':
    sc = scpgen(10, 100, 0.5, 0)
    draw(sc)
