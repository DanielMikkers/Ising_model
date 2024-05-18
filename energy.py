import numpy as np
from utils import X_dot_sigma

class Energy:
    def __init__(self, J, K, h) -> None:
        self.Jint = J
        self.Kint = K
        self.hfield = h

    def binary_energy_diff(self, lattice, idx):
        x, y = idx
        dE = np.zeros_like(x)

       
        J_dot_s = X_dot_sigma(lattice, self.Jint, (x,y))
        K_dot_s = X_dot_sigma(lattice*lattice, self.Kint, (x,y))

        dE = 2 * lattice[x, y] * ( np.sum( J_dot_s ) + self.hfield[x,y] + np.sum(K_dot_s))

        return dE
    
    def gen_energy_diff(self, lattice, idx, spin_arr):
        x, y = idx
        
        J_dot_s = X_dot_sigma(lattice, self.Jint, idx)
        K_dot_s = X_dot_sigma(lattice*lattice, self.Kint, idx)

        dE = np.zeros(np.size(spin_arr))

        for i in range(np.size(spin_arr)):
            dE[i] = (lattice[x,y] - spin_arr[i]) * ( np.sum(J_dot_s) + self.hfield[x,y] ) + (lattice[x,y]**2 - spin_arr[i]**2) * np.sum(K_dot_s) 

        return dE