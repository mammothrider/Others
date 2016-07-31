#pac man
#Mammothrider
#Start on Jul.6 2016

from processing import *
from random import *
#by Mammothrider
#2016.4.12

_debug_ = 1

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
		#four monster is needed, their color should be red, blue, pink, yellow
		#0 means ready to generate, -1 means cooldown, 1 means has been generated
		self.monster = {"red":0, "pink":0, "blue":0, "yellow":0}
		
	def generateMonster(self, monsterList):
		num = len(monsterList)
		if num > 3:
			return
		
		

class cMovingBody(cBody):
	def __init__(self):
		cBody.__init__(self)
		self.direct = [0, 1]
		self.nextDirection = [0, 1]
		self.movingState = 1
		self.velocity = 0.1
		self.percentage = 0
		self.deathFlag = 0
		
	def move(self):
		if self.deathFlag:
			return
			
		self.percentage += self.velocity
		#from -0.5 to 0.49
		if self.percentage > 0.5:
			self.position[0] += self.direct[0]
			self.position[1] += self.direct[1]
			self.changeDirection()
	
	def changeDirection(self):
		self.direction[0] = self.nextDirection[0]
		self.direction[1] = self.nextDirection[1]
		
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
	
	
class cMonster(cMovingBody):
	#path finding
	def __init__(self):
		cMovingBody.__init__(self)
		
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
					1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, \
					1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, \
					1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, \
					1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, \
					1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, \
					1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, \
					1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, \
					]
		self.pacman = None
		self.monster = []
		self.monsterGenerator = None
		self.initializeMap()
		
	def initializeMap(self):
		for i in range(len(self.map)):
			if self.map[i] == 0:
				self.map[i] = cFood()
			elif self.map[i] == 1:
				self.map[i] = cWall()
			elif self.map[i] == 2:
				if self.monsterGenerator is None:
					self.monsterGenerator = cMonsterGenerator()
				self.map[i] = self.monsterGenerator
			else:
				self.map[i] = cBody()
			self.map[i].setPosition(i%self.mapSize[0], int(i/self.mapSize[0]))
		
	
class cController():
	def __init__(self):
		pass
		
	def gameStart(self):
		self.map = cMap()
		self.map.initializeMap()
		self.map.pacman = cPacMan()
		self.monsterGenerator = cMonsterGenerator()
		sekf.initializeMap()
		
		
		
	
class cGUI():
	def __init__(self, screenSizeX, screenSizeY, background):
		self.screenSize = (screenSizeX, screenSizeY)
		self.pixalSize = 20
		self.mapSize = (int(self.screenSize[0]/self.pixalSize), int(self.screenSize[1]/self.pixalSize))
		self.background = background
		
	def drawPacman(self, pac):
		mapx, mapy = pac.getPosition()
		center = (mapx * self.pixalSize, mapy * self.pixalSize)
		radius = int(self.pixalSize * 0.45)
		
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
		rectSize = int(self.pixalSize * 0.6)
		radius = int(self.pixalSize * 0.2)
		
		noStroke()
		color = monster.getColor()
		fill(*color)
		rect(topLeft[0], topLeft[1], rectSize, rectSize, radius, radius, 0, 0)
		
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
		
	def default(self, obj):
		if _debug_:
			print("Enter default function, with type", type(obj))
	
	def drawMap(self, _map):
		func = {cWall:self.drawWall, cFood:self.drawFood, cPacMan:self.drawPacman, cMonster:self.drawMonster}
		for i in _map.map:
			func.get(type(i), self.default)(i)
		
	
game_state = 0 #0-title, 1-prepare, 2-ingame, 3-game end
map = cMap()
pixel = 10
playerNumber = 1
conti = True


gui = cGUI(600, 400, [0, 0, 0])
pac = cPacMan()
pac.setPosition(1, 1)
pac.setColor(0, 255, 0)
mon = cMonster()
mon.setColor(255, 0, 0)
mon.setPosition(2, 2)
map = cMap()
	 
def setup():
	size(600, 450)
	background(0, 0, 0)


def draw():
	global map, game_state, pixel, playerNumber, conti, gui, pac, mon
	#title
	if game_state == 0:
		background(0, 0, 0)
		textSize(100)
		fill(255, 255, 0)
		text("PacMan", 140, 200)
		textSize(20)
		text("1.Single Player", 230, 270)
		text("2.Double Player", 230, 300)
	
	elif game_state == 1:

		
		game_state = 2
		
	
	elif game_state == 2:
		background(0, 0, 0)
		gui.drawMap(map)
		
	elif game_state == 3:
		textSize(60)
		fill(255, 0, 0)
		text("GAME OVER", 120, 150)
		textSize(30)
	
		score = []
		for s in map.snakeList:
			score.append(len(s.returnSnake()))
		for i in range(len(score)):
			text("Player %d: %d" %(i + 1, score[i] - 5), 200, 200 + 30 * i)
		text("Press Space to return menu", 120, 350)
	else:
		game_state = 0
	
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