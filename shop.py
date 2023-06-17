from spieler import spieler

event1 = None
event2 = event1
event3 = event1
event = [event1, event2, event3]

class shop():
    
    def __init__(self):
        pass
    
    def pruefen_ob_genug_punkte(self, spieler, event_nummer):
        genug_punkte = spieler.spieler_punkte >= event[event_nummer].get_kosten()
        if genug_punkte:
            self.event_ausführen(spieler, event_nummer)
            spieler.spieler_punkte = spieler.spieler_punkte - event[event_nummer].get_kosten()
            return "Event gekauft!"
            
        else:
            return "Nicht genügend Punkte!"
    
    def event_ausführen(self, spieler, event_nummer):
        event[event_nummer].ausfuehren(spieler)
