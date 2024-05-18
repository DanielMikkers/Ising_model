# Binary Choices of Groups of People using An Ising-Like Model

TO DO:

- magnetic moment function: create something for magnetic moment, such that not everyone may align with the opinion of the external field
- long range function: some sites act as long range site which have a positive (or negative influence) on most if not all sites
- choice changing function: now minimalization algorithm, thus everything tends to either $+1$ or $-1$. Some if-statements or different terms in the Hamiltonian may change this to something more realistic for human behaviour

## Physics \& Mathematics
The Ising model describes a lattice where spin causes interactions, where the spins can either be $+1$ or $-1$. Consider a set $\Lambda$ of lattice sites, each with neighbouring lattice sites, forming a $d$-dimensional lattice. For each lattice site $k \in \Lambda$ there is a discrete variable $\sigma_k \in \{ -1, +1\}$ representing the spin of the site. The spin configuration of the lattice is then $\sigma = \{ \sigma_k\}_{k\in\Lambda}$. 

Between sites $i,j \in \Lambda$ there is an interaction $J_{ij}$. The most commonly used interaction type between sites is the nearest neighbor (NN) interaction. Although NN interactions are commonly used, the interaction $J_{ij}$ can incorporate the interaction with the whole lattice. The downside of this is that it may be numerically more costly than NN or next-to-NN interactions.

Site $j \in \Lambda$ can also be subject to a external magnetic field $h_j$ and interact with it. The magnetic moment $\mu$ of the lattice sites influences how the sites interact with the magnetic field. 

The energy of the lattice for a certain configuration $\sigma$ is given by the Hamiltonian:

$$H = - \sum_{\langle i,j \rangle} J_{ij} \sigma_i \sigma_j - \sum_i \mu_i h_i \sigma_i.$$

Here the sum over $\langle i,j \rangle$ represents the sum over nearest neighbors, i.e. the sum only sums over sites where $i$ and $j$ are neighboring lattice sites. This can be extended to the whole lattice. 

The configuration probability is given by the Boltzmann distribution

$$ P_\beta(\sigma) = \frac{e^{-\beta H(\sigma)}}{Z_{\beta}},$$

where $\beta = 1/k_BT$ and the normalization function

$$ Z_\beta = \sum_\sigma e^{-\beta H(\sigma)}$$

is the partition function. For a function $f(\sigma)$ the expectation value is given by

$$\langle f \rangle_{\beta} = \sum_\sigma f(\sigma) P_\beta(\sigma).$$

Probability $P_\beta(\sigma)$ is the probability of finding the lattice $\Lambda$ in configuration $\sigma$. The system will always tend to state or configuration with a lower energy.

The inverse temperature $\beta$ can be thought of as a randomness factor. If $\beta$ is small (and $T$ is large), there is a lot of randomness. This is because as $\beta \to 0$ the probability $P_\beta(\sigma)$ goes to a uniform distribution, as the probability for all configurations is equal ($1/Z_{\beta}$). As $\beta$ increases (and $T$ decreases) there is less randomness. This is because numerator of $P_\beta(\sigma)$ tends to zero $\forall \sigma$ and the probability of changing spin is extremely small. Physically one can interpret this as for small $\beta$ the system borrows energy from the temperature and is able to be in every configuration it wants, because there is enough energy available to be in all configurations with equal probability. And for large $\beta$ this can be thought of as going towards absolute zero, the lattice sites do not have energy to change spin. 

Using the sign convention of the Hamiltonian $H(\sigma)$ as given above, the signs of $J_{ij}$ and $h_j$ have the following consequences for pair $i,j$ and site $j$, respectively:

- $J_{ij} < 0$: the spins favor anti-alignment of spins on neighbouring sites (ant-ferromagnetism);
- $J_{ij} = 0$: no interaction between neighboring spin sites;
- $J_{ij} > 0$: the spins favor to line up with the spins on neighbouring sites in the same direction (ferromagnetism);

- $h_j < 0$: the spin site  favor to line up in the negative direction;
- $h_j = 0$: there is no external field influence on the spins;
- $h_j > 0$: the spin site  favor to line up in the positive direction.

Let's say that $\mu$ can also have a different signs and may be site dependent, then

- $\mu_j < 0$: the influence of $h_j$ on the spin at site $j$ is reversed relative to the signs above, i.e. spins favour to anti-align with external magnetic field $h$;
- $\mu_j = 0$: $h_j$ does not influence the spin of site $j$
- $\mu_j > 0$: the influence of $h_j$ on the spin at site $j$ stays the same as stated above, i.e. favours alignment with the external magnetic field $h$.

Both $\mu$ and $h$ being site dependent is overkill. Therefore I would choose either one of the two to be site dependent and the other can be set to some constant value for the whole lattice. 

