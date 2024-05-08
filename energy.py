import numpy as np


def get_periodic_bc(lattice, size_J, idx):
    i, j = idx
    n, m = np.shape(lattice)

    d1, d2 = size_J

    di = np.arange(-d1/2+0.5, d1/2+0.5)
    dj = np.arange(-d2/2+0.5, d2/2+0.5)

    I, J = np.meshgrid((i + di) % n, (j + dj) % m, indexing='ij')

    return lattice[I,J]

def J_dot_sigma(lattice, J, idx):
    size_J = np.size(J)
    sublattice = get_periodic_bc(lattice, size_J, idx)
    J_dot_s = J * sublattice

    return 

class BinaryEnergy:
    def binary_energy_diff(self, lattice, J, h, x, y):
        idx = np.array([x, y])
        J_dot_s = J_dot_sigma(lattice, J, idx)

        dE = 2 * lattice[x, y] * ( np.sum( J_dot_s ) + h[x,y])

        return dE