from processing import *
from random import *
#by Mammothrider
#2016.4.12

#defined on a uniform coordinate
#snake can only move integer distance
class cSnake():
	def __init__(self, map):
		self.length = 5
		self.velocity = 0.1
		self.direction = [1, 0]
		self.nextDirection = [1, 0]
		self.body = [[0, 0] for i in range(self.length)]
		self.per = 0
		self.growLength = 0
		self.deathFlag = 0
		self.color = [255, 255, 255]
		
		self.alive = True
		
		self.map = map
	
	def setHeadPosition(self, x, y):
		for i in range(self.length):
			self.body[i][0] = x - i
			self.body[i][1] = y
		
	def moveOneStepForward(self):
		if not self.alive:
			return False
			
		next = [self.body[0][0] + self.direction[0], \
				self.body[0][1] + self.direction[1]]
			
		#snake may cross boundary, get the new position, then hit check
		next = self.map.warpmap(next)
		if self.map.hitCheck(next[0], next[1]):
			self.alive = False
			return False
		
		#move forward
		self.body.insert(0, next)
		
		#delete one tail if not eated
		if self.growLength == 0:
			self.body.pop()
		else:
			self.growLength -= 1
		
		return True

	def move(self):
		if not self.alive:
			return False
			
		#snake will move when per > 1
		self.per += self.velocity
		if self.per > 0:
			t = int(self.per)
			self.per -= t
			for i in range(t):
				if not self.moveOneStepForward():
					return False
				self.changeDirection()
		return True
	
	def setVelocity(self, x):
		self.velocity = x
	
	def changeDirection(self):
		self.direction[0] = self.nextDirection[0]
		self.direction[1] = self.nextDirection[1]
	
	def setDirection(self, x):
		#there is no turning back
		if self.direction[0] * x[0] + self.direction[1] * x[1] == 0:
			self.nextDirection = x
	
	def setColor(self, c):
		self.color = c[0:3]
	
	def increaseLength(self, x):
		self.growLength += x
	
	def velocityIncress(self, x):
		self.velocity += x
	
	def returnSnake(self):
		return self.body
	
	def returnColor(self):
		return self.color
	
	def eat(self, food):
		food.specialFunction(self)
	
class cFood():
	def __init__(self):
		self.lengthIncrease = 1
		self.velocityIncress = 0.02
		self.position = [0, 0]
		self.color = [255, 255, 255]
	
	def setPosition(self, x, y):
		self.position[0] = x
		self.position[1] = y
	
	def returnPosition(self):
		return self.position
	
	def returnColor(self):
		return self.color
	
	def specialFunction(self, snake):
		snake.increaseLength(self.lengthIncrease)
		snake.velocityIncress(self.velocityIncress)
	
	 
