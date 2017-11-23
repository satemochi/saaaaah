from matplotlib import rc
from matplotlib import pyplot as plt



def greedy():
    rc('mathtext', **{'rm': 'serif', 'it': 'serif:itelic', 'bf': 'serif:bold',
                      'fontset': 'cm'})
    fn = {'fontname': 'Times New Roman', 'fontsize': 12}

    s = r'$I \leftarrow \emptyset$'
    plt.gca().text(2.0, 3.0, s, **fn)

    s = r'$\hat{S}_j \leftarrow S_j \ \ \ \ \ \ \forall j$'
    plt.gca().text(2.0, 3.0 - 0.4, s, **fn)

    s = r'${\bf while} \ I \ $ is not a set cover $\ {\bf do}$'
    plt.gca().text(2.0, 3.0 - 0.72, s, **fn)

    s = r'$\ell \leftarrow \argmin_{j: \hat{S}_j \neq \emptyset} \ \ \frac{w_j}{|\hat{S}_j|}$'
    plt.gca().text(4.5, 3.0 - 1.2, s, **fn)

    s = r'$I \leftarrow I \cup \{\ell\}$'
    plt.gca().text(4.5, 3.0 - 1.8, s, **fn)

    s = r'$\hat{S}_j \leftarrow \hat{S}_j - S_\ell \ \ \ \ \forall j$'
    plt.gca().text(4.5, 1.0 - 0.2, s, **fn)

    plt.gca().set_xlim([0, 20])
    plt.gca().set_ylim([0.5, 3.4])
    plt.gca().set_title(r'${\bf Algorithm\ 1.2}$: A greedy algorithm for the set cover problem.')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
#    plt.axis('off')

if __name__ == '__main__':
    plt.figure(figsize=(5.5, 2.5))
    greedy()
    plt.tight_layout()
    plt.savefig('greedy_pseudo_code.png', bbox_inches='tight')
    plt.show()
