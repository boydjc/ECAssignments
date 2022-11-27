import random
from math import sqrt

class GhostParseTree():

	def __init__(self):
		pass

	@staticmethod
	def full(depth_limit=0, current_depth=0):

		if not(current_depth == depth_limit):
			node = GhostParseTree.getOperatorNode()

			node.left = GhostParseTree.full(depth_limit, current_depth+1)
			node.right = GhostParseTree.full(depth_limit, current_depth+1)

		elif(current_depth >= depth_limit):
			node = GhostParseTree.getSensorNode()

		return node

	@staticmethod
	def grow(depth_limit=0, current_depth=0):

		if not(current_depth == depth_limit):
			randChoice = random.randint(0, 1)
			if(randChoice == 0):
				node = GhostParseTree.getOperatorNode()

				node.left = GhostParseTree.grow(depth_limit, current_depth+1)
				node.right = GhostParseTree.grow(depth_limit, current_depth+1)

			elif(randChoice == 1):
				node = GhostParseTree.getSensorNode()

		elif(current_depth >= depth_limit):

			node = GhostParseTree.getSensorNode()

		return node

	@staticmethod
	def getOperatorNode():
		# choose random operator node if we are not at the max depth
		operator_inputs = ['+', '-', '*', '/', 'RAND']
		rand_operator = operator_inputs[random.randint(0, len(operator_inputs)-1)]

		new_node = Node()
		new_node.value = rand_operator
		new_node.left = Node()
		new_node.right = Node()

		return new_node

	@staticmethod
	def getSensorNode():
		sensor_inputs = ['G', 'P', 'W', 'F', 'M', '#.#']
		rand_sensor = sensor_inputs[random.randint(0, len(sensor_inputs)-1)]

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

	def execute(self, state, cache=None):
		# Sensor decisions
		if(self.value == 'G'):
			if('nearestGhostDist' in cache):
				return cache['nearestGhostDist'], cache
			else:
				gDist, cache = self.ghostDist(state, cache)

				return gDist, cache

		elif(self.value == 'P'):
			if('pillDist' in cache):
				return cache['pillDist'], cache
			else:
				pDist, cache =  self.pillDist(state, cache)

				return pDist, cache

		elif(self.value == 'W'):
			if('numOfWalls' in cache):
				return cache['numOfWalls'], cache
			else:
				 numWalls, cache = self.numOfAdjWalls(state, cache)

				 return numWalls, cache
		elif(self.value == 'F'):
			if('fruitDist' in cache):
				return cache['fruitDist'], cache
			else:
				fDist, cache = self.fruitDist(state, cache)

				return fDist, cache
		elif(self.value == 'M'):
			if('nearestPacDist' in cache):
				return cache['nearestPacDist'], cache
			else:
				playerDist, cache = self.pacDist(state, cache)

				return playerDist, cache
		elif(isinstance(self.value, float)):
			return self.value, cache

		# Operator decisions
		elif(self.value == '+'):
			leftResult, cache = self.left.execute(state, cache)

			rightResult, cache = self.right.execute(state, cache)

			opResult = leftResult + rightResult

			return opResult, cache
		elif(self.value == '-'):
			leftResult, cache = self.left.execute(state, cache)

			rightResult, cache = self.right.execute(state, cache)

			opResult = leftResult - rightResult

			return opResult, cache
		elif(self.value == '*'):
			leftResult, cache = self.left.execute(state, cache)

			rightResult, cache = self.right.execute(state, cache)

			opResult = leftResult * rightResult

			return opResult, cache
		elif(self.value == '/'):
			try:
				leftResult, cache = self.left.execute(state, cache)

				rightResult, cache = self.right.execute(state, cache)

				opResult = leftResult / rightResult

				return opResult, cache	
			except:
				return 0, cache
		elif(self.value == 'RAND'):
			leftResult, cache = self.left.execute(state, cache)

			rightResult, cache = self.right.execute(state, cache)

			opResult = random.uniform(leftResult, rightResult)

			return opResult, cache

	def pacDist(self, state, cache):
		pacPlayerLocation = [state['players'][key] for key in state['players'].keys() if 'm' in key][0]
		ghostLocations = [state['players'][key] for key in state['players'].keys() if not 'm' in key]

		pacDistances = []

		for ghostLoc in ghostLocations:

			pacDistances.append(sum(abs(val1-val2) for val1, val2 in zip(pacPlayerLocation, ghostLoc)))

		minimumDistance = min(pacDistances)

		# store in cache for future use
		cache.update({'nearestPacDist': minimumDistance})

		return minimumDistance, cache

	def pillDist(self, state, cache):
		pacPlayerLocation = None
		pillLocations = state['pills']

		for key, value in state['players'].items():
			if(key == 'm'):
				pacPlayerLocation = state['players'][key]

		manhattanDistances = []

		for pillLoc in pillLocations:

			manhattanDistances.append(sum(abs(val1-val2) for val1, val2 in zip(pacPlayerLocation, pillLoc)))

		minimumDistance = min(manhattanDistances)

		cache.update({'pillDist' : minimumDistance})

		return minimumDistance, cache

	def numOfAdjWalls(self, state, cache):
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

		cache.update({'numOfWalls': numberOfWalls})

		return numberOfWalls, cache


	def fruitDist(self, state, cache):
		if(state['fruit']):
			pacPlayerLocation = None

			for key, value in state['players'].items():
				if(key == 'm'):
					pacPlayerLocation = state['players'][key]

			fruitDistance = sum(abs(val1-val2) for val1, val2 in zip(pacPlayerLocation, state['fruit']))

			cache.update({'fruitDist': fruitDistance})

			return fruitDistance, cache

		else:

			cache.update({'fruitDist': 0})
			return 0, cache

	def ghostDist(self, state, cache):

		ghostLocations = [state['players'][key] for key in state['players'].keys() if not 'm' in key]

		ghostConsidered = ghostLocations[0]

		otherGhostDistances = []

		for locCount in range(1, len(ghostLocations)):
			otherGhostDistances.append(sum(abs(val1-val2) for val1, val2 in zip(ghostConsidered, ghostLocations[locCount])))

		nearestGhostDist = min(otherGhostDistances)

		cache.update({'nearestGhostDist': nearestGhostDist})

		return nearestGhostDist, cache



