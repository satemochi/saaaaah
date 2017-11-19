from matplotlib import pyplot as plt
from matplotlib import rc


def matching():
    fn = {'fontname': 'Times New Roman',
          'fontsize': 16}
#    fs = 11
    objective = r'$\max \ \ \ \sum_{i = 1}^n \ \ y_i$'
#    plt.gca().text(1.0, 2.0, objective, fontsize=fs, **fn)
    plt.gca().text(1.0, 3.5, objective, **fn)

    subjects = r'$\sum_{i: e_i \in S_j} \ y_i \  \leq \ w_j, \ \ \ \ \ j = 1, \ldots, m,$'
#    plt.gca().text(1.45, 2 - 0.85, subjects, fontsize=fs, **fn)
    plt.gca().text(1.45, 1.5, subjects, **fn)

    subjects = r'$y_i \geq 0, \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ i = 1, \ldots, n$'
#    plt.gca().text(1.5, 1 - 0.65, subjects, fontsize=fs, **fn)
    plt.gca().text(1.5, 0.0, subjects, **fn)

    plt.gca().set_xlim([0, 5])
    plt.gca().set_ylim([0.0, 5.0])
    plt.gca().set_title('A linear program relaxation for the dual of set cover')
    plt.axis('off')

if __name__ == '__main__':
    rc('mathtext', **{'rm': 'serif',
                      'it': 'serif:itelic',
                      'bf': 'serif:bold',
                      'fontset': 'cm'})
    plt.figure(figsize=(5, 2.5))
    matching()
    plt.tight_layout()
#    plt.savefig('sc_dual_form.png', bbox_inches='tight')
    plt.show()
