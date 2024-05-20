import numpy as np

def get_periodic_bc(lattice, shape_lattice, shape_X, idx):
    i, j = idx
    n, m = shape_lattice

    d1, d2 = shape_X

    di = np.arange(-d1/2+0.5, d1/2+0.5)
    dj = np.arange(-d2/2+0.5, d2/2+0.5)
    
    I, J = np.meshgrid((i + di) % n, (j + dj) % m, indexing='ij')

    return lattice[I.astype(int),J.astype(int)]

def X_dot_sigma(lattice, X, idx):
    shape_X = np.shape(X)
    shape_lattice = np.shape(lattice)

    if shape_X == shape_lattice:
        X_dot_s = X * lattice
    else:
        sublattice = get_periodic_bc(lattice, shape_lattice, shape_X, idx)

        X_dot_s = X * sublattice

    return X_dot_s

def spin_array(spin):
    ceil_spin = int(np.ceil(spin/2))
    spin_arr = np.arange(-ceil_spin,ceil_spin+1)

    if spin % 2 == 1:
        spin_arr = np.delete(spin_arr,ceil_spin)

    return spin_arr