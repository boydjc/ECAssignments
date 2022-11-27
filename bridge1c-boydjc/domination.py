from math import inf
# 1c TODO: return True if A dominates B based on the objective member variables of both objects
def dominates(A, B):
    if((A.objectives[0] >= B.objectives[0] and A.objectives[1] >= B.objectives[1]) and 
        (A.objectives[0] > B.objectives[0] or A.objectives[1] > B.objectives[1])):
            return True
    
    return False

# 1c TODO:  Use the dominates function (above) to sort the input population into levels of
#           non-domination and assign fitness based on an individual's level. This is also
#           where you should incorporate the yellow deliverable for crowding as described
#           in the Assignment Description Document.
def non_domination_sort(population, yellow=False):
    # green deliverable code goes here
    
    # calculate a domination lookup table
    dominationTable = dict()

    for index in range(len(population)):
        dominationTable[index+1] = []
        for opponent_index in range(len(population)):
            if dominates(population[index], population[opponent_index]):
                dominationTable[index+1].append(opponent_index+1)


    # sort individual into levels of non-domination with the algorithm performed
    # and where level 0 is the Pareto front

    nonDomTable = dict()

    for key in dominationTable.keys():
        nonDomTable[key] = 0
        for value in dominationTable.values():
            nonDomTable[key] += value.count(key)

    sortedNonDom = {key : value for key, value in sorted(nonDomTable.items(), key=lambda item: item[1])}

    levelTable = dict()

    level = 0
    prevKeyValue = -inf
    keys = list(sortedNonDom.keys())

    for keyCount in range(len(keys)):

        if not level in levelTable:
            levelTable[level] = []

        levelTable[level].append(keys[keyCount])

        try:
            if(sortedNonDom[keys[keyCount]] < sortedNonDom[keys[keyCount+1]]):
                level += 1
        except:
            # end of list
            level += 1

    paretoFront = []

    for value in levelTable[0]:
        paretoFront.append(population[value-1])

    # Assign each individual a representative fitness to their fitness member variable equal to the negation of its level of non-domination
    for key in levelTable.keys():
        for value in levelTable[key]:
            population[value-1].fitness = len(levelTable.keys()) - key

    if yellow:
        # (as per Deacon in discord chat)
        # assign the individuals at the ends of the front (i.e. those individuals with the max fitness of an 
        # objective) with a value approaching but less than 1 (e.g., 0.999)

        if len(paretoFront) > 2:
            paretoFront[0].crowdingDistance = 0.999
            paretoFront[-1].crowdingDistance = 0.999

            for individual in paretoFront:
                individual.crowdingDistance = 0

            # Everyone else in the front has their crowding distance calculated 
            # (see function from NSGA-II paper above) and is assigned a normalized value [0, upper_lim) 
            # where upper_lim < Z (e.g., upper_lim could be 0.8).

            for objCount in range(len(paretoFront[0].objectives)):
                # sort by objective value
                paretoFront = sorted(paretoFront, key=lambda individual: individual.objectives[objCount], reverse=True)
                paretoFront[1].crowdingDistance = paretoFront[len(paretoFront)-1].crowdingDistance

                for count in range(2, len(paretoFront)-1):
                    paretoFront[count].crowdingDistance = paretoFront[count].crowdingDistance + \
                        (paretoFront[count+1].objectives[objCount] - paretoFront[count-1].objectives[objCount]) / \
                        (max(individual.objectives[0] for individual in paretoFront) - min(individual.objectives[0] for individual in paretoFront))

            # now order by the crowding distance and get the ones with the highest score
            paretoFront = sorted(paretoFront, key=lambda individual: individual.crowdingDistance, reverse=True)
            bestCrowdingDistance = max(individual.crowdingDistance for individual in paretoFront)
            paretoFront = [individual for individual in paretoFront if individual.crowdingDistance == bestCrowdingDistance]
            

    return paretoFront
