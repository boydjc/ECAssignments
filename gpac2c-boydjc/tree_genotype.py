from parse_tree import ParseTree
import random
from copy import deepcopy
from math import inf

# GPac primitives
# internal_nodes = {'+','-','*','/','RAND'}
# leaf_nodes = {'G', 'M', 'P','W','F','#.#'}

class TreeGenotype():
    def __init__(self):
        self.fitness = None
        self.gene = None
        self.root_node = None

    def assignTree(self, depth_limit, assignMethod):

        if(assignMethod == "full"):
            self.gene = ParseTree.full(depth_limit=depth_limit)
        elif(assignMethod == "grow"):
            self.gene = ParseTree.grow(depth_limit=depth_limit)

    def recombine(self, mate, **kwargs):
        child = self.__class__()

        self_number_of_nodes = self.findNumOfNodes(self.gene)

        self_crossover_point = random.randint(0, self_number_of_nodes-1)

        self_sub_tree = self.getSubTree(deepcopy(self.gene), self_crossover_point)

        self_sub_tree_depth = self.findDepth(self_sub_tree)

        mate_number_of_nodes = self.findNumOfNodes(mate.gene)

        child_depth = inf

        # changing from pruning to checking ahead of time if recombination 
        # with the mate sub tree will exceed max depth specified. As per TA feedback 
        # from 2b assignment

        mate_node_num_subtract_rate = 0

        while(child_depth > kwargs['depth_limit']):

            mate_node_num_subtract_rate += 1

            # I had an issue before with it infinitely running
            # to find the appropriate crossover point at around depth 8 or 9.
            # this 'mate_node_num_subtract_rate' is used to decrease the selection
            # of crossover points more and more as the while loop keeps iterating

            mate_crossover_point = random.randint(0, mate_number_of_nodes-mate_node_num_subtract_rate)

            mate_sub_tree = self.getSubTree(deepcopy(mate.gene), mate_crossover_point)

            mate_sub_tree_depth = self.findDepth(mate_sub_tree)

            child.gene, _ = self.crossTrees(node=deepcopy(self.gene),
                                        base_tree_crossover_point = self_crossover_point, 
                                        mate_sub_tree = mate_sub_tree)

            child_depth = self.findDepth(child.gene)

        return child

    def crossTrees(self, node, base_tree_crossover_point, mate_sub_tree, node_count=0, cross_occured=False):

        if(node_count == base_tree_crossover_point):
            node = mate_sub_tree
            cross_occured = True
        else:
            if(node.left and not cross_occured):
                node.left, cross_occured = self.crossTrees(node.left, base_tree_crossover_point, 
                                                            mate_sub_tree, (2*node_count)+1, cross_occured)

            if(node.right and not cross_occured):
                node.right, cross_occured = self.crossTrees(node.right, base_tree_crossover_point, 
                                                            mate_sub_tree, 2*(node_count+1), cross_occured)

        return node, cross_occured

    def getSubTree(self, node, crossover_point):

        node_count = -1

        nodeQueue = []
        nodeQueue.append(node)

        while node_count <= crossover_point:

            node = nodeQueue.pop(0)
            node_count += 1

            if(node_count == crossover_point):
                break
            else:
                if(node.left):
                    nodeQueue.append(node.left)

                if(node.right):
                    nodeQueue.append(node.right)

        return node

    def findDepth(self, node=None, current_depth=0):

        if(node == None):
            return -1

        leftDepth = self.findDepth(node.left)

        rightDepth = self.findDepth(node.right)

        return max(leftDepth, rightDepth) + 1

    def findNumOfNodes(self, node=None):

        count = 0

        if not node:
            return 0

        nodeQueue = []

        nodeQueue.append(node)
        count += 1

        while(len(nodeQueue) > 0):
            node = nodeQueue.pop(0)

            if node.left:
                count += 1
                nodeQueue.append(node.left)

            if node.right:
                count += 1
                nodeQueue.append(node.right)


        return count

    def mutate(self, **kwargs):
        copy = self.__class__()

        # TODO: copy self.gene to copy.gene
        copy.gene = deepcopy(self.gene)

        # TODO: mutate gene of copy
        mutate_point = random.randint(0, self.findNumOfNodes(copy.gene)-1)

        copy.gene, _ = self.mutateGene(copy.gene, mutate_point)
        
        return copy

    def mutateGene(self, node, mutate_point, node_count=0, mutation_occured=False):

        operator_inputs = ['+', '-', '*', '/', 'RAND']

        if(mutate_point == node_count):
            if(node.value in operator_inputs):
                new_node = ParseTree.getOperatorNode()
            else:
                new_node = ParseTree.getSensorNode()

            node.value = new_node.value
            mutation_occured = True
        else:
            if(node.left and not mutation_occured):
                node.left, mutation_occured = self.mutateGene(node.left, mutate_point, 
                                                                (2*node_count)+1, mutation_occured)

            if(node.right and not mutation_occured):
                node.right, mutation_occured = self.mutateGene(node.right, mutate_point, 
                                                                (2*node_count)+2, mutation_occured)

        return node, mutation_occured


    def print(self, node=None, treeString="", depth=0):
        # TODO: return a string representation of self.gene
        #       (see assignment description doc for more info)

        if not node:
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
