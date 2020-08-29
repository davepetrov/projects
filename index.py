#!/usr/bin/python3
#--------------------#
# MAIN PAGE [RUN THIS]
#    Includes
#         -sortByDistance()
#         -findGoalPath()
#         -A_StartCP()
#--------------------#
# David Petrov
# Completed April 29, 2020 Through May 3, 2020
# A* Pathfinding algorithm Visualizer
#--------------------#

from time import sleep
from board import Board, MazeBoard, RandomBoard, ObsticleBoard, set_remove
import pygame
from display import *
from button import Button
from interactive import interactive
pygame.init()


def sortcp(origin, checkpoints, newcheckpoints=[]):
    '''
    Returns checkpoints in sorted order based on distance starting with the origin

    Node, List(Node), List -> List(Node)

    '''
    if len(checkpoints)==0:
        return checkpoints
    distances={}
    
    for i in checkpoints:
        dist = pow(i.x-origin.x, 2) + pow(i.y-origin.y, 2)
        distances[i]=dist

    origin = min(distances.keys(), key=(lambda k: distances[k])) #New origin is the node with the smallest dist from the previous origin

    newcheckpoints.append(origin)
    checkpoints.remove(origin)
    sortcp(origin, checkpoints, newcheckpoints)
    return newcheckpoints


# The last path
# This is called when the path has already passed the last checkpoint or if there are no checkpoints
def findGoalPath(b, winner, currentOpenSet, currentClosedSet):
    for i in range(len(b.openSet)):
        if b.openSet[i].f < b.openSet[winner].f:
            winner = i
    b.current = b.openSet[winner]
    # Check if we are at the goal node
    if b.current.isGoal(b): 
        b.finish = True
        b.act = "done"
        temp  = b.current 
        b.path.append(temp)
        b.paths.extend(b.path)
        b.path = b.paths
        print("Path found")
        return True

    # In the proccess of finding the goal node
    set_remove(b.openSet, b.current)
    currentClosedSet.append(b.current);
    neighbors = b.current.neighbors
    
    for i in range(len(neighbors)):
        neighbor = neighbors[i]
        newPath = False
        if neighbor not in currentClosedSet and not neighbor.wall:
            temp_g = b.current.g + 1

            if neighbor in b.openSet:
                if temp_g < neighbor.g: 
                    neighbor.g = temp_g
                    newPath = True
            else:
                neighbor.g = temp_g
                b.openSet.append(neighbor)
                newPath = True
            
            if newPath:
                neighbor.h = neighbor.heuristic(b.goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.previous=b.current  

def A_starCP(b):
    cp = 0
    skip=False
    skip_b = Button(GOLD, WIDTH-100, HEIGHT-30, 90, 20, text="Fast Forward")
    b.checkpoints = sortcp(b.start, b.checkpoints, []) #first reference point - b.start
    while len(b.openSetsCP[cp])>0:
        b.act = 'work'
        winner = 0
        currentOpenSet = b.openSetsCP[cp]
        currentClosedSet = b.closedSetCP[cp]
        if len(b.openSetsCP)>1:
            if cp < len(b.checkpoints):
                for i in range(len(currentOpenSet)):
                    if currentOpenSet[i].f < currentOpenSet[winner].f:
                        winner = i
                b.current = currentOpenSet[winner]
                
                #Found the closest checkpint
                if b.current.isCP(b.checkpoints[cp]): 
                    b.currentCP +=1
                    b.checkpointsFound[cp] = True
                    b.current.previous=None

                    cp+=1
                    b.paths.extend(b.path)
                    b.openSetsCP[cp][0] = b.current
                    b.openSet = b.openSetsCP[cp]
                    b.closedSetCP.append([])
                    print("CP FOUND")

                
                #If the the processes of finding the next checkpoint    
                else:

                    #Remove the current node from the open set
                    #Mark the node as visited
                    #Update the list of neighbors of the current node
                    set_remove(currentOpenSet, b.current)
                    currentClosedSet.append(b.current)
                    neighbors = b.current.neighbors
                    
                    #Look through the neigbors
                    for i in range(len(neighbors)):
                        neighbor = neighbors[i]
                        newPath = False
                    
                        if neighbor not in currentClosedSet and not neighbor.wall:
                            temp_g = b.current.g + 1

                            if neighbor in currentOpenSet:
                                # if the exact cost from the neigbor node from the cp is -
                                # less than the current node, update it's exact cost (g)
                                if temp_g < neighbor.g:
                                    neighbor.g = temp_g
                                    newPath = True
                                    
                            else:
                                neighbor.g = temp_g
                                currentOpenSet.append(neighbor)
                                newPath = True
                            
                            if newPath:
                                #New path has been chosen
                                #Update the estimated cost from the neigbor's node to the checkpoint 
                                neighbor.h = neighbor.heuristic(b.checkpoints[cp])
                                neighbor.f = neighbor.g + neighbor.h
                                neighbor.previous=b.current 


            else:
                if findGoalPath(b, winner, currentOpenSet,currentClosedSet): return
        else:
            if findGoalPath(b, winner, currentOpenSet, currentClosedSet): return

        b.path = []
        temp  = b.current 
        b.path.append(temp)
        while temp.previous:
            b.path.append(temp.previous)
            temp = temp.previous
            
        #Check if user fastforwards
        for e in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if skip_b.isOver(pos): 
                skip_b.color= ORANGE
                if e.type == pygame.MOUSEBUTTONDOWN:
                    skip = True
                    skip_b.color= D_ORANGE
            else:
                skip_b.color=GOLD
        
        if not skip:
            display_l(b)
            skip_b.draw(screen)
            pygame.display.update()
    else:
        print("No Solution")

    display(b)

def main():
    b=Board(rows,cols)
    b.initilize()
    
    while True:
        b = interactive(b)
        A_starCP(b)
        b.finish = False

    pygame.quit()
    sys.exit()

main()
