import random
from math import sqrt

class ParseTree():

	def __init__(self):

		''' Sensor Inputs

			G - Manhattan Distance to nearest ghost
			P - Manhattan Distance to nearest pill
			W - Number of immediately adjacent walls
			F - Manhattan Distance to nearest fruit
			#.# - Constant value
			
		'''
		self.sensor_inputs = ['G', 'P', 'W', 'F', '#.#']
		self.operator_inputs = ['+', '-', '*', '/', 'RAND']

	def full(self, depth_limit=0, current_depth=0):

		if not(current_depth == depth_limit):
			node = self.getOperatorNode()

			node.left = self.full(depth_limit, current_depth+1)
			node.right = self.full(depth_limit, current_depth+1)

		elif(current_depth >= depth_limit):
			node = self.getSensorNode()

		return node

	def grow(self, depth_limit=0, current_depth=0):

		if not(current_depth == depth_limit):
			randChoice = random.randint(0, 1)
			if(randChoice == 0):
				node = self.getOperatorNode()

				node.left = self.grow(depth_limit, current_depth+1)
				node.right = self.grow(depth_limit, current_depth+1)

			elif(randChoice == 1):
				node = self.getSensorNode()

		elif(current_depth >= depth_limit):

			node = self.getSensorNode()

		return node

	def getOperatorNode(self):
		# choose random operator node if we are not at the max depth
		rand_operator = self.operator_inputs[random.randint(0, len(self.operator_inputs)-1)]

		new_node = Node()
		new_node.value = rand_operator
		new_node.left = Node()
		new_node.right = Node()

		return new_node

	def getSensorNode(self):
		rand_sensor = self.sensor_inputs[random.randint(0, len(self.sensor_inputs)-1)]

		if(rand_sensor == "#.#"):
			rand_sensor = round(random.uniform(9, -9),1)

		new_node = Node()
		new_node.value = rand_sensor

		return new_node

class Node():
	def __init__(self):
		self.value = None
		self.left = None
		self.right = None
		self.cache = {}

	def execute(self, state, cache=None):
		# Sensor decisions
		if(self.value == 'G'):
			if('ghostDist' in self.cache):
				return self.cache['ghostDist']
			else:
				return self.ghostDist(state)
		elif(self.value == 'P'):
			if('pillDist' in self.cache):
				return self.cache['pillDist']
			else:
				return self.pillDist(state)
		elif(self.value == 'W'):
			if('numOfWalls' in self.cache):
				return self.cache['numOfWalls']
			else:
				return self.numOfAdjWalls(state)
		elif(self.value == 'F'):
			if('fruitDist' in self.cache):
				return self.cache['fruitDist']
			else:
				return self.fruitDist(state)
		elif(isinstance(self.value, float)):
			return self.value

		# Operator decisions
		elif(self.value == '+'):
			return self.left.execute(state) + self.right.execute(state)
		elif(self.value == '-'):
			return self.left.execute(state) - self.right.execute(state)
		elif(self.value == '*'):
			return self.left.execute(state) * self.right.execute(state)
		elif(self.value == '/'):
			try:	
				return self.left.execute(state) / self.right.execute(state)
			except:
				return 0
		elif(self.value == 'RAND'):
			return random.uniform(self.left.execute(state), self.right.execute(state))


	def ghostDist(self, state):
		pacPlayerLocation = None
		ghostLocations = []

		for key, value in state['players'].items():
			if(key == 'm'):
				pacPlayerLocation = state['players'][key]
			else:
				ghostLocations.append(state['players'][key])

		manhattanDistances = []

		for ghostLoc in ghostLocations:

			manhattanDistances.append(sum(abs(val1-val2) for val1, val2 in zip(pacPlayerLocation, ghostLoc)))

		minimumDistance = min(manhattanDistances)

		# store in cache for future use
		self.cache.update({'ghostDist': minimumDistance})

		return minimumDistance


	def pillDist(self, state):
		pacPlayerLocation = None
		pillLocations = state['pills']

		for key, value in state['players'].items():
			if(key == 'm'):
				pacPlayerLocation = state['players'][key]

		manhattanDistances = []

		for pillLoc in pillLocations:

			manhattanDistances.append(sum(abs(val1-val2) for val1, val2 in zip(pacPlayerLocation, pillLoc)))

		minimumDistance = min(manhattanDistances)

		self.cache.update({'pillDist' : minimumDistance})

		return minimumDistance

	def numOfAdjWalls(self, state):
		pacPlayerLocation = None

		for key, value in state['players'].items():
			if(key == 'm'):
				pacPlayerLocation = state['players'][key]

		walls = state['walls']

		numberOfWalls = 0

		if(pacPlayerLocation[0] == 0 or pacPlayerLocation[0] == len(walls)-1):
			# checking if we are on the first or last row of the map
			# if so we have to count the end of the map as a wall
			#print('Player at either top or bottom of map')
			numberOfWalls += 1
		
		if not pacPlayerLocation[0] == 0:
			# check above the player
			#print('Checking above the player')
			#print('Element above player: ', walls[pacPlayerLocation[0]-1][pacPlayerLocation[1]])
			if(walls[pacPlayerLocation[0]-1][pacPlayerLocation[1]] == 1):
				numberOfWalls += 1

		if not pacPlayerLocation[0] == len(walls)-1:
			# check under the player
			#print('Checking under player')
			#print('Element under player: ', walls[pacPlayerLocation[0]+1][pacPlayerLocation[1]])
			if(walls[pacPlayerLocation[0]+1][pacPlayerLocation[1]] == 1):
				numberOfWalls += 1

		# checking for the sides of the map here
		if(pacPlayerLocation[1] == 0 or pacPlayerLocation[1] == len(walls[0])-1):
			#print('Player at either far left or far right of map')
			numberOfWalls += 1

		if not pacPlayerLocation[1] == 0:
			#print('Checking to the left of player')
			#print('Element to left of player: ', walls[pacPlayerLocation[0]][pacPlayerLocation[1]-1])
			if(walls[pacPlayerLocation[0]][pacPlayerLocation[1]-1] == 1):
				numberOfWalls += 1

		if not pacPlayerLocation[1] == len(walls[0])-1:
			#print('Checking to the right of player')
			#print('Element to right of player: ', walls[pacPlayerLocation[0]][pacPlayerLocation[1]+1])
			if(walls[pacPlayerLocation[0]][pacPlayerLocation[1]+1] == 1):
				numberOfWalls += 1

		#print('Number of Adjacent Walls: ', numberOfWalls)

		self.cache.update({'numOfWalls': numberOfWalls})

		return numberOfWalls



	def fruitDist(self, state):
		if(state['fruit']):
			pacPlayerLocation = None

			for key, value in state['players'].items():
				if(key == 'm'):
					pacPlayerLocation = state['players'][key]

			fruitDistance = sum(abs(val1-val2) for val1, val2 in zip(pacPlayerLocation, state['fruit']))

			self.cache.update({'fruitDist': fruitDistance})

			return fruitDistance

		else:

			self.cache.update({'fruitDist': 0})
			return 0