For a $d$-dimensional lattice a $d$-dimensional coordinate vector is needed to express the location of the lattice site. A visual example of a 2D square lattice is given below, where the red arrows represent the connection of site $(i_1,i_2)$ to its nearest neighbours. In a $d$-dimensional square lattice the number of nearest neighbours is $2d$, so in two dimensions the number of nearest neighbours is 4. I believe it is also possible to have different lattice configurations, such as hexagonal, but computationally and visually square lattices are easy. 

## Translation to Groups
The main idea is that one can think people in a group making binary decisions as a lattice with spins $+1$ and $-1$. The spins represent the decisions which can be made. Each individual person represents a lattice site and their neighbouring sites represent the people closest to that person that can effect the choice a person makes. The closer sites are (like NN) the more the they effect the lattice site in question.

As an example take the 2 dimensional Ising model, as in Fig. \ref{fig:lattice}; each 'person' has four close contacts which can heavily influence the 'person'. If one chooses to go beyond NN, the NNN also have some influence but they may be less then the NN -- note that this depends heavily on the choice of $J_{ij}$ as this interaction can be chosen to be anything you want. 

The external magnetic field can be thought of as external influences which reaches a lot of people, such as political campaigns, a speech of the Dutch king or Dutch PM. If we take $h$ to be position independent -- i.e. constant for the whole lattice -- $\mu$ can be thought of as the agreement/disagreement variable: does one want to align or anti-align with choice of the external influence. For example if Geert Wilders or Frans Timmermans gives a speech, there are people which will align easily with the opinion/choice of either one, but there will also be people who will want to do the opposite of what they say or are against the person itself (i.e. anti-align). 

The inverse temperature $\beta$ is some randomness factor which can give or take away randomness. This can be thought of as fake news or a financial crisis for example. These influences give more randomness to the system as people may not know what to believe and change opinion with a higher probability. Examples of how $\beta$ can be chosen: 

- In a strictly controlled dictatorship, such as North-Korea, the randomness factor $\beta$ will be very high. There is not much randomness, because all media, internet and economy is controlled by the government. There is less freedom to switch your opinion/choice, because most people are aligned with the ideas of the government and there are no influences from outside (which cause a higher `temperature', not to be confused with an external field) to change their opinion.
- If there were elections during the COVID pandemic in the USA, there may have been more randomness than before. Although people usually may align with either Democratic or Republican ideas and legislation, the ideas of the parties during pandemic may have moved people from one side to the other or vice versa. Although usually these people would have stayed with ``their'' party, they may have changed opinion only because of the actions and ideas of the respective party during the pandemic.

## Algorithm
A specific algorithm that can be used is the Metropolis algorithm. One sets a lattice and then calculate the difference in energy by staying or changing from spin. The acceptance probability in the algorithm for changing spin is given by

$$ A(s \to s') = \text{min}\left(1, \exp{\left(-\beta\Delta E \right)}\right),$$

where

$$ \Delta E_i = E_{k,i} - E_{0,i} = 2\sigma_i \sum_j J_{ij} \sigma_j + 2h\mu_i\sigma_i $$

for fixed $i$.
This can be fed to a binomial distribution and which then with probability $A$ either accepts or rejects a change of spin.

The new lattice is fed again and again to the algorithm and then new lattices are created for new time-steps.

## Extensions
Changing opinion every time is maybe not favourable, but staying with your opinion for more than $X$ iterations may also not be favourable. Therefore one may change certain conditions, such that the probability can be increased or decreased by a certain amount. It is also possible to add other conditions with if-statements. This may make it numerically more intense.

Moreover, one is able to make a number of sites have a large radius of influence, such as influences, politicians, writers and journalists. These have an $J_{ij}$ covering the whole lattice instead of just their neighbours (NN, NNN, NNNN, etc.).

It is possible to have more options than just binary options, than one could go to spin- $\frac{3}{2}$ ($\sigma_k \in \{ -2, -1, 1, 2 \}$) or spin-2 ( $\sigma_k \in [ -1,0,1 ]$ ) models. These give more complexity and may be more prone to errors. This makes the model more complex, as there will be more terms in the Hamiltonian. Therefore it will be numerically more intense and it will make the code more complex. 

The simple binary Ising model as described above can be made more complex by including also more complex interaction terms between the spins and external fields.

I also believe that external fields are additive. So suppose one has two fields: $h_1$ and $h_2$ which are position independent and have equal $\mu = 1$. The effect of the both fields simultaneously can be seen as a new field $h_{tot} = h_1 + h_2$.

Concluding that the spin-1 Ising model is just a simple model and may be made more complex, either mathematically or code-wise. 
