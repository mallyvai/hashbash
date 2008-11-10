Proposal: Using a genetic algorithm to create a hash function(s).

Most commonly used hash functions operate by repeatedly applying small, simple operations to input blocks. The usefulness of a hash function is measured by a series of metrics, including confusion, diffusion, apparent randomness, and difficulty of invertibility of the output. All but the last of these metrics are easy to test. It is possible to use these facts to design a genetic algorithm that operates in the following way: Randomly create a large number of hash functions using the discrete bitwise operators, plus additional trivial expansion, slicing, and segmenting operators. Test the fitness of each generated hash function and order them by fitness. Discard the least fit, and create a series of new hash functions that consist of subsets of operations of the fittest existing hash functions, and incorporate a chance of mutation. Randomly generate a new batch, and the constructed hash functions to the new batch, and repeat the algorithm. After a significant interval, the algorithm should pause, and allow for manual pruning of the functions.

Generation
First, all possible operations ("genes") have to be defined in some compact, easily-representable way, so that the generation and the recombining/breeding process can be done as easily and efficiently as possible. Also, it would be nice to have the stipulation that it is impossible (or at least very difficult) to have an "illegal" chromosome that violates syntax rules, for further simplification. Essentially what we want is an easily parseable language that is difficult or impossible to have syntax errors in. I'm not sure yet whether or not it would be wise to give the hash function language full Turing-completeness, but I'm going to try both.

I'm going to first try using a kind of reverse polish notation so i can avoid avoid to deal with parentheses and order of operations in my parser and generator.

&, +, ~, b, slice(parameters, blocks), I for input, and a simple conditional.
I'm going try this approach first.


-Vaibhav

