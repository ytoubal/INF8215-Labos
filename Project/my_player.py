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
import utils
from quoridor import *


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
        #print("percept:", percepts)
        #print("player:", player)
        #print("step:", step)
        #print("time left:", time_left if time_left else '+inf')

        # TODO: implement your agent and return an action for the current step.
        
        board = dict_to_board(percepts)
        #hardcode start
        if step < 7 and board.nb_walls[0]+board.nb_walls[1] == 20 :
            (x, y) = board.get_shortest_path(player)[0]
            return ('P', x, y)
        #alpha beta
        else :
            if time_left >= 30:
                value, action = self.h_alphabeta_search(board, player, step,time_left)
                #print(value, action)
            else:
                (x, y) = board.get_shortest_path(player)[0]
                action = ('P', x, y)
        return action
    
    def cutoff_depth(d):
        """A cutoff function that searches to depth d."""
        #TODO ameliorer
        def cutoff(game, state, step, depth, start_time, time_left):
            current_time = time.time()
            #20 seconds to search
            if current_time - start_time >= 5:
                #print("time limit > 5s: ", current_time - start_time)
                return True
            #We consider a lower depth (2) if the time_left is lower than 2 minutes
            #Or if we are at the very begining of the game.
            if step < 7 or time_left < 120:
                return depth >= 2
            return depth > d
        
        return cutoff

    def heuristic():
        #TODO ameliorer

        def estimate_score(game:Board , state: Board, player):
            opponent = (player + 1) % 2
            my_score = state.get_score(player) #difference between lengths of my shortest path and of my opponent
            print('score BEFORE WALLSSSSSS: ', my_score)
            #Consider the remaining walls of each player.
            #It helps the AI not to waste all its walls and try to save them.
            my_score += ((game.nb_walls[player]) - (game.nb_walls[opponent])) 
            #If no walls left and player lost
            # if game.nb_walls[player] == 0 and my_score < 0:
            #     my_score -= 1
            # if game.nb_walls[(player+1)%2] == 0 and my_score > 0:
            #     my_score += 1
            if state.pawns[player][0] == state.goals[player]: my_score += 1000
            elif state.pawns[opponent][0] == state.goals[opponent]: my_score -= 1000
            print('score: ', my_score)
            return my_score
    
        return estimate_score

    def get_actions():

        def filter_wall_moves(wall_moves, state: Board, other_player):
            best_wall_moves = []
            #best_wall_moves = wall_moves
            position_opponent = state.pawns[other_player]
            #print("START", len(wall_moves))
            for wall_move in wall_moves:
                (_, x, y) = wall_move
                #walls close to opponent
                position_from_opponent = utils.manhattan([x,y], position_opponent)
                if position_from_opponent <= 3:
                    best_wall_moves.append(wall_move)
            #print("END", len(best_wall_moves))
            return best_wall_moves

        def filter_actions(state: Board, player):
            #all_actions = state.get_actions(player)
            actions_to_explore = []
            all_pawn_moves = state.get_legal_pawn_moves(player)
            all_wall_moves = state.get_legal_wall_moves(player)

            other_player = (player + 1) % 2

            #player_steps_victory = state.min_steps_before_victory(player)
            #adv_steps_victory = state.min_steps_before_victory(other_player)

            #if player_steps_victory < adv_steps_victory:
                #actions_to_explore.extend(all_pawn_moves)       
            #elif player_steps_victory > adv_steps_victory:
                #actions_to_explore.extend(filter_wall_moves(all_wall_moves, #state, other_player))
            #else:
            actions_to_explore.extend(filter_wall_moves(all_wall_moves, state, other_player))
            actions_to_explore.extend(all_pawn_moves)
            
            #print("player", player)
            #print("PAWN", player_steps_victory)
            #print("WALL", adv_steps_victory)
            #print("STATE PLAYER")
            #print(state, player)
            return actions_to_explore 

        return filter_actions

    def h_alphabeta_search(self, game: Board, player, step, time_left, cutoff=cutoff_depth(25), heuristic=heuristic(), actions = get_actions()):
        start = time.time()

        def max_value(state: Board, alpha, beta, depth):
            if cutoff(game, state, step, depth, start, time_left):
                return heuristic(game,state, player), None

            if state.is_finished():
                return state.get_score(player), None

            v_star = -math.inf
            m_star = None
            for action in actions(state, player):
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
            if cutoff(game, state, step, depth, start, time_left):
                return heuristic(game,state, player), None

            if state.is_finished():
                return state.get_score(player), None

            v_star = math.inf
            m_star = None
            for action in actions(state, player):
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

if __name__ == "__main__":
    agent_main(MyAgent())
