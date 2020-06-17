#--------------------#
#!/usr/bin/python3
# DISPLAY PAGE
#    Includes
#         -display()
#--------------------#

import pygame
import sys
from node import *
from time import sleep
pygame.init()

# note: Maze version only works when cols and row are odd [BUG]
cols = 61
rows = 31
ppb = 15           # Pixels Per Block

# Colours
ORANGE = (240, 94, 35)
GREEN = (0, 255, 0)
D_GREEN = (0, 200, 0)
GOLD = (255, 191, 0)
AQUA = (102, 221, 170)
L_AQUA = (127, 255, 212)
L2_AQUA = (127, 255, 169)
D_AQUA = (26, 101, 101)
L_RED = (255, 0, 0)
RED = (166, 25, 25)
WHITE = (255, 255, 255)
BLACK = (153, 76, 0)
AMBER = (255, 213, 0)
VIOLET = (185, 139, 231)
D_VIOLET = (185-30, 139-30, 231-30)

PATHSHADE1 = (221, 105, 242)
PATHSHADE2 = (224, 117, 219)
PATHSHADE3 = (227, 130, 196)
PATHSHADE4 = (231, 143, 173)
PATHSHADE5 = (234, 155, 151)
PATHSHADE6 = (238, 168, 128)
PATHSHADE7 = (244, 193, 83)
PATHSHADE8 = (248, 206, 60)


# Display
padding = 50
WIDTH = padding+cols*ppb+100
HEIGHT = padding*2+rows*ppb

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# fonts/text

font = pygame.font.Font('rainyhearts.ttf', 20)
font1 = pygame.font.Font('rainyhearts.ttf', 15)
font2 = pygame.font.Font('rainyhearts.ttf', 30)
action = font.render(None, True, BLACK)


