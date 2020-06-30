direction=[[1,0],[1,1],[1,-1],[0,1]]
class board:
	bg   ="\x1b[48;5;"
	color="\x1b[38;5;"
	end  ="m"
	reset="\x1b[0m"
	def __init__(self,grid=[]):
		if grid!=[]:
			self.grid=grid
			return
		self.grid=[]
		for x in range(6):
			self.grid.append([])
			for y in range(7):
				self.grid[-1].append(0)
	def win(self):
		for x in range(6):
			for y in range(7):
				if self.grid[x][y]==0:continue
				color=self.grid[x][y]
				for i in range(4):
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
	def dump(self,ytocolor=7):
		black='16';white='255';none='172'
		a='    0 1 2 3 4 5 6\n'
		a+=u'  \u250F\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2513\n'
		colored=False
		for x in range(6):
			if(len(str(x))==1):
				a+=' '+str(x)
			else:
				a+=str(x)
			a=a+u'\u2503'
			for y in range(7):
				if y==0:
					a=a+self.color+black+self.end+self.bg+none+self.end+' '+self.reset#for the first space.  If you can't understand, comment these lines.
				if not colored and y==ytocolor and self.grid[x][y]!=0:
					black='196';white='201'
					colored=True
				else:
					black='16';white='255'
				if self.grid[x][y]==1:
					a=a+self.color+black+self.end+self.bg+none+self.end+u'\u25cf '+self.reset
				elif self.grid[x][y]==2:
					a=a+self.color+white+self.end+self.bg+none+self.end+u'\u25cf '+self.reset
				elif self.grid[x][y]==0:
					a=a+self.color+black+self.end+self.bg+none+self.end+'. '+self.reset
				else:
					a=a+str(self.grid[x][y])+' '
			a=a+u'\u2503'
			if(len(str(x))==1):
				a+=' '+str(x)
			else:
				a+=str(x)
			a+='\n'
		a+=u'  \u2517\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u251B\n'
		a+='    0 1 2 3 4 5 6\n'
		print(u'{}'.format(a))
	def play(self,y,color):
		x=self.get_top_x(y)
		if x==0:return
		self.grid[x-1][y]=color
	def remove(self,y):
		x=self.get_top_x(y)
		if x>=6:return
		self.grid[x][y]=0
	def get_top_x(self,y):
		tx=0
		while 1:
			if self.grid[tx][y]!=0:
				return tx
			tx+=1
			if tx==6:return 6
	
	def value(self):#ONLY for searchonly test
		points=0.0
		for x in range(6):
			for y in range(7):
				if self.grid[x][y]==0:continue
				color=self.grid[x][y]
				for i in range(4):
					tx=x-direction[i][0];ty=y-direction[i][1]
					if tx<6 and tx>=0 and ty<7 and ty>=0:
						if self.grid[tx][ty]==color:continue
					
					inarow=1
					tx=x;ty=y
					while 1:
						tx=tx+direction[i][0];ty=ty+direction[i][1]
						if tx>=6 or tx<0 or ty>=7 or ty<0:
							break
						if self.grid[tx][ty]!=color:
							break
						inarow+=1
					if color==1:
						if inarow==2:points+=0.0001
						if inarow==3:points+=0.01
						if inarow>=4:points+=1
					else:
						if inarow==2:points-=0.0001
						if inarow==3:points-=0.01
						if inarow>=4:points-=1
		return points
