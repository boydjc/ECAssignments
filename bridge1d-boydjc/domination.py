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
    
    fronts = [[]]
    for individual in population:
        individual.domination_count = 0
        individual.dominated_solutions = []
        for other_individual in population:
            if dominates(individual, other_individual):
                individual.dominated_solutions.append(other_individual)
            elif dominates(other_individual, individual):
                individual.domination_count += 1
        if individual.domination_count == 0:
            individual.rank = 0
            fronts[0].append(individual)
    i = 0
    while len(fronts[i]) > 0:
        temp = []
        for individual in fronts[i]:
            for other_individual in individual.dominated_solutions:
                other_individual.domination_count -= 1
                if other_individual.domination_count == 0:
                    other_individual.rank = i+1
                    temp.append(other_individual)
        i = i+1
        fronts.append(temp)


    # Assign each individual a representative fitness to their fitness member variable equal to the negation of its level of non-domination
    for front in range(len(fronts)):
        for individual in fronts[front]:
            individual.fitness = len(fronts) - front

    if yellow:
        # (as per Deacon in discord chat)
        # assign the individuals at the ends of the front (i.e. those individuals with the max fitness of an 
        # objective) with a value approaching but less than 1 (e.g., 0.999)

        if len(fronts) > 2:
            fronts[0].crowdingDistance = 0.999
            fronts[-1].crowdingDistance = 0.999

            for individual in fronts:
                individual.crowdingDistance = 0

            # Everyone else in the front has their crowding distance calculated 
            # (see function from NSGA-II paper above) and is assigned a normalized value [0, upper_lim) 
            # where upper_lim < Z (e.g., upper_lim could be 0.8).

            for objCount in range(len(fronts[0].objectives)):
                # sort by objective value
                fronts = sorted(fronts, key=lambda individual: individual.objectives[objCount], reverse=True)
                fronts[1].crowdingDistance = fronts[len(fronts)-1].crowdingDistance

                for count in range(2, len(fronts)-1):
                    fronts[count].crowdingDistance = fronts[count].crowdingDistance + \
                        (fronts[count+1].objectives[objCount] - fronts[count-1].objectives[objCount]) / \
                        (max(individual.objectives[0] for individual in fronts) - min(individual.objectives[0] for individual in paretoFront))

            # now order by the crowding distance and get the ones with the highest score
            fronts = sorted(fronts, key=lambda individual: individual.crowdingDistance, reverse=True)
            bestCrowdingDistance = max(individual.crowdingDistance for individual in fronts)
            fronts = [individual for individual in fronts if individual.crowdingDistance == bestCrowdingDistance]
            

        return fronts
