import numpy as np
from energy import Energy
from interaction import IntType
from utils import spin_array

class SpinChange:
    """
    Class to represent to spin change for the lattice in one time iteration.
    
    Args:
    ----------
    spin:   int. This value is only relevant if general spin function 
            (gen_spin_change) is called. In turn this value is used to generate
            array of possible spins given the spin value

    Inside this class are two functions, binary_spin_change and gen_spin_change,
    which use the same algorithm to determine the spin changes: Metropolis-Hastings
    algorithm. The two functions work the same, only small details change.
    The code works as follows:
        1. Energy class in called to initialize the energy with the 
           interactions, frustration and the external field;
        2. For-loop in started in range of the number of sites on the lattice;
        3. Inside the for-loop a random coordinate is drawn from the lattice, then
           the energy difference of the (sub)lattice is calculated. The probability 
           of changing the spin is calculated which is the minimum value of 1 and the 
           exponential of the energy difference. The new spin is chosen on the given 
           the probability and spin, using a binomial/multinomial drawing. 
        4. After the for-loop ended the new lattice is returned.

    """

    def __init__(self, spin) -> None:
        self.spin = spin
        self.spin_arr = spin_array(spin)

    def binary_spin_change(self, lattice, interaction, frustration, beta, h=None):
        """
        binary_spin_change is a function which calculates the energy difference by 
        changing spin and returns the new lattice, for a spin (-1,+1) system.

        Input
        ----------
        lattice:     2d array. The old lattice with spin values (-1,+1);
        interaction: 2d array. The interaction array (e.g. nearest neighbor interaction);
        frustration: 2d array. The frustration array of the system.
        beta:        float. The inverse temperature, i.e. how much randomness there is 
                     inside the lattice
        h:           TBA

        Output
        ---------
        lattice:    2d array. The new lattice array with possibly changed spins.
        
        """
        n_lattice = np.shape(lattice)
        n_sites = np.size(lattice)
        idx1, idx2 = n_lattice

        J = interaction
        K = frustration

        if h is None:
            h = np.zeros(n_lattice)

        energy_lattice = Energy(J, K, h)
        
        for _ in range(n_sites):
            idx = (np.random.randint(0, idx1),np.random.randint(0, idx2))
            dE = energy_lattice.binary_energy_diff(lattice, idx)

            prob = np.minimum(1,np.exp(-beta*dE))

            spin = lattice[idx].copy()

            lattice[idx] = np.random.choice([spin,-spin], p=[1-prob, prob])

        return lattice
    
    def gen_spin_change(self, lattice, interaction, frustration, beta, h=None):
        """
        gen_spin_change is a function which calculates the energy difference by 
        changing spin and returns the new lattice, for a general spin system.
        See spin_array inside utils for what the spin array given some spin.

        Input
        ----------
        lattice:     2d array. The old lattice with spin values (-s,...,s) or (-s,...,-1,1,...,s);
        interaction: 2d array. The interaction array (e.g. nearest neighbor interaction);
        frustration: 2d array. The frustration array of the system.
        beta:        float. The inverse temperature, i.e. how much randomness there is 
                     inside the lattice
        h:           TBA

        Output
        ---------
        lattice:    2d array. The new lattice array with possibly changed spins.
        
        """

        n_lattice = np.shape(lattice)
        n_sites = np.size(lattice)

        J = interaction
        K = frustration

        if h is None:
            h = np.zeros(n_lattice)
        
        energy_lattice = Energy(J, K, h)

        for _ in range(n_sites):
            idx = (np.random.randint(0, n_sites), np.random.randint(0, n_sites))
            dE = energy_lattice.gen_energy_diff(lattice, idx)

            exp = np.exp(-beta * dE)

            prob = np.minimum(1,exp)
            norm = np.sum(prob)
            if norm > 1:
                prob = prob / norm 
            
            spin = lattice[idx]
            new_spin = np.random.choice(self.spin_arr, p=prob)
            lattice[idx] = new_spin
            
        return lattice
    
class TimeEvolution:
    """
    Class to obtain the time evolution of the spin system.

    Args:
    ----------
    spin:           int. This value is only relevant if general spin function 
                    (gen_spin_change) is called. In turn this value is used to generate
                    array of possible spins given the spin value
    beta:           float. 
    h:              NoneType or 2d array
    interaction:    string.
    frustration:    string.
    antiferro:      bool. If there is antiferromagnetic behavior
    """

    def __init__(self, spin, beta=1, h=None, interaction='NN', frustration=None, antiferro=False) -> None:
        self.spin = int(spin)
        self.beta = beta
        self.hfield = h 
        self.Jint = interaction
        self.Kint = frustration
        self.antiferro = antiferro
    
    def time_evolve(self, lattice, t_end=20):
        n_lattice = np.shape(lattice)

        spin_change = SpinChange(self.spin)
        
        spin_change_dict = {
                'bin': spin_change.binary_spin_change,
                'gen': spin_change.gen_spin_change
            }

        if self.spin == 1:
            type = 'bin'
        elif self.spin > 1:
            type = 'gen'
        else:
            type = 'bin'
            print("Invalid spin, binary model is chosen.")

        if self.Jint == 'lattice':
            use_lattice = True
        else:
            use_lattice = False

        int_type = IntType(n_lattice, use_lattice, self.antiferro)

        J = int_type.type_Jint(self.Jint)
        
        if self.Kint is None:
            K = np.zeros(n_lattice)
        else:
            K = int_type.type_Kint(self.Kint)

        lattice_evolve = []
        lattice_evolve.append(lattice)

        latt = lattice.copy()

        for i in range(t_end):
            
            latt = spin_change_dict[type](lattice, beta=self.beta, h=self.hfield, interaction=J, frustration=K)
            lattice_evolve.append(latt.copy())

        return lattice_evolve