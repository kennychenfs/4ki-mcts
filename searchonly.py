#give vlue with a simple function, and do mcts(without policy)

from copy import deepcopy as dc
from math import sqrt
from time import sleep,time
import random
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
	def dump(self,tx=6,ty=7):
		black='16';white='255';none='172'
		a='    0 1 2 3 4 5 6\n'
		a+=u'  \u250F\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2513\n'
		for x in range(6):
			if(len(str(x))==1):
				a+=' '+str(x)
			else:
				a+=str(x)
			a=a+u'\u2503'
			for y in range(7):
				if y==0:
					a=a+self.color+black+self.end+self.bg+none+self.end+' '+self.reset
				if x is tx and y is ty:
					black='196';white='201'
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
		tx=0
		while 1:
			if self.grid[tx][y]!=0:
				if tx==0:return
				break
			tx+=1
			if tx==6:break
		self.grid[tx-1][y]=color
	def remove(self,y):
		tx=0
		while 1:
			if self.grid[tx][y]!=0:
				self.grid[tx][y]=0
				return
			tx+=1
			if tx==6:return
	def value(self):
		bpoints=0.0
		wpoints=0.0
		for x in range(6):
			for y in range(7):
				if self.grid[x][y]==0:continue
				color=self.grid[x][y]
				for i in range(4):
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
						if inarow==2:bpoints+=0.0001
						if inarow==3:bpoints+=0.01
						if inarow>=4:bpoints+=1
					else:
						if inarow==2:wpoints+=0.0001
						if inarow==3:wpoints+=0.01
						if inarow>=4:wpoints+=1
		return bpoints-wpoints

c_puct=0.1

class node:#due to search only, no policy
	def __init__(self,parent=0,y=0,color=2,board=board(),depth=0):#action169 is pass
		global c_puct
		self.b=board#which the move itself represent has been played
		self.depth=depth
		self.parent=parent
		self.w=0
		self.n=0
		self.q=0
		self.update_u(c_puct)
		self.child={}#{action(y):children(node)...}
		self.y=y
		self.color=color
	def get_q_add_u(self):
		return self.q+self.u
	def select(self):
		#for i in self.child.values():
		#	print(i.u)
		move=max(self.child.items(), key=lambda node: node[1].get_q_add_u())
		return move[1]
	def update_u(self,c_puct):
		if self.parent==0:return
		self.u=c_puct*sqrt(self.parent.n)/(1+self.n)
	def backup(self,v):
		global c_puct
		self.w+=v
		self.n+=1
		self.q=self.w/self.n
		for i in self.child.values():
			i.update_u(c_puct)
		if self.parent is not 0:
			self.parent.backup(-v)
	def expand(self):
		if self.b.win()!=0:
			return
		color=1 if self.color==2 else 2#color for children
		for y in range(7):
			if self.b.grid[0][y]!=0:
				continue#not able to play here
			self.b.play(y,color)
			newnode=node(self,y,color,dc(self.b),depth=self.depth+1)
			self.b.remove(y)
			self.child[y]=newnode
class tree:
	def __init__(self,root):
		self.root=root
		self.nowsearching=root
	def godown(self):
		self.nowsearching=self.root
		while 1:
			if self.nowsearching.child=={}:
				break
			self.nowsearching=self.nowsearching.select()
	def expand(self):
		self.nowsearching.expand()
	def backup(self):
		v=self.nowsearching.b.value()
		if self.nowsearching.color==2:
			v=-v
		v*=random.random()*0+1
		self.nowsearching.backup(v)
	def play(self):
		best=max(self.root.child.values(), key=lambda node: node.n)
		self.root=best
		self.root.parent=0
po=int(input('playouts?'))
root=node()
t=tree(root)
while 1:
	start=time()
	for _ in range(po):
		t.godown()
		t.expand()
		t.backup()
	timeuse=time()-start
	print(po,'playouts,',t.root.n,'visits,',round(t.root.n/timeuse),'visits/s.')
	#	t.nowsearching.b.dump()
	for i in t.root.child.values():
	#	i.b.dump()
		print(i.n,i.q)
	t.play()
	t.root.b.dump()
	y=int(input("y?\n"))
	t.root=t.root.child[y]
	
