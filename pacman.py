#pac man
#Mammothrider
#Start on Jul.6 2016

from processing import *
from random import *
import time
#by Mammothrider
#2016.4.12

_debug_ = 0
_statedebug_ = 0
_energizedDebug_ = 0

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
        #0 means ready to generate, 1 means has been generated
        cBody.__init__(self)
        self.monster = {(255, 0, 0):0, (255, 0, 255):0, (0, 255, 255):0, (255, 180,0):0}
        # self.monster = {(255, 0, 0):0}
        self.monsterTimer = {}
        self.scatterPosition = {(255, 0, 0):[1, 1], (255, 0, 255):[1, 23], (0, 255, 255):[23, 1], (255, 180,0):[23, 23]}
        self.velocity = 0.05
        
    def initialMonster(self, monsterList):
        #first time generate
        tmp = 0
        shift = 0
        for c in self.monster:
            if self.monster[c] == 0:
                tmp = cMonster()
                tmp.setColor(*c)
                tmp.setPosition(self.position[0], self.position[1] - shift)
                shift += 1
                tmp.setScatterPosition(*self.scatterPosition[c])
                tmp.setVelocity(self.velocity)
                monsterList.append(tmp)
                self.monster[c] = 1
        
    def reviveMonster(self, monsterList):
        #check monster state
        for m in monsterList:
            c = m.getColor()
            c = tuple(c)
            if c in self.monster \
            and (self.monster[c] == 0 \
            # in nest
                    and m.getState() == "Dead" \
                    #dead
                    and self.monsterTimer[c].isFinished()): 
                    #ready to generate
                self.monster[c] = 1
                m.setState("Chase")
                m.setVelocity(self.velocity)
                

                
    def recycle(self, monster):
        color = tuple(monster.getColor())
        if monster.getState() == "Dead" \
        and self.monster[color] == 1 \
        and monster.getPosition() == self.getPosition():
            self.monsterTimer[color] = cTimer()
            self.monsterTimer[color].timerStart(5)
            self.monster[color] = 0 #cooldown
            monster.setVelocity(0)
            
    def setVelocity(self, v):
        self.velocity = v
                
                

class cMovingBody(cBody):
    def __init__(self):
        cBody.__init__(self)
        self.direction = [0, -1]
        self.nextDirection = [0, -1]
        self.movingState = 1
        self.velocity = 0.05
        self.percentage = 0
        self.deathFlag = 0
        
    def move(self, map):
        if self.deathFlag:
            return
            
        self.percentage += self.velocity
        while self.percentage >= 1:
            next = [self.position[0] + self.direction[0], \
                    self.position[1] + self.direction[1]]
            if not map.blocked(*next):
                self.position[0] = next[0]
                self.position[1] = next[1]
            
            self.percentage -= 1
    
    def changeDirection(self):
        self.direction[0] = self.nextDirection[0]
        self.direction[1] = self.nextDirection[1]
        
    def setDirection(self, x):
        self.nextDirection = x
        self.changeDirection()
    
    def getDirect(self):
        return self.direction
        
    def setVelocity(self, v):
        self.velocity = v
        #self.percentage = 0
        #print("speed set to", v)

class cPacMan(cMovingBody):
    def __init__(self):
        cMovingBody.__init__(self)
        #super(cPacMan, self).__init__(self)
        self.setColor(255, 255, 0)
        self.startPoint = [0, 0]
        self.score = 0
        self.timer = cTimer()
        self.energized = False
        self.life = 3
    
        
    def setStartPosition(self, *p):
        self.setPosition(*p)
        self.startPoint[0], self.startPoint[1] = p[0], p[1]
        
        if _energizedDebug_:
            self.setPosition(1, 1)
        
    def move(self, map):
        #check twice, two situation: p -> m, m -> p. Otherwise will sometime cause meeting and missing
        self.checkMonster(map)
    
        #move one step forward
        cMovingBody.move(self, map)
        
        if _energizedDebug_:
            self.energized = True
            self.velocity = 0.08
            map.energized()
        
        #check if on a food
        food = map.getItemInPosition(self.position[0], self.position[1])
        self.eat(food, map)
        
        self.checkMonster(map)
        
        #timer for energized
        if self.timer.isFinished():
            self.energized = False
            map.deenergized()
            
    def checkMonster(self, map):
        #check if on a monster
        monster = map.getMonsterOnPacman()
        if monster:
            if monster.getState() not in ["Frightened", "Dead"]:
                if self.death():
                    map.gameEnd()
            elif monster.getState() == "Frightened":
                self.eatMonster(monster, map)
        
    def eat(self, food, map):
        if type(food) == cBody:
            return
            
        elif type(food) == cFood:
            self.score += 10
            
        elif type(food) == cSuperFood:
            self.score += 50
            self.energized = True
            map.energized()
            self.timer.timerStart(20)
            
        map.foodEaten(food)
        
    def eatMonster(self, monster, map):
        self.score += 200
        monster.setState("Dead")
        monster.setVelocity(map.standardVelocity * 2)
            
    def death(self):
        self.life -= 1
        if self.life > 0:
            self.setPosition(*self.startPoint)
            return True
        return False
        
    def isAlive(self):
        return self.life > 0
        
    def getScore(self):
        return self.score
    
    
