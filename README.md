# Triangle-free-finite-random-graphs
A github repository for searching for $k$-existentially closed triangle free graphs, inspired by the generic triangle free random graph. 

Inside this repository you will find collections of scripts using different methods to find finite models of fragments of the theory of the generic triangle free random graph. The goal of the project is to perform an exaustive search for $k$-existentially closed graphs for graphs to verify if any small size examples have been missed, while also currating relevant research.

It is a well known in model theory that the generic triangle free random graph is axiomatized by the following sentences; 

1. $\phi_0: \forall x_1,x_2,x_3, \neg\exists (E(x_1,x_2)\wedge E(x_1,x_3)\wedge E(x_2,x_3))$,
2. $\psi_k$: For $1\leq a \leq k$,  $\forall x_1,...,x_a, \wedge_{i\neq j} \neg E(x_i,x_j)\bigwedge y_1,...,y_{k-a}, \exists z : [\bigwedge_{1\leq i\leq k} E(z,x_i)]\wedge [\bigwedge_{1\leq i\leq k} \neg E(z,y_i)]$

The property $psi_k$ is known as being $k$-existentially closed. It is easy to find graphs which satisfy $(\phi_0$ and $\psi_2)$, they are maximal triangle-free, twin-free graphs. For $(\phi_0$ and $\psi_3)$ a handful of families are known to exist. It is unknown if any graphs exist which satisfy $(\phi_0\wedge \psi_4)$, let alone some larger $n$. It is known that if a graph which satisfies $(\phi_0\wedge \psi_4)$ exists,  it must be have minimal vertex degree of 66 via Cor. 12.7.1 in [1] and thus is vastly outside of computational search. Nevertheless, given how sparse examples for the case of $psi_3$ are, hopefully more knowledge of examples could shed some light on this problem. 

If a class of graphs $\mathcal{G}=\{G_n:n\in \mathbb{N}\}$ could be found where $G_n\vDash \phi_0\wedge \psi_n$ then this would resolve demonstrate pseudofiniteness of the generic triangle free random graph. Likewise, the lack of existence of such a family would refute pseudofiniteness.  

## Variations of Axiomatizations
**Corollary 4 in [2]** 

For $k\leq 3$, A finite triangle-free graph $G$ has property $\psi_k$ if and only if the following properties hold:
1. Every independent set of vertices of cardinality $\leq k$ has a common neighbor
2. There do not exist two vertices $x,y\in G$ with $N(x)=N(y)$. 
3. $G$ is not isomorphic to the circular graph $O_{3n-1}$ for $n \geq 1$. 

It is much easier to check the above three properties rather than $\psi_k$ so this is how we will start. Furthermore we can use other restrictions on the implied property of the graph to limit the search space as follows: 
### Limiting the Search Space

## Enumeration Techniques

## Monte Carlo Methods

## Bibliography

### Of Direct Concern: 
1. "Two Problems on Homogeneous Structures, Revisted" https://sites.math.rutgers.edu/~cherlin/Paper/census.pdf
2. "On Triply Existentially Complete Triangle-Free Graphs" https://arxiv.org/abs/1306.5637
3. "On Existentially Complete Triangle-Free Graphs" https://arxiv.org/abs/1708.08817
4. "Triange-Free Graphs with Diameter 2" https://arxiv.org/pdf/2406.00246
5. "Notes on Pseudofinite theories" https://www.math.ucla.edu/~chernikov/teaching/19F-MATH223M/Notes.pdf

### Interesting and Adjacent Papers:
1. "The minimum number of maximal independent sets in twin-free graphs" https://uu.diva-portal.org/smash/get/diva2:1926761/FULLTEXT01.pdf
2. "Triangle-Free Graphs with Diameter 2" https://arxiv.org/pdf/2406.00246
3. "UNIVERSAL GRAPHS WITH A FORBIDDEN SUBGRAPH:
BLOCK PATH SOLIDITY" https://sites.math.rutgers.edu/~cherlin/Paper/PathSolidity.pdf
