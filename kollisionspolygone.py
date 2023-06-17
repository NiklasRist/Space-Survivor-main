import math

class polygon:
    def __init__(self) -> None:
        self.collision_polygon=[]
        self.mittelpunkt=[]
        self.sides=0
    def rescale_polygon(self, object_size):
        '''Passt die Größe des Polygons an die Größe eines Objekts an'''
        add_all=[0,0]
        for eckpunkt in self.collision_polygon:
            eckpunkt[0]=eckpunkt[0]/48*object_size
            eckpunkt[1]=eckpunkt[1]/48*object_size
            add_all[0]+=eckpunkt[0]
            add_all[1]+=eckpunkt[1]
        self.mittelpunkt=[int(add_all[0]/self.sides),int(add_all[1]/self.sides)]
      
    def move_polygon(self, vektor):
        '''Bewegt das Polygon um einen Vektor.'''
        for eckpunkt in self.collision_polygon: 
            eckpunkt[0]+=vektor[0]
            eckpunkt[1]+=vektor[1]  
        self.mittelpunkt[0]+=vektor[0]
        self.mittelpunkt[1]+=vektor[1]   
    
    def give_schnittpunkt(self, polygon_side, polygon_object) -> list: 
        '''
            Jedes Kollisionspolygon hat viele Seiten.
            Die Seitennummerierung beginnt bei den Strecke zwischen den ersten beiden Punkten mit Seite 1.
            Diese Funktion berechnet den Schnittpunkt zweier Liniensegmente:
            a:x=self.mittelpunkt+r*(polygon_object.mittelpunkt-self.mittelpunkt)) (Teil der Abstandsgerade)
            s:x=self.collison_polygon[polygon_side-1]+r*(self.collison_polygon[polygon_side]-self.collision_polygon[polygon_side-1]))) (Teil der Polygonseitengerade)
            schittpunkt(x,y,lines_are_identical)
        '''
        x_1=self.mittelpunkt[0]
        y_1=self.mittelpunkt[1]
        x_2=polygon_object.mittelpunkt[0]
        y_2=polygon_object.mittelpunkt[1]
        x_3=self.collision_polygon[polygon_side-1][0]
        y_3=self.collision_polygon[polygon_side-1][1]
        x_4=self.collision_polygon[polygon_side][0]
        y_4=self.collision_polygon[polygon_side][1]
        zaehler=(x_1-x_3)*(y_3-y_4)-(y_1-y_3)*(x_3-x_4)
        nenner=(x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4)
        if nenner==0: return None
        parametergleichungsvariable=zaehler/nenner
        schnittpunkt=[(self.mittelpunkt[0]+parametergleichungsvariable*(polygon_object.mittelpunkt[0]-self.mittelpunkt[0])),(self.mittelpunkt[1]+parametergleichungsvariable*(polygon_object.mittelpunkt[1]-self.mittelpunkt[1]))]
        if 0<=parametergleichungsvariable<=1: #nicht parallel und nicht identisch?
            schnittpunkt.append(False)
            return schnittpunkt
        elif self.mittelpunkt==self.collision_polygon[polygon_side-1] and polygon_object.mittelpunkt==self.collision_polygon[polygon_side]: #identisch?
            schnittpunkt.append(True)
            return schnittpunkt
        else: return None #parallel?
        
    def collision_0(self, polygon_object):
        '''
            Prüft ob der Schnittpunkt eines anderen Polygons auf oder zwischen dem Mittelpunkt oder dem Schnittpunkt dieses Polygons ist.
        '''
        schnittpunkt_1=[]
        schnittpunkt_2=[]
        for side in range(self.sides):
            
            zw=self.give_schnittpunkt(side, polygon_object)
            if type(zw)==list and math.sqrt((polygon_object.mittelpunkt[0]-zw[0])**2 + (polygon_object.mittelpunkt[1]-zw[1])**2)<= math.sqrt((polygon_object.mittelpunkt[0]-self.mittelpunkt[0])**2+(polygon_object.mittelpunkt[1]-self.mittelpunkt[1])**2): #nicht parallel und mittelpunkt_1<=Schnittpunkt<=mittelpunkt_2
                schnittpunkt_1=zw
                schnittpunkt_2=schnittpunkt_1
                if zw[2]==False:
                    for p_side in range(polygon_object.sides):
                        zw=polygon_object.give_schnittpunkt(p_side, self)
                        if type(zw)==list and math.sqrt((self.mittelpunkt[0]-zw[0])**2 + (self.mittelpunkt[1]-zw[1])**2)<= math.sqrt((polygon_object.mittelpunkt[0]-self.mittelpunkt[0])**2+(polygon_object.mittelpunkt[1]-self.mittelpunkt[1])**2): #nicht parallel und mittelpunkt_1<=Schnittpunkt<=mittelpunkt_2
                            schnittpunkt_2=zw
        if polygon_object.mittelpunkt<=schnittpunkt_1<=schnittpunkt_2 or polygon_object.mittelpunkt>=schnittpunkt_1>=schnittpunkt_2 : #zwischen mittelpunkt und schnitt punkt von polygon_object?
            return True
        if self.polygon_1_is_in_polygon_2(self,polygon_object):
            return True
        if self.polygon_1_is_in_polygon_2(polygon_object, self):
            return True
        return False
    def collision(self, polygon_object):
        '''
            Prüft ob das Polygon mit dem anderen Polygon kollidiert
        '''
        for side in range(self.sides):
            '''
                Seitengleichung finden 
                Normalenachse erstellen 
                relative Position des Schnittpunkts zur Normalenachse finden (Skalarprodukt) 
                Array mit Schnittpunkten pro Objekt 
                min und max Werte im Array finden 
                Position der min und max Werte beider Polygone auf einem Zahlenstrahl vergleichen 
                Falls es eine Lücke gibt return False 
            '''
            seitengleichung_richtungsvektor=[]
            if side+1==self.sides:
                seitengleichung_richtungsvektor=[self.collision_polygon[-1][0]-self.collision_polygon[side][0], self.collision_polygon[-1][1]-self.collision_polygon[side][1]]
            else:
                seitengleichung_richtungsvektor=[self.collision_polygon[side+1][0]-self.collision_polygon[side][0], self.collision_polygon[side+1][1]-self.collision_polygon[side][1]]
            normalenachse_richtungsvektor=[-1*seitengleichung_richtungsvektor[1], seitengleichung_richtungsvektor[0]]
            self_shadow=[]
            polygon_object_shadow=[]
            for eckpunkt in self.collision_polygon:
                skalarprodukt=eckpunkt[0]*normalenachse_richtungsvektor[0]+eckpunkt[1]*normalenachse_richtungsvektor[1]
                self_shadow.append(skalarprodukt)
            for eckpunkt in polygon_object.collision_polygon:
                skalarprodukt=eckpunkt[0]*normalenachse_richtungsvektor[0]+eckpunkt[1]*normalenachse_richtungsvektor[1]
                polygon_object_shadow.append(skalarprodukt)
            if (min(self_shadow) > max(polygon_object_shadow)) or (min(polygon_object_shadow) > max(self_shadow)):
                return False
        return True   
 
    
