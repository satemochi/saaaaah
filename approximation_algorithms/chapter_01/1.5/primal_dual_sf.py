from matplotlib import rc
from matplotlib import pyplot as plt



def primal_dual():
    rc('mathtext', **{'rm': 'serif', 'it': 'serif:itelic', 'bf': 'serif:bold',
                      'fontset': 'cm'})
    fn = {'fontname': 'Times New Roman',
          'fontsize': 12}

    s = r'$y \rightarrow 0$'
    plt.gca().text(2.0, 3.0, s, **fn)

    s = r'$I \rightarrow \emptyset$'
    plt.gca().text(2.0, 3.0 - 0.5, s, **fn)

    s = r'${\bf while} \ $ there exists $\ e_i \ \ \notin \ \bigcup_{j \in I} \ S_j \ \ {\bf do}$'
    plt.gca().text(2.0, 3.0 - 1., s, **fn)

    s = r'Increase the dual variable $y_i$ until there is some $\ell$ with '
    s += r'$e_i \in S_\ell$ such that'
    plt.gca().text(3.5, 3.0 - 1.5, s, **fn)

    s = r'$\sum_{j : e_j \in S_\ell} y_j = w_\ell$'
    plt.gca().text(4.5, 3.0 - 2.1, s, **fn)

    s = r'$I \leftarrow I \cup \{\ell\}$'
    plt.gca().text(3.5, 3.0 - 2.8, s, **fn)

    plt.gca().set_xlim([0, 20])
    plt.gca().set_ylim([0, 3.4])
    plt.gca().set_title(r'${\bf Algorithm 1.1}$: Primal-dual algorithm for the set cover problem')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
#    plt.axis('off')

if __name__ == '__main__':
    plt.figure(figsize=(6.5, 3))
    primal_dual()
    plt.tight_layout()
    plt.savefig('primal_dual_pseudo_code.png', bbox_inches='tight')
    plt.show()
