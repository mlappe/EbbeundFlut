#!/usr/bin/env python3

from terminaltables import SingleTable

class terminal():
	
	def _display_field(self,gamestate):
		field = gamestate._get_top_card_field()
		table = SingleTable(field)
		table.inner_row_border = True
		print(table.table)
		

	def _clear_and_header(self,gamestate):
		
		#clear screen
		print("\033[2J")

		#return cursor to top
		print("\033[H")

		print("Ebbe und Flut")
		print("Turn: "+ str(gamestate.turn_number))
		print(gamestate.get_points())

	def after_move(self,gamestate):
		self._clear_and_header(gamestate)
		print("A move was made")
		self._display_field(gamestate)
		input()

	def start_of_turn(self,gamestate):
		self._clear_and_header(gamestate)
		print("Start of Turn")
		self._display_field(gamestate)
		input()

	def after_card_set(self,gamestate):
		self._clear_and_header(gamestate)
		print("A Card was set")
		self._display_field(gamestate)
		input()


if __name__ == "__main__":
	pass
