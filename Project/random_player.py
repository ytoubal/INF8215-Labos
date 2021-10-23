#!/usr/bin/env python3
"""
Dummy random Quoridor agent.
Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
Copyright (C) 2013, Université catholique de Louvain

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

import random
from quoridor import *


class RandomAgent(Agent):

    """A dumb random Quoridor agent."""
    def play(self, percepts, player, step, time_left):
        board = dict_to_board(percepts)
        actions = list(board.get_actions(player))
        print('step', step, 'player', player, 'actions', len(actions))
        return random.choice(actions)


if __name__ == "__main__":
    agent_main(RandomAgent())
