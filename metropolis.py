import numpy as np
from lattice import RandomLattice
from energy import Energy
from interaction import Interaction, Moment

class ChoiceInt:

    def __init__(self, n_lattice):
        self.n_lattice = n_lattice

        self.interaction_dict = {'NN': Interaction.init_J((5,5),4),
               'NNN': Interaction.init_J((3,3),8),
               '4N': Interaction.init_J((5,5),12),
               '5N': Interaction.init_J((5,5),20),
               '6N': Interaction.init_J((5,5),24),
               'lattice': Interaction.init_J((int(np.sqrt(self.n_lattice)),int(np.sqrt(self.n_lattice))))
               }
    
    def choose_J(self, interaction, n_lattice):
        if isinstance(interaction, np.ndarray):
            if np.size(interaction) % 2 == 1:
                J = Interaction.init_J(interaction)
            else:
                raise ValueError("The size of the interaction matrix should be an odd value.")
                
        elif isinstance(interaction, float) or isinstance(interaction, int):
            J = interaction

        elif isinstance(interaction, str) and interaction in self.interaction_dict:
            J = self.interaction_dict[interaction]
        
        else:
            J = self.interaction_dict['NN']
            print("Nearest neighbors used, because invalid interaction is given.")

        return J
    
    def choose_K(self, frustration):
        if isinstance(frustration, np.ndarray):
            if np.size(frustration) % 2 == 1:
                K = frustration
            else:
                raise ValueError("The size of the interaction matrix should be an odd value.")
                
        elif isinstance(frustration, float) or isinstance(frustration, int):
            K = frustration

        elif frustration is None:
            K = 0
        
        else:
            K = Interaction.init_K(frustration)
            print("Nearest neighbors used, because invalid interaction is given.")

        return K

class TimeEvolution:
        def spin_array(self, spin):
            spin_arr = np.arange(-spin, spin+1)
            
            if spin % 2 == 1:
                spin_arr = np.delete(spin_arr,int(spin/2))

            return spin_arr

        def time_evolution(self, lattice, type, spin, t_end=20, beta=1, h=None, interaction='NN', frustration=None):
            spin_change_dict = {
                'bin': SpinChange.binary_spin_change,
                'gen': SpinChange.general_spin_change
            }

            n_lattice = np.shape(lattice)
            J = ChoiceInt.choose_J(interaction, n_lattice)
            K = ChoiceInt.choose_K(frustration, n_lattice)

            time_list = []
            time_list.append(lattice)

            for _ in range(t_end):
                lattice = spin_change_dict[type](lattice, spin, beta, h, J, K)

            return time_list
    
class SpinChange:

    def binary_spin_change(self, lattice, beta=1, h=None, interaction=None, frustration=None):
        n_lattice = np.size(lattice)
        
        if interaction is None:
            J = ChoiceInt.choose_J(interaction)

        if frustration is None:
            K = ChoiceInt.choose_K(frustration)

        if h is None:
            h = 0

        for _ in range(int(n_lattice)):
            x, y = np.random.randint(0, n_lattice), np.random.randint(0, n_lattice)
            dE = Energy.binary_energy_diff(lattice, J, K, h, x, y)
            
            prob = np.min(1,np.exp(-beta * dE))
            spin = lattice[x, y]

            factor = np.random.choice([spin,-spin], p=[1-prob, prob])
            lattice[x, y] *= factor

        return lattice
    

    def general_spin_change(self, lattice, spin_arr, beta=1, h=None, interaction='NN', frustration=0):
        n_lattice = np.size(lattice)

        if interaction is not None:
            J = ChoiceInt.choose_J(interaction, n_lattice)
            
        if frustration is not None:
            K = ChoiceInt.choose_K(frustration, n_lattice)

        if h is None:
            h = 0

        for _ in range(int(n_lattice)):
            x, y = np.random.randint(0, n_lattice), np.random.randint(0, n_lattice)
            dE = Energy.general_energy_diff(lattice, J, K, h, x, y, spin_arr)
            
            prob = np.exp(-beta * dE)
            prob_norm = prob / np.sum(prob)

            new_spin = np.random.choice(spin_arr, p=prob_norm)
            lattice[x, y] = new_spin

        return lattice