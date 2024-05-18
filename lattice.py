import numpy as np
from utils import spin_array

class GenLattice:
    def __init__(self, size_lattice, spin):
        self.size_lattice = size_lattice
        self.n_sites = np.prod(size_lattice)
        self.spin = spin
    
    def perf_square(self):
        sqrt_n = np.sqrt(self.n_sites)

        return int(sqrt_n)
    
    def random_lattice(self, prob=None):
        sqrt_size = self.perf_square()
        size = (sqrt_size,sqrt_size)
        spin_arr = spin_array(self.spin)
        if prob is None:
            prob = np.ones(self.spin+1)/(self.spin+1)
        lattice = np.random.choice(spin_arr, size=size, p=prob)

        return lattice
    
