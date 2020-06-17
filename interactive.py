#!/usr/bin/python3
#--------------------#
# INTERACTIVE PAGE
#--------------------#

from board import *
import pygame
from display import *
from button import Button
from slider import Slider


def interactive(b):
    exit = False
    userPick = False
    possibleStart = False
    possibleRestart = False
    boardCleared = False
    showSlider = False
    #Initialize all buttons
    opta = Button(GREEN, padding, 10, 70, 30, "MAZE")
    optb = Button(GREEN, padding+80, 10, 70, 30, "RANDOM")
    optc = Button(GREEN, padding+160, 10, 70, 30, "CREATIVE")
    optd = Button(GREEN, padding+240, 10, 70, 30, "BASIC")
    optStart = Button(GREEN, WIDTH-100, 10, 70, 30, "Start")
    optClear = Button(D_VIOLET, WIDTH-180, 10, 70, 30, "Clear")
    optRestart = Button(D_VIOLET, WIDTH-260, 10, 70, 30, "Restart")
    slider = Slider(padding+320, 10, 140, 20, 100)
    b.act="choose"
    while not exit:
        possibleRestart = True
        screen.fill(WHITE)
        display_l(b)
        selection = False
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if opta.isOver(pos):
                    # User selected maze board
                    showSlider = False
                    userPick = True
                    possibleStart = False
                    boardCleared = False
                    b = MazeBoard(rows, cols)

                elif optb.isOver(pos):
                    #User selected random board
                    showSlider = True
                    userPick = False
                    possibleStart = False

                elif optc.isOver(pos):
                    #User selected creative board
                    showSlider = False
                    userPick = True
                    possibleStart = False
                    boardCleared = False
                    b = ObsticleBoard(rows, cols, 'map51x51.txt')

                elif optd.isOver(pos):
                    #User selected basic board
                    showSlider = False
                    userPick = True
                    possibleStart = False
                    boardCleared = False
                    b = Board(rows, cols)

                elif optClear.isOver(pos):
                    #User cleared board
                    b.clear()
                    possibleStart = False
                    possibleRestart = False
                    userPick = False
                    boardCleared = True

                elif optRestart.isOver(pos):
                    # User restarted board
                    # None of the nodes are removed 
                    # (The path is cleared only for the user to replay the animation)
                    if possibleRestart and not boardCleared:
                        b.restart()
                        #User will be able to start the path finding
                        possibleStart = True
                    else:
                        possibleStart = False

            #Change colour of button on mouse hover
            if opta.isOver(pos):
                opta.color = GREEN
            else:
                opta.color = AQUA
            if optb.isOver(pos):
                optb.color = GREEN
            else:
                optb.color = AQUA
            if optc.isOver(pos):
                optc.color = GREEN
            else:
                optc.color = AQUA
            if optd.isOver(pos):
                optd.color = GREEN
            else:
                optd.color = AQUA
            if optClear.isOver(pos):
                optClear.color = VIOLET
            else:
                optClear.color = D_VIOLET
            if optRestart.isOver(pos) and possibleRestart:
                optRestart.color = VIOLET
            else:
                optRestart.color = D_VIOLET

            
            if showSlider and not possibleStart:
                #Draw slider if board is random
                slider.draw(screen)
                if slider.isOver(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                    selection = True

                if event.type == pygame.MOUSEBUTTONUP:
                    selection = False

                if selection:
                    slider.setValueByMousePos(pos[0])
                    #Display recommended value of random wall spawn rate
                    #Lower -> Less walls, Higher -> More walls
                    if 0 <= slider.val < 30:
                        recommended_text = font1.render('Recommended value', True, GREEN)
                    else:
                        recommended_text = font1.render('Recommended [0,30]', True, RED)
                    screen.blit(recommended_text, (padding+320, 30))
                    slider.draw(screen)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    #In case of user presses space, selection is over
                    b = RandomBoard(rows, cols, slider.val)
                    boardCleared = False
                    userPick = True
                    selection = False

            if userPick and not possibleStart:
                b.initilize()
                b.act = 'choose'
                b.userChoose()
                possibleStart = True
                possibleRestart = False

            if possibleStart and not boardCleared and b.start.x:
                #User has option to start the Pathfinding
                optStart.color = GREEN
                if optStart.isOver(pos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        b.initChildren()
                        possibleRestart = False
                        return b
                else:
                    optStart.color = D_GREEN
            else:
                optStart.color = L_RED

            # Draw board options
            opta.draw(screen)
            optb.draw(screen)
            optc.draw(screen)
            optd.draw(screen)
            if possibleStart:
                optStart.draw(screen, (0,150,0))
            else:
                optStart.draw(screen, (150,0,0))
            optClear.draw(screen)
            optRestart.draw(screen)
            pygame.display.update()
