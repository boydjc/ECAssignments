import random
import numpy.random as npr
from operator import attrgetter

# Parent selection functions---------------------------------------------------
def uniform_random_selection(population, n, **kwargs):
    # select n individuals uniform randomly

    selected = []

    while len(selected) < n:
        selected.append(random.choice(population))

    return selected


def k_tournament_with_replacement(population, n, k, **kwargs):
    #   perform n k-tournaments with replacement to select n individuals

    selected = []

    while(len(selected) < n):
        selected.append(max(random.sample(population, k), key=attrgetter('fitness')))

    return selected


def fitness_proportionate_selection(population, n, **kwargs):
    # select n individuals using fitness proportionate selection

    hasNegative = any(individual.fitness < 0 for individual in population)

    if(hasNegative):
        tempFitnesses = []
        minimumFitness = min([individual.fitness for individual in population])

        for individual in population:
            tempFitnesses.append(individual.fitness - (minimumFitness * 1.5))

        fitnessSum = sum(tempFitnesses)
        selectionProbs = [fitness / fitnessSum for fitness in tempFitnesses]
    else:
        fitnessSum = sum(individual.fitness for individual in population)
        selectionProbs = [individual.fitness / fitnessSum for individual in population]

    selected = []

    while(len(selected) < n):
        selected.append(population[npr.choice(len(population), p=selectionProbs)])

    return selected


# Survival selection functions-------------------------------------------------
def truncation(population, n, **kwargs):
    # perform truncation selection to select n individuals

    sortedPopulation = sorted(population, key=lambda individual: individual.fitness, reverse=True)

    return sortedPopulation[:n]

def k_tournament_without_replacement(population, n, k, **kwargs):
    # perform n k-tournaments without replacement to select n individuals
    # Note: an individual should never be cloned from surviving twice!
    
    selected = []

    popCopy = population.copy()

    while(len(selected) < n):
        selectedIndividual = max(random.sample(popCopy, k), key=attrgetter('fitness'))
        selected.append(selectedIndividual)
        popCopy.pop(popCopy.index(selectedIndividual))

    return selected

# Yellow deliverable parent selection function---------------------------------
def stochastic_universal_sampling(population, n, **kwargs):
    # Recall that yellow deliverables are required for students in the grad
    # section but bonus for those in the undergrad section.
    # select n individuals using stochastic universal sampling

    totalFitness = sum([individual.fitness for individual in population])

    start = random.uniform(0, (totalFitness/len(population)))

    points = [start + i * (totalFitness/len(population)) for i in range(len(population))]

    selected = []

    currentPoint = start
    lastPosition = 0
    for _ in range(n):
        for position in range(lastPosition, len(points)):
            if points[position] >= currentPoint:
                selected.append(population[position])
                lastPosition = position
                break
        currentPoint += (totalFitness/len(population))

    return selected



    
