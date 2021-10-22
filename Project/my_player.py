#!/usr/bin/env python3
"""
Quoridor agent.
Copyright (C) 2013, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>

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

import math
import time
from quoridor import *

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    #TODO ameliorer
    def cutoff(game, state, depth, start_time):
        current_time = time.time()
        #20 seconds to search
        if current_time - start_time >= 5:
            print("time limit > 5s: ", current_time - start_time)
            return True
        return depth > d
    
    return cutoff

def heuristic():
    #TODO ameliorer
    def estimate_score(game:Board , state: Board, player):
        
        return state.get_score(player)
    
    return estimate_score

def h_alphabeta_search(game: Board, player, cutoff=cutoff_depth(50), heuristic=heuristic()):
        start = time.time()

        def max_value(state: Board, alpha, beta, depth):
            if cutoff(game, state, depth, start):
                return heuristic(game,state, player), None

            if state.is_finished():
                return state.get_score(player), None

            v_star = -math.inf
            m_star = None
            for action in state.get_actions(player):
                clone = state.clone()
                clone.play_action(action, player)
                next_state = clone
                v,_ = min_value(next_state, alpha, beta, depth+1)
                if v > v_star:
                    v_star = v
                    m_star = action
                    alpha = max(alpha, v_star)
                if v >= beta: return v_star,m_star
            return v_star,m_star

        def min_value(state: Board, alpha, beta, depth):
            # TODO: include a recursive call to max_value function
            if cutoff(game, state, depth, start):
                return heuristic(game,state, player), None

            if state.is_finished():
                return state.get_score(player), None

            v_star = math.inf
            m_star = None
            for action in state.get_actions(player):
                clone = state.clone()
                clone.play_action(action, player)
                next_state = clone
                v,_ = max_value(next_state, alpha, beta, depth+1)
                if v < v_star:
                    v_star = v
                    m_star = action
                    beta = min(beta, v_star)
                if v <= alpha: return v_star,m_star
            return v_star,m_star

        return max_value(game, -math.inf, +math.inf, 0)

class MyAgent(Agent):

    """My Quoridor agent."""

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
        print("percept:", percepts)
        #print("player:", player)
        #print("step:", step)
        print("time left:", time_left if time_left else '+inf')

        # TODO: implement your agent and return an action for the current step.
        
        board = dict_to_board(percepts)
        #hardcode start
        if step < 7 and 18 <= board.nb_walls[0]+board.nb_walls[1] <= 20 :
            (x, y) = board.get_shortest_path(player)[0]
            return ('P', x, y)
        #alpha beta
        else :
            if time_left >= 30:
                value, action = h_alphabeta_search(board, player)
                print(value, action)
            else:
                (x, y) = board.get_shortest_path(player)[0]
                action = ('P', x, y)
        return action
    

if __name__ == "__main__":
    agent_main(MyAgent())
