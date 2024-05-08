import numpy as np
import scipy as sp
import scipy.linalg as spla
from scipy.ndimage import convolve
import matplotlib.pyplot as plt

class BinaryChoice_Ising: 
    def rnd_lattice_gen(self, sites):

        sq_int = int(np.sqrt(sites))
        if sites == sq_int * sq_int:
            spin = np.array([-1,1])
            lattice = np.random.choice(spin, size= (sq_int, sq_int), p = [0.5, 0.5])

            return lattice

        else:
            raise ValueError("'sites' should be a perfect square. Please give perfect square as input for 'sites'")

    def change_opinion(self, lattice, beta = 1., h = 0., mu_input = None, long_range = 0):
        dim = np.shape(lattice)

        if long_range == 0:
            long_range_arr = None
        else:
            long_range_arr = np.random.randint(0, [dim[0], dim[1]], size = (long_range,2))

        if isinstance(mu_input, np.ndarray):
            mu = mu_input
        else:
            mu = self.mag_mom_mu(lattice, long_range_arr)

        J_int = self.interaction_J(lattice, long_range_arr)

        Interaction_mult = lattice * J_int

        NN_int_sum = np.sum(Interaction_mult, axis = (3,2))
        
        dE = 2 * ( lattice * NN_int_sum ) + 2 * h * mu * lattice

        ones_array = np.ones(dim)
        p_exp = np.exp(- beta * dE)

        p_accept = np.minimum(ones_array, p_exp)

        p_flat = p_accept.flatten()
        lattice_flat = lattice.flatten()
        new_flat = np.zeros(np.size(lattice))
        for i in range(np.size(lattice)):
            new_flat[i] = np.random.choice( [lattice_flat[i], -lattice_flat[i]], size = None, p = [1-p_flat[i], p_flat[i]] )

        new_lattice_config = new_flat.reshape(np.shape(lattice))

        return new_lattice_config
    
    def mag_mom_mu(self, lattice, long_range_arr):
        dim = np.shape(lattice)
        num_NN = np.size(dim)
        N = np.size(lattice)

        NN_kernel = np.array([[0,1,0],
                              [1,0,1],
                              [0,1,0]])

        mu = lattice + convolve(lattice, NN_kernel, mode = 'wrap') / num_NN
        
        if isinstance(long_range_arr, np.ndarray):
            mu_new = mu.copy()
            long_range_kernel = np.ones(dim)
            NN_kernel_lattice = np.zeros(dim)

            for k in range(np.shape(long_range_arr)[0]):
                i = long_range_arr[k,0]
                j = long_range_arr[k,1]

                long_range_kernel[i][j] = 0

                rows = [(i-1) % NN_kernel_lattice.shape[0], i, (i+1) % NN_kernel_lattice.shape[0]]
                cols = [(j-1) % NN_kernel_lattice.shape[1], j, (j+1) % NN_kernel_lattice.shape[1]]

                NN_kernel_lattice[np.ix_(rows, cols)] = NN_kernel

                mu_new[i,j] = lattice[i,j] + np.sum(lattice * NN_kernel_lattice) / (num_NN) + np.sum(long_range_kernel * lattice)/(N-num_NN-1)
            return mu_new
    
        else:
            return mu

    def interaction_J(self, lattice, long_range_arr):
        dim_0 = np.shape(lattice)[0]
        dim_1 = np.shape(lattice)[1]

        J_interaction = np.zeros((dim_0,dim_1,dim_0,dim_1))

        NN_kernel = np.array([[0,1,0],
                              [1,0,1],
                              [0,1,0]])
        
        if isinstance(long_range_arr, np.ndarray):
            for i in range(dim_0):
                for j in range(dim_1):
                    rows = [(i-1) % J_interaction[i,j].shape[0], i, (i+1) % J_interaction[i,j].shape[0]]
                    cols = [(j-1) % J_interaction[i,j].shape[1], j, (j+1) % J_interaction[i,j].shape[1]]

                    J_interaction[i,j][np.ix_(rows, cols)] = NN_kernel

                    for q in range(np.shape(long_range_arr)[0]):
                        row_long, col_long = long_range_arr[q]
                        J_interaction[i,j][row_long,col_long] = 1
            
            long_range_kernel = np.ones((dim_0,dim_1))

            long_fact = 4

            J_new = J_interaction.copy()

            for k in range(np.shape(long_range_arr)[0]):
                site_array = np.zeros((dim_0,dim_1))
                site_array[long_range_arr[k][0]][long_range_arr[k][1]] = 1
                J_new[long_range_arr[k][0]][long_range_arr[k][1]] = ( (J_interaction[long_range_arr[k][0]][long_range_arr[k][1]] + (long_range_kernel - site_array) ) / 2 ) / long_fact
            
            return J_new

        else:
            for i in range(dim_0):
                for j in range(dim_1):
                    rows = [(i-1) % J_interaction[i,j].shape[0], i, (i+1) % J_interaction[i,j].shape[0]]
                    cols = [(j-1) % J_interaction[i,j].shape[1], j, (j+1) % J_interaction[i,j].shape[1]]

                    J_interaction[i,j][np.ix_(rows, cols)] = NN_kernel

            return J_interaction

    def change_opinion_ntimes(self, ntimes, lattice, beta = 1., h = 0., mu_input = None, long_range = 0):
        list_configs = []

        dim = np.shape(lattice)

        if long_range == 0:
            long_range_array = None
        else: 
            random_rows = np.random.randint(0, dim[0], size=long_range)
            random_cols = np.random.randint(0, dim[1], size=long_range)
            long_range_array = np.zeros((long_range, 2), dtype=int)

            long_range_array[:, 0] = random_rows
            long_range_array[:, 1] = random_cols

        J_int = self.interaction_J(lattice, long_range_array)
        Interaction_mult = lattice * J_int
        NN_int_sum = np.sum(Interaction_mult, axis = (3,2))

        ones_array = np.ones(dim)

        sum_configs = np.zeros(dim)

        for k in range(ntimes):
            if mu_input == None:
                mu = self.mag_mom_mu(lattice, long_range_array)
            else:
                mu = mu_input

            dE = 2 * ( lattice * NN_int_sum ) + 2 * h * mu * lattice

            ones_array = np.ones(dim)
            
            p_exp = np.exp(- beta * dE)

            if k < 3:
                p_accept = np.minimum(ones_array, p_exp)
            else:
                change = np.absolute(list_configs[k-1] - list_configs[k-2])
                change_loc = np.argwhere( change == 2 )
                for loc in change_loc:
                    row, col = loc
                    p_accept[row, col] /= 1.5

            if k > int(beta*5):
                no_change = np.absolute(sum_configs)
                no_change_loc = np.argwhere( no_change > k/1.25 )
                
                for loc in no_change_loc:
                    row_nc, col_nc = loc
                    p_exp[row_nc, col_nc] = no_change[row_nc, col_nc]*np.exp(- beta * dE[row_nc, col_nc]) / (k/1.25)
                
                p_accept = np.minimum(ones_array, p_exp)
            else: 
                p_accept = np.minimum(ones_array, p_exp)

            p_flat = p_accept.flatten()
            lattice_flat = lattice.flatten()
            new_flat = np.zeros(np.size(lattice))
            for i in range(np.size(lattice)):
                new_flat[i] = np.random.choice( [lattice_flat[i], -lattice_flat[i]], size = None, p = [1-p_flat[i], p_flat[i]] )

            new_lattice_config = new_flat.reshape(np.shape(lattice))

            list_configs.append(new_lattice_config)
            sum_configs += list_configs[k]

        return list_configs, long_range_array

class Plot_lattice:
    def plot_lattice(lattice, color = 'Greys'):
        plt.figure()
        plt.imshow(lattice, cmap = color, origin = 'lower', interpolation = None)
        plt.show()

        return 0


binaryChoiceModel = BinaryChoice_Ising()
lattice_plotter = Plot_lattice()