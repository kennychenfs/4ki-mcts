from copy import deepcopy as dc
from rule import board
from time import time
from math import sqrt
import random
import playerexample
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
class mcts_tree:
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
		self.nowsearching.backup(v)
	def play(self):
		if self.root.child=={}:return
		best=max(self.root.child.items(), key=lambda item: item[1].n)
		self.root=best[1]
		self.root.parent=0
		return best[0]
class player(playerexample.player):
	def __init__(self,tree):
		super().__init__()
		self.tree=tree
	def play(self,y,color):#only accept color 1,2,1,2
		super().play(y,color)
		self.tree.root=self.tree.root.child[y]
	def genmove(self,color):
		for _ in range(30):
			self.tree.godown()
			self.tree.expand()
			self.tree.backup()
		
		for i in self.tree.root.child.values():
			print(i.n,i.q)
		return self.tree.play()
