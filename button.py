import sys
import pygame

class button():

    def __init__(self, x, y, width, height, unpressed_img, pressed_img, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.unpressed_img = unpressed_img
        self.pressed_img = pressed_img
        self.img = self.unpressed_img
        self.label = label

    def draw(self, screen):
        screen.spiel_fenster.blit(self.img, self.rect)
        
