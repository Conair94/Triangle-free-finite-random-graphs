# Triangle-free-finite-random-graphs
A github repository for searching for specific finite triangle free random graphs. 

Inside this repository you will find collections of scripts using different methods to find finite models of fragments of the theory of the generic triangle free random graph. 

It is a well known in model theory that the generic triangle free random graph is axiomatized by the following sentences; 

1. $\phi_0: \forall x_1,x_2,x_3, \neg\exists (E(x_1,x_2)\wedge E(x_1,x_3)\wedge E(x_2,x_3))$,
2. $\psi_k$: For $1\leq a \leq k$,  $\forall x_1,...,x_a, \wedge_{i\neq j} \neg E(x_i,x_j)\bigwedge y_1,...,y_{k-a}, \exists z : [\bigwedge_{1\leq i\leq k} E(z,x_i)]\wedge [\bigwedge_{1\leq i\leq k} \neg E(z,y_i)]$

It is easy to find graphs which satisfy $(\phi_0$ and $\psi_2)$, they are maximal triangle-free, twin-free graphs. For $(\phi_0$ and $\psi_3)$ a handful of families are known to exist It is unknown if any graphs exist which satisfy $(\phi_0\wedge \psi_4)$, let alone some large $n$. The goal of the project is to perform an exaustive and probalistic search for more examples of these types of graphs and furthermore determine if any examples in small number of vertices have been missed. 

If a class of graphs $\mathcal{G}=\{G_n:n\in \mathbb{N}\}$ could be found where $G_n\vDash \phi_0\wedge \psi_n$ then this would resolve Cherlin's problem on the pseudofiniteness of the generic triangle free random graph. 
## Variations of Axiomatizations
**Corollary 4 in [1]** 

For $k\leq 3$, A finite triangle-free graph $G$ has property $\psi_k$ if and only if the following properties hold:
1. Every independent set of vertices of cardinality $\leq k$ has a common neighbor
2. There do not exist two vertices $x,y\in G$ with $N(x)=N(y)$. 
3. $G$ is not isomorphic to the circular graph $O_{3n-1}$ for $n \geq 1$. 

It is much easier to check the above three properties rather than $\psi_k$ so this is how we will start. Furthermore we can use other restrictions on the implied property of the graph to limit the search space as follows: 
### Limiting the Search Space

## Enumeration Techniques

## Monte Carlo Methods

## Bibliography
1. "On Triply Existentially Complete Triangle-Free Graphs" https://arxiv.org/abs/1306.5637
2. "On Existentially Complete Triangle-Free Graphs" https://arxiv.org/abs/1708.08817
3. "Notes on Pseudofinite theories" https://www.math.ucla.edu/~chernikov/teaching/19F-MATH223M/Notes.pdf
