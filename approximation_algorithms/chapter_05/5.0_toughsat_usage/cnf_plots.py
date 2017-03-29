from random_ksat import generate_instance
import matplotlib.pyplot as plt
import random


def val(n):
    return 'x_{' + str(abs(n)) + '}'


def tex_string(literals):
    t = [r'\neg ' + val(l) if l < 0 else val(l) for l in literals]
    return '$' + r'\ \vee \ '.join(t) + '$'


def draw(tex_str, ypos):
    plt.text(1.0, ypos, tex_str, fontsize=11)


def clauses(s):
    return [[int(v) for v in l.split(' ')[:-1]] for l in s.split('\n')[2:-1]]


if __name__ == '__main__':
    random.seed(0)
    nc, nv, k, op = 15, 10, 5, False
    sat_inst = generate_instance(nc, nv, k, op)
    print sat_inst

    for i, l in enumerate(clauses(sat_inst)):
        draw(tex_string(l), nc - i)
        print l

    plt.gca().set_xlim([0, 20])
    plt.gca().set_ylim([0, nc + 1])
    plt.savefig('cnf_plots.png', bbox_inches='tight')
    plt.show()
