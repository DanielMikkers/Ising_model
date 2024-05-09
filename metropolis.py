import numpy as np
from lattice import RandomLattice
from energy import BinaryEnergy
from interaction import Interaction, Moment

class ChoiceInt:

    def __init__(self, n_lattice):
        self.n_lattice = n_lattice

        self.interaction_dict = {'NN': Interaction.init_J(3,1),
               'NNN': Interaction.init_J(3,2),
               '4N': Interaction.init_J(5,3),
               '5N': Interaction.init_J(5,4),
               '6N': Interaction.init_J(5,4),
               'lattice': Interaction.init_J(self.n_lattice)
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
    
    def choose_K(self, frustration, n_lattice):
        K = 1

        return K

class TimeEvolution:
        def spin_array(self, spin):
            spin_arr = np.arange(-spin, spin+1)
            
            if spin % 2 == 1:
                spin_arr = np.delete(spin_arr,int(spin/2))

            return spin_arr

        def time_evolution(self, lattice, type, spin, t_end=20, beta=1, h=None, interaction='NN', frustration=0):
            spin_change_dict = {
                'bin': SpinChange.binary_spin_change,
                'gen': SpinChange.general_spin_change
            }

            time_list = []
            time_list.append(lattice)

            for _ in range(t_end):
                lattice = spin_change_dict[type](lattice, spin, beta, h, interaction, frustration)

            return time_list
    
class SpinChange:

    def binary_spin_change(self, lattice, spin, beta=1, h=None, interaction='NN', frustration=0):
        n_lattice = np.size(lattice)
        J = ChoiceInt.choose_J(interaction, n_lattice)
        K = ChoiceInt.choose_K(frustration, n_lattice)

        if h is None:
            h = 0

        for _ in range(int(n_lattice)):
            x, y = np.random.randint(0, n_lattice), np.random.randint(0, n_lattice)
            dE = BinaryEnergy.binary_energy_diff(lattice, J, K, h, x, y)
            
            if dE < 0:
                pass
            else:
                prob = np.min(1,np.exp(-beta * dE))
                spin = lattice[x, y]

                factor = np.random.choice([spin,-spin], p=(prob, 1-prob))
                lattice[x, y] *= factor

        return lattice
    

    def general_spin_change(self, lattice, beta=1, h=0, interaction='NN', frustration=0):



        return lattice