class cMonster(cMovingBody):
    def __init__(self):
        cMovingBody.__init__(self)
        #chase, scatter, frightened
        #in chase mode, monster run towards pacman
        #in scatter mode, monster moves towards a specific position
        #in frightened mode, monster runs on random
        self.state = "Chase"
        self.scatterPosition = [0, 0]
        self.scatterTime = 0
        
        
        self.timer = cTimer()
        self.timer.initialTimer()
        self.timer.timerStart(20)
        
    def chooseDirection(self, _map, getValue):
        #randomly choose one directiong from possible direction
        #using value function getValue
        x, y = self.position[0], self.position[1]
        dir = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        
        #monster can not turn back unless state change
        dir.remove([-self.direction[0], -self.direction[1]])
        
        minValue = 9999
        next = self.direction
        for i in dir:
            newPos = [x + i[0], y + i[1]]
            if not _map.blocked(*newPos):
                tmpValue = getValue(*newPos)
                if tmpValue < minValue:
                    next = i
                    minValue = tmpValue
                    
        newPos = [x + next[0], y + next[1]]
        if not _map.blocked(*newPos):
            return next
        else:
            return [-self.direction[0], -self.direction[1]]
                            
    
    def dfsPathFinding(self, tx, ty, _map):
        #using dfs to find the shortest path
        dfsValue = [0 for i in range(len(_map.map))]
        maxValue = _map.mapSize[0] * _map.mapSize[1] + 1
    
        def dfs(x, y, dist):
            #transform 2d coordinate into 1d coor
            t = y * _map.mapSize[0] + x 
            
            #terminated condition
            if type(_map.map[t]) is cWall:
                dfsValue[t] = maxValue
                return
            elif dfsValue[t] != 0 and dfsValue[t] < dist:
                return
                
            #set value
            dfsValue[t] = dist
            
            #recursion
            dfs(x + 1, y, dist + 1)
            dfs(x - 1, y, dist + 1)
            dfs(x, y + 1, dist + 1)
            dfs(x, y - 1, dist + 1)
            
            
        def getDFSvalue(x, y):
            t = y * _map.mapSize[0] + x     
            return dfsValue[t]
            
        def drawNumber(mapx, mapy, value):
            topLeft = (mapx * 40, mapy * 40 + 40)
            textSize(20)
            fill(255)
            text(value, topLeft[0], topLeft[1])
            
        dfs(tx, ty, 0)
        
        if _debug_:
            for x in range(map.mapSize[1]):
                for y in range(map.mapSize[0]):
                    drawNumber(x, y, getDFSvalue(x, y))
        
        return self.chooseDirection(_map, getDFSvalue)
        
    def setState(self, state):
        #change monster state
        
        #dead monster can only be change to chase
        if self.state == "Dead":
            if state == "Chase":
                self.state = state
                self.timer.timerStart(20)
            return
        
        #reverse direction when state change occured    
        elif self.state != state:
            self.setDirection([-self.direction[0], -self.direction[1]])
            
            #change into frightened mode will pause timer
            if state == "Frightened":
                self.timer.timerPause()
            else:
                self.timer.timerContinue()
    
        self.state = state
        
    def frightenedPathFinding(self, map):
        x, y = self.position[0], self.position[1]
        dir = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        
        #monster can not turn back unless state change
        dir.remove([-self.direction[0], -self.direction[1]])
        
        #bug: remove second item makes for=loop skip third one
        # for i in dir:
            # if map.blocked(x + i[0], y + i[1]):
                # print(i, 'removed')
                # dir.remove(i)
        dir = [i for i in dir if not map.blocked(x + i[0], y + i[1])]

        if _statedebug_:
            print(self.position, dir)
        
        #in case empty
        if dir: 
            nextMove = dir[int(random()*len(dir))]
        else:
            nextMove = [-self.direction[0], -self.direction[1]]
        return nextMove
    
    def move(self, map):        
        #check state before moving
        self.changeState()
    
        #check the percentage before the direction
        #when it moves, it move in the the right direction
        self.percentage += self.velocity
        if self.percentage >= 1:
            #get moving direction
            nextMove = []
            if self.state == "Chase":
                tmp = map.pacman.getPosition()
                nextMove = self.dfsPathFinding(tmp[0], tmp[1], map)
            elif self.state == "Scatter":
                nextMove = self.dfsPathFinding(self.scatterPosition[0], self.scatterPosition[1], map)
            elif self.state == "Frightened":
                nextMove = self.frightenedPathFinding(map)
            elif self.state == "Dead":
                tmp = map.monsterGenerator.getPosition()
                if self.getPosition() != tmp:
                    nextMove = self.dfsPathFinding(tmp[0], tmp[1], map)
                else:
                    map.recycleDeadMonster(self)
                    return
            
            #set direction
            self.setDirection(nextMove)
            self.changeDirection()
            
            #move one step
            next = [self.position[0] + self.direction[0], \
                    self.position[1] + self.direction[1]]
            if not map.blocked(*next):
                self.position[0] = next[0]
                self.position[1] = next[1]
            
            self.percentage -= 1
            
            #debug
            if _statedebug_:
                print(self.state, self.direction)
            
    def changeState(self):
        if not self.timer.isFinished():
            return

        if self.state == "Chase" and self.scatterTime < 4: # change from Chase mode to scatter mode
            if self.scatterTime < 2:
                self.timer.timerStart(7)
            else:
                self.timer.timerStart(5)
            self.setState("Scatter")
        elif self.state == "Scatter":
            self.scatterTime += 1
            self.timer.timerStart(20)
            self.setState("Chase")
        else:
            pass
            
        return
        
    def getState(self):
        return self.state
        
    def setScatterPosition(self, *p):
        self.scatterPosition[0] = p[0]
        self.scatterPosition[1] = p[1]
    
    
