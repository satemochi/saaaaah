from matplotlib import pyplot as plt


def form(y):
    plane, indent = [], []

    plane.append(r'Let $x$ be an LP solution')
    indent.append(r' ')

    t = r'${\bf for}$ all $1 \leq i \leq k \ \ $'
    t += r'${\bf do}\ \ C_i \leftarrow \emptyset$'
    plane.append(t)
    indent.append(r' ')

    plane.append(r'Pick $r \in (0, 1)$ uniformly at random')
    indent.append(r' ')

    plane.append(r'Pick a random permutation $\pi$ of $\{1, \ldots, k\}$')
    indent.append(r' ')

    plane.append(r'$X \leftarrow \emptyset$')
    indent.append(r' ')

    plane.append(r'${\bf for}\ \ i \leftarrow 1$ to $k - 1\ \ {\bf do}$')
    indent.append(r' ')

    plane.append(r' ')
    indent.append(r'$C_{\pi(i)} \leftarrow B(s_{\pi(i)}, r) - X$')

    plane.append(r' ')
    indent.append(r'$X \leftarrow X \cup C_{\pi(i)}$')

    plane.append(r'$C_{\pi(i)} \leftarrow V - X$')
    indent.append(r' ')

    plane.append(r'${\bf return}\ \ F = \bigcup_{i=1}^k \delta(C_i)$')
    indent.append(r' ')

    fs = 12
    delta = 0.8
    xspace = 6
    for i, (c, s) in enumerate(zip(plane, indent)):
        plt.text(1.0, y - delta * i, c, fontsize=fs)
        plt.text(0.5 + xspace, y - delta * i, s, fontsize=fs)


if __name__ == '__main__':
    plt.figure(figsize=(6, 4))
    form(8)
    plt.title('Randomized rounding for the multiway cut problem.',
              weight='bold')
    plt.gca().set_xlim([-2, 20])
    plt.gca().set_ylim([0, 9])
#    plt.gca().margins(0.1)
#    plt.axis('off')
    plt.tight_layout()
    plt.savefig('multiway_pseudo_code.png', bbox_inches='tight')
    plt.show()
