import random

class sampleai():
	def move(self,gamestate):
		while gamestate.possible_moves() != set():
			gamestate.make_Move(random.choice(list(gamestate.possible_moves())))


	def set_card(self,gamestate):

		possible_coords = [(0,0),(0,1),(1,0)]
		gamestate.set_card(*random.choice(possible_coords))
