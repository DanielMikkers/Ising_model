import numpy as np

choice_dict = {'binary': np.array([-1,1]),
               'ternary': np.array([-1,0,1]),
               'quaternary': np.array([-2,-1,1,2]),
               'quinary': np.array([-2,-1,0,1,2])
               }

class RandomLattice:

  def perf_square(self, n_sites):
    sqrt_n = np.sqrt(n_sites)

    return int(sqrt_n)

  def random_lattice(self, n_sites, model='binary', prob=np.array([0.5,0.5])):
    sqrt_size = self.perf_square(n_sites)
    size = (sqrt_size,sqrt_size)
    choice = choice_dict[model]
    lattice = np.random.uniform(choice, size=size, p=prob)

    return lattice