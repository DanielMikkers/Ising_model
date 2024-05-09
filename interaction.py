import numpy as np

interaction_dict_arrays = {'4': np.array([[0,1,0],[1,0,1],[0,1,0]]),
                           '8': np.array([[1/2,1,1/2],[1,0,1],[1/2,1,1/2]]),
                           '12': np.array([[0,0,1/4,0,0],[0,1/2,1,1/2,0],[1/4,1,0,1,1/4],[0,1/2,1,1/2,0],[0,0,1/4,0,0]]),
                           '20': np.array([[0,1/8,1/4,1/8,0],[1/8,1/2,1,1/2,1/8],[1/4,1,0,1,1/4],[1/8,1/2,1,1/2,1/8],[0,1/8,1/4,1/8,0]]),
                           '24': np.array([[1/16,1/8,1/4,1/8,1/16],[1/8,1/2,1,1/2,1/8],[1/4,1,0,1,1/4],[1/8,1/2,1,1/2,1/8],[1/16,1/8,1/4,1/8,1/16]])}

class Interaction:
    def init_J(self, size, nearest=0, ferro=True):
        n, m = size
        alpha = n*np.log(2)/2
        x = np.linspace(-1,1,n)
        y = np.linspace(-1,1,m)
        X,Y = np.meshgrid(x,y)
        J = np.exp(-alpha*(np.absolute(X) +np.absolute(Y)))
        J[J<1e-10] = 0

        anti_ferro = np.random.choice([-1,1], size=size, p=[0.1,0.9])

        if nearest == 0:
            if ferro:
                return J
            else:
                return J*anti_ferro
        
        else:
            near = str(nearest)
            J = interaction_dict_arrays[near]

            if ferro:
                return J
            else:
                return J*anti_ferro
    
    def init_K(self, size):
        if size[0] == size[1] and size[0] % 2 == 0:
            raise ValueError("Wrong array size")
        alpha = size[0]*np.log(2)/4

        x = np.linspace(-1,1,size[0])
        y = np.linspace(-1,1,size[0])
        X,Y = np.meshgrid(x,y)

        K = np.exp(-alpha*(np.absolute(X) +np.absolute(Y)))
        K[K<1e-10] = 0
        
        return K
    
class Moment:
    def init_mu(self):
        mu = 1
        return mu
    