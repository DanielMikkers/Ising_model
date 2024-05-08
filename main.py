import numpy as np

choice_dict = {'binary': np.array([-1,1])}

class RandomLattice:
  def perf_square(self, n_sites):
    sqrt_n = np.sqrt(n_sites)
    if not isinstance(sqrt_n, int):
      sqrt_n = int(sqrt_n)
      print("n_sites is not a perfect square \n")
      print("n_sites rounded to integer: {%d}".format(sqrt_n)
    return sqrt_n

  def random_lattice(self, n_sites, model='binary', prob=np.array([0.5,0.5])):
    sqrt_size = perf_square(n_sites)
    size = (sqrt_size,sqrt_size)
    choice = choice_dict[model]
    lattice = np.random.uniform(choice, size=size), p=prob)

    return lattice
