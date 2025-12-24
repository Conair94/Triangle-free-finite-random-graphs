## Triangle-free-finite-random-graphs
A github repository for searching for finite triangle free random graphs. 

Inside this repository you will find collections of scripts using different methods to find finite models of fragments of the theory of the generic triangle free random graph. 

It is a well known in model theory that the generic triangle free random graph is axiomatized by the following sentences; 

1. $phi_0: \forall x_1,x_2,x_3, \neg\exists (E(x_1,x_2)\wedge E(x_1,x_3)\wedge E(x_2,x_3))$,
2. $psi_n: \forall x_1,...,x_n, \wedge_{i\neq j} \neg E(x_i,x_j)\bigwedge y_1,...,y_n, \exists z : [\bigwedge_{1\leq i\leq n} E(z,x_i)]\wedge [\bigwedge_{1\leq i\leq n} \neg E(z,y_i)]$

It is easy to find graphs which satisfy \phi_0 and \psi_1. It is unknown if any graphs exist which satisfy \phi_0\wedge \psi_2, let alone some large n. 

If a class of graphs $G=\{G_n:n\in \N\}$ could be found where $G_n\vDash \phi_0\wedge \psi_n$ then this would resolve Cherlin's problem on the pseudofiniteness of the generic triangle free random graph. 

# Enumeration

# Monte Carlo Methods
