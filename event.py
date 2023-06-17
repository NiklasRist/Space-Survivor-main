import pygame
from taste import verwalter
class event:
    def __init__(self):
        pass
    
    def get_kosten(self):
        pass
    
    def ausfuehren(self, spieler):
        pass

class event_1(event):
    "Shwarzes loch wird erscheinen und das Raum Schiff zu sich anziehen"

class event_2(event):
    "Gegner wird für ein paar sekunden doppelt so viel schießen"

class verwirrung(event):
    "die richtungen werden vertaucht"
    def key_änderung(steurung_obj):
        steuerung_obj.spieler_1_rechts = pygame.K_LEFT
        steuerung_obj.spieler_1_links = pygame.K_RIGHT
        steuerung_obj.self.spieler_1_oben = pygame.K_DOWN
        steuerung_obj.self.spieler_1_unten = pygame.K_UP

        steuerung_obj.self.spieler_2_rechts = pygame.K_a
        steuerung_obj.self.spieler_2_links = pygame.K_d
        steuerung_obj.self.spieler_2_oben = pygame.K_s
        steuerung_obj.self.spieler_2_unten = pygame.K_w 


class event_4(event):
    "ist die "
