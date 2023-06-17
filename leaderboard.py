class leaderboard:
	spieler=[]
	punktzahl=[]
	
	def __init__(self):
		self.spieler = []
		self.punktzahl = []
	
	def addToBoard(self, p_spieler, p_punktzahl):
		self.spieler.append(p_spieler)
		self.punktzahl.append(p_punktzahl)
  
	def sortBoardByScoreDesc(self):
		for i in range(len(self.punktzahl)):
			for j in range(len(self.punktzahl)-1-i):
				if self.punktzahl[j] > self.punktzahl[j + 1]:
						self.punktzahl[j], self.punktzahl[j+1],self.spieler[j], self.spieler[j+1] = self.punktzahl[j+1], self.punktzahl[j],self.spieler[j+1], self.spieler[j]
      
	def deleteUnnecessaryEntries(self, speicher_obj):
		while len(self.punktzahl)>10:
			self.punktzahl, self.spieler=self.punktzahl[1:], self.spieler[1:]

	def updateBoard(self, p_spieler, p_punktzahl, speicher_obj):
		self.addToBoard(p_spieler, p_punktzahl)
		self.sortBoardByScoreDesc()
		self.deleteUnnecessaryEntries(speicher_obj)