def display_l(b):
    global action
    global textTect
    global screen

    screen.fill(WHITE)
    for row in range(b.rows):
        for col in range(b.cols):
            node = b.matrix[row][col]

            # Draw open/closed sets
            for cpSet in b.openSetsCP:
                if node in cpSet:
                    pygame.draw.rect(screen, AQUA, [padding+col*ppb, padding+row*ppb, ppb, ppb])
            if node in b.openSet:
                pygame.draw.rect(screen, L2_AQUA, [padding+col*ppb, padding+row*ppb, ppb, ppb])
            for cpSet in b.closedSetCP:
                if node in cpSet:
                    pygame.draw.rect(screen, VIOLET, [padding+col*ppb, padding+row*ppb, ppb, ppb])

            # Draw path
            if node in b.paths:
                pygame.draw.rect(screen, GOLD, [padding+col*ppb, padding+row*ppb, ppb, ppb])

                # Draw finished path
                if b.finish:
                    pygame.draw.rect(screen, AMBER, [padding+col*ppb, padding+row*ppb, ppb, ppb])

            if node in b.path and node != b. currentCP:
                pygame.draw.rect(
                    screen, GOLD, [padding+col*ppb, padding+row*ppb, ppb, ppb])
                if b.current != None:
                    if node == b.current:
                        pygame.draw.rect(screen, VIOLET, [padding+col*ppb, padding+row*ppb, ppb, ppb])
                    # TODO: Fix this[INEFFICIENT]
                    elif b.current.previous != None:
                        if node == b.current.previous:
                            pygame.draw.rect(screen, PATHSHADE1, [padding+col*ppb, padding+row*ppb, ppb, ppb])
                        elif b.current.previous.previous != None:
                            if node == b.current.previous.previous:
                                pygame.draw.rect(screen, PATHSHADE2, [padding+col*ppb, padding+row*ppb, ppb, ppb])
                            elif b.current.previous.previous.previous != None:
                                if node == b.current.previous.previous.previous:
                                    pygame.draw.rect(screen, PATHSHADE3, [padding+col*ppb, padding+row*ppb, ppb, ppb])
                                elif b.current.previous.previous.previous.previous != None:
                                    if node == b.current.previous.previous.previous.previous:
                                        pygame.draw.rect(screen, PATHSHADE4, [ padding+col*ppb, padding+row*ppb, ppb, ppb])
                                    elif b.current.previous.previous.previous.previous.previous != None:
                                        if node == b.current.previous.previous.previous.previous.previous:
                                            pygame.draw.rect(screen, PATHSHADE5, [padding+col*ppb, padding+row*ppb, ppb, ppb])
                                        elif b.current.previous.previous.previous.previous.previous.previous != None:
                                            if node == b.current.previous.previous.previous.previous.previous.previous:
                                                pygame.draw.rect(screen, PATHSHADE6, [padding+col*ppb, padding+row*ppb, ppb, ppb])
                                            elif b.current.previous.previous.previous.previous.previous.previous.previous != None:
                                                if node == b.current.previous.previous.previous.previous.previous.previous.previous:
                                                    pygame.draw.rect(screen, PATHSHADE7, [padding+col*ppb, padding+row*ppb, ppb, ppb])
                                                elif b.current.previous.previous.previous.previous.previous.previous.previous.previous != None:
                                                    if node == b.current.previous.previous.previous.previous.previous.previous.previous.previous:
                                                        pygame.draw.rect(screen, PATHSHADE8, [padding+col*ppb, padding+row*ppb, ppb, ppb])
            else:
                pygame.draw.ellipse(screen, WHITE, [padding+col*ppb, padding+row*ppb, ppb, ppb])

            # Draw nodes
            if node in b.checkpoints:
                pygame.draw.ellipse(screen,  BLACK, [padding+col*ppb, padding+row*ppb, ppb, ppb])
            elif node == b.start:
                pygame.draw.ellipse(screen, ORANGE, [padding+col*ppb, padding+row*ppb, ppb, ppb])
            elif node == b.goal:
                pygame.draw.ellipse(screen, RED, [padding+col*ppb, padding+row*ppb, ppb, ppb])
            elif node != None and node.wall:
                pygame.draw.rect(screen, D_AQUA, [padding+col*ppb, padding+row*ppb, ppb, ppb])

            elif node == b.current:
                pygame.draw.ellipse(screen, VIOLET, [padding+col*ppb, padding+row*ppb, ppb, ppb])

            # Draw Node selection interface
            if b.userSelect == 's':
                choose = font.render("Start", True, D_AQUA)
                screen.blit(choose, (WIDTH-55, padding+40))
                pygame.draw.ellipse(screen, ORANGE, [WIDTH-80, padding+40, 20, 20])
            elif b.userSelect == 'g':
                choose = font.render("Goal", True, D_AQUA)
                screen.blit(choose, (WIDTH-55, padding+80))
                pygame.draw.ellipse(screen, RED, [WIDTH-80, padding+80, 20, 20])
            elif b.userSelect == 'cp':
                choose = font.render("CP", True, D_AQUA)
                screen.blit(choose, (WIDTH-55, padding+120))
                pygame.draw.ellipse(screen, BLACK, [WIDTH-80, padding+120, 20, 20])
            elif b.userSelect == 'w':
                choose = font.render("Wall", True, D_AQUA)
                screen.blit(choose, (WIDTH-55, padding+160))
                pygame.draw.rect(screen, D_AQUA, [WIDTH-80, padding+160, 20, 20])

            bigtextX = WIDTH//2-100
            bigtextY = HEIGHT-40
            # Draw action of the user.
            # work: Pathfinding
            if b.act == 'work':
                if len(b.openSetsCP) > 1:
                    if b.currentCP < len(b.openSetsCP):
                        currentCP = font.render(
                            "Looking for CP #"+str(b.currentCP), True, BLACK)
                    else:
                        currentCP = font.render("Looking for Goal", True, RED)
                    screen.blit(currentCP, (padding, HEIGHT-35))

            # fail: Unable to find a path to goal/ readh every checkpoint
            elif b.act == 'fail':
                action = font2.render('Fail: There exists no path to read every node selection', True, RED)
            # done: Path found
            elif b.act == 'done':
                action = font2.render('Path found: Completed!', True, RED)

            # generating: Map generation ensues
            elif b.act == "generating":
                action = font2.render('Generating Map...', True, GOLD)

            # choose: User selects board mode
            if b.act == 'choose':
                choose = font2.render('User Selection', True, D_AQUA)
                screen.blit(choose, (bigtextX, bigtextY))

            screen.blit(action, (bigtextX, bigtextY))


def display(b):
    display_l(b)
    pygame.display.update()