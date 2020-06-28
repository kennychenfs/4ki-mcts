#test how many games have result, just for inference

import random
direction=[[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0],[-1,1],[-1,-1]]
class board:
	def __init__(self):
		self.grid=[]
		for x in range(6):
			self.grid.append([])
			for y in range(7):
				self.grid[-1].append(0)
	def win(self):
		for x in range(6):
			for y in range(7):
				color=self.grid[x][y]
				for i in range(8):
					now=1
					tx=x;ty=y
					while 1:
						tx=tx+direction[i][0];ty=ty+direction[i][1]
						if tx>=6 or tx<0 or ty>=7 or ty<0:
							break
						if self.grid[tx][ty]!=color:
							break
						now+=1
						if now==4:return color
		return 0
	def fill(self):
		black=21
		white=21
		for x in range(6):
			for y in range(7):
				r=random.randint(1,black+white)
				if r<=black:
					color=1
					black-=1
				else:
					color=2
					white-=1
				self.grid[x][y]=color
	def dump(self):
		for x in range(6):
			for y in range(7):
				print(self.grid[x][y],end='')
			print()
b=board()
a=0
for i in range(10000):
	b.fill()
	if b.win()!=0:
		a+=1
print(str(a)+'games of 10000 games have result.')
