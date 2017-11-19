from matplotlib import pyplot as plt
from matplotlib import rc


def vc(ax):
    objective = r'$\min \ \ \ \sum_{v \in V} \ \ x_v$'
    ax.text(1.0, 2.2, objective, fontsize=11)

    subjects = r'$\sum_{v \in e} \ x_v \geq 1,  \ \ \ \ \ \ \ \ \ \forall e \in E$'
    ax.text(1.5, 2 - 0.55, subjects, fontsize=11)

    subjects = r'$x_v \in \{0, 1\}, \ \ \ \ \ \ \forall v \in V$'
    ax.text(1.5 + 0.1, 1 - 0.3, subjects, fontsize=11)

    ax.set_xlim([0, 5])
    ax.set_ylim([0, 3])
    ax.set_title('vertex cover')


def matching(ax):
    objective = r'$\max \ \ \ \sum_{(u, v) \in E} \ \ y_{(u, v)}$'
    ax.text(1.0, 2, objective, fontsize=11)

    subjects = r'$\sum_{u: (u, v) \in E} \ y_{(u, v)} \  \leq 1, \ \ \ \ \ \forall v \in V$'
    ax.text(1.5, 2 - 0.75, subjects, fontsize=11)

    subjects = r'$y_{(u, v)} \in \{0, 1\}, \ \ \ \ \ \ \ \ \ \ \ \forall (u, v) \in E$'
    ax.text(1.5, 1 - 0.55, subjects, fontsize=11)

    ax.set_xlim([0, 5])
    ax.set_ylim([0, 3])
    ax.set_title('matching')

if __name__ == '__main__':
    rc('mathtext', **{'rm': 'serif',
                      'it': 'serif:itelic',
                      'bf': 'serif:bold',
                      'fontset': 'cm'})
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 3))
    vc(ax1)
    matching(ax2)
    plt.tight_layout()
    plt.savefig('vc_matching_forms.png', bbox_inches='tight')
    plt.show()