class cMap():
	def __init__(self):
		self.boardSize = [60, 40]
		self.snakeList = []
		self.foodList = []
		self.backgroundColor = [0, 0, 0]
		self.boundaryCross = False
	
	def setBoardSize(self, x, y):
		self.boardSize[0] = x
		self.boardSize[1] = y
	
	def coordinateUnoccupied(self):
		x = self.boardSize[0]
		y = self.boardSize[1]
	
		board = [[0 for i in range(x)] for j in range(y)]
		coor = []
		
		for i in self.snakeList:
			for c in i.returnSnake():
				board[c[1]][c[0]] = 1
		
		for i in self.foodList:
			c = i.returnPosition()
			board[c[1]][c[0]] = 2
			
		for i in range(y):
			for j in range(x):
				if board[i][j] == 0:
					coor.append([j, i])
		
		return coor
	
	def generateFood(self):
		coor = self.coordinateUnoccupied()
		t = int(random() * len(coor))
		x, y = coor[t][0], coor[t][1]
		newFood = cFood()
		newFood.setPosition(x, y)
		self.foodList.append(newFood)
	
	def warpmap(self, c):
		if self.boundaryCross == True:
			if c[0] >= self.boardSize[0]:
				c[0] -= self.boardSize[0]
				
			if c[1] >= self.boardSize[1]:
				c[1] -= self.boardSize[1]
			
			if c[0] < 0:
				c[0] += self.boardSize[0]
				
			if c[1] < 0:
				c[1] += self.boardSize[1]
			
		return c
	
	def foodCheck(self):
		p = []
		h = []
		for i in self.foodList:
			p.append(i.returnPosition())
			
		for i in self.snakeList:
			h.append(i.returnSnake()[0])
			
		#snake's head on food
		for i in h:
			if i in p:
				t = p.index(i)
				s = h.index(i)
				self.snakeList[s].eat(self.foodList[t])
				del self.foodList[t]
		
	def hitCheck(self, x, y):
		obstacle = []
		for i in self.snakeList:
			t = i.returnSnake()
			obstacle += t[0:]
			
		nextPace = [x, y]
			
		if nextPace in obstacle:
			return True
				
		if nextPace[0] < 0 or nextPace[0] >= self.boardSize[0] \
		or nextPace[1] < 0 or nextPace[1] >= self.boardSize[1]:
			return True
				
		return False
		
	def generationCheck(self):
		if not self.foodList:
			return True
		return False
		
	def initGame(self, playerNumber):
		if playerNumber == 1:
			s = cSnake(self)
			s.setHeadPosition(int(self.boardSize[0]/2), int(self.boardSize[1]/2))
			self.snakeList.append(s)
		elif playerNumber == 2:
			s = cSnake(self)
			s.setColor([255, 0, 0])
			s.setHeadPosition(int(self.boardSize[0]/2), int(self.boardSize[1]/3))
			self.snakeList.append(s)
			
			s = cSnake(self)
			s.setColor([0, 255, 0])
			s.setHeadPosition(int(self.boardSize[0]/2), int(2 * self.boardSize[1]/3))
			self.snakeList.append(s)
			
		self.generateFood()
	
	def changeSnakeDirection(self, snakeNumber, dir):
		self.snakeList[snakeNumber].setDirection(dir)
	
	def run(self):
		if self.generationCheck():
			self.generateFood()
		
		moveFlag = False
		for i in self.snakeList:
			if i.move():
				moveFlag = True
		
		#creat new food if needed
		self.foodCheck()
		
		#game continue when any snake is alive
		if moveFlag:
			return True
		return False
	
game_state = 0 #0-title, 1-prepare, 2-ingame, 3-game end
map = cMap()
pixel = 10
playerNumber = 1
conti = True
	 
def setup():
	size(600, 450)
	background(0, 0, 0)

def draw():
	global map, game_state, pixel, playerNumber, conti
	#title
	if game_state == 0:
		background(0, 0, 0)
		textSize(100)
		fill(255, 255, 0)
		text("SNAKE", 140, 200)
		textSize(20)
		text("1.Single Player", 230, 270)
		text("2.Double Player", 230, 300)
	
	elif game_state == 1:
		map = cMap()
		map.setBoardSize(60, 40)
		map.initGame(playerNumber)
		game_state = 2
		conti = True
	
	elif game_state == 2:

		#draw part
		background(map.backgroundColor[0], map.backgroundColor[1], map.backgroundColor[2])
		
		conti = map.run()
		
		#draw snake
		for s in map.snakeList:
			c = s.returnColor()		 
			noStroke()
			fill(c[0], c[1], c[2])
			rectMode(CENTER)
			for b in s.returnSnake():
				rect(b[0] * pixel + pixel / 2, b[1] * pixel + pixel / 2, pixel, pixel)
			
		#draw food
		for f in map.foodList:
			c = f.returnColor()		 
			noStroke()
			fill(c[0], c[1], c[2])
			rectMode(CENTER)
			b = f.returnPosition()
			rect(b[0] * pixel + pixel / 2, b[1] * pixel + pixel / 2, pixel, pixel)
		
		#score board
		score = []
		for s in map.snakeList:
			score.append(len(s.returnSnake()))
		
		stroke(255)
		line(0, 401, 600, 401)
		
		fill(255)
		textSize(30)
		for i in range(len(score)):
			text("Player %d: %d" %(i + 1, score[i] - 5), 10 + 180 * i, 430)
		
		#snake died
		if not conti:
			game_state = 3
		
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