import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as coll
import random

width = 1
height = 1
nrows = 20
ncols = 24
inbetween = 0

xx = np.arange(0, ncols, (width+inbetween))
yy = np.arange(0, nrows, (height+inbetween))

fig = plt.figure()
ax = plt.subplot(111, aspect="equal")

pat = []
for xi in xx:
    for yi in yy:
        sq = patches.Rectangle((xi, yi), width, height, fill=True, color=random.choice(["red", "green", "blue", "blue"]))
        ax.add_patch(sq)

pc = coll.PatchCollection(pat)
ax.add_collection(pc)

ax.relim()
ax.autoscale_view()
plt.axis('off')
plt.show()
