#!/usr/bin/python3
import pygame
import display
pygame.init()

class Button():
    def __init__(self, color, x,y,w,h, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    def draw(self,screen,outline=None):
        #Call this method to draw the button
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.w+4,self.h+4),5)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.w,self.h),0)
        if self.text != '':
            font = pygame.font.SysFont('rainyhearts', 15)
            text = font.render(self.text, 1, (255,255,255))
            screen.blit(text, (self.x + (self.w/2 - text.get_width()/2), self.y + (self.h/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
            
        return False
