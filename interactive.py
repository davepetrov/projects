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
    showSlider =False
    opta = Button(GREEN,padding, 10, 70, 30, "MAZE" )
    optb = Button(GREEN,padding+80, 10, 70, 30, "RANDOM" )
    optc = Button(GREEN,padding+160, 10, 70, 30, "CREATIVE" )
    optd = Button(GREEN,padding+240, 10, 70, 30, "BASIC" )
    optStart = Button(GREEN,WIDTH-100, 10, 70, 30, "Start" )
    optClear = Button(D_VIOLET,WIDTH-180, 10, 70, 30, "Clear" )
    optRestart = Button(D_VIOLET,WIDTH-260, 10, 70, 30, "Restart" )
    slider = Slider(padding+320, 10, 140, 20, 100)
    currentSelect = None

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
                    showSlider = False
                    userPick = True
                    possibleStart = False
                    boardCleared = False
                    currentSelect = "maze"
                    b = MazeBoard(rows, cols)
                    print("maze")

                elif optb.isOver(pos):
                    showSlider = True
                    userPick = False
                    possibleStart = False
                    print("random")

                elif optc.isOver(pos):
                    showSlider = False
                    userPick = True
                    possibleStart = False
                    boardCleared = False
                    b = ObsticleBoard(rows, cols, 'map51x51.txt')
                    print("creative")

                elif optd.isOver(pos):
                    showSlider = False
                    userPick = True
                    possibleStart = False
                    boardCleared = False
                    b = Board(rows, cols)
                    print("basic")

                elif optClear.isOver(pos):
                    b.clear()
                    possibleStart = False
                    possibleRestart = False
                    userPick = False
                    boardCleared = True
                
                elif optRestart.isOver(pos):
                    if possibleRestart and not boardCleared:
                        b.restart()
                        possibleStart = True
                    else:
                        possibleStart = False

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
                slider.draw(screen)
                if slider.isOver(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                    selection = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    selection = False

                if selection:
                    slider.setValueByMousePos(pos[0])
                    if 0<=slider.value<30:
                        recommended_text = font1.render('Recommended value',True, GREEN)     
                    else:
                        recommended_text = font1.render('Recommended [0,30]',True, RED)
                    screen.blit(recommended_text, (padding+320, 30)) 
                    slider.draw(screen)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    b = RandomBoard(rows, cols, slider.value)
                    boardCleared = False
                    userPick = True
                    selection = False

            if userPick and not possibleStart:
                b.initilize()
                print(b.start.x)
                b.act = 'choose'
                b.userChoose()
                possibleStart = True
                possibleRestart = False

            if possibleStart and not boardCleared and b.start.x:
                optStart.color = GREEN
                if optStart.isOver(pos) :
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print('Start! based off' ,b)
                        b.initChildren() 
                        possibleRestart = False
                        return b
                else:
                    optStart.color = D_GREEN
            else:
                optStart.color = L_RED

            opta.draw(screen)
            optb.draw(screen)
            optc.draw(screen)
            optd.draw(screen)
            optStart.draw(screen)
            optClear.draw(screen)
            optRestart.draw(screen)
            pygame.display.update()