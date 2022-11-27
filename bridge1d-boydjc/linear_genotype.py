import random

class LinearGenotype():
    def __init__(self):
        self.fitness = None
        self.gene = None

    def random_initialization(self, length, x_bounds, y_bounds):
        # Add random initialization of fixed-length linear gene
        # IMPORTANT: must be generated as floating-point (real) values, NOT integers
        # try using random.uniform()

        self.gene = [(random.uniform(*x_bounds), random.uniform(*y_bounds)) for _ in range(length)]
        
        return self.gene

    def recombine(self, mate, method, **kwargs):
        child = LinearGenotype()
        
        # Recombine genes of self with mate and assign to child's gene member variable
        assert method.casefold() in {'uniform', '1-point crossover', 'bonus'}
        if method.casefold() == 'uniform':
            # perform uniform recombination
            gene = []

            randomAmounts = [random.uniform(0, 1) for _ in range(len(self.gene))]

            for index in range(len(self.gene)):
                gene.append(self.gene[index]) if randomAmounts[index] < 0.5 else gene.append(mate.gene[index])

            child.gene = gene

        elif method.casefold() == '1-point crossover':
            # perform 1-point crossover

            crossoverPoint = random.randint(1, len(self.gene)-1)

            child.gene = self.gene[:crossoverPoint] + mate.gene[crossoverPoint:]

        elif method.casefold() == 'bonus':
            # shuffle crossover
            # http://www.cse.unsw.edu.au/~cs9417ml/GA2/crossover_alternate.html

            # choose crossoverPoint
            crossoverPoint = random.randint(1, len(self.gene)-1)

            # shuffle each parent with same shuffle order
            shuffleOrder = random.sample(range(len(self.gene)), k=len(self.gene))

            selfGeneShuffled = [self.gene[i] for i in shuffleOrder]

            mateGeneShuffled = [mate.gene[i] for i in shuffleOrder]

            # make the crossover based on the shuffled parents
            child.gene = selfGeneShuffled[:crossoverPoint] + mateGeneShuffled[crossoverPoint:]

            # unshuffle the positions in the child
            for count in range(len(child.gene)):
                if count <= crossoverPoint:
                    for selfGeneCount in range(crossoverPoint-1):
                        if(self.gene.index(child.gene[selfGeneCount]) > self.gene.index(child.gene[selfGeneCount+1])):
                            temp = child.gene[selfGeneCount+1]
                            child.gene[selfGeneCount+1] = child.gene[selfGeneCount]
                            child.gene[selfGeneCount] = temp
                else:
                    for count in range(crossoverPoint, len(child.gene)-1):
                        if(mate.gene.index(child.gene[count]) > mate.gene.index(child.gene[count+1])):
                            temp = child.gene[count+1]
                            child.gene[count+1] = child.gene[count]
                            child.gene[count] = temp


        return child

    def mutate(self, x_bounds, y_bounds, **kwargs):
        copy = LinearGenotype()
        copy.gene = self.gene.copy()
    

        # changing this based on feedback from assignment 1c
        genesToMutate = random.sample(range(len(copy.gene)), k=random.randint(0, len(copy.gene)))

        for geneIndex in genesToMutate:
            copy.gene[geneIndex] = (random.uniform(*x_bounds), random.uniform(*y_bounds))

        return copy

    @classmethod
    def initialization(cls, mu, *args, **kwargs):
        population = [cls() for _ in range(mu)]
        for i in range(len(population)):
            population[i].random_initialization(*args, **kwargs)
        return population
