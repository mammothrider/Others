#pac man
#Mammothrider
#Start on Jul.6 2016

from processing import *
from random import *
#by Mammothrider
#2016.4.12

_debug_ = 0

class cBody(object):
	def __init__(self):
		self.color = [0, 0, 0]
		self.position = [0, 0]
		
	def getColor(self):
		return self.color
		
	def getPosition(self):
		return self.position
	
	def setColor(self, *c):
		if len(c) == 1:
			for i in range(3):
				self.color[i] = c[0]
		elif len(c) == 3:
			for i in range(3):
				self.color[i] = c[i]

	def setPosition(self, *p):
		self.position[0], self.position[1] = p[0], p[1]
		
class cMonsterGenerator(cBody):
	def __init__(self):
		#four monster is needed, their color should be red, cyan, pink, orange
		#0 means ready to generate, -1 means cooldown, 1 means has been generated
		cBody.__init__(self)
		self.monster = {(255, 0, 0):0, (255, 0, 255):0, (0, 255, 255):0, (255, 180,0):0}
		
	def generateMonster(self, monsterList):
		num = len(monsterList)
		if num > 3:
			return
			
		tmp = 0
		for m in monsterList:
			c = m.getColor()
			c = tuple(c)
			if c in self.monster:
				self.monster[c] = 1
			
		for c in self.monster:
			if self.monster[c] == 0:
				tmp = cMonster()
				tmp.setColor(*c)
				tmp.setPosition(*self.position)
				monsterList.append(tmp)

class cMovingBody(cBody):
	def __init__(self):
		cBody.__init__(self)
		self.direct = [0, 1]
		self.nextDirection = [0, 1]
		self.movingState = 1
		self.velocity = 0.1
		self.percentage = 0
		self.deathFlag = 0
		
	def move(self, map):
		if self.deathFlag:
			return
			
		self.percentage += self.velocity
		#from -0.5 to 0.49
		while self.percentage > 0.5:
			next = [self.position[0] + self.direct[0], \
					self.position[1] + self.direct[1]]
			if not map.blocked(*next):
				self.position[0] = next[0]
				self.position[1] = next[1]
			
			self.percentage -= 1
			self.changeDirection()
	
	def changeDirection(self):
		self.direct[0] = self.nextDirection[0]
		self.direct[1] = self.nextDirection[1]
		
	def setDirection(self, x):
		self.nextDirection = x
	
	def getDirect(self):
		return self.direct
	
	def getState(self):
		return self.movingState
		
	def setVelocity(self, v):
		self.velocity = v

class cPacMan(cMovingBody):
	def __init__(self):
		cMovingBody.__init__(self)
		#super(cPacMan, self).__init__(self)
		self.setColor(255, 255, 0)
		self.startPoint = [0, 0]
		
		
	def setStartPosition(self, *p):
		self.setPosition(*p)
		self.startPoint[0], self.startPoint[1] = p[0], p[1]
		
	
	
class cMonster(cMovingBody):
	#path finding
	def __init__(self):
		cMovingBody.__init__(self)
		
	def pathFinding(self, _map):
		x, y = self.position[0], self.position[1]
		curValue = _map.getPFMvalue(*self.position)
		posDirect = []
		dir = [[0, 1], [1, 0], [0, -1], [-1, 0]]
		for i in dir:
			newPos = [x + i[0], y + i[1]]
			if _map.legalCheck(*newPos):
				tmpValue = _map.getPFMvalue(*newPos)
				if tmpValue < curValue:
					posDirect.append(i)
					
			if _debug_:
				print(i, tmpValue, curValue)
		if posDirect:
			nextMove = posDirect[int(random()*len(posDirect))]
		else:
			r = int(random() * 4)
			nextMove = dir[r]
		return nextMove
		
class cDeadMonster(cMovingBody):
	pass
	
class cFood(cBody):
	def __init__(self):
		cBody.__init__(self)
		self.setColor(255, 255, 0)
		return
	
class cWall(cBody):
	def __init__(self):
		cBody.__init__(self)
		self.setColor(0, 255, 255)
		return

