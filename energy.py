import numpy as np


def get_periodic_bc(lattice, size_J, idx):
    i, j = idx
    n, m = np.shape(lattice)

    d1, d2 = size_J

    di = np.arange(-d1/2+0.5, d1/2+0.5)
    dj = np.arange(-d2/2+0.5, d2/2+0.5)

    I, J = np.meshgrid((i + di) % n, (j + dj) % m, indexing='ij')

    return lattice[I,J]

def X_dot_sigma(lattice, X, idx):
    size_X = np.size(X)
    sublattice = get_periodic_bc(lattice, size_X, idx)
    X_dot_s = X * sublattice

    return X_dot_s

spin_dict ={'binary': (np.array([-1,1])),
            'ternary': np.array([-1,0,1]),
            'quaternary': np.array([-2,-1,1,2]),
            'quinary': np.array([-2,-1,0,1,2])
}

class Energy:
    def binary_energy_diff(self, lattice, J, K, h, x, y):
        idx = np.array([x, y])
        shape_lat = np.shape(lattice)
        shape_J = np.shape(J)
        
        J_dot_s = X_dot_sigma(lattice, J, idx)
        K_dot_s = X_dot_sigma(lattice*lattice, K, idx)

        dE = 2 * lattice[x, y] * ( np.sum( J_dot_s ) + h[x,y])

        return dE
    
    def gen_energy_diff(self, lattice, J, K, h, x, y, spin_arr):
        
        dE = 1

        return dE