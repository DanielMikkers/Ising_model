from Ising_model_main import binaryChoiceModel as bcm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
from matplotlib import cm
import time

start_time = time.time()

random_lattice = bcm.rnd_lattice_gen(10000)
lattice_prop, long_range_array = bcm.change_opinion_ntimes(150,random_lattice, h=3)

end_time = time.time()
execution_time = end_time - start_time

print("Execution time:", execution_time, "seconds")

black = np.array([0/256, 0/256, 0/256, 1])
white = np.array([256/256, 256/256, 256/256, 1])
blue = np.array([10/256, 10/256, 256/256, 1])
red = np.array([256/256, 10/256, 10/256, 1])

newcolors = [red, black, white, blue]

newcmp = mcolors.ListedColormap(newcolors)

colors = ['red', 'black', 'white', 'blue']
labels = ['-1, long range sites', '-1', '1', '1, long range sites']

bounds = [-2.5, -1.5, 0.5, 1.5, 2.5] 
norm = mcolors.BoundaryNorm(bounds, newcmp.N)

start_time_anim = time.time()

frames = np.arange(0,len(lattice_prop))

fig = plt.figure( figsize=(8,8), dpi = 200 )

#zero_array = np.zeros(np.shape(lattice_prop[0]))
#zero_array[long_range_array[:, 0], long_range_array[:, 1]] = lattice_prop[0][long_range_array[:, 0], long_range_array[:, 1]]
#new_lattice = lattice_prop[0] + zero_array

im = plt.imshow(lattice_prop[0], cmap = newcmp, norm=norm , origin = 'lower', interpolation = None)

cbar = plt.colorbar(ticks=[-2, -1, 1, 2], format=mcolors.Normalize())
cbar.ax.set_yticklabels(['-1 (long range)', '-1', '1', '1 (long range)'])

#plt.show()

def animate_func(i):
    #zero_array = np.zeros(np.shape(lattice_prop[i]))
    #zero_array[long_range_array[:, 0], long_range_array[:, 1]] = lattice_prop[i][long_range_array[:, 0], long_range_array[:, 1]]

    #new_lattice_prop = lattice_prop[i] + zero_array

    im.set_array(lattice_prop[i])
    return [im]

anim = animation.FuncAnimation(fig, animate_func, frames, interval = 20)

anim.save('test.mp4', fps=30, writer='ffmpeg')

end_time_anim = time.time()
execution_time_anim = end_time_anim - start_time_anim

print("Execution time:", execution_time_anim, "seconds")