class cMap():
	def __init__(self):
		self.mapSize = [25, 25]
		self.map = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, \
					1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, \
					1, 0, 1, 3, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, \
					1, 0, 1, 3, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, \
					1, 0, 1, 3, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, \
					1, 0, 1, 2, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, \
					1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, \
					1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, \
					1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, \
					1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, \
					1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, \
					1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, \
					1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, \
					1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, \
					1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
					1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
					1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, \
					1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
					1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 1, \
					1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, \
					1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, \
					1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, \
					1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, \
					1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, \
					1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, \
					]
		self.pacman = cPacMan()
		self.monsterGenerator = cMonsterGenerator()
		self.monster = []
		self.pfm = [0 for i in range(len(self.map))]
		
	def initializeMap(self):
		for i in range(len(self.map)):
			if self.map[i] == 0:
				self.map[i] = cFood()
			elif self.map[i] == 1:
				self.map[i] = cWall()
			elif self.map[i] == 2:
				self.map[i] = cBody()
				self.monsterGenerator.setPosition(i%self.mapSize[0], int(i/self.mapSize[0]))
			elif self.map[i] == 3: #start point
				self.map[i] = cBody()
				self.pacman.setStartPosition(i%self.mapSize[0], int(i/self.mapSize[0]))
			else:
				self.map[i] = cBody()
			self.map[i].setPosition(i%self.mapSize[0], int(i/self.mapSize[0]))
			
			
	def pathFindingMap(self):
		p = self.pacman.getPosition()
		# maxValue = self.mapSize[0] * self.mapSize[1]
		# for i in range(len(self.map)):
			# if (type(self.map[i]) == cWall):
				# self.pfm[i] = maxValue
			# else:
				# self.pfm[i] = abs(i%self.mapSize[0] - p[0]) \
							# + abs(i/self.mapSize[0] - p[1])
							
		self.dfsPathFinding(p[0], p[1], 0)
							
	def dfsPathFinding(self, x, y, dist):
		if self.legalCheck(x, y) != True:
			return
			
		t = y * self.mapSize[0] + x
		maxValue = self.mapSize[0] * self.mapSize[1] + 1
		
		if type(self.map[t]) is cWall:
			self.pfm[t] = maxValue
			return
		elif self.pfm[t] != 0 and self.pfm[t] < dist:
			return
			
		self.pfm[t] = dist
		
		self.dfsPathFinding(x + 1, y, dist + 1)
		self.dfsPathFinding(x - 1, y, dist + 1)
		self.dfsPathFinding(x, y + 1, dist + 1)
		self.dfsPathFinding(x, y - 1, dist + 1)
		
							
	def getPFMvalue(self, x, y):
		t = y * self.mapSize[0] + x
		return self.pfm[t]
				
	
	def blocked(self, *position):
		if position[0] >= self.mapSize[0] or position[0] < 0 \
		or position[1] >= self.mapSize[1] or position[1] < 0:
			return True
		
		
		tmp = position[0] + position[1] * self.mapSize[0]
		if type(self.map[tmp]) == cWall:
			return True
			
		if _debug_:
			print(position[0], position[1], 'unblock, type ', type(self.map[tmp]))
			
		return False
		
	def legalCheck(self, *c):
		if c[0] >= self.mapSize[0] or c[1] >= self.mapSize[1] or c[0] < 0 or c[1] < 0:
			return False
			
		return True
	
	def warpmap(self, *c):
		if c[0] >= self.mapSize[0]:
			c[0] -= self.mapSize[0]
			
		if c[1] >= self.mapSize[1]:
			c[1] -= self.mapSize[1]
		
		if c[0] < 0:
			c[0] += self.mapSize[0]
			
		if c[1] < 0:
			c[1] += self.mapSize[1]
			
		return c
	
class cCore():
	def __init__(self):
		self.map = cMap()
		self.map.initializeMap()
		
	def gameRun(self):
		#generate monster
		self.map.monsterGenerator.generateMonster(self.map.monster)
		
		#pathfinding
		self.map.pathFindingMap()
		for m in self.map.monster:
			dir = m.pathFinding(self.map)
			m.setDirection(dir)
		
		#move monster
		for i in self.map.monster:
			i.move(self.map)
		
		#move pacman
		self.map.pacman.move(self.map)
		
		#death check
		
class cController():
	pass	
	
