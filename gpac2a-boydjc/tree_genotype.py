from parse_tree import ParseTree
# GPac primitives
# internal_nodes = {'+','-','*','/','RAND'}
# leaf_nodes = {'G','P','W','F','#.#'}

class TreeGenotype():
    def __init__(self):
        self.fitness = None
        self.gene = None
        self.root_node = None

    def assignTree(self, depth_limit, assignMethod):

        parse_tree = ParseTree()

        if(assignMethod == "full"):
            self.gene = parse_tree.full(depth_limit=depth_limit)
        elif(assignMethod == "grow"):
            self.gene = parse_tree.grow(depth_limit=depth_limit)

    def recombine(self, mate, **kwargs):
        child = self.__class__()

        # TODO: recombine genes of self and mate and assign to child's gene member variable
        pass

        return child

    def mutate(self, **kwargs):
        copy = self.__class__()

        # TODO: copy self.gene to copy.gene
        pass

        # TODO: mutate gene of copy
        pass

        return copy

    def print(self, node=None, treeString="", depth=0):
        # TODO: return a string representation of self.gene
        #       (see assignment description doc for more info)

        if(depth == 0):
            node = self.gene

        treeString += str(node.value) + "\n"

        depth += 1

        if(node.left):
            for _ in range(depth):
                treeString += "|"
            treeString = self.print(node.left, treeString, depth)

        if(node.right):
            for _ in range(depth):
                treeString += "|"
            treeString = self.print(node.right, treeString, depth)

        return treeString



    @classmethod
    def initialization(cls, mu, *args, **kwargs):
        population = [cls() for _ in range(mu)]
        depth_limit = kwargs['depth_limit']
        # TODO: initialize gene member variables of individuals in 
        # population using ramped half-and-half

        depth = 0
        # population first half
        for count in range(int(len(population)/2)):
            if(depth > depth_limit):
                depth = 0

            population[count].assignTree(depth, "full")

            depth += 1

        depth = 0
        # population second half
        for count in range(int(len(population)/2), len(population)):
            if(depth > depth_limit):
                depth = 0

            population[count].assignTree(depth, "grow")

            depth += 1

        return population
