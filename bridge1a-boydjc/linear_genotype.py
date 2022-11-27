import random
import numpy as np

class LinearGenotype():
    def __init__(self):
        self.fitness = None
        self.gene = None

    def random_initialization(self, length, x_bounds, y_bounds):
        # DONE: Add random initialization of fixed-length linear gene
        # IMPORTANT: must be generated as floating-point (real) values, NOT integers
        # try using random.uniform()

        xValues = np.random.uniform(x_bounds[0], x_bounds[1], length)
        yValues = np.random.uniform(y_bounds[0], y_bounds[1], length)
	
        # combine the two xValues and yValues np arrays
        self.gene = np.stack((xValues, yValues), axis=-1)

        # convert numpy array to list of tuples
        self.gene = list(map(tuple, self.gene))
        
        return self.gene

    def recombine(self, mate, method, **kwargs):
        child = LinearGenotype()
        
        # TODO: Recombine genes of self with mate and assign to child's gene member variable
        assert method.casefold() in {'uniform', '1-point crossover', 'bonus'}
        if method.casefold() == 'uniform':
            # perform uniform recombination
            pass
        elif method.casefold() == '1-point crossover':
            # perform 1-point crossover
            pass
        elif method.casefold() == 'bonus':
            ''' 
            This is a red deliverable (i.e., bonus for anyone).

            Implement the bonus crossover operator as described in deliverable
            Red 1 of Assignment 1b.
            '''
            pass

        return child

    def mutate(self, x_bounds, y_bounds, **kwargs):
        copy = LinearGenotype()
        copy.gene = self.gene.copy()
        
        # TODO: mutate gene of copy
        pass

        return copy

    @classmethod
    def initialization(cls, mu, *args, **kwargs):
        population = [cls() for _ in range(mu)]
        for i in range(len(population)):
            population[i].random_initialization(*args, **kwargs)
        return population
