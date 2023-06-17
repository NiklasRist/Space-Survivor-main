import pygame
from spielfeld import feld
import random

pygame.init()


class gegner():
    

    def __init__(self, feld_obj_2):


        self.leben = 1
        self.size=int(0.05*feld_obj_2.spielfeld_width)
        self.schaden = 1
        

        self.gegner_img = pygame.image.load(".\images\gegner.png") 
        self.gegner_img = pygame.transform.scale(self.gegner_img, (self.size, self.size))
        self.aktuelles_bild=self.gegner_img
        #bestimmt von wo bis wo in x ache der Gegener kommen darf
        self.x = random.randrange(0,feld_obj_2.spielfeld_width)
        self.y = -500
        self.gegner_speed = 8
        self.mittelpunkt=[int(self.x+(34/64)*self.size), int(self.y+(44/64)*self.size)]


        
        self.side = feld_obj_2.side





