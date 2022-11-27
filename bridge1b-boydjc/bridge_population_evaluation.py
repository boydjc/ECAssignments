from bridge_fitness import *

# 1b TODO: evaluate the population and assign fitness and bridge as described in the Assignment 1b notebook
def basic_population_evaluation(population, **fitness_kwargs):
    # hint: print(fitness_kwargs) to see the data structure and contents if you're confused

    for individual in population:

        individual.fitness, individual.bridge = basic_simulation(individual.gene, solid=fitness_kwargs['solid'],
                                                                   material=fitness_kwargs['material'],
                                                                   width=fitness_kwargs['width'],
                                                                   fixed_points=fitness_kwargs['fixed_points'],
                                                                   load_points=fitness_kwargs['load_points'],
                                                                   connection_distance=fitness_kwargs['connection_distance'])

    return population

# 1c TODO: evaluate the population and assign fitness, raw_fitness, and bridges as described in the constraint satisfaction segment of Assignment 1c
def constraint_satisfaction_population_evaluation(population, penalty_coefficient, yellow = None, **fitness_kwargs):
    if yellow == None:
        # GREEN deliverable logic goes here
        pass
    else:
        # YELLOW deliverable logic goes here
        pass

# 1c TODO: evaluate the population and assign objectives and bridges as described in the multi-objective segment of Assignment 1c
def multi_objective_population_evaluation(population, yellow = None, red = None, **fitness_kwargs):
    pass
