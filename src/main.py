#!/usr/bin/env python3

import Gamestate as Gamestate
import interface as interface
import sampleai as  randomai


ai1 = randomai.sampleai()
ai2 = randomai.sampleai()


g = Gamestate.Gamestate(ai1,ai2)
t = interface.terminal()



while True:
	g._new_turn()
	player = g._get_ac_player()
	player.ai.set_card(g)
	t._display_field(g)
	player.ai.move(g)
	t._display_field(g)
	#input()




