import pygame
class projektil:
    '''In der Klasse Projektil sind die Attribute die für die Projektilobjekte benötigt werden.'''
    def __init__(self, x, y, feld_obj_2, schuetze_obj, richtungsvektor) -> None:
        self.x=x
        self.y=y
        self.size=int(0.0125*feld_obj_2.spielfeld_width)
        self.mittelpunkt=[self.x+0.5*self.size, self.y+0.5*self.size]
        self.side=feld_obj_2.side
        self.image=pygame.image.load(".\images\projectile_normal.png")
        self.image=pygame.transform.scale(self.image, (self.size, self.size))
        self.aktuelles_bild=self.image
        self.schuetze=schuetze_obj
        self.richtungsvektor=richtungsvektor
        
        