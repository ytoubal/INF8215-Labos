#!/usr/bin/env python3
"""
Greedy Quoridor agent.
Copyright (C) 2021, École Polytechnique de Montréal

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

from quoridor import *
import random


class GreedyAgent(Agent):

    """
    A Greedy agent.
    It will take the shortest path 75% of the time and place a wall in front of the other player 25% of the time.
    """

    def play(self, percepts, player, step, time_left):
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in quoridor.py.
        :param player: the player to control in this step (0 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
          eg: ('P', 5, 2) to move your pawn to cell (5,2)
          eg: ('WH', 5, 2) to put a horizontal wall on corridor (5,2)
          for more details, see `Board.get_actions()` in quoridor.py
        """
        print("-"*20)

        board = dict_to_board(percepts)

        # current position
        print(f"current position: {board.pawns[player]}")
        print(f"opponent position: {board.pawns[1-player]}")

        # 25% of the time, place a wall in front of other player
        if random.random() <= 0.25:
            # opponent position
            oppo_y, oppo_x = board.pawns[1-player]
            # opponent goal
            oppo_goal_y = board.goals[1-player]
            # set of legal wall moves
            wall_actions = board.get_legal_wall_moves(player)

            # find valid walls in front of opponent
            candidate_walls = []
            if oppo_goal_y < oppo_y:
                print("opponent moving north")
                for wall_action in wall_actions:
                    wall_dir, wall_y, wall_x = wall_action
                    if wall_dir == 'WH' and wall_y == oppo_y - 1 and wall_x in (oppo_x, oppo_x - 1):
                        candidate_walls.append(wall_action)
            else:
                print("opponent moving south")
                for wall_action in wall_actions:
                    wall_dir, wall_y, wall_x = wall_action
                    if wall_dir == 'WH' and wall_y == oppo_y and wall_x in (oppo_x, oppo_x - 1):
                        candidate_walls.append(wall_action)
            print(f"candidate walls: {candidate_walls}")

            if len(candidate_walls) > 0:
                choice = random.choice(candidate_walls)
                print(f"placing a wall: {choice}")
                return choice
            else:
                print(f"cannot put a wall in front of opponent. will move pawn instead.")

        # if I reach this line, either we didn't try to put a wall,
        # or it's not possible to put a wall in front of opponent.

        # set of legal pawn moves
        pawn_actions = board.get_legal_pawn_moves(player)
        print(f"possible moves: {pawn_actions}")

        # list of future positions
        shortest_path = board.get_shortest_path(player)
        print(f"shortest path: {shortest_path}")

        next_y, next_x = shortest_path[0]
        next_move = ('P', next_y, next_x)
        return next_move


if __name__ == "__main__":
    agent_main(GreedyAgent())
