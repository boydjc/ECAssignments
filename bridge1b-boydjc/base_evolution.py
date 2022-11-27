class BaseEvolutionPopulation():
    def __init__(self, individual_class, mu, num_children, mutation_rate,
                 parent_selection, survival_selection,
                 initialization_kwargs=dict(), parent_selection_kwargs=dict(),
                 recombination_kwargs = dict(), mutation_kwargs = dict(),
                 survival_selection_kwargs=dict(), **kwargs):
        self.mu = mu
        self.num_children = num_children
        self.mutation_rate = mutation_rate
        self.parent_selection = parent_selection
        self.survival_selection = survival_selection
        self.parent_selection_kwargs = parent_selection_kwargs
        self.recombination_kwargs = recombination_kwargs
        self.mutation_kwargs = mutation_kwargs
        self.survival_selection_kwargs = survival_selection_kwargs

        self.population = individual_class.initialization(self.mu, **initialization_kwargs)

    def generate_children(self):
        children = list()

        # Select parents
        # hint: self.parent_selection(self.population, **self.parent_selection_kwargs)

        for _ in range(self.num_children):
            parents = self.parent_selection(self.population, n=2, **self.parent_selection_kwargs)

            # Recombine parents to generate children
            child = parents[0].recombine(parents[1], **self.recombination_kwargs)

            # Mutate children if appropriate
            mutant = child.mutate(**self.mutation_kwargs)
            children.append(child)

        # return children
        return children


    def survival(self):
        self.population = self.survival_selection(self.population, self.mu, **self.survival_selection_kwargs)
