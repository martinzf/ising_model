import numpy as np
import scipy as sp
import numba 

# Lattice energy calculation
def energy(spins, J, h):
    kern = [
        [False, True, False],
        [True, False, True],
        [False, True, False]
    ]
    conv = sp.signal.convolve2d(spins, kern, 'same')
    return - np.sum(J * spins * conv + h * spins)

# A few steps of the Metropolis algorithm, accelerated with Numba
@numba.njit(fastmath=True)
def metropolis(N, spins, beta, J, h, E, iters=1_000):
    for _ in range(iters):
        # Random point
        x, y = np.random.randint(0, N, size=2) 
        # Proposed spin flip
        spin_i = spins[x, y]
        spin_f = - spin_i
        # Energy change
        spinspin_i, spinspin_f = 0, 0
        if x > 0:
            spinspin_i -= spin_i * spins[x - 1, y]
            spinspin_f -= spin_f * spins[x - 1, y]
        if x < N-1:
            spinspin_i -= spin_i * spins[x + 1, y]
            spinspin_f -= spin_f * spins[x + 1, y]
        if y > 0:
            spinspin_i -= spin_i * spins[x, y - 1]
            spinspin_f -= spin_f * spins[x, y - 1]
        if y < N-1:
            spinspin_i -= spin_i * spins[x, y + 1]
            spinspin_f -= spin_f * spins[x, y + 1]
        dE = - J * (spinspin_f - spinspin_i) - h * (spin_f - spin_i)
        # Change state
        if dE <= 0:
            spins[x, y] = spin_f
            E += dE
        elif np.random.random() < np.exp(- beta * dE):
            spins[x, y] = spin_f
            E += dE
    return spins, E