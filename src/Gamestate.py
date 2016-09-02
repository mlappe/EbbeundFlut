#!/usr/bin/env python3

import collections
import random
import operator

# a namedtuple containig all information relating to a player
# ai: pointer to an ai instance
# deck: list of all remaining cards in that players deck, for example [("A",1,1),("E",3,0)]
PlayerData = collections.namedtuple("PlayerData",["ai","deck","cards_won"])

# a namedtuple representing a Card
# for example ("A",1,0)
# subclassing namedtuple
class Card(collections.namedtuple("Card",["character","number","side"])):

	def __init__(self,character,number,side):
		"""
		checking for valid input Data
		"""
		assert character in {None,"A","B","C","D","E"}
		assert number in {None,1,2,3,4,5}
		assert side in {None,0,1}

	def __repr__(self):
		"""
		shows placeholder cards as empty string, else character,number colored
		placeholder cards are cards where all attributes are set to None
		"""
		if self.character == None and self.number == None and self.side == None:
			return "  "
		else:
			#ANSI sequences for colors
			if self.side == 0:

				#red
				color = 31

			elif self.side == 1:

				#blue
				color = 34

			color = str(color)

			return "\033["+color+"m" +str(self.character) + str(self.number) + "\033[0m"

# start is a tuple i,j with the start cell
# end is a tuple i,j with the end cell
# Move = collections.namedtuple("Move",["start","end"])
class Move(collections.namedtuple("Move",["start","end"])):

	def __init__(self,start,end):
		"""
		checking for valid input Data
		"""
		#checking that all coords are valid
		assert start[0] in {0,1,2,3,4}
		assert start[1] in {0,1,2,3,4}
		assert end[0] in {0,1,2,3,4,5}
		assert end[1] in {0,1,2,3,4,5}

		#checking that end is one step away from start
		assert operator.xor(start[0] == end[0]-1 , start[1] == end[1]-1)

