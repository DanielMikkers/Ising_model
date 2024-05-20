import numpy as np

class Interaction:
    def __init__(self, n_lattice, antiferro) -> None:
        self.n_lattice = n_lattice
        self.n_sites = np.prod(n_lattice)
        self.n, self.m = n_lattice
        self.antiferro = antiferro

        self.interaction_dict_arrays = {'4': np.array([[0,1,0],[1,0,1],[0,1,0]]),
                           '8': np.array([[1/2,1,1/2],[1,0,1],[1/2,1,1/2]]),
                           '12': np.array([[0,0,1/4,0,0],[0,1/2,1,1/2,0],[1/4,1,0,1,1/4],[0,1/2,1,1/2,0],[0,0,1/4,0,0]]),
                           '20': np.array([[0,1/8,1/4,1/8,0],[1/8,1/2,1,1/2,1/8],[1/4,1,0,1,1/4],[1/8,1/2,1,1/2,1/8],[0,1/8,1/4,1/8,0]]),
                           '24': np.array([[1/16,1/8,1/4,1/8,1/16],[1/8,1/2,1,1/2,1/8],[1/4,1,0,1,1/4],[1/8,1/2,1,1/2,1/8],[1/16,1/8,1/4,1/8,1/16]]),
                           'lattice': 0}

    def init_J(self, sub_lattice, n_neighbours, use_lattice=False):
        if use_lattice is True:
            alpha = self.n*np.log(2)/2
            x = np.linspace(-1,1,self.n)
            y = np.linspace(-1,1,self.m)
            X,Y = np.meshgrid(x,y)
            J = np.exp(-alpha*(np.absolute(X) +np.absolute(Y)))
            J[J<1e-10] = 0
        else:
            J = self.interaction_dict_arrays[n_neighbours]

        if self.antiferro:
            anti_ferro_fact = np.random.choice([-1,1], size=sub_lattice, p=[0.25,0.75])
            return J*anti_ferro_fact
        else:
            return J
    
    def init_K(self, n_neighbours, use_lattice=False):
        if use_lattice is True:
            alpha = self.n*np.log(2)/2
            x = np.linspace(-1,1,self.n)
            y = np.linspace(-1,1,self.m)
            X,Y = np.meshgrid(x,y)
            K = np.exp(-alpha*(np.absolute(X) +np.absolute(Y)))
            K[K<1e-10] = 0
        else:
            K = self.interaction_dict_arrays[n_neighbours]

class IntType:
    def __init__(self, n_lattice, use_lattice, antiferro) -> None:
        self.n_lattice = n_lattice
        self.n_sites = np.prod(n_lattice)
        self.use_lattice = use_lattice
        self.antiferro = antiferro

        self.interaction_dict = {'NN': Interaction(self.n_lattice,self.antiferro).init_J((3,3),'4'),
               'NNN': Interaction(self.n_lattice,self.antiferro).init_J((3,3),'8'),
               '4N': Interaction(self.n_lattice,self.antiferro).init_J((5,5),'12'),
               '5N': Interaction(self.n_lattice,self.antiferro).init_J((5,5),'20'),
               '6N': Interaction(self.n_lattice,self.antiferro).init_J((5,5),'24'),
               'lattice': Interaction(self.n_lattice,self.antiferro).init_J(self.n_lattice, 'lattice', use_lattice=self.use_lattice)
               }

    def type_Jint(self, interaction):
        if interaction in self.interaction_dict:
            return self.interaction_dict[interaction]
    
    def type_Kint(self, interaction):
        if interaction in self.interaction_dict:
            return self.interaction_dict[interaction]