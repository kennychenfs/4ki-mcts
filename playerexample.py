from rule import board
class player:
	def __init__(self):
		self.board=board()
	def play(self,y,color):
		self.board.play(y,color)
	def genmove(self,color):
		pass
		#None is pass(finish)
