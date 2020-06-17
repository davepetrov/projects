#!/usr/bin/python3
#--------------------#
# BOARD PAGE
#    Includes
#         -class Board
#         -class MazeBoard
#         -class RandomBoard
#         -class ObsticleBoard
#--------------------#

from maze_generator import *
from random import choice
import pygame
from node import *
from display import *
from button import Button
pygame.init()

class Board():
    def __init__(self, rows, cols):
        self.start = Node(None, None)  # start node
        self.goal = Node(None, None)  # goal node
        self.current = Node(None,None)
        self.path = []
        self.matrix = []
        self.cols = cols
        self.rows = rows
        self.finish = False
        self.userSelect = None  # 'w' or 's' or 'g (wall, start, goal)
        self.act = 'select' #'select' or 'work' or 'success' ror 'fail'

        self.checkpoints=[]
        self.checkpointsFound = []
        self.openSetsCP = [[self.start]]
        self.openSet = [self.start]  # nodes to be visited per ct
        self.closedSetCP = [[]]  # nodes visited per ct
        self.currentCP = 1
        self.paths = []

    def setBorder(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if j == 0 or i == 0 or j == self.cols-1 or i == self.rows-1:
                    self.matrix[i][j].wall = True

    def selectCheckpoints(self):
        click = 0
        cont = True
        self.userSelect = 'cp'
        count=0
        while cont:
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and e.type != pygame.MOUSEBUTTONUP:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    x = (mouseX-padding)//ppb
                    y = (mouseY-padding)//ppb
                    if 1 <= x < (self.cols-1) and 1 <= y < (self.rows-1):
                        self.checkpoints.append(Node(None,None))
                        self.checkpoints[count].x = x
                        self.checkpoints[count].y = y
                        self.matrix[y][x] = self.checkpoints[count]
                        self.openSetsCP.append([self.checkpoints[count]])
                        count+=1
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    if count > 0 :
                        for cp in range(len(self.checkpoints)):
                            self.checkpointsFound.append(False)
                    else:
                        self.openSet = self.openSetsCP[0]
                    self.userSelect=None
                    cont = False
                    
            display(self)

    def selectStartAndGoal(self):
        self.act == 'choose'
        click = 0
        cont = True
        self.userSelect = 's'
        self.act = None
        while cont:
            for e in pygame.event.get():
                mouseX, mouseY = pygame.mouse.get_pos()
                x = (mouseX-padding)//ppb
                y = (mouseY-padding)//ppb
                if e.type == pygame.MOUSEBUTTONDOWN :
                    if 1 <= x < (self.cols-1) and 1 <= y < (self.rows-1):
                        if click == 0:
                            self.start.x = x
                            self.start.y = y
                            self.matrix[y][x] = self.start
                            click += 1
                            self.userSelect='g'

                        else:
                            if self.start.x != x or self.start.y != y:
                                self.goal.x = x
                                self.goal.y = y
                                self.userSelect=None
                                self.matrix[y][x] = self.goal
                                cont = False
            display(self)

    def initChildren(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.matrix[row][col].createChildren(self)

    def loadBoard(self):
        for row in range(self.rows):
            self.matrix.append([])
            for col in range(self.cols):
                self.matrix[row].append(Node(row, col))

    def initilize(self):
        self.loadBoard()
        self.setBorder()
        self.initChildren()

    def userChoose(self):
        self.selectStartAndGoal()
        self.selectCheckpoints()
        self.start.wall = False
        self.goal.wall = False
        for i in range(len(self.checkpoints)):
            self.checkpoints[i].wall = False
        self.act = None

    def prnt_display(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.matrix[row][col].show(self)

            print()
        print('-'*60)

    def clear(self):
        for i in range(1,self.rows-1):
            for j in range(1,self.cols-1):
                self.matrix[i][j] = None
    
    def restart(self):
        self.openSet = [self.start]  # nodes to be visited per ct
        self.openSetsCP = [[self.start]]
        self.closedSetCP = [[]]  # nodes visited per ct

        for i in range(len(self.checkpoints)):
            self.openSetsCP.append([self.checkpoints[i]])

        self.path = []
        self.paths = []
        self.finish = False
        self.currentCP = 1
                


####---------------------------------------------------------------------------#####


class RandomBoard(Board):
    def __init__(self, rows, cols, probability):
        super().__init__(rows, cols)
        self.wallSpawnProbability = probability

    def generateObstacles(self):
        # Probability
        self.act = "generating"
        for row in range(self.rows):
            for col in range(self.cols):
                i = randint(0, 99)
                if -1 <= i <= self.wallSpawnProbability:
                    self.matrix[row][col].wall = True
                    #display(self)

    def initilize(self):
        self.loadBoard()
        self.setBorder()
        self.initChildren()

    def userChoose(self):
        self.generateObstacles()
        self.selectStartAndGoal()
        self.selectCheckpoints()
        self.start.wall = False
        self.goal.wall = False

####---------------------------------------------------------------------------#####


class MazeBoard(Board):
    def __init__(self, rows, cols):
        super().__init__(rows, cols)

    def loadBoard(self):
        for row in range(self.rows):
            self.matrix.append([])
            for col in range(self.cols):
                self.matrix[row].append(Node(row,col))#MazeNode(row, col))

    def loadMaze(self):
        maze = makeMaze((self.cols//2), (self.rows//2))
        maze_string = mazeString(maze, ("#", " "))

        file_out = open('map.txt', 'w')
        file_out.write(maze_string)
        file_out.close()

        file_in = open('map.txt', 'r')
        lines = file_in.readlines()

        for row in range(self.rows):
            for col in range(self.cols):
                if lines[row][col] == '#':
                    self.matrix[row][col].wall = True
        file_in.close()

    def initilize(self):
        self.loadBoard()
        self.setBorder()
        self.loadMaze()

    def userChoose(self):
        self.selectStartAndGoal()
        self.selectCheckpoints()
        self.start.wall = False
        self.goal.wall = False
        for i in range(len(self.checkpoints)):
            self.checkpoints[i].wall = False

####---------------------------------------------------------------------------#####

class ObsticleBoard(Board):
    def __init__(self, rows, cols, map):
        super().__init__(rows, cols)
        self.obstacleMap = map
        self.wallShape = 1 #1,2,3,4

    def selectObstacles(self):
        click = 0
        cont = True
        self.userSelect = 'w'
        selection = False
        opta = Button(D_GREEN,WIDTH-80, padding+190, 20, 20, "1" )
        optb = Button(D_GREEN,WIDTH-80, padding+220, 20, 20, "2" )
        optc = Button(D_GREEN,WIDTH-80, padding+250, 20, 20, "3" )
        optd = Button(D_GREEN,WIDTH-80, padding+280, 20, 20, "4" )
        wallBrush_txt = font.render("WallBrush",True, BLACK)                                                           
        while cont:
            for e in pygame.event.get():
                pos=pygame.mouse.get_pos()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if opta.isOver(pos):
                        self.wallShape = 1
                    elif optb.isOver(pos):
                        self.wallShape = 2
                    elif optc.isOver(pos):
                        self.wallShape = 3
                    elif optd.isOver(pos):
                        self.wallShape = 4

                if opta.isOver(pos):
                    opta.color = D_GREEN
                else:
                    opta.color = AQUA
                if optb.isOver(pos):
                    optb.color = D_GREEN
                else:
                    optb.color = AQUA
                if optc.isOver(pos):
                    optc.color = D_GREEN
                else:
                    optc.color = AQUA
                if optd.isOver(pos):
                    optd.color = D_GREEN
                else:
                    optd.color = AQUA
                    
                if e.type == pygame.MOUSEBUTTONDOWN:
                    selection = True
                if e.type == pygame.MOUSEBUTTONUP:
                    selection = False
                if selection:
                    x = (pos[0]-padding)//ppb
                    y = (pos[1]-padding)//ppb
                    if 0<x<self.cols and 0<y<self.rows:
                        if self.wallShape == 1:
                            self.matrix[y][x].wall = True
                        elif self.wallShape == 2 and 2<=y<self.rows-2 and 2<=x<self.cols-2:
                            self.matrix[y+1][x+1].wall = True
                            self.matrix[y][x+1].wall = True
                            self.matrix[y-1][x+1].wall = True
                            self.matrix[y+1][x-1].wall = True
                            self.matrix[y][x-1].wall = True
                            self.matrix[y-1][x-1].wall = True
                            self.matrix[y+1][x].wall = True
                            self.matrix[y-1][x].wall = True
                        elif self.wallShape == 3 and 2<=y<self.rows-2:
                            self.matrix[y+1][x].wall = True
                            self.matrix[y][x].wall = True
                            self.matrix[y-1][x].wall = True
                        elif self.wallShape == 4 and 2<=x<self.cols-2:
                            self.matrix[y][x+1].wall = True
                            self.matrix[y][x].wall = True
                            self.matrix[y][x-1].wall = True

                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.userSelect=None
                    cont = False
                display(self)
                opta.draw(screen)
                optb.draw(screen)
                optc.draw(screen)
                optd.draw(screen)
                pygame.display.update()
                


    def loadMap(self):
        file_in = open(self.obstacleMap, 'r')
        lines = file_in.readlines()
        # Returns a list with each line as an element.
        for row in range(self.rows):
            for col in range(self.cols):
                if lines[row][col] == '#':
                    self.matrix[row][col].wall = True
        file_in.close()

    def initilize(self):
        self.loadBoard()
        self.setBorder()
    
    def userChoose(self):
        self.selectStartAndGoal()
        self.selectCheckpoints()
        self.selectObstacles()
        self.initChildren()
        self.start.wall = False
        self.goal.wall = False
        for i in range(len(self.checkpoints)):
            self.checkpoints[i].wall = False



####---------------------------------------------------------------------------#####
# Other functions board funcs

def set_remove(set, current):
    for i, o in enumerate(set):
        if o.x == current.x and o.y == current.y:
            del set[i]
            return

