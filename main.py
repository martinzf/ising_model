import numpy as np
import ising
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.widgets import Slider
plt.style.use('fast')

N = 50
hmax = 10
alpha = .5
Jmax = 10

# Initial spin grid
spins = np.zeros((N,N))
idx = np.random.random((N,N))
spins[idx <= alpha] = 1
spins[idx > alpha] = -1

# Plot setup
fig, ax = plt.subplots(1, 2)
plt.subplots_adjust(bottom=.17 , wspace=.4)
fig.suptitle('Ising model')
ax[0].set_title('Spins')
ax[1].set_title('Magnetisation')
ax[1].set_box_aspect(1)

# Define the axes for the sliders [left, bottom, width, height]  
ax_beta_slider = plt.axes([.25, .15, .65, .03])
ax_h_slider = plt.axes([.25, .10, .65, .03])
ax_J_slider = plt.axes([.25, .05, .65, .03])

# Create sliders for h and beta
h = Slider(ax_h_slider, 'h', - hmax, hmax, valinit=0)
beta = Slider(ax_beta_slider, r'$\beta$', 0.1, 5.0, valinit=.1)
J = Slider(ax_J_slider, 'J', - Jmax, Jmax, valinit=0)

# First frame
# Colourmap
cmap = mcolors.ListedColormap(['red', 'blue'])
bounds = [-1, 1, 2]
norm = mcolors.BoundaryNorm(bounds, cmap.N)
im = ax[0].imshow(spins, cmap=cmap, norm=norm)
# Colourbar
cbar = plt.colorbar(im, ax=ax[0], shrink=0.5)
cbar.set_ticks([-0.5, 1.5])
cbar.set_ticklabels([-1, 1])
#cbar.set_label('Colorbar Title', rotation=90)
# Limits and labels
ax[1].set_xlim(- hmax, hmax)
ax[1].set_ylim(- 1, 1)
ax[1].set_xlabel('h')
ax[1].set_ylabel('m')
line, = ax[1].plot([], [], 'b.')
data = [[h.val], [np.sum(spins) / N**2]]
line.set_data(data)
plt.pause(0.05)

# Simulation/plot loop
spins, E = ising.metropolis(N, spins, beta.val, J.val, h.val, ising.energy(spins, J.val, h.val))
im.remove()
im = ax[0].imshow(spins, cmap=cmap, norm=norm)
data = np.hstack((data, [[h.val], [np.sum(spins) / N**2]]))
line.set_data(data)
plt.pause(0.05)
while plt.fignum_exists(fig.number):
    spins, E = ising.metropolis(N, spins, beta.val, J.val, h.val, E)
    im.remove()
    im = ax[0].imshow(spins, cmap=cmap, norm=norm)
    data = np.hstack((data, [[h.val], [np.sum(spins) / N**2]]))
    line.set_data(data)
    plt.pause(0.05)

plt.show()