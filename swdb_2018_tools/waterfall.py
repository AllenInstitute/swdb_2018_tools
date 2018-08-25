from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection, LineCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np

"""
from swdb_2018_tools import waterfall
import numpy as np
import matplotlib.pyplot as plt
%matplotlib notebook

# build some random data
arrs = []
colors = []
for i in range(20):
    N = np.random.choice(np.array([8,9,10,11,12])*10)
    arrs.append(np.random.random(N))
    colors.append(np.random.random(3))

waterfall.waterfall(arrs, colors)
"""
    
def waterfall(arrs, colors=None):
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.gca(projection='3d')

    def cc(arg):
        return mcolors.to_rgba(arg, alpha=0.6)

    verts = [ zip(np.arange(len(a)), a) for a in arrs ]
    zs = np.arange(len(verts))


    poly = LineCollection(verts, colors=colors)
    poly.set_alpha(0.8)
    ax.add_collection3d(poly, zs=zs, zdir='y')

    #ax.set_xlabel('X')
    ax.set_xlim3d(0, max([len(a) for a in arrs])-1)
    #ax.set_ylabel('Y')
    ax.set_ylim3d(0, len(arrs))
    #ax.set_zlabel('Z')
    ax.set_zlim3d(0, max([max(a) for a in arrs])*3)

    plt.show()