class spieler_polygon(polygon):
    def __init__(self) -> None:
        self.collision_polygon=[[22,15],[6,31],[6,45],[41,45],[41,31],[25,15]]
        self.mittelpunkt=[24, 30]
        self.sides=6
    def rescale_polygon(self, object_size):
        '''Passt die Größe des Polygons an die Größe eines Objekts an'''
        add_all=[0,0]
        for eckpunkt in self.collision_polygon:
            eckpunkt[0]=eckpunkt[0]/48*object_size
            eckpunkt[1]=eckpunkt[1]/48*object_size
            add_all[0]+=eckpunkt[0]
            add_all[1]+=eckpunkt[1]
        self.mittelpunkt=[int(add_all[0]/6),int(add_all[1]/6)]
        
 
class projektil_polygon(polygon):
    def __init__(self) -> None:
        self.collision_polygon=[[3,0],[0,3],[0,6],[3,9],[6,9],[9,6],[9,3],[6,0]]
        self.mittelpunkt=[]
        self.sides=8
    def rescale_polygon(self, object_size):
        '''Passt die Größe des Polygons an die Größe eines Objekts an'''
        add_all=[0,0]
        for eckpunkt in self.collision_polygon:
            eckpunkt[0]=eckpunkt[0]/10*object_size
            eckpunkt[1]=eckpunkt[1]/10*object_size
            add_all[0]+=eckpunkt[0]
            add_all[1]+=eckpunkt[1]
        self.mittelpunkt=[int(add_all[0]/self.sides),int(add_all[1]/self.sides)]

class asteroid_polygon(polygon):
    def __init__(self) -> None:
        self.collision_polygon=[[26,9],[7,28],[7,40],[22,55],[43,55],[59,39],[59,27],[41,29]]
        self.sides=8
    def rescale_polygon(self, object_size):
        '''Passt die Größe des Polygons an die Größe eines Objekts an'''
        add_all=[0,0]
        for eckpunkt in self.collision_polygon:
            eckpunkt[0]=eckpunkt[0]/67*object_size
            eckpunkt[1]=eckpunkt[1]/63*object_size
            add_all[0]+=eckpunkt[0]
            add_all[1]+=eckpunkt[1]
        self.mittelpunkt=[int(add_all[0]/self.sides),int(add_all[1]/self.sides)]
         
class enemy_polygon(polygon):
    def __init__(self) -> None:
        self.collision_polygon=[[26,23],[15,34],[15,52],[24,61],[38,61],[49,50],[49,35],[37,23]]
        self.sides=8
    def rescale_polygon(self, object_size):
        '''Passt die Größe des Polygons an die Größe eines Objekts an'''
        add_all=[0,0]
        for eckpunkt in self.collision_polygon:
            eckpunkt[0]=eckpunkt[0]/64*object_size
            eckpunkt[1]=eckpunkt[1]/64*object_size
            add_all[0]+=eckpunkt[0]
            add_all[1]+=eckpunkt[1]
        self.mittelpunkt=[int(add_all[0]/self.sides),int(add_all[1]/self.sides)]

        