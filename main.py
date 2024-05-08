import numpy as np

class Lattice:
  def __init__(self, n_sites):
    self.n_sites = n_sites

  def perf_square(self, n_sites):
    sqrt_n = np.sqrt(n_sites)
    if not isinstance(sqrt_n, int):
      sqrt_n = int(sqrt_n)
      print("n_sites is not a perfect square \n")
      print("n_sites rounded to integer: {%d}".format(sqrt_n)
    return sqrt_n

  def random_lattice(self, n_sites):
    n_sites = perf_square(n_sites)

    
