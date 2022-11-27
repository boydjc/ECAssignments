from bridge_fitness import *

# 1b TODO: evaluate the population and assign fitness and bridge as described in the Assignment 1b notebook
def basic_population_evaluation(population, **fitness_kwargs):
    # hint: print(fitness_kwargs) to see the data structure and contents if you're confused

    for individual in population:

        individual.fitness, individual.bridge = basic_simulation(individual.gene, **fitness_kwargs)

    return population

# 1c TODO: evaluate the population and assign fitness, raw_fitness, and bridges as described in the constraint satisfaction segment of Assignment 1c
def constraint_satisfaction_population_evaluation(population, penalty_coefficient, yellow = None, **fitness_kwargs):
    for individual in population:
        individual.raw_fitness, unpenalized_fitness, violations, individual.bridge \
                                 = constraint_satisfaction_simulation(individual.gene, **fitness_kwargs)

        individual.penalized_fitness = unpenalized_fitness - penalty_coefficient * violations

# 1c TODO: evaluate the population and assign objectives and bridges as described in the multi-objective segment of Assignment 1c
def multi_objective_population_evaluation(population, yellow = None, red = None, **fitness_kwargs):
    
    # GREEN deliverable logic goes here
    for individual in population:
        individual.objectives, individual.bridge = multi_objective_simulation(individual.gene, **fitness_kwargs)
	
    return population
    