class cTimer():
    def __init__(self):
        self.startTime = 0
        self.interval = 0
        self.pauseTime = 0
        
    def initialTimer(self):
        self.startTime = 0
        self.interval = 0
        self.pauseTime = 0
        
    def setInterval(self, t):
        self.interval = t
        
    def timerStart(self, interval = 20):
        self.setInterval(interval)
        self.startTime = time.time()
        
    def isFinished(self):
        if self.pauseTime > 0:
            return False
        if self.startTime == 0:
            return False
        return time.time() - self.startTime > self.interval
        
    def timerPause(self):
        self.pauseTime = time.time()
        
    def timerContinue(self):
        if self.pauseTime != 0:
            self.interval += time.time() - self.pauseTime
        self.pauseTime = 0
        
class cFood(cBody):
    def __init__(self):
        cBody.__init__(self)
        self.setColor(255, 255, 0)
        return
        
class cSuperFood(cFood):
    pass
    
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
        self.standardVelocity = 0.05
        self.pacman = cPacMan()
        self.pacman.setVelocity(self.standardVelocity)
        
        self.monsterGenerator = cMonsterGenerator()
        self.monsterGenerator.setVelocity(self.standardVelocity)
        
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
        
    def foodEaten(self, food):
        x, y = food.getPosition()
        self.map[y * self.mapSize[0] + x] = cBody()
        
    def energized(self):
        self.pacman.setVelocity(self.standardVelocity * 1.5)
        for i in self.monster:
            i.setState("Frightened")
            
    def deenergized(self):
        pacman.setVelocity(self.standardVelocity)
        for i in self.monster:
            i.setState("Chase")
        
    def getItemInPosition(self, x, y):
        return self.map[y * self.mapSize[0] + x]
        
    def getMonsterOnPacman(self):
        for m in self.monster:
            if m.getPosition() == self.pacman.getPosition():
                return m
        return None
        
    def recycleDeadMonster(self, monster):
        self.monsterGenerator.recycle(monster)
        
    def gameEnd(self):
        pass
    
class cCore():
    def __init__(self):
        self.map = cMap()
        self.map.initializeMap()
        #generate monster
        self.map.monsterGenerator.initialMonster(self.map.monster)
        
    def gameRun(self):
        #revive dead monster
        self.map.monsterGenerator.reviveMonster(self.map.monster)
        
        #chooseDirection
        # self.map.pathFindingMap()
        # p = self.map.pacman.getPosition()
        # for m in self.map.monster:
            # dir = m.chooseDirection(self.map)
            # dir = m.dfsPathFinding(p[0], p[1], self.map)
            # m.setDirection(dir)
        
        #move monster
        for i in self.map.monster:
            i.move(self.map)
        
        #move pacman
        self.map.pacman.move(self.map)
        
    def gameContinue(self):
        return self.map.pacman.isAlive()
    
    def returnScore(self):
        return self.map.pacman.getScore()
        
class cController():
    pass    
    
