import random
import playerexample
class player(playerexample.player):
	def genmove(self,color):
		probs=[]
		for y in range(7):
			if self.board.grid[0][y]==0:
				probs.append(y)
		if probs==[]:return
		y=probs[random.randint(0,len(probs)-1)]
		self.board.play(y,color)
		return y
		#None is pass(finish)
