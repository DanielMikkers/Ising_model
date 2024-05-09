import numpy as np
from metropolis import TimeEvolution

class RandomLattice:

  def perf_square(self, n_sites):
    sqrt_n = np.sqrt(n_sites)

    return int(sqrt_n)

  def random_lattice(self, n_sites, spin, prob=None):
    sqrt_size = self.perf_square(n_sites)
    size = (sqrt_size,sqrt_size)
    spin_arr = TimeEvolution.spin_array(spin)
    if prob is None:
      prob = np.ones(spin+1)/(spin+1)
    lattice = np.random.uniform(spin_arr, size=size, p=prob)

    return lattice