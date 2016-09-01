#!/usr/bin/env python3

from terminaltables import SingleTable

class terminal():
	
	def _display_field(self,gamestate):
		field = gamestate.get_field()
		table = SingleTable(field)
		table.inner_row_border = True
		print(table.table)

if __name__ == "__main__":
	pass
