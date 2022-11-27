from fitness import *

# 2b TODO:  evaluate input Pac-Man population and assign fitness, raw_fitness, and log as 
#           described in the Assignment 2b notebook
def basic_population_evaluation(population, parsimony_coefficient, **fitness_kwargs):
    # hint: print(fitness_kwargs) to see the data structure and contents if you're confused
    
    for individual in population:

        individual.raw_fitness, individual.log = play_GPac(individual, **fitness_kwargs)

        if(fitness_kwargs['parsimony_type'] == 'size'):
            individual.fitness = individual.raw_fitness - parsimony_coefficient * individual.findNumOfNodes(individual.gene)
        elif(fitness_kwargs['parsimony_type'] == 'depth'):
            individual.fitness = individual.raw_fitness - parsimony_coefficient * individual.findDepth(individual.gene)

    return population

def ghost_basic_population_evaluation(population, parsimony_coefficient, **fitness_kwargs):
    # hint: print(fitness_kwargs) to see the data structure and contents if you're confused
    
    for individual in population:

        individual.raw_fitness, individual.log = play_ghost_GPac(individual, **fitness_kwargs)

        endGameTime = int(individual.log[-1].split(' ')[1])
        endGameScore = int(individual.log[-1].split(' ')[2])

        # use negative game score plus remaining time as the fitness metric
        individual.raw_fitness = -endGameScore + endGameTime

        if(fitness_kwargs['parsimony_type'] == 'size'):
            individual.fitness = individual.raw_fitness - parsimony_coefficient * individual.findNumOfNodes(individual.gene)
        elif(fitness_kwargs['parsimony_type'] == 'depth'):
            individual.fitness = individual.raw_fitness - parsimony_coefficient * individual.findDepth(individual.gene)

    return population

# 2c TODO:  evaluate input Pac-Man and Ghost populations and assign fitness, raw_fitness, 
#           and log as described in the Assignment 2c notebook
def competitive_population_evaluation(pac_population, ghost_population, 
                                        pac_parsimony_coefficient,
                                        ghost_parsimony_coefficient, **fitness_kwargs):
    # TODO: perform matchmaking
    matchBasket = [[pac_population[count], 
                        ghost_population[count]] for count in range(min(len(pac_population), 
                                                                        len(ghost_population)))]

    # which ever population is shorter just take the last 
    # individual from that population and make them compete with the rest of the longer population
    if len(pac_population) < len(ghost_population):
        for e in ghost_population[len(matchBasket):]:
                matchBasket.append([pac_population[-1], e])
    elif len(pac_population) > len(ghost_population):
        for e in pac_population[len(matchBasket):]:
                matchBasket.append([e, ghost_population[-1]])

    #for couple in matchBasket:
    #    print(couple)

    # TODO: evaluate matches with play_GPac
    # Hint: play_GPac(pac_controller, ghost_controller, **fitness_kwargs)
    for couple in matchBasket:
        couple[0].raw_fitness, couple[0].log = play_GPac(couple[0], couple[1], **fitness_kwargs)

        #print(game_fitness)

        # TODO: calculate and assign fitness (don't forget the per-species parsimony penalty)
        endGameTime = int(couple[0].log[-1].split(' ')[1])
        endGameScore = int(couple[0].log[-1].split(' ')[2])

        couple[1].raw_fitness = -endGameScore + endGameTime

        if(fitness_kwargs['parsimony_type'] == 'size'):
            couple[0].fitness = couple[0].raw_fitness - pac_parsimony_coefficient * couple[0].findNumOfNodes(couple[0].gene)
            couple[1].fitness = couple[1].raw_fitness - ghost_parsimony_coefficient * couple[1].findNumOfNodes(couple[1].gene)
        elif(fitness_kwargs['parsimony_type'] == 'depth'):
            couple[0].fitness = couple[0].raw_fitness - pac_parsimony_coefficient * couple[0].findDepth(couple[0].gene)
            couple[1].fitness = couple[1].raw_fitness - ghost_parsimony_coefficient * couple[1].findDepth(couple[1].gene)


        #print(f'Pac Fitness (Raw): {couple[0].raw_fitness}\t\tGhost Fitnesss (Raw): {couple[1].raw_fitness}')
        #print(f'Pac Fitness (Penalized): {couple[0].fitness}\t\tGhost Fitnesss (Penalized): {couple[1].fitness}')

    return pac_population, ghost_population
