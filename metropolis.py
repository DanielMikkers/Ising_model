import numpy as np
from energy import Energy
from interaction import IntType
from utils import spin_array

class SpinChange:
    def __init__(self, spin) -> None:
        self.spin = spin

    def binary_spin_change(self, lattice, interaction, frustration, beta, h=None):
        n_lattice = np.shape(lattice)
        n_sites = np.size(lattice)
        idx1, idx2 = n_lattice

        J = interaction
        K = frustration

        if h is None:
            h = np.zeros(n_lattice)

        energy_lattice = Energy(J, K, h)
        
        for i in range(n_sites):
            idx = (np.random.randint(0, idx1),np.random.randint(0, idx2))
            dE = energy_lattice.binary_energy_diff(lattice, idx)

            prob = np.minimum(1,np.exp(-beta*dE))

            spin = lattice[idx].copy()

            lattice[idx] = np.random.choice([spin,-spin], p=[1-prob, prob])

        return lattice
    
    def gen_spin_change(self, lattice, interaction, frustration, beta=1, h=None):

        n_lattice = np.shape(lattice)
        n_sites = np.size(lattice)

        spin_arr = spin_array(spin)

        J = interaction
        K = frustration

        if h is None:
            h = np.zeros(n_lattice)
        
        energy_lattice = Energy(J, K, h)

        for _ in range(n_sites*n_sites):
            idx = (np.random.randint(0, n_sites), np.random.randint(0, n_sites))
            dE = energy_lattice.gen_energy_diff(lattice, idx)

            exp = np.exp(-beta * dE)

            prob = np.minimum(1,exp)
            norm = np.sum(prob)
            if norm > 1:
                prob = prob / norm 
            
            spin = lattice[idx]
            new_spin = np.random.choice(spin_arr, p=prob)
            lattice[idx] = new_spin
            
        return lattice
    
class TimeEvolution:
    def __init__(self, spin, beta=1, h=None, interaction='NN', frustration=None, antiferro=False) -> None:
        self.spin = spin
        self.beta = beta
        self.hfield = h 
        self.Jint = 'NN'
        self.Kint = frustration
        self.antiferro = antiferro
    
    def time_evolve(self, lattice, t_end=20):
        n_lattice = np.shape(lattice)
        
        spin_change_dict = {
                'bin': SpinChange(self.spin).binary_spin_change,
                'gen': SpinChange(self.spin).gen_spin_change
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