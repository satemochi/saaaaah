import matplotlib.pyplot as plt


def form(i):
    delta = 1.3
    suffix_pos = 11.5

    objective = r'$\max \ \ \sum_{j = 0}^{m - 1} w_j z_j$'
    plt.text(0.0, i, objective, fontsize=12)

    subjects = r'$\sum_{i \in P_j} y_i + '
    subjects += r'\sum_{i \in N_j} \left(1 - y_i \right) \geq z_j,$'
    plt.text(1.0, i - delta, subjects, fontsize=13)
    suffix = r'$\forall C_j = \bigvee_{i \in P_j} x_i \vee'
    suffix += r'\bigvee_{i \in N_j} \neg x_i,$'
    plt.text(suffix_pos, i - delta, suffix, fontsize=12)

    subjects = r'$0 \leq y_i \leq 1,$'
    plt.text(1.0, i - delta * 2, subjects, fontsize=13)
    suffix = r'$i = 0, \ldots, n - 1,$'
    plt.text(suffix_pos, i - delta * 2, suffix, fontsize=12)

    subjects = r'$0 \leq z_j \leq 1,$'
    plt.text(1.0, i - delta * 2.5, subjects, fontsize=13)
    suffix = r'$j = 0, \ldots, m - 1.$'
    plt.text(suffix_pos, i - delta * 2.5, suffix, fontsize=12)


if __name__ == '__main__':
    form(4)
    plt.title('An integer program for Integer Multicommodity flows')
    plt.gca().set_xlim([-2, 20])
    plt.gca().set_ylim([-1.5, 6])
    plt.gca().margins(0.1)
    plt.savefig("maxsat_forms.png", bbox_inches='tight')
    plt.show()
