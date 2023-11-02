# ISING MODEL 
### About
Numerical simulation of the most well known ferromagnet toy model. This programme carries out a Monte Carlo simulation through the Metropolis algorithm.

### Preview
![alt text](preview.png)

### How to use
1. Clone the repository and open its folder from the CLI.
1. Run the command `pip install -r requirements.txt` to install dependencies.
Run the command `python main.py` (or `python3 main.py` if both Python 2 and Python 3 are installed on your computer).
You will be prompted to input your desired lattice size and initial fraction of spins pointing up. Press enter after answering each prompt. A lattice size of around $50\times50$ points is recommended.
1. The programme will open a Matplotlib window with sliders to modify the temperature ($kT$), magnetic field ($h$) and spin coupling ($J$).

### Theory

The Ising model consists of a lattice of $N$ atoms and seeks to explain their magnetic properties. The Hamiltonian of a single spin $1/2$ particle interacting with a magnetic field along the $z$ direction is:

$$
H=-\frac{g}{\hbar}\mu_B S_z B=-\frac{g}{2}\mu_B \sigma_zB
$$

where $g$ is the spin g-factor, $\mu_B$ is the Bohr magneton and $S_z$, $\sigma_z$ are the spin operator and Pauli matrix along the $z$ direction, respectively. We may encapsulate all prefactors into some $h=\frac{g}{2}\mu_BB$ with units of energy, and write

$$
H = -h\sigma
$$

noting that $\sigma$ has eigenvalues $\pm1$. For a system of non interacting particles, the Hamiltonian would be

$$
H = -\sum\limits_i h_i\sigma_i
$$

We may however heuristically introduce an interaction term that tends to align (or antialign) spins of neighbouring particles. We introduce it as follows, where $\langle ij\rangle$ indicates the indices of nearest neighbours on the lattice

$$
H=-\left(\sum\limits_{\langle ij\rangle}J_{ij}\sigma_i\sigma_j+ \sum\limits_i h_i\sigma_i\right)
$$

If we consider an isotropic system, we obtain the following:

$$
H=-\left(J\sum\limits_{\langle ij\rangle}\sigma_i\sigma_j+ h\sum\limits_i\sigma_i\right)
$$

Through multiple iterations, this programme calculates the system's evolution via the Metropolis algorithm, of which [Wikipedia](https://en.wikipedia.org/wiki/Ising_model#Metropolis_algorithm) gives a brief outline. The key consideration is that our system follows a Boltzmann distribution $\rho=\frac{1}{Z}e^{-\beta H}$. One can then calculate the total magnetic moment $m=-\frac{\partial H}{\partial B}$ as the system evolves (here we simply take $m=\sum\limits_i\sigma_i$). It is typical to express the total magnetic moment in terms of magnetisation per atom $M=m/N$, an intensive measurement, so this is what is presented here. I have also arbitrarily chosen to impose free boundary conditions for the simulation (spins don't interact with anything outside the grid), whereas I could have chosen periodic boundary conditions for instance.