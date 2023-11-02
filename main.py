import numpy as np
import ising
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.widgets import Slider
plt.style.use('fast')

KTMIN, KTMAX = .1, 10
HMAX = 10
JMAX = 10

# Get user input
def request(type, prompt):
    while True:
        try:
            answer = type(input(prompt))
            if answer > 0:
                return answer
            print('Input must be strictly positive.')
        except ValueError:
            print(f'Input must be {type}.')

# Initialise plot
def init_fig():
    fig, ax = plt.subplots(1, 2)
    plt.subplots_adjust(bottom=.17 , wspace=.55)
    fig.suptitle('Ising model')
    ax[0].set_title('Spins')
    ax[1].set_title('Magnetisation')
    ax[1].set_box_aspect(1)
    ax[1].grid()
    ax[1].set_xlim(- HMAX, HMAX)
    ax[1].set_ylim(- 1, 1)
    ax[1].set_xlabel('h')
    ax[1].set_ylabel('M', labelpad=-2)
    # Define the axes for the sliders [left, bottom, width, height]  
    ax_kT_slider = plt.axes([.18, .15, .65, .03])
    ax_J_slider = plt.axes([.18, .10, .65, .03])
    ax_h_slider = plt.axes([.18, .05, .65, .03])
    # Create sliders for h and beta
    kT = Slider(ax_kT_slider, 'kT', KTMIN, KTMAX, valinit=.1)
    J = Slider(ax_J_slider, 'J', - JMAX, JMAX, valinit=0)
    h = Slider(ax_h_slider, 'h', - HMAX, HMAX, valinit=0)
    return fig, ax, kT, J, h

def animate(n, fig, ax, spins, kT, J, h):
    # Spin colourmap
    cmap = mcolors.ListedColormap(['red', 'blue'])
    bounds = [-1, 1, 2]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    im = ax[0].imshow(spins, cmap=cmap, norm=norm)
    # Colourbar [left, bottom, width, height] 
    cb_ax = fig.add_axes([.45,.32,.02,.41])
    cbar = plt.colorbar(im, cax=cb_ax)
    cbar.set_ticks([0, 1.5])
    cbar.set_ticklabels([-1, 1])
    # Magnetisation curve
    line, = ax[1].plot([], [], 'b.')
    data = [[h.val], [np.sum(spins) / n**2]]
    line.set_data(data)
    plt.pause(0.05)
    # Simulation/plot loop
    spins, E = ising.metropolis(n, spins, 1 / kT.val, J.val, h.val, ising.energy(spins, J.val, h.val))
    im.remove()
    im = ax[0].imshow(spins, cmap=cmap, norm=norm)
    data = np.hstack((data, [[h.val], [np.sum(spins) / n**2]]))
    line.set_data(data)
    plt.pause(0.05)
    while plt.fignum_exists(fig.number):
        spins, E = ising.metropolis(n, spins, 1 / kT.val, J.val, h.val, E)
        im.remove()
        im = ax[0].imshow(spins, cmap=cmap, norm=norm)
        data = np.hstack((data, [[h.val], [np.sum(spins) / n**2]]))
        line.set_data(data)
        plt.pause(0.05)

if __name__ == '__main__':
    n = request(int, 'Input the side length n of the spin lattice, which is nxn: ')
    alpha = request(float, 'Input the initial fraction of up spins: ')

    # Initial spin grid
    spins = np.zeros((n,n))
    idx = np.random.random((n,n))
    spins[idx <= alpha] = 1
    spins[idx > alpha] = -1

    # Simulation
    fig, ax, kT, J, h = init_fig()
    animate(n, fig, ax, spins, kT, J, h)

    plt.show()