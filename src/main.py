#!/usr/bin/env python3

import Gamestate as Gamestate
import Interface
import Ai


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




