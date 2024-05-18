from lattice import GenLattice
from metropolis import TimeEvolution
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

generate_lattice = GenLattice((30,30), 1)
rnd_lattice = generate_lattice.random_lattice(np.array([0.5,0.5]))

evolve = TimeEvolution(1)
time_list = evolve.time_evolve(rnd_lattice, t_end=60)

frames = np.arange(0,len(time_list))
fig = plt.figure(figsize=(8,8), dpi=200)
im = plt.imshow(time_list[0], cmap='Grays', origin='lower', interpolation=None)

cbar = plt.colorbar(ticks=[-1,1])
cbar.ax.set_yticklabels(['-1','1'])

def animate_func(i):
    im.set_array(time_list[i])
    return [im]

anim = animation.FuncAnimation(fig, animate_func, frames, interval=20)

anim.save('test.mp4', fps=30, writer='ffmpeg')

