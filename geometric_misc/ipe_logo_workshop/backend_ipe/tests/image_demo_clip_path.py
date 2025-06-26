"""
Demo of image that's been clipped by a circular patch.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook
from matplotlib import use
use('module://backend_ipe_sa2')

datafile = cbook.get_sample_data('grace_hopper.jpg', asfileobj=False)
image = plt.imread(datafile)
fig, ax = plt.subplots()
im = ax.imshow(image)
patch = patches.Circle((260, 200), radius=200, transform=ax.transData)
im.set_clip_path(patch)

plt.axis('off')
#plt.show()
plt.savefig('image_demo_clip_path.ipe')
