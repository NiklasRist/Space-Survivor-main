import sys
import pygame
from spieler import spieler
from spielfeld import feld
from taste import verwalter



pygame.init()
class gui:
  
  
  def __init__(self, feld_obj_2):
    gui.lost_font_text = pygame.font.SysFont('arial',200)
    gui.lifeFont = pygame.font.SysFont('Verdana',400)
    gui.spiel_fenster = pygame.display.set_mode([2*feld_obj_2.spielfeld_width,feld_obj_2.spielfeld_height])

  def create_fenster(self):
    white = (255,255,255) 
    pygame.display.set_caption("Space survior")

  def display_text(self, px, py, text, color, size):
    font = pygame.font.SysFont("arial", size)
    img = font.render(text, True, color)
    self.spiel_fenster.blit(img, (px, py))
    

  def display(self, obj): 
    self.spiel_fenster.blit(obj.aktuelles_bild, (obj.x,obj.y))

  def fill(self, color):
    self.spiel_fenster.fill(color)
 