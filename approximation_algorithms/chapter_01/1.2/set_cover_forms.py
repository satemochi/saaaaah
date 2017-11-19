from matplotlib import pyplot as plt


def form(y):
    fs = 12
    delta = 2.5
    xspace = 11

    objective = r'$\min \ \ \sum_{j = 1}^m w_j x_j$'
    plt.text(1.5, y + 0.0, objective, fontsize=fs)

    subjects, suffixes = [], []

    subjects.append(r'$\sum_{j:\ e_i \in S_j} x_j \geq 1,$')
    suffixes.append(r'$i = 1, \ldots, n,$')

    subjects.append(r'$x_j \in \{0, 1\},$')
    suffixes.append(r'$j = 1, \ldots, m.$')

    for i, (c, s) in enumerate(zip(subjects, suffixes), start=1):
        plt.text(3.0, y - delta * i, c, fontsize=fs)
        plt.text(0.5 + xspace, y - delta * i, s, fontsize=fs)


if __name__ == '__main__':
    plt.figure(figsize=(6, 2))
    form(2)
    plt.title('An integer formulation for the set coverproblem',
              weight='bold')
    plt.gca().set_xlim([-2, 20])
    plt.gca().set_ylim([-2, 4])
    plt.gca().margins(0.1)
    plt.axis('off')
    plt.savefig('set_cover_forms.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
