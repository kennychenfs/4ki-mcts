from player_random import player as randomplayer
from player_mcts import player as mctsplayer 
from player_mcts import node,mcts_tree
from rule import board

root=node()
t=mcts_tree(root)
mcts=mctsplayer(t)

random=randomplayer()

b=board()
def agame():
	while 1:
		y=mcts.genmove(1)
		if y==None:
			return b.win()
		b.play(y,1)
		b.dump()
		if b.win()!=0:
			return b.win()
		random.play(y,1)
			
		y=random.genmove(2)
		if y==None:
			return b.win()
		b.play(y,2)
		b.dump()
		if b.win()!=0:
			return b.win()
		mcts.play(y,2)
mcts_win=0
random_win=0
for _ in range(100):
	win=agame()
	if win==1:
		mcts_win+=1
	if win==2:
		random_win+=1
	root=node()
	t=mcts_tree(root)
	mcts=mctsplayer(t)
	
	random=randomplayer()
	b=board()
print(mcts_win,random_win)
