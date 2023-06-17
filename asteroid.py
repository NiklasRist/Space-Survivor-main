import pygame
from spielfeld import feld
import random
pygame.init()
clock = pygame.time.Clock()



class asteroid:
    '''Asteroiden die mit dem Spieler kollidieren können'''

    def __init__(self, feld_obj_2):
        self.G_leben = 4
        self.side=feld_obj_2.side
        self.x = 0+feld_obj_2.x
        self.size=int(0.0375*feld_obj_2.spielfeld_width)
        if random.randint(0,1)==1: #entscheidet von welcher Seite der Asteroid kommt
            self.x+=feld_obj_2.spielfeld_width-self.size
        self.y = random.randint(0, feld_obj_2.spielfeld_height-self.size)
        self.mittelpunkt=[self.x+0.5*self.size, self.y+0.5*self.size]
        self.asteroid_img = pygame.image.load(r".\images\asteroid-01.png")
        self.asteroid_img = pygame.transform.scale(self.asteroid_img, (self.size, self.size))
        self.aktuelles_bild=self.asteroid_img
        self.schaden=1
        

    
    



    

        
    
    
    
    


    
    
    
    
