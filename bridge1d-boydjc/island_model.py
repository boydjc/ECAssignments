import random
from base_evolution import BaseEvolutionPopulation

class IslandModel():

    # ---------------------------------------------------
    # --- You may modify this class however you want, ---
    # ---   if done carefully and with good reason.   ---
    # --- It must work on all attempted deliverables. ---
    # --- GREEN and YELLOW only require implementing  ---
    # ---  the TODOs. We recommend that you make no   ---
    # ---   other changes unless attempting a RED.    ---
    # ---------------------------------------------------

    def __init__(self, topology, size, interval, migrant_selection, num_migrants,
                         migrant_selection_kwargs = dict(), EA_configs = dict(), multipleConfigs=False, 
                         EA_configs_1 = dict(), EA_configs_2 = dict(), 
                         EA_configs_3 = dict(), **kwargs):
        self.topology = topology.casefold()
        self.interval = interval
        self.migrant_selection = migrant_selection
        self.num_migrants = num_migrants
        self.migrant_selection_kwargs = migrant_selection_kwargs
        self.generation_count = 0

        if(multipleConfigs):
            assert self.num_migrants < EA_configs_1['mu']
            assert self.num_migrants < EA_configs_2['mu']
            assert self.num_migrants < EA_configs_3['mu']
        else:
            assert self.num_migrants < EA_configs['mu']

        assert self.topology in {'uni_circle', 'bi_circle', 'all_to_all', 'toroid', 'red'}
        if self.topology == 'uni_circle' or self.topology == 'bi_circle':
            assert self.topology == 'uni_circle' or self.num_migrants % 2 == 0
        
            # This is given for you to use as an example.
            # The other topologies may have better representations,
            # don't just copy-paste this without thinking.
            # You can use any data structure(s) with any name(s) you want.

            if(multipleConfigs):
                self.islands = []
                configCount = 1
                for count in range(size):
                    if(configCount == 1):
                        self.islands.append(BaseEvolutionPopulation(**EA_configs_1, **kwargs))
                    elif(configCount == 2):
                        self.islands.append(BaseEvolutionPopulation(**EA_configs_2, **kwargs))
                    else:
                        self.islands.append(BaseEvolutionPopulation(**EA_configs_3, **kwargs))

                    if(configCount == 3):
                        configCount = 1
                    else:
                        configCount += 1
            else:
                self.islands = [BaseEvolutionPopulation(**EA_configs, **kwargs) for _ in range(size)]

        elif self.topology == 'all_to_all':
            assert self.num_migrants % (size - 1) == 0
            
            # DONE: initialize the all-to-all topology
            # this should still probably work for the all to all
            self.islands = [BaseEvolutionPopulation(**EA_configs, **kwargs) for _ in range(size)]

            
        elif self.topology == 'toroid':
            assert self.num_migrants % 4 == 0
            # DONE: initialize the toroid topology

            self.islands = []

            for _ in range(size[0]):
                islandRow = [BaseEvolutionPopulation(**EA_configs, **kwargs) for _ in range(size[1])]
                self.islands.append(islandRow)

        elif self.topology == 'red':
            assert size[1] == 3

            self.islands = []

            for _ in range(size[0]):
                islandRow = [BaseEvolutionPopulation(**EA_configs, **kwargs) for _ in range(size[1])]

                self.islands.append(islandRow)



    
    def __iter__(self):
        # Filling this class out will let your EA loop in the notebook handle
        # any topology interchangeably. It should iterate through every island
        # in your topology, returning each one a single time. See the notebook
        # for a more in-depth explanation of how this can be accomplished.
        
        if self.topology == 'uni_circle' or self.topology == 'bi_circle':
            # We put a custom generator here to serve as an example; this could
            # just as easily have been written using the built-in list iterator:
            # yield from self.islands
            for island in self.islands:
                yield island
        
        elif self.topology == 'all_to_all':
            yield from self.islands
        
        elif self.topology == 'toroid':
            for islandRow in self.islands:
                yield from islandRow

        elif self.topology == 'red':
            for islandRow in self.islands:
                yield from islandRow

    def migrate(self):
        # Only migrate with a frequency based on our interval.
        self.generation_count += 1
        if self.generation_count != self.interval:
            return
        self.generation_count = 0
        
        # Migrants are pre-selected before any movement occurs to ensure no individual
        # is selected to migrate multiple times in a row. migrants is a dictionary
        # mapping each island to the migrants that were selected & removed from it.
        # Each island's migrants are shuffled, so feel free to just iterate through
        # the list for topologies where each island has multiple out-edges.
        # DO NOT RANDOMLY SAMPLE FROM THE MIGRANT LISTS
        migrants = {island:get_migrants(island, self.num_migrants, self.migrant_selection,
                                   self.migrant_selection_kwargs) for island in self}

    
        if self.topology == 'uni_circle':
            for i in range(len(self.islands)):
                # Tip: Many python data structures allow negative indices,
                #      and will cleanly wrap around to the back of the array.
                #      i.e., self.islands[-1] is self.islands[len(self.islands)-1]
                # [1 -> 2 -> 3 -> 4]
                self.islands[i].population += migrants[self.islands[i-1]]


        elif self.topology == 'bi_circle':
            # DONE: perform migration with bidirectional circle topology
            
            for i in range(len(self.islands)):
                # [1 -> 2 -> 3 -> 4]
                self.island[i].population += migrants[self.islands[i-1]]

                # [1 <- 2 <- 3 <- 4]
                self.islands[i-1].population += migrants[self.islands[i]]

        elif self.topology == 'all_to_all':
            # DONE: perform migration with all-to-all topology
            
            for i in range(len(self.islands)):
                # [1 -> 2 -> 3 -> 4]
                self.island[i].population += migrants[self.islands[i-1]]

                # [1 <- 2 <- 3 <- 4]
                self.islands[i-1].population += migrants[self.islands[i]]

                # [2 <- 4] [1 <- 3]

                self.islands[i-2].population += migrants[self.islands[i]]

                # [2 -> 4] [1 -> 3]

                self.islands[i].population += migrants[self.islands[i-2]]


        elif self.topology == 'toroid':
            # DONE: perform migration with toroid topology

            for islandRowCount in range(len(self.islands)):
                for i in range(len(self.islands[islandRowCount])):
                    # [1 -> 2 -> 3]
                    self.island[islandRowCount][i].population += migrants[self.islands[islandRowCount][i-1]]

                    # [1 <- 2 <- 3]
                    self.islands[islandRowCount][i-1].population += migrants[self.islands[islandRowCount][i]]

                    # [1 -> 4] [2 -> 5] [3 -> 6]
                    # with multi dimension wrap around 
                    self.island[islandRowCount][i].population += migrants[self.islands[islandRowCount-1][i]]

                    # [1 <- 4] [2 <- 5] [3 <- 6]
                    # with multi dimension wrap around 
                    self.islands[islandRowCount-1][i].population += migrants[self.islands[islandRowCount][i]]

        elif self.topology == 'red':

            for islandRowCount in range(len(self.islands)):
                for i in range(len(self.islands[islandRowCount])):

                    # column migration
                    # if we are in the middle column...
                    if not (i % 2 == 0):
                        # making sure here that there is no loopback with the middle element for each row
                        # to preserve directional loopbacks
                        
                        if not(islandRowCount == 0):
                            # if not in the first row, we can go backwards a row
                            self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount-1][i]]

                        if not(islandRowCount == (len(self.islands))):
                            # if not in the last row we can go forwards a row
                            self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount+1][i]]

                    else: # not in the middle column
                        if(i == 3):
                            if not(islandRowCount == (len(self.islands))):
                                # column with loopback
                                self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount+1][i]]
                            else:
                                self.islands[islandRowCount][i].population += migrants[self.islands[0][i]]
                        elif(i == 0):
                            # column with loopback
                            self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount-1][i]]

                    # row migration with loopback
                    # first row
                    if(islandRowCount == 0):
                        if not(i == 3):
                            # column with loopback
                            self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount][i+1]]
                        else:
                            self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount][0]]
                    # last row
                    elif(islandRowCount == len(self.islands)):
                        self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount][i-1]]
                    else:
                        self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount][i-1]]

                        self.islands[islandRowCount][i].population += migrants[self.islands[islandRowCount][i+1]]








            

def get_migrants(island, num_migrants, migrant_selection, migrant_selection_kwargs = dict()):
    migrants = migrant_selection(island.population, n=num_migrants, **migrant_selection_kwargs)

    # Probably needs to be fixed by-hand for some implementations, particularly numpy arrays
    if not isinstance(island.population, list):
        raise RuntimeError('Contact a TA: select_migrants() expects your population to be a list')

    # Remove migrants from the population via set difference.
    # Lots of error-checking because somebody's EA implementation will certainly be bugged.
    pop_set = set(island.population)
    assert len(pop_set) == len(island.population), \
            "Population contained duplicate individuals"
    migrant_set = set(migrants)
    assert len(migrant_set) == len(migrants), \
            "Migrants contained duplicates (must be selected without replacement)"
    island.population = list(pop_set - migrant_set)
    assert len(island.population) == len(pop_set) - len(migrant_set), \
            "Migrants were not a subset of the population (selection shouldn't copy individuals)"

    random.shuffle(migrants)
    return migrants