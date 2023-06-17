import pygame
from spieler import spieler
from spielfeld import feld
import sys
import math
from shop import shop


pygame.init()
class verwalter:
    
    def __init__(self):
        self.x_spieler_1 = 0
        self.x_spieler_2 = 0
        self.x_1 = 0
        self.x_2 = 0
        self.y_spieler_1 = 0
        self.y_spieler_2 = 0
        self.y_1 = 0
        self.y_2 = 0

        self.spieler_1_rechts = pygame.K_RIGHT
        self.spieler_1_links = pygame.K_LEFT
        self.spieler_1_oben= pygame.K_UP
        self.spieler_1_unten = pygame.K_DOWN


        self.spieler_2_rechts = pygame.K_d
        self.spieler_2_links = pygame.K_a
        self.spieler_2_oben = pygame.K_w
        self.spieler_2_unten = pygame.K_s

        
    def handle_mouse_button_events(self, event, buttons):  
            game_mode=0
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.left<=mouse_pos[0]<=button.rect.right and button.rect.top<=mouse_pos[1]<=button.rect.bottom:
                        if button.label == 'menue_button':
                            return 4
                        if button.label == 'play_local_button':
                            return 1
                        if button.label == 'play_lan_button':
                            return 2
                        if button.label == 'score_button':
                            return 4
                        button.img = button.pressed_img   
                        return game_mode   
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.img = button.unpressed_img



    def react_input(self, end, spieler_object, spieler_object_2, feld_obj_2, feld_obj, buttons):
        
        
        for event in pygame.event.get():
            game_mode=self.handle_mouse_button_events(event, buttons)
            if event.type == pygame.QUIT:
                end = True
                pygame.quit()
                sys.exit(0)                
            if event.type == pygame.KEYDOWN:
                
                if event.__dict__["key"] == self.spieler_1_rechts: #keycode von K_RIGHT
                    self.x_spieler_1 += 10
                    spieler_object.aktuelles_bild = spieler_object.spieler_img_rechts
                if event.__dict__["key"] == self.spieler_1_links: #keycode von K_LEFT
                    self.x_spieler_1 -= 10
                    spieler_object.aktuelles_bild = spieler_object.spieler_img_links 
                if event.__dict__["key"] == self.spieler_2_rechts: #keycode von K_d
                    self.x_spieler_2 += 10
                    spieler_object_2.aktuelles_bild = spieler_object_2.spieler_img_rechts
                if event.__dict__["key"] == self.spieler_2_links: #keycode von K_a
                    self.x_spieler_2 -= 10
                    spieler_object_2.aktuelles_bild = spieler_object_2.spieler_img_links
                
                #shop S1
                if event.__dict__["key"] == pygame.K_1: #keycode von K_1
                    print(shop.pruefen_ob_genug_punkte(spieler_object, event_nummer = 1))
                if event.__dict__["key"] == pygame.K_2: #keycode von K_2
                    pass
                if event.__dict__["key"] == pygame.K_3: #keycode von K_3
                    pass
                #shop S2
                if event.__dict__["key"] == pygame.K_KP1: #keycode von K_KP1
                    pass
                if event.__dict__["key"] == pygame.K_KP2: #keycode von K_KP2
                    pass
                if event.__dict__["key"] == pygame.K_KP3: #keycode von K_KP3
                    pass

                if event.__dict__["key"] == self.spieler_1_unten: #keycode von K_DOWN
                    self.y_spieler_1 += 10                   
                if event.__dict__["key"] == self.spieler_1_oben: #keycode von K_UP
                    self.y_spieler_1 -= 10                   
                if event.__dict__["key"] == self.spieler_2_unten: #keycode von K_s
                    self.y_spieler_2 += 10
                if event.__dict__["key"] == self.spieler_2_oben: #keycode von K_w
                    self.y_spieler_2 -= 10

                if event.__dict__["key"] == pygame.K_0:
                    return True                    
            if event.type == pygame.KEYUP:
                
                if (event.__dict__["key"] == self.spieler_1_rechts or  event.__dict__["key"] == self.spieler_1_links):
                    spieler_object.aktuelles_bild = spieler_object.spieler_img
                    self.x_spieler_1 = 0
                if (event.__dict__["key"] ==  self.spieler_2_links or  event.__dict__["key"] == self.spieler_2_rechts):
                    spieler_object_2.aktuelles_bild = spieler_object_2.spieler_img
                    self.x_spieler_2 = 0

            
                if (event.__dict__["key"] ==  self.spieler_1_oben or  event.__dict__["key"] == self.spieler_1_unten):
                    self.y_spieler_1 = 0
                    spieler_object.aktuelles_bild = spieler_object.spieler_img
                if (event.__dict__["key"] ==  self.spieler_2_unten or  event.__dict__["key"] == self.spieler_2_oben):
                    spieler_object_2.aktuelles_bild = spieler_object_2.spieler_img
                    self.y_spieler_2 = 0    
            
            if game_mode!=0 and isinstance(game_mode, int):
                    print(game_mode)
                    return game_mode
  



        if math.sqrt(self.x_spieler_1**2+self.y_spieler_1**2)!=0:
            spieler_object.aktueller_richtungsvektor=self.x_spieler_1, self.y_spieler_1
        if math.sqrt(self.x_spieler_2**2+self.y_spieler_2**2)!=0:
            spieler_object_2.aktueller_richtungsvektor=self.x_spieler_2, self.y_spieler_2
        
        spieler_object.x += self.x_spieler_1
        spieler_object_2.x += self.x_spieler_2 

        spieler_object.y += self.y_spieler_1
        spieler_object_2.y += self.y_spieler_2 


        
        if spieler_object_2.x > feld_obj_2.spielfeld_width + feld_obj_2.x - int(0.05*feld_obj_2.spielfeld_width):
            spieler_object_2.x = feld_obj_2.spielfeld_width + feld_obj_2.x -int(0.05*feld_obj_2.spielfeld_width)
        if spieler_object_2.x < feld_obj_2.x:
            spieler_object_2.x =feld_obj_2.x
        if spieler_object_2.y > feld_obj_2.spielfeld_height-int(0.05*feld_obj_2.spielfeld_width):
            spieler_object_2.y = feld_obj_2.spielfeld_height-int(0.05*feld_obj_2.spielfeld_width)
        if spieler_object_2.y < feld_obj_2.y:
            spieler_object_2.y =feld_obj_2.y  
            
        if spieler_object.x > feld_obj.x + feld_obj.spielfeld_width-int(0.05*feld_obj_2.spielfeld_width):
            spieler_object.x = feld_obj.x + feld_obj.spielfeld_width-int(0.05*feld_obj_2.spielfeld_width)
        if spieler_object.x < feld_obj.x: #stinks
            spieler_object.x = feld_obj.x
        if spieler_object.y > feld_obj.spielfeld_height-int(0.05*feld_obj_2.spielfeld_width):
            spieler_object.y = feld_obj.spielfeld_height-int(0.05*feld_obj_2.spielfeld_width)
        if spieler_object.y < feld_obj.y:
            spieler_object.y =feld_obj.y  
        ''' 
            
        if spieler_object.x > feld_obj_2.spielfeld_width - spieler_object.size: 
            spieler_object.x = feld_obj_2.spielfeld_width - spieler_object.size     
        if spieler_object.x < feld_obj_2.x:
            spieler_object.x = feld_obj_2.x 
        if spieler_object.y > feld_obj_2.spielfeld_height - spieler_object.size:
            spieler_object.y = feld_obj_2.spielfeld_height - spieler_object.size
        if spieler_object.y < feld_obj_2.y: 
            spieler_object.y = feld_obj_2.y
            
        if spieler_object_2.x > feld_obj.spielfeld_width + feld_obj.x - spieler_object_2.size: 
            spieler_object_2.x = feld_obj.spielfeld_width + feld_obj.x - spieler_object_2.size     
        if spieler_object_2.x < feld_obj.x:
            spieler_object_2.x = feld_obj.x 
        if spieler_object_2.y > feld_obj.spielfeld_height - spieler_object_2.size:
            spieler_object_2.y = feld_obj.spielfeld_height - spieler_object_2.size
        if spieler_object_2.y < feld_obj.y: 
            spieler_object_2.y = feld_obj.y
        '''
        spieler_object.mittelpunkt= [spieler_object.x+0.5*spieler_object.size, spieler_object.y+0.625*spieler_object.size]   
        spieler_object_2.mittelpunkt= [spieler_object_2.x+0.5*spieler_object_2.size, spieler_object_2.y+0.625*spieler_object_2.size]                          
            
