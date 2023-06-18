import sys
import pygame
import math
import pygame_gui
from gui import gui
from spieler import spieler
from shop import shop
from asteroid import asteroid
from event import event
from spielfeld import feld
from taste import verwalter
from leaderboard import leaderboard
from speicher import speicher
from projektil import projektil
from kollisionspolygone import spieler_polygon, asteroid_polygon, projektil_polygon, enemy_polygon
from gegner import gegner
from button import button
import os
from lan_communication import lan_communication as l_c



class steuerung():
    def __init__(self):
        pygame.init()
        self.l_c=l_c()
        self.server_erstellt=False
        self.client_erstellt=False
        self.i_am_server=False
        self.clock = pygame.time.Clock()
        self.spielfeld_1 = feld(0,0,0)
        self.spielfeld_2 = feld(self.spielfeld_1.spielfeld_width,0,1)
        self.background=pygame.transform.scale(self.spielfeld_1.aktuelles_bild, (self.spielfeld_1.spielfeld_width*2, self.spielfeld_1.spielfeld_height))
        self.leaderboard_background=pygame.transform.scale(pygame.image.load("images\leaderboard_background.png"),(1.6*self.spielfeld_1.spielfeld_width, 0.8*self.spielfeld_1.spielfeld_height))
        self.gui_1 = gui(self.spielfeld_1)
        self.shop_1 = shop()
        self.event_1 = event()
        self.spieler_1 = spieler((0.5*self.spielfeld_1.spielfeld_width), (self.spielfeld_1.spielfeld_height*0.5), self.spielfeld_1)
        self.spieler_1_collision_polygon=spieler_polygon()
        self.init_polygon(self.spieler_1, self.spieler_1_collision_polygon)
        self.spieler_2 = spieler((1.5*self.spielfeld_2.spielfeld_width), (self.spielfeld_2.spielfeld_height*0.5), self.spielfeld_2)
        self.spieler_2_collision_polygon=spieler_polygon()
        self.init_polygon(self.spieler_2, self.spieler_2_collision_polygon)
        self.taste_1 = verwalter()
        self.leaderboard_1 = leaderboard()
        self.speicher_1 = speicher()
        self.speicher_1.create_table()
        self.saved_leaderboard=self.speicher_1.load_entries()
        for entry in self.saved_leaderboard:
            self.leaderboard_1.addToBoard(entry[0], entry[1])
        self.projektile=[]
        self.projektil_polygone=[]
        self.gegner=[]
        self.gegner_polygon= []
        self.end = False 
        self.game_mode=0 #0=Main Menu, 1=lokaler Mehrspieler, 2=LAN Mehrspieler, 3=Optionen
        self.spiel_start=True
        self.asteroiden=[]
        self.asteroiden_polygon=[] 
        self.maximale_asteroiden_anzahl=15
        self.maximale_projektil_anzahl=30
        self.count=0
        self.text_size=int(34*(self.spielfeld_1.spielfeld_width/800))
        
        self.menue_image = pygame.transform.scale(pygame.image.load(r'.\images\buttons\b_menue.png').convert_alpha(),(0.16*self.spielfeld_1.spielfeld_width,0.04*self.spielfeld_1.spielfeld_height))
        self.menue_p_image = pygame.transform.scale(pygame.image.load(r'.\images\buttons\b_menue_pressed.png').convert_alpha(),(0.16*self.spielfeld_1.spielfeld_width,0.04*self.spielfeld_1.spielfeld_height))

        self.play_lan_image = pygame.transform.scale(pygame.image.load(r'.\images\buttons\b_play_lan.png').convert_alpha(),(0.16*self.spielfeld_1.spielfeld_width,0.04*self.spielfeld_1.spielfeld_height))
        self.play_lan_p_image = pygame.transform.scale(pygame.image.load(r'.\images\buttons\b_play_lan_pressed.png').convert_alpha(),(0.16*self.spielfeld_1.spielfeld_width,0.04*self.spielfeld_1.spielfeld_height))

        self.play_local_image = pygame.transform.scale(pygame.image.load(r'.\images\buttons\b_play_local.png').convert_alpha(),(0.16*self.spielfeld_1.spielfeld_width,0.04*self.spielfeld_1.spielfeld_height))
        self.play_local_p_image = pygame.transform.scale(pygame.image.load(r'.\images\buttons\b_play_local_pressed.png').convert_alpha(),(0.16*self.spielfeld_1.spielfeld_width,0.04*self.spielfeld_1.spielfeld_height))

        self.score_image = pygame.transform.scale(pygame.image.load(r'.\images\buttons\b_score.png').convert_alpha(),(0.16*self.spielfeld_1.spielfeld_width,0.04*self.spielfeld_1.spielfeld_height))
        self.score_p_image = pygame.transform.scale(pygame.image.load(r'.\images\buttons\b_score_pressed.png').convert_alpha(),(0.16*self.spielfeld_1.spielfeld_width,0.04*self.spielfeld_1.spielfeld_height))


        self.feld_steuer = pygame_gui.UIManager((int(self.spielfeld_1.spielfeld_width),self.spielfeld_1.spielfeld_height))
        self.spieler1_name_input = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((400,300),(800,100)),manager = self.feld_steuer,object_id="#Spieler_1_Name:" )
        self.spieler2_name_input = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((800,600),(400,200)),manager = self.feld_steuer,object_id="#Spieler_2_Name:" )

        self.name_hintergrund = pygame.image.load(r'.\images\leaderboard_background.png')

        self.font = pygame.font.Font(None, 32)
        self.name_hintergrund = pygame.image.load(r'.\images\leaderboard_background.png')
        self.aktive_input= None
        self.white =  (255, 255, 255)
        self.black = (0, 0, 0)
        self.spieler_name_1 = ""
        self.spieler_name_2 = ""


        self.buttons = [
            button((self.spielfeld_1.spielfeld_width-0.16*self.spielfeld_1.spielfeld_width), 0.125*self.spielfeld_1.spielfeld_height, 0.16*self.spielfeld_1.spielfeld_width, 0.02*self.spielfeld_1.spielfeld_height, self.menue_image, self.menue_p_image, 'menue_button'),
            button((self.spielfeld_1.spielfeld_width-0.16*self.spielfeld_1.spielfeld_width), 0.25*self.spielfeld_1.spielfeld_height, 0.16*self.spielfeld_1.spielfeld_width, 0.02*self.spielfeld_1.spielfeld_height, self.play_lan_image, self.play_lan_p_image, 'play_lan_button'),
            button((self.spielfeld_1.spielfeld_width-0.16*self.spielfeld_1.spielfeld_width), 0.375*self.spielfeld_1.spielfeld_height, 0.16*self.spielfeld_1.spielfeld_width, 0.02*self.spielfeld_1.spielfeld_height, self.play_local_image, self.play_local_p_image, 'play_local_button'),
            button((self.spielfeld_1.spielfeld_width-0.16*self.spielfeld_1.spielfeld_width), 0.5*self.spielfeld_1.spielfeld_height, 0.16*self.spielfeld_1.spielfeld_width, 0.02*self.spielfeld_1.spielfeld_height, self.score_image, self.score_p_image, 'score_button')
        ]
        self.main_loop()
        
    def init_polygon(self, obj, col_pol_obj) -> None:
        '''Rescaled und verschiebt das Polygon.'''
        col_pol_obj.rescale_polygon(obj.size)
        col_pol_obj.move_polygon([obj.mittelpunkt[0]-col_pol_obj.mittelpunkt[0], obj.mittelpunkt[1]-col_pol_obj.mittelpunkt[1]])
    def move_polygon(self, obj, col_pol_obj):
        col_pol_obj.move_polygon([obj.mittelpunkt[0]-col_pol_obj.mittelpunkt[0], obj.mittelpunkt[1]-col_pol_obj.mittelpunkt[1]])
    def main_loop(self):
        '''
            Enthält die Mainloop. Hier wird das Bild aktualisiert und die FPS werden festgelegt. Über die gamemode Variable kann man zwischen verschiedenen Bildschirmen hin- und herschalten.
        '''
        self.gui_1.create_fenster()
        while not self.end:
            if self.game_mode==0:
                self.main_menue()
            elif self.game_mode==1:
                self.lokaler_mehrspieler()
            elif self.game_mode==2:
                self.lan_mehrspieler()
            elif self.game_mode==3:
                self.optionen()
            elif self.game_mode==4:
                self.game_over_screen()
                #self.game_mode=1
            elif self.game_mode==5:
                self.spieler_namen()
                self.namen_anzeigen()
            else:
                self.game_mode=0
            
            pygame.display.flip()
            self.clock.tick(60)                 
            
    def game_over_screen(self):
        '''In Arbeit'''
        self.update_screen_4()
        
        #bei null: zurück zu main menu
        if isinstance(self.taste_1.react_input(self.end, self.spieler_2, self.spieler_1, self.spielfeld_2, self.spielfeld_1, self.buttons ), bool):
            self.__init__()
            self.main_loop()
                
    def main_menue(self):
        '''In Arbeit'''
        self.game_mode=self.taste_1.react_input(self.end, self.spieler_1, self.spieler_2, self.spielfeld_2, self.spielfeld_1, self.buttons)
        self.spiel_start=True
        for button in self.buttons:
            button.draw(self.gui_1)
        '''
            3 Buttons die game_mode verändern
        '''
    def lokaler_mehrspieler(self):
        '''
        Führt die Aktionen für den lokalen Mehrspielermodus aus.

        Wenn spieler 1 keine Lebenspunkte mehr hat, wird der Spielmodus auf 4 gesetzt.
        Wenn spieler 2 keine Lebenspunkte mehr hat, wird der Spielmodus auf 4 gesetzt.

        Wenn das Spiel gerade gestartet wurde, wird der Startzustand zurückgesetzt.

        Falls die Anzahl der Asteroiden kleiner ist als das doppelte der maximalen Anzahl an Asteroiden,
        werden neue Asteroiden auf beiden Spielfeldern erzeugt.

        Wenn der Zähler den Wert 15 erreicht, werden Projektile für spieler 1 und spieler 2 erzeugt.
        Der Zähler wird zurückgesetzt und geprüft, ob die maximale Anzahl an Projektilen überschritten wurde.
        In diesem Fall werden die ältesten Projektile entfernt.

        Andernfalls wird der Zähler inkrementiert.

        Die Projektile werden bewegt.
        Die Tastenreaktionen von taste_1 werden ausgelöst.

        Die Asteroiden, spieler 1 und spieler 2 werden bewegt.

        Die Kollisionspolygone von spieler 1 und spieler 2 werden bewegt.

        Es wird auf Kollisionen getestet.

        Die Positionen der Bilder wird aktualisiert.
        '''

        if self.spieler_1.leben<=0 or self.spieler_2.leben<=0:
            self.game_mode=4
            if len(self.leaderboard_1.spieler)<=10:
                self.leaderboard_1.updateBoard(self.spieler_1.name, self.spieler_1.score, self.speicher_1)
                self.leaderboard_1.updateBoard(self.spieler_2.name, self.spieler_2.score, self.speicher_1) 
                for i in range(len(self.leaderboard_1.spieler)):
                    if (self.leaderboard_1.spieler[i], self.leaderboard_1.punktzahl[i]) not in self.saved_leaderboard:
                        self.speicher_1.save_one_entry_in_leaderboard(self.leaderboard_1.spieler[i], self.leaderboard_1.punktzahl[i])
                        self.speicher_1.sort_and_limit_table()
            else:
                self.leaderboard_1.updateBoard(self.spieler_1.name, self.spieler_1.score, self.speicher_1)
                self.leaderboard_1.updateBoard(self.spieler_2.name, self.spieler_2.score, self.speicher_1)
                for i in range(len(self.leaderboard_1.spieler)):
                    if (self.leaderboard_1.spieler[i], self.leaderboard_1.punktzahl[i]) not in self.saved_leaderboard:
                        self.speicher_1.save_one_entry_in_leaderboard(self.leaderboard_1.spieler[i], self.leaderboard_1.punktzahl[i])
                        self.speicher_1.sort_and_limit_table()
        
        if self.spiel_start:
            self.spiel_start=False
        
        #erschafft neue Asteroiden
        if len(self.asteroiden)<self.maximale_asteroiden_anzahl*2:
            self.create_asteroiden(self.spielfeld_1)
            self.create_asteroiden(self.spielfeld_2)
        
        '''
        if len(self.gegner)<10:
            
            self.gegner.append(gegner(self.spielfeld_1))
            self.gegner_polygon.append(enemy_polygon())
            self.init_polygon(self.gegner[-1], self.gegner_polygon[-1])
            self.gegner.append(gegner(self.spielfeld_2))
            self.gegner_polygon.append(enemy_polygon())
            self.init_polygon(self.gegner[-1], self.gegner_polygon[-1])
        '''
        if self.count==15:
                self.create_projectile(self.spielfeld_1, self.spieler_1)
                self.create_projectile(self.spielfeld_2, self.spieler_2)
                self.count=0
                
                for gegner_obj in self.gegner:
                    if gegner_obj.side == 0:
                        self.create_projectile(self.spielfeld_1,gegner_obj) 
                    else:
                        self.create_projectile(self.spielfeld_2,gegner_obj)
                                     



        else:
            self.count+=1
        




        self.move_projectile()
        self.taste_1.react_input(self.end, self.spieler_2, self.spieler_1, self.spielfeld_1, self.spielfeld_2, self.buttons)
        self.move_asteroid(self.spieler_1, self.spieler_2) 
        self.move_polygon(self.spieler_1, self.spieler_1_collision_polygon)
        self.move_polygon(self.spieler_2, self.spieler_2_collision_polygon)
        self.move_gegner(self.spieler_1,self.spieler_2)



        self.test_for_collision()
        self.update_screen_1()
        if self.count == 15 and self.maximale_projektil_anzahl<len(self.projektile): #entfernt je ein Projektil jedes Schützen nach einer bestimmten Frameanzahl
            projektil_schon_entfernt_von_schuetze=[]
            projektil_schon_entfernt=False
            for projektil in self.projektile:
                for schuetze in projektil_schon_entfernt_von_schuetze:
                    if projektil_schon_entfernt==False and projektil.schuetze==schuetze and not schuetze in projektil_schon_entfernt_von_schuetze:
                        self.projektil_polygone.pop(self.projektile.index(projektil))
                        self.projektile.pop(self.projektile.index(projektil))
    def lan_mehrspieler(self):
        '''
        Führt die Aktionen des LAN Mehrspielers aus

        Wenn spieler 1 keine Lebenspunkte mehr hat, wird der Spielmodus auf 4 gesetzt.
        Wenn spieler 2 keine Lebenspunkte mehr hat, wird der Spielmodus auf 4 gesetzt.

        Wenn das Spiel gerade gestartet wurde, wird der Startzustand zurückgesetzt.

        Falls die Anzahl der Asteroiden kleiner ist als das doppelte der maximalen Anzahl an Asteroiden,
        werden neue Asteroiden auf beiden Spielfeldern erzeugt.

        Wenn der Zähler den Wert 15 erreicht, werden Projektile für spieler 1 und spieler 2 erzeugt.
        Der Zähler wird zurückgesetzt und geprüft, ob die maximale Anzahl an Projektilen überschritten wurde.
        In diesem Fall werden die ältesten Projektile entfernt.

        Andernfalls wird der Zähler inkrementiert.

        Die Projektile werden bewegt.
        Die Tastenreaktionen von taste_1 werden ausgelöst.

        Die Asteroiden, spieler 1 und spieler 2 werden bewegt.

        Die Kollisionspolygone von spieler 1 und spieler 2 werden bewegt.

        Es wird auf Kollisionen getestet.

        Die Positionen der Bilder wird aktualisiert.

        Spieler 1 (S1) ist der Host, das heißt, alles wird bei Spieler 1 berechnet. Spieler 2 (S2) repliziert mit den Daten, die S1 mitgiebt die Anzeige.
        Die einzigen Daten, die S2 an S1 überträgt, sind die Buttoninputs.
        

        Spieler 2 wird mitgegeben:
        *Positionen von Asteroiden, Gegnern, Spielern, Projektilen
        *HP der Asteroiden, Gegnern und der Spieler
        *Punkte der Spieler
        
        Spieler 2 gibt an Spieler 1:
        *Buttoninputs S2
        '''
        if self.i_am_server:
            if not self.server_erstellt:
                self.l_c.setup_connection_as_server()
        else:
            if not self.client_erstellt:
                self.l_c.setup_connection_as_client()
            
        
        pass
    def optionen(self):
        '''In Arbeit'''
        pass          
    def create_asteroiden(self, feld_obj_2):
        """
        Erzeugt einen neuen Asteroiden auf dem angegebenen Spielfeld.

        Ein neues Asteroidenobjekt wird der Liste der Asteroiden hinzugefügt.
        Ein neues Asteroiden-Polygonobjekt wird der Liste der Asteroiden-Polygone hinzugefügt.
        Das Polygon des neuen Asteroidenobjekts wird initialisiert.
        Der neue Asteroid wird im GUI-Objekt angezeigt.
        """

        self.asteroiden.append(asteroid(feld_obj_2))
        self.asteroiden_polygon.append(asteroid_polygon())
        self.init_polygon(self.asteroiden[-1],self.asteroiden_polygon[-1])
        self.gui_1.display(self.asteroiden[len(self.asteroiden)-1])
    def create_projectile(self, feld_obj_2, schuetze_obj): 
        '''Erstellt ein Projektil mit zugehörigem Polygon (gleicher index)'''
        self.projektile.append(projektil(schuetze_obj.mittelpunkt[0], schuetze_obj.mittelpunkt[1], feld_obj_2, schuetze_obj, [-1*schuetze_obj.aktueller_richtungsvektor[0], -1*schuetze_obj.aktueller_richtungsvektor[1]]))
        self.projektil_polygone.append(projektil_polygon())
        self.init_polygon(self.projektile[-1], self.projektil_polygone[-1])
        self.gui_1.display(self.projektile[len(self.projektile)-1])    
    def update_screen_1(self): #_1 = game_mode
        '''
        Aktualisiert den Bildschirm für den Spielmodus 1.

        Diese Methode aktualisiert den Bildschirm, indem sie alle Spielfeldobjekte, spieler, Gegner, Projektile,
        Scoreanzeigen, Lebensanzeigen und Eventpunkteanzeigen darstellt.
        '''
        #erstellt beide Spielfelder
        self.gui_1.display(self.spielfeld_1)
        self.gui_1.display(self.spielfeld_2)
        #erstellt beide Spieler
        self.gui_1.display(self.spieler_1)
        self.gui_1.display(self.spieler_2)
        #stellt alle Gegner dar
        for asteroid in self.asteroiden:
            self.gui_1.display(asteroid)

        for gegner_obj in self.gegner:
            self.gui_1.display(gegner_obj)  
        #stellt alle Projektile dar
        for projectile in self.projektile:
            self.gui_1.display(projectile)
        #stellt den Score beider Spieler dar
        self.gui_1.display_text(0, 0, f"Score: {self.spieler_1.score}", pygame.Color(255, 255, 255, a=255), self.text_size)
        self.gui_1.display_text(self.spielfeld_1.spielfeld_width, 0, f"Score: {self.spieler_2.score}", pygame.Color(255, 255, 255, a=255), self.text_size)
        #stellt Leben beider Spieler dar
        self.gui_1.display_text(self.spielfeld_1.spielfeld_width*0.4, 0, f"Leben: {self.spieler_1.leben}", pygame.Color(255, 255, 255, a=255), self.text_size)
        self.gui_1.display_text(self.spielfeld_1.spielfeld_width*1.4, 0, f"Leben: {self.spieler_2.leben}", pygame.Color(255, 255, 255, a=255), self.text_size)
        #stellt Eventpunkte Spieler dar
        self.gui_1.display_text(self.spielfeld_1.spielfeld_width*0.8, 0, f"Punkte: {self.spieler_1.punkte}", pygame.Color(255, 255, 255, a=255), self.text_size)
        self.gui_1.display_text(self.spielfeld_1.spielfeld_width*1.8, 0, f"Punkte: {self.spieler_2.punkte}", pygame.Color(255, 255, 255, a=255), self.text_size)
    def update_screen_4(self):
        self.gui_1.spiel_fenster.blit(self.background, (0,0))
        self.gui_1.spiel_fenster.blit(self.leaderboard_background, (0.2*self.spielfeld_1.spielfeld_width, 0.1*self.spielfeld_1.spielfeld_height))
        y=0.4*self.spielfeld_1.spielfeld_height
        x=0.9*self.spielfeld_1.spielfeld_width
        
        for i in range(len(self.leaderboard_1.spieler)):
            self.gui_1.display_text(x, y, f"{i+1}. {self.leaderboard_1.spieler[i]} {self.leaderboard_1.punktzahl[i]}", pygame.Color(255, 255, 255, a=255), self.text_size)
            y+=0.05*self.spielfeld_1.spielfeld_height
            
    
    
    def namen_anzeigen(self):
        
        self.text_surface1 = self.font.render(self.spieler_name_1, True, self.black)
        self.text_surface2 = self.font.render(self.spieler_name_2 , True, self.black)
       
        pygame.draw.rect(self.gui_1.spiel_fenster,self.black, self.neue_text_rect_1, 1)
        pygame.draw.rect(self.gui_1.spiel_fenster,self.black, self.neue_text_rect_2, 1)
        self.gui_1.spiel_fenster.blit(self.text_surface1,self.neue_text_rect_1)
        self.gui_1.spiel_fenster.blit(self.text_surface2,self.neue_text_rect_2)
    def spieler_namen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.neue_text_rect_1.collidepoint(event.pos):
                    self.aktive_input = self.neue_text_rect_1
                elif self.neue_text_rect_2.collidepoint(event.pos):
                    self.aktive_input =  self.neue_text_rect_2
                else:
                    self.aktive_input = None
            if event.type == pygame.KEYDOWN:
                if self.aktive_input:
                    if event.key == pygame.K_RETURN:
                        self.game_mode = 1        
                    if event.key == pygame.K_BACKSPACE:
                        if self.aktive_input == self.neue_text_rect_1:
                            self.spieler_name_1 = self.spieler_name_1[:-1]
                        elif self.aktive_input == self.neue_text_rect_2:
                            self.spieler_name_2 = self.spieler_name_2[:-1]
                    else:
                        if self.aktive_input == self.neue_text_rect_1:
                            self.spieler_name_1 += event.unicode
                        elif self.aktive_input == self.neue_text_rect_2:
                            self.spieler_name_2 += event.unicode
        
        self.gui_1.fill(self.white)
        self.neue_text_rect_1 = pygame.Rect(300,200,200,40)
        self.neue_text_rect_2 = pygame.Rect(300,300,200,40) 
          

    
    
    
    def move_projectile(self): 
        '''Bewegt Projektile & ihre Polygone um einen Richtungsvektor und setzt ihre Position zurück, wenn sie außerhalb des Spielfelds sind. Beschleunigt den Richtungsvektor um einen Faktor'''
        for projectile in self.projektile:
            projectile.x+=projectile.richtungsvektor[0]
            projectile.y+=projectile.richtungsvektor[1]
            self.projektil_polygone[self.projektile.index(projectile)].move_polygon(projectile.richtungsvektor)
            self.projectile_boundaries()
            projectile.richtungsvektor[0]=projectile.richtungsvektor[0]*1.002
            projectile.richtungsvektor[1]=projectile.richtungsvektor[1]*1.002  
    def move_asteroid(self, spieler_obj, spieler_obj_2):
        '''Bewegt die Asteroiden und ihre Polygone um einen Einheitsvektor auf den Spieler zu.'''
        for asteroid in self.asteroiden:
            x=0
            y=0
        #Abstandsberechnung Gegner Spieler (Vektorrechnung)
            if self.asteroiden[self.asteroiden.index(asteroid)].side==0:
                x,y = self.berechne_vektor(asteroid, spieler_obj)
            if self.asteroiden[self.asteroiden.index(asteroid)].side==1:
                x,y = self.berechne_vektor(asteroid ,spieler_obj_2)
            abstand=self.berechne_abstand(x,y)
            if abstand>=1:
                x_change,y_change=self.berechne_einheitsvektor(x,y,abstand)
                asteroid.x+=x_change
                asteroid.y+=y_change
                asteroid.mittelpunkt=self.asteroiden_polygon[self.asteroiden.index(asteroid)].mittelpunkt
                self.asteroiden_polygon[self.asteroiden.index(asteroid)].move_polygon([x_change, y_change])      
    def move_gegner(self, spieler_obj, spieler_obj_2):
        '''Bewegt die gegner und ihre Polygone um einen Einheitsvektor auf den Spieler zu.'''
        for gegner in self.gegner:
            x=0
            y=0
        #Abstandsberechnung Gegner Spieler (Vektorrechnung)
            if self.gegner[self.gegner.index(gegner)].side==0:
                x,y = self.berechne_vektor(gegner, spieler_obj)
            if self.gegner[self.gegner.index(gegner)].side==1:
                x,y = self.berechne_vektor(gegner ,spieler_obj_2)
            abstand=self.berechne_abstand(x,y)
            if abstand>=1:
                x_change,y_change=self.berechne_einheitsvektor(x,y,abstand)
                gegner.x+=2*x_change
                gegner.y+=2*y_change
                gegner.aktueller_richtungsvektor = [x_change,y_change]

                gegner.mittelpunkt=self.gegner_polygon[self.gegner.index(gegner)].mittelpunkt
                self.gegner_polygon[self.gegner.index(gegner)].move_polygon([x_change, y_change])
    def berechne_vektor(self, obj_1, obj_2):
        '''Berechnet einen Richtungsvektor aus den Koordinaten zweier Objekte'''
        if obj_1!=obj_2:
            return obj_2.mittelpunkt[0]-obj_1.mittelpunkt[0], obj_2.mittelpunkt[1]-obj_1.mittelpunkt[1]
        else:
            return obj_1.aktueller_richtungsvektor[0]-obj_1.mittelpunkt[0], obj_1.aktueller_richtungsvektor[1]-obj_1.mittelpunkt[1]  
    def berechne_abstand(self, x, y):
        '''Berechnet den Betrag(/Abstand) eines Vektors'''
        return math.sqrt(x**2+y**2)       
    def berechne_einheitsvektor(self, x, y, abstand):
        '''Berechnet aus einem Richtungsvektor und Abstand einen Einheitsvektor'''
        if abstand==0:
            return 0,0
        else:
            return x/abstand, y/abstand        
    def projectile_boundaries(self):
        '''Entfernt Projektile aus der Liste, wenn diese außerhalb des Spielfelds sind'''
        for projectile in self.projektile:
            if projectile.side == self.spielfeld_1.side:
                if projectile.x < self.spielfeld_1.x or projectile.x > self.spielfeld_1.x+self.spielfeld_1.spielfeld_width-0.0125*self.spielfeld_1.spielfeld_width or projectile.y < self.spielfeld_1.y or projectile.y > self.spielfeld_1.y+self.spielfeld_1.spielfeld_height:
                    self.projektil_polygone.pop(self.projektile.index(projectile))
                    self.projektile.pop(self.projektile.index(projectile))
            if projectile.side == self.spielfeld_2.side:
                if projectile.x < self.spielfeld_2.x or projectile.x > self.spielfeld_2.x+self.spielfeld_2.spielfeld_width or projectile.y < self.spielfeld_2.y or projectile.y > self.spielfeld_2.y+self.spielfeld_2.spielfeld_height:
                    self.projektil_polygone.pop(self.projektile.index(projectile))
                    self.projektile.pop(self.projektile.index(projectile))                   
    def test_for_collision (self):
        '''In Arbeit. Prüft bisher auf Kollisionen mit Asteroiden und reagiert auf Kollisionen'''
        for gegner in self.gegner:
            #try:
                if gegner.side == 0:
                    if self.spieler_1_collision_polygon.collision(self.gegner_polygon[self.gegner.index(gegner)]):
                        self.spieler_1.leben -= 1
                        '''
                        self.gegner_polygon.pop(self.gegner.index(gegner))
                        self.gegner.pop(self.gegner.index(gegner))
                        '''

                if gegner.side == 1:
                    if self.spieler_2_collision_polygon.collision(self.gegner_polygon[self.gegner.index(gegner)]):
                        self.spieler_2.leben -= 1
                        '''
                        self.gegner_polygon.pop(self.gegner.index(gegner))
                        self.gegner.pop(self.gegner.index(gegner))
                        '''
                if gegner in self.gegner:
                    for projektile in self.projektile:
                        #try:
                        bool_1=projektile.side == gegner.side
                        bool_2=self.gegner_polygon[self.gegner.index(gegner)].collision(self.projektil_polygone[self.projektile.index(projektile)])
                        if bool_1 and bool_2:
                            if projektile.side == 0:
                                self.spieler_1.score += 1
                                self.spieler_1.punkte += 1

                            if projektile.side == 1:
                                self.spieler_2.score += 1
                                self.spieler_2.punkte += 1
                        #except:
                            #pass

                            self.gegner_polygon.pop(self.gegner.index(gegner))
                            self.gegner.pop(self.gegner.index(gegner))
                            self.projektil_polygone.pop(self.projektile.index(projektile))
                            self.projektile.pop(self.projektile.index(projektile))        
                        


            #except:
                #pass
        
        for asteroid in self.asteroiden:
            try:
                if asteroid.side==0:
                    if self.spieler_1_collision_polygon.collision(self.asteroiden_polygon[self.asteroiden.index(asteroid)]):
                        self.spieler_1.leben-=1            
                if asteroid.side==1:
                    if self.asteroiden_polygon[self.asteroiden.index(asteroid)].collision(self.spieler_2_collision_polygon):
                        self.spieler_2.leben-=1
                for projektil in self.projektile:
                        if projektil.side==asteroid.side:
                            if self.asteroiden_polygon[self.asteroiden.index(asteroid)].collision(self.projektil_polygone[self.projektile.index(projektil)]):
                                if projektil.side==0:
                                    self.spieler_1.score+=1
                                    self.spieler_1.punkte+=1
                                else:
                                    self.spieler_2.punkte+=1
                                    self.spieler_2.score+=1
                                self.asteroiden_polygon.pop(self.asteroiden.index(asteroid))
                                self.asteroiden.pop(self.asteroiden.index(asteroid))
                                self.projektil_polygone.pop(self.projektile.index(projektil))
                                self.projektile.pop(self.projektile.index(projektil))
                                
            except:
                print("Asteroid not in list")
            
