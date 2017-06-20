from matplotlib import pyplot as plt


def form(y):
    fs = 12
    delta = 1.2
    xspace = 12

    objective = r'$\min \ \ \frac{1}{2}\sum_{e \in E} c_e \sum_{i=1}^k z_e^i$'
    plt.text(-1.0, y + 0.5, objective, fontsize=fs)

    subjects, suffixes = [], []

    subjects.append(r'$\sum_{i=1}^k x_u^i = 1,$')
    suffixes.append(r'$\forall u \in V,$')

    subjects.append(r'$z_e^i \geq x_u^i - x_v^i,$')
    suffixes.append(r'$\forall e = (u, v) \in E,$')

    subjects.append(r'$z_e^i \geq x_v^i - x_u^i,$')
    suffixes.append(r'$\forall e = (u, v) \in E,$')

    subjects.append(r'$x_{s_i}^i = 1,$')
    suffixes.append(r'$i = 1, \ldots, k,$')

    subjects.append(r'$x_u^i \in \{0, 1\},$')
    suffixes.append(r'$\forall u \in V, \ i = 1, \ldots, k.$')

    for i, (c, s) in enumerate(zip(subjects, suffixes), start=1):
        plt.text(3.0, y - delta * i, c, fontsize=fs)
        plt.text(0.5 + xspace, y - delta * i, s, fontsize=fs)


def form2(y):
    fs = 12
    delta = 0.8
    xspace = 12

    objective = r'$\min \ \ \frac{1}{2}\sum_{e=(u,v)\in E} c_e ||x_u-x_v||_1$'
    plt.text(-1.0, y + 0.5, objective, fontsize=fs)

    subjects, suffixes = [], []

    subjects.append(r'$x_{s_i} = e_i,$')
    suffixes.append(r'$i = 1, \ldots, k,$')

    subjects.append(r'$x_u \in \Delta_k,$')
    suffixes.append(r'$\forall u \in V.$')

    for i, (c, s) in enumerate(zip(subjects, suffixes), start=1):
        plt.text(3.0, y - delta * i, c, fontsize=fs)
        plt.text(0.5 + xspace, y - delta * i, s, fontsize=fs)


if __name__ == '__main__':
    plt.figure(figsize=(6, 6))
    form(11)
    form2(2)
    plt.title('An integer formulation for the multiway cut problem',
              weight='bold')
    plt.gca().set_xlim([-2, 20])
    plt.gca().set_ylim([-2, 13])
    plt.gca().margins(0.1)
    plt.axis('off')
    plt.savefig('multiway_forms.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