class Gamestate():
	"""
	This class contains the Gamestate and methods to get and change the gamestate
	"""
	

	def __init__(self,*,ai1,ai2,interface):
		
		player1 = PlayerData(ai1,self._create_new_deck(0),[])
		player2 = PlayerData(ai2,self._create_new_deck(1),[])
		self.players = [player1,player2]
		self.active_player = 1 # newturn changes the active player having player 2 here results in player1 starting
		self.turn_number = 0
		self.card_drawn = True #was a card drawn this turn?
		self.card = None #card that has to be played this turn
		self.card_played = True #did the player already play his card?
		self.field = self._create_empty_field()
		self.interface = interface

	def _get_top_card_field(self):
		"""
		returns a field with only the top card of every cell
		"""
		return [[cell[-1] if len(cell) >0 else Card(None,None,None) for cell in row] for row in self.field]
	

	def possible_moves(self):
		"""
		returns all moves the active player could make
		every move is a namedtuple of type Move
		"""
		field = self.get_field()
		moves = list()

		for j, row in enumerate(field):
			for i, card in enumerate(row):

				assert card.side in {None,0,1}

				#empty fields or oponents cards
				if card.side != self.active_player:
					continue

				#checking for clashes in the same row
				for i2,card2 in enumerate(row):

					#empty fields or oponents cards
					if card2.side != self.active_player:
						continue

					#same card
					if i == i2:
						continue

					#every card should only be there once
					assert card != card2 or card.side == None

					if card.character == card2.character or card.number == card2.number:
						moves.append(Move((i,j),(i,j+1)))

				#checking for clashes in the same column
				for j2,row2 in enumerate(field):
					card2 = row2[i]

					#empty fields or oponents cards
					if card2.side != self.active_player:
						continue

					#same card
					if j == j2:
						continue

					#every card should only be there once
					assert card != card2 or card.side == None

					if card.character == card2.character or card.number == card2.number:
						moves.append(Move((i,j),(i+1,j)))

		return set(moves)

	def move_is_legal(self,move):
		"""
		is this move legal? returns true or false
		move must be of type Move
		use self.create_Move() to create one
		"""
		assert isinstance(move,Move)

		if move in self.possible_moves():
			return True
		else:
			return False

	@staticmethod
	def _mirror_coords(i,j):
		"""
		mirrors all coordinates, so that player2 sees the field like player1
		"""
		# 5 means a move outside of the field => point for the opponent
		assert i in {0,1,2,3,4,5}
		assert j in {0,1,2,3,4,5}
		return 4-i,4-j
		return 4-j,4-i

	def _get_reversed_top_card_field(self):
		"""
		mirrors the field
		Player2s home field is 44, but should look like 00 to him
		"""
		field = self._get_top_card_field()
		#i = column j = row
		mirrored_field = [[field[Gamestate._mirror_coords(i,j)[1]][Gamestate._mirror_coords(i,j)[0]] for i in range(5)] for j in range(5)]
		return mirrored_field
					

	def _create_empty_field(self):
		#i = column j = row
		return [[[Card(None,None,None)] for i in range(5)] for j in range(5)]
 

	def _get_ac_player(self):
		"""
		returns the PlayerData of the active player
		"""
		return self.players[self.active_player]

	def _get_nac_player(self):
		"""
		returns the PlayerData of the non active player
		"""
		assert self.active_player in {None,0,1}

		result = self.players[1-self.active_player]

		assert result != self._get_ac_player()

		return result

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

		assert self.card_played == True
		self.card_played = False

		#hook for interface commands
		self.interface.start_of_turn(self)

	def _draw_card(self):
		"""
		removes the front card of the deck of the active players
		"""
		#check that it is the first draw of the turn
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

	def create_Move(self,si,sj,ei,ej):
		"""
		create a Move namedtuple
		move from si,sj to ei,ej
		"""
		return Move((si,sj),(ei,ej))


	def set_card(self,i,j):
		"""
		sets the drawn card at position i,j
		i,j elem of (0,0)(0,1)(1,0)
		"""

		#every card must nor be set more than once
		assert self.card_played == False
		self.card_played = True

		#card has to be set on a starting field
		assert (i,j) == (0,0) or (i,j) == (1,0) or (i,j) == (0,1)

		#mirror coords for player2
		if self.active_player == 1:
			i,j = Gamestate._mirror_coords(i,j)

		self.field[j][i].append(self.card)
		
		#interface hook
		self.interface.after_card_set(self)

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

	def get_points(self):
		"""
		returns a namedtuple with the points of both players
		"""

		Points = collections.namedtuple("Points",["Player1","Player2"])

		return Points(*[len(player.cards_won) for player in self.players])

	def make_Move(self,move):
		"""
		commits move
		"""
		# you have to set a card first
		assert self.card_played == True

		assert isinstance(move,Move)
		assert self.move_is_legal(move)

		start = move.start
		end = move.end

		if self.active_player == 1:
			start = Gamestate._mirror_coords(start[0],start[1])
			end = Gamestate._mirror_coords(end[0],end[1])


		cell = self.field[start[1]][start[0]]

		# the following assertions are probably redundant
		# there has to be a card on the field
		assert len(cell) > 0

		# getting top card
		card = cell.pop()

		#card must not be a placeholder
		assert card != Card(None,None,None)

		# card has to be owned by the active player
		assert card.side == self.active_player

		#reached opponents start fields
		if move.end in {(4,4),(3,4),(4,3)}:
			self._get_ac_player().cards_won.append(card)
		#moved out of the field
		elif move.end[0] in {5}  or move.end[1] in {5}:
			self._get_nac_player().cards_won.append(card)
		else:
			self.field[end[1]][end[0]].append(card)

		self.interface.after_move(self)


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
	print(g.set_card(0,0))
	g._new_turn()
	print(g.set_card(0,1))
	g._new_turn()
	print(g.set_card(0,1))
	print(g._get_top_card_field())
	print(g.possible_moves())


