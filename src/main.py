#!/usr/bin/env python3

import argparse

import Gamestate as Gamestate
import Interface
import Ai
from tools import factory

ai_factory = factory.Factory(Ai.sampleai.sampleai)

parser = argparse.ArgumentParser(description = "Ebbe und Flut main program")

player_options = [cls.__name__ for cls in ai_factory]
parser.add_argument("player1",
			choices = player_options,
			help = "Choose an ai for player1")
parser.add_argument("player2",
			choices = player_options,
			help = "Choose an ai for player2")


FLAGS = parser.parse_args()

ai1 = Ai.sampleai.sampleai()
ai2 = Ai.sampleai.sampleai()



t = Interface.interface.terminal()
g = Gamestate.Gamestate(ai1=ai1,ai2=ai2,interface=t)


while True:
	g._new_turn()
	player = g._get_ac_player()
	player.ai.set_card(g)
	player.ai.move(g)
	#input()




