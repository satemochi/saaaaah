from math import pi, cos, sin, sqrt
from matplotlib import cm
from matplotlib import pyplot as plt
import networkx as nx
from scipy.spatial.transform import Rotation


def wire_sphere(z_div, c_div):
    g = nx.Graph()
    n_pole, s_pole = (0, z_div), (0, -z_div)
    for i in range(1, z_div):
        for j in range(c_div):
            n = n_pole if i == 1 else (j, i-1)
            s = s_pole if i == z_div-1 else (j, i+1)
            e = ((j+1) % c_div, i)
            w = ((j-1) % c_div, i)
            c = (j, i)
            g.add_edges_from([(c, n), (c, s), (c, e), (c, w)])
    return g


def coord(xy0, z0, z_div, c_div):
    z = 1 - 2/z_div*z0 if abs(z0) != z_div else z0/z_div
    r = sqrt(1 - z*z)
    dt = 2*pi / c_div
    return (r*cos(dt*xy0), r*sin(dt*xy0), z)


def ecc_color(g, e=None, c=cm.rainbow):
    if not e:
        e = nx.eccentricity(g)
    d, r = nx.diameter(g, e=e), nx.radius(g, e=e)
    print(f'diameter: {d}, radius: {r}')
    return c(list(map(lambda x: (x-r)/(d-r), (e[v] for v in g))))


if __name__ == '__main__':
    dz, dxy = 50, 50
    g = wire_sphere(dz, dxy)

    rot = Rotation.from_rotvec([pi/2-0.3, 0.2, 0])
#    rot = Rotation.from_rotvec([pi/2, 0., 0])
    pos = {v: (x, y) for v in g for x, y, _ in [rot.apply(coord(*v, dz, dxy))]}

    colors = ecc_color(g, e=nx.eccentricity(g), c=cm.rainbow_r)
    nx.draw_networkx_nodes(g, pos, node_size=20, node_color=colors)
    nx.draw_networkx_edges(g, pos, alpha=0.3)

    plt.axis('off')
    plt.gca().set_aspect('equal')
#    plt.savefig('wire_sphere_eccentricity.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