class cGUI():
	def __init__(self, screenSizeX, screenSizeY, background):
		self.screenSize = (screenSizeX, screenSizeY)
		self.pixalSize = 40
		self.mapSize = (int(self.screenSize[0]/self.pixalSize), int(self.screenSize[1]/self.pixalSize))
		self.background = background
		
	def drawPacman(self, pac):
		mapx, mapy = pac.getPosition()
		center = (mapx * self.pixalSize + self.pixalSize/2, mapy * self.pixalSize + self.pixalSize/2)
		radius = int(self.pixalSize * 0.5)
		
		noStroke()
		color = pac.getColor()	
		fill(*color)
		ellipse(center[0], center[1], radius, radius)
		
		direct = pac.getDirect() #right -> 1, 0
		state = pac.getState() #moving state
		mouthSize = int(state * 1.0 / 10 * self.pixalSize)
		
		fill(*self.background) #fill with background color
		if direct[1] == 0:
			trangle(center[0], center[1], \
				center[0] + direct[0] * self.pixalSize/2, center[1] + mouthSize, \
				center[0] + direct[0] * self.pixalSize/2, center[1] - mouthSize)
		else:
			triangle(center[0], center[1], \
				center[0] + mouthSize, center[1] + direct[1] * self.pixalSize/2,\
				center[0] - mouthSize, center[1] + direct[1] * self.pixalSize/2)
				
	def drawMonster(self, monster):
		mapx, mapy = monster.getPosition()
		topLeft = (mapx * self.pixalSize, mapy * self.pixalSize)
		rectSize = [int(self.pixalSize * 0.6), int(self.pixalSize * 0.6)]
		margin = int((self.pixalSize - rectSize[0])/2)
		radius = int(self.pixalSize * 0.2)
		
		noStroke()
		color = monster.getColor()
		fill(*color)
		rect(topLeft[0], topLeft[1], rectSize[0], rectSize[1], radius, radius, 0, 0)
		
	def drawWall(self, wall):
		mapx, mapy = wall.getPosition()
		topLeft = (mapx * self.pixalSize, mapy * self.pixalSize)
		fill(*wall.getColor())
		rect(topLeft[0], topLeft[1], self.pixalSize, self.pixalSize)
		
	def drawFood(self, food):
		mapx, mapy = food.getPosition()
		topLeft = (mapx * self.pixalSize, mapy * self.pixalSize)
		half = int(self.pixalSize/2)
		center = (topLeft[0] + half, topLeft[1] + half)
		radius = int(self.pixalSize * 0.2)
		
		fill(*food.getColor())
		ellipse(center[0], center[1], radius, radius)
		
	def drawNumber(self, body, map):
		mapx, mapy = body.getPosition()
		topLeft = (mapx * self.pixalSize, mapy * self.pixalSize)
		textSize(20)
		fill(255)
		text(map.getPFMvalue(mapx, mapy), topLeft[0], topLeft[1])
		
	def default(self, obj):
		if _debug_:
			print("Enter default function, with type", type(obj))
	
	def drawMap(self, _map):
		func = {cWall:self.drawWall, cFood:self.drawFood, cPacMan:self.drawPacman, cMonster:self.drawMonster}
		for i in _map.map + [_map.pacman] + _map.monster:
			func.get(type(i), self.default)(i)
			
			if _debug_:
				self.drawNumber(i, _map)
		
	
game_state = 0 #0-title, 1-prepare, 2-ingame, 3-game end
map = cMap()
pixel = 10
playerNumber = 1
conti = True


gui = cGUI(1000, 1000, [0, 0, 0])
con = cCore()
   
def setup():
  size(1000, 1000)
  background(0, 0, 0)


def draw():
  background(0, 0, 0)
  con.gameRun()
  gui.drawMap(con.map)  
	
def keyPressed():
	global map, game_state, playerNumber
	if keyboard.key == "1":
		if game_state == 0 or game_state == 3:
			game_state = 1
			playerNumber = 1
	elif keyboard.key == "2":
		if game_state == 0 or game_state == 3:
			game_state = 1
			playerNumber = 2
			
	elif keyboard.keyCode == 32:
		if game_state == 0 or game_state == 3:
			game_state = 0

	#Player 1 -- White and Red
	elif keyboard.keyCode == 38:
		map.changeSnakeDirection(0, [0, -1])
	elif keyboard.keyCode == 40:
		map.changeSnakeDirection(0, [0, 1])
	elif keyboard.keyCode == 37:
		map.changeSnakeDirection(0, [-1, 0])
	elif keyboard.keyCode == 39:
		map.changeSnakeDirection(0, [1, 0])
	
	#Player 2 -- Green	
	elif keyboard.keyCode == 87:
		map.changeSnakeDirection(1, [0, -1])
	elif keyboard.keyCode == 83:
		map.changeSnakeDirection(1, [0, 1])
	elif keyboard.keyCode == 65:
		map.changeSnakeDirection(1, [-1, 0])
	elif keyboard.keyCode == 68:
		map.changeSnakeDirection(1, [1, 0])
	
run()