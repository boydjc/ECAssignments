from base_evolution import BaseEvolutionPopulation
import random

class GeneticProgrammingPopulation(BaseEvolutionPopulation):
	def generate_children(self):
		children = list()

		# do this later
		#childrenToMutate = random.sample(range(self.num_children), k=int(self.num_children * self.mutation_rate))

		for count in range(self.num_children):

			parents = self.parent_selection(self.population, n=2, **self.parent_selection_kwargs)

			if random.random() < self.mutation_rate:
				child = parents[0].mutate(**self.mutation_kwargs)
			else:
				child = parents[0].recombine(parents[1], **self.recombination_kwargs)

			children.append(child)

		return children