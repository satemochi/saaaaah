from matplotlib import pyplot as plt, use
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
# use('module://backend_ipe')

v0 = (1, 0, 0)
v1 = (np.cos((t := np.pi*2/3)), np.sin(t), 0)
v2 = (np.cos(2*t), np.sin(2*t), 0)

v3 = (np.cos((a := -np.pi/6)), np.sin(a), 1)
v4 = (np.cos((t := np.pi*2/3) + a), np.sin(t + a), 1)
v5 = (np.cos(2*t+a), np.sin(2*t+a), 1)

verts = np.array([
    [v0, v1, v2],
    [v3, v4, v5],
    [v0, v1, v3],
    [v1, v3, v4],
    [v1, v2, v4],
    [v2, v4, v5],
    [v2, v0, v5],
    [v0, v5, v3],
])

ax = plt.figure().add_subplot(projection='3d')
poly = Poly3DCollection(verts, facecolors='#ffcccc', edgecolors='k',
                        shade=True, zsort='min', alpha=.45)
ax.add_collection3d(poly)
ax.set_aspect('equalxy')
ax.axis('off')
ax.view_init(elev=90, azim=-90, roll=30)

# plt.savefig('schonhardt_polyhedron.ipe')
# plt.savefig('schonhardt_polyhedron.png', bbox_inches='tight')
plt.show()