class cGUI():
    def __init__(self, screenSizeX, screenSizeY, background, core):
        self.screenSize = (screenSizeX, screenSizeY)
        self.mapSize = core.map.mapSize
        self.pixalSize = int(screenSizeX/self.mapSize[0])
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
        state = pac.movingState #moving state
        mouthSize = int(state * 1.0 / 10 * self.pixalSize)
        
        fill(*self.background) #fill with background color
        if direct[1] == 0:
            triangle(center[0], center[1], \
                center[0] + direct[0] * self.pixalSize/2, center[1] + mouthSize, \
                center[0] + direct[0] * self.pixalSize/2, center[1] - mouthSize)
        else:
            triangle(center[0], center[1], \
                center[0] + mouthSize, center[1] + direct[1] * self.pixalSize/2,\
                center[0] - mouthSize, center[1] + direct[1] * self.pixalSize/2)
                
    def drawMonster(self, monster):
        mapx, mapy = monster.getPosition()
        topLeft = (mapx * self.pixalSize, mapy * self.pixalSize)
        
        
        def drawBody(color):
            #body
            rectSize = [int(self.pixalSize * 0.6), int(self.pixalSize * 0.6)] #length * width
            margin = int((self.pixalSize - rectSize[0])/2)
            radius = int(self.pixalSize * 0.2)
            
            noStroke()
            fill(*color)
            rect(topLeft[0], topLeft[1], rectSize[0], rectSize[1], radius, radius, 0, 0)
            
            #foot
            if monster.movingState == 1:
                triangle(topLeft[0], topLeft[1] + rectSize[0], \
                    topLeft[0] + rectSize[1] / 2, topLeft[1] + rectSize[0], \
                    topLeft[0] + rectSize[1] / 4, topLeft[1] + rectSize[0] + self.pixalSize * 0.1)
                triangle(topLeft[0] + rectSize[1], topLeft[1] + rectSize[0], \
                    topLeft[0] + rectSize[1] / 2, topLeft[1] + rectSize[0], \
                    topLeft[0] + rectSize[1] * 3 / 4, topLeft[1] + rectSize[0] + self.pixalSize * 0.1)
                    
        
        if monster.getState() == "Dead":
            #only monster eyes
            drawBody([255, 255, 255])
            
            
        elif monster.getState() == "Frightened":
            drawBody([0, 0, 255])
        else:
            drawBody(monster.getColor())
            
            
        
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
        
    # def drawNumber(self, body, map):
        # mapx, mapy = body.getPosition()
        # topLeft = (mapx * self.pixalSize, mapy * self.pixalSize)
        # textSize(20)
        # fill(255)
        # text(map.getPFMvalue(mapx, mapy), topLeft[0], topLeft[1])
        
    def default(self, obj):
        # if _debug_:
            # print("Enter default function, with type", type(obj))
        pass
    
    def drawMap(self, _map):
        func = {cWall:self.drawWall, cFood:self.drawFood, cPacMan:self.drawPacman, cMonster:self.drawMonster}
        for i in _map.map + [_map.pacman] + _map.monster:
            func.get(type(i), self.default)(i)
        
    
game_state = 0 #0-title, 1-prepare, 2-ingame, 3-game end
window_size = 500
con = gui = 0


def setup():
    size(window_size, window_size)
    background(0, 0, 0)


def draw():
    global game_state, window_size, con, gui
    #title
    if game_state == 0:
        background(0, 0, 0)
        textSize(window_size/5)
        fill(255, 255, 0)
        text("PACMAN", 40 *window_size/500, 200 *window_size/500)
        textSize(20)
        text("1.Game Start", 180 *window_size/500, 270 *window_size/500)
    
    elif game_state == 1:
        con = cCore()
        gui = cGUI(window_size, window_size, [0, 0, 0], con)
        game_state = 2
    
    elif game_state == 2:
        if con.gameContinue():
            background(0, 0, 0)
            con.gameRun()
            gui.drawMap(con.map)
        else:
            game_state = 3
        
    elif game_state == 3:
        textSize(60)
        fill(255, 0, 0)
        text("GAME OVER", 80 *window_size/500, 150 *window_size/500)
        textSize(30)
    
        score = con.returnScore()
        text("Final Score: %d" %(score), 130 *window_size/500, 250 *window_size/500)
        text("Press Space to return menu", 50 *window_size/500, 350 *window_size/500)
    else:
        game_state = 0   
    
def keyPressed():
    global game_state

    if keyCode == 49: # key '1'
        if game_state == 0:
            game_state = 1
            
    elif keyCode == 32: # key "Space"
        if game_state == 0 or game_state == 3:
            game_state = 0
            
    if keyCode == UP:
        # print(UP)
        con.map.pacman.setDirection([0, -1])
    elif keyCode == DOWN:
        # print(DOWN)
        con.map.pacman.setDirection([0, 1])
    elif keyCode == LEFT:
        # print(LEFT)
        con.map.pacman.setDirection([-1, 0])
    elif keyCode == RIGHT:
        # print(RIGHT)
        con.map.pacman.setDirection([1, 0])
    
# run()