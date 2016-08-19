#!/usr/bin/env python3

import collections
import random

#ai: pointer to an ai instance
#deck: list of all remaining cards in that players deck, for example [("A",1,"Flut"),("E",3,"Flut")]
PlayerData = collections.namedtuple("PlayerData",["ai","deck"])

# for example ("A",1,"Flut")
Card = collections.namedtuple("Card",["character","number","side"])

class Gamestate():
	"""
	This class contains the Gamestate and methods to get and change the gamestate
	"""
	

	def __init__(self,ai1,ai2):
		
		player1 = PlayerData(ai1,self._create_new_deck(0))
		player2 = PlayerData(ai2,self._create_new_deck(1))
		self.players = [player1,player2]
		self.active_player = 1 # newturn changes the active player having player 2 here results in player1 starting
		self.turn_number = 0
		self.card_drawn = True #was a card drawn this turn?
		self.card = None #card that has to played this turn
		self.card_payed = True #did the player already play his card?
		self.field = self._create_empty_field()

	def _get_top_card_field(self):
		"""
		returns a field with only the top card of every cell
		"""
		return [[cell[-1] if len(cell) >0 else Card(None,None,None) for cell in row] for row in self.field]
	
	@staticmethod
	def _mirror_coords(i,j):
		"""
		mirrors all coordinates, so that player2 sees the field like player1
		"""
		return 4-j,4-i

	def _get_reversed_top_card_field(self):
		"""
		mirrors the field
		Player2s home field is 44, but should look like 00 to him
		"""
		field = self._get_top_card_field()
		#i = column j = row
		mirrored_field = [[field[Gamestate._mirror_coords(i,j)[0]][Gamestate._mirror_coords(i,j)[1]] for i in range(5)] for j in range(5)]
		return mirrored_field
					

	def _create_empty_field(self):
		#i = column j = row
		return [[[(i,j)] for i in range(5)] for j in range(5)]
 

	def _get_ac_player(self):
		"""
		returns the PlayerData of the active player
		"""
		return self.players[self.active_player]

	def _new_turn(self):
		"""

		"""
		self.turn_number += 1

		#change of the active player
		assert self.active_player in {0,1}
		self.active_player = 1 if self.active_player == 0 else 0

		assert self.card_drawn == True
		self.card_drawn = False
		self._draw_card()

		assert self.card_payed == True
		self.card_payed = False

	def _draw_card(self):
		"""
		removes the front card of the deck of the active players
		"""
		assert not self.card_drawn
		self.card_drawn = True
		self.card = self._get_ac_player().deck.pop()


	def _create_new_deck(self,player):
		"""
		creates a new deck of 25 cards and shuffles it
		cards range from A1 to E5 and are of type "Card"
		"""
		deck = [Card(character,number,player) for character in ["A","B","C","D","E"] for number in range(1,6)]
		random.shuffle(deck)
		return deck


	def set_card(self):
		pass

	def get_field(self):
		"""
		returns the top card on every cell
		(a list of list of Card namedtuples)
		a card := collections.namedtuple("Card",["character","number","side"])
		if there is no card, a empty card with all values set to None is returned
		the field is mirrored if for player2, so that there is no difference in position inidices 
		between player1 and 2
		"""
		assert self.active_player in {0,1}
		if self.active_player == 0:
			return self._get_top_card_field()
		else:
			return self._get_reversed_top_card_field()

	def drawn_card(self):
		"""
		get the card that was drawn this turn
		"""
		return self.card

	def cards_left(self):
		"""
		returns the number of cards in the deck of the active player
		"""
		return len(self._get_ac_player().deck)


if __name__ == "__main__":
	pass
	g = Gamestate(1,1)
	g._new_turn()
	print(g.drawn_card())
	print(g.cards_left())
	print(g._get_top_card_field())
	print(g._get_reversed_top_card_field())

