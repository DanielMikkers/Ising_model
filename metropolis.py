import numpy as np
from lattice import RandomLattice
from energy import BinaryEnergy
from interaction import Interaction, Moment

interaction_dict = {'NN': Interaction.init_J(3,1),
               'NNN': Interaction.init_J(3,2),
               '4N': Interaction.init_J(5,3),
               '5N': Interaction.init_J(5,4),
               '6N': Interaction.init_J(5,5)
               }

class Metropolis:

    def spin_change(self, lattice, beta, h, interaction='NN'):
        n_lattice = np.size(lattice)
        J = self.choose_J(interaction)

        if h is None:
            h = 0

        for _ in range(int(n_lattice*n_lattice)):
            x, y = np.random.randint(0, n_lattice), np.random.randint(0, n_lattice)
            dE = BinaryEnergy.binary_energy_diff(lattice, J, h, x, y)
            
            if dE < 0:
                pass
            else:
                prob = np.exp(-beta * dE)
                spin = lattice[x, y]
                factor = np.random.choice([spin,-spin], p=(prob, 1-prob))
                lattice[x, y] *= factor

        return lattice
    
    def choose_J(self, interaction):
        if not isinstance(interaction, np.ndarray):
            if not isinstance(interaction, str):
                if interaction % 2 == 1:
                    J = Interaction.init_J(interaction)
                else:
                    raise ValueError("The size of the interaction matrix should be an odd value.")
            elif interaction in interaction_dict:
                J = interaction_dict[interaction]
        
        elif isinstance(interaction, np.ndarray):
            J = interaction
        else:
            raise ValueError("Incorrect value of 'interaction' given")
        return J
    
    def time_evolution(self, lattice, t_end, beta=1, h=None, interaction='NN'):
        time_list = []
        time_list.append(lattice)

        for _ in range(t_end):
            lattice = self.spin_change(lattice, t_end, beta, h, interaction)

        return time_list