import matplotlib.pyplot as plt


def math(i):
    objective = r'$\max \ \ \frac{1}{2} \ \sum_{(i, j) \in E} \ \ '
    objective += 'c_{ij} \ (1 - y_i \  y_j)$' 
    plt.text(1.0, i, objective, fontsize=11)

    subjects = r'$y_i \in \{-1, +1\}, \ \ \ i = 1, \ldots, n$'
    plt.text(7.5, i - 0.75, subjects, fontsize=11)


def vec(i):
    objective = r'$\max \ \ \frac{1}{2} \ \sum_{(i, j) \in E} \ \ '
    objective += 'c_{ij} \ (1 - v_i \  v_j)$' 
    plt.text(1.0, i, objective, fontsize=11)

    subjects = r'$v_i \cdot v_i = 1, \ \ \ i = 1, \ldots, n$'
    plt.text(7.5, i - 0.75, subjects, fontsize=11)
    subjects = r'$v_i \in \mathbb{R}^n, \ \ \ i = 1, \ldots, n$'
    plt.text(7.5, i - 1.5, subjects, fontsize=11)


def sdp(i):
    objective = r'$\max \ \ \frac{1}{4} \ L \circ X$'
    plt.text(1.0, i, objective, fontsize=11)

    subjects = r'$diag(X) = diag(I)$'
    plt.text(7.5, i - 0.75, subjects, fontsize=11)
    subjects = r'$X \succeq 0$'
    plt.text(7.5, i - 1.5, subjects, fontsize=11)

if __name__ == '__main__':
    math(5)
    vec(3)
    sdp(0.5)
    plt.title('Mathematical programmings for Max Cut problems')
    plt.gca().set_xlim([-2, 20])
    plt.gca().set_ylim([-1.5, 6])
    plt.gca().margins(0.1)
    plt.savefig("maxcut_forms.png", bbox_inches='tight')
    plt.show()
