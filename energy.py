import numpy as np


def get_periodic_bc(lattice, shape_lattice, shape_X, idx):
    i, j = idx
    n, m = shape_lattice

    d1, d2 = shape_X

    di = np.arange(-d1/2+0.5, d1/2+0.5)
    dj = np.arange(-d2/2+0.5, d2/2+0.5)

    I, J = np.meshgrid((i + di) % n, (j + dj) % m, indexing='ij')

    return lattice[I,J]

def X_dot_sigma(lattice, X, idx):
    shape_X = np.size(X)
    shape_lattice = np.shape(lattice)

    if shape_X == shape_lattice:
        X_dot_s = X * lattice
    else:
        sublattice = get_periodic_bc(lattice, shape_lattice, shape_X, idx)
        X_dot_s = X * sublattice

    return X_dot_s

class Energy:
    def binary_energy_diff(self, lattice, J, K, h, x, y):
        idx = np.array([x, y])
        
        J_dot_s = X_dot_sigma(lattice, J, idx)
        K_dot_s = X_dot_sigma(lattice*lattice, K, idx)

        dE = 2 * lattice[x, y] * ( np.sum( J_dot_s ) + h[x,y] + np.sum(K_dot_s))

        return dE
    
    def gen_energy_diff(self, lattice, J, K, h, x, y, spin_arr):
        idx = np.array([x, y])
        
        J_dot_s = X_dot_sigma(lattice, J, idx)
        K_dot_ssq = X_dot_sigma(lattice*lattice, K, idx)

        dE = np.zeros(np.size(spin_arr))

        for i in range(np.size(spin_arr)):
            dE[i] = (lattice[x,y] - spin_arr[i]) * ( np.sum(J_dot_s) + h[x,y] ) + (lattice[x,y]**2 - spin_arr[i]**2) * np.sum(K_dot_ssq) 

        return dE