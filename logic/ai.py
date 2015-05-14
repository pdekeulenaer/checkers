# /usr/bin/env/python
import checkers
import random
import time
from playerhandler import PlayerHandler

class BasicAI(PlayerHandler):
	def __init__(self,ctrl,player):
		super(BasicAI, self).__init__(ctrl, player)

	def mandatory_move(self):
		moves = self.control.mandatory_moves(self.player)
		if not (moves is None) and len(moves) > 0:
			return random.choice(moves)
		return None


	def random_move(self):
		moves = self.control.valid_moves(self.player)
		return random.choice(moves)

	def make_move(self):
		if self.control.turn == self.player:
			self.log("my turn!")
			self.play()

	def play(self):
		move = self.mandatory_move()
		if move is None:
			move = self.random_move()
		self.log(move)

		time.sleep(0.5)
		source,target = move

		super(BasicAI, self).submit_move(source, target)


	def log(self,msg):
		print "[AI]",msg

