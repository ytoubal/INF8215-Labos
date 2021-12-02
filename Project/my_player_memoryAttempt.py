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
import random

def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class MyAgent(Agent):

    state_table_pawn = [[random.randint(0, 2**64) for _ in range(10)] for _ in range(10)]
    state_table_horizontal_wall = [[random.randint(0, 2**64) for _ in range(10)] for _ in range(10)]
    state_table_vertical_wall = [[random.randint(0, 2**64) for _ in range(10) ] for _ in range(10)] 
    min_values_map = {}
    max_values_map = {}

    def calculate_hash(self, board):
        hash = 0
        for (x,y) in board.pawns:
            hash ^= self.state_table_pawn[x][y]

        for (x,y) in board.horiz_walls:
            hash ^= self.state_table_horizontal_wall[x][y]

        for (x,y) in board.verti_walls:
            hash ^= self.state_table_vertical_wall[x][y]

        return hash

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
        
        board = dict_to_board(percepts)
        #hardcode start
        if step < 7 and board.nb_walls[0]+board.nb_walls[1] == 20 :
            try:
                (x, y) = board.get_shortest_path(player)[0]
            except NoPath:
                print("NO PATH 1 play()")
            return ('P', x, y)
        elif step < 5 and board.nb_walls[0]+board.nb_walls[1] < 20:
            try:
                (x, y) = board.get_shortest_path(player)[0]
            except NoPath:
                print("NO PATH 1 play()")
            return ('P', x, y)
        #alpha beta
        else :
            if time_left >= 45 and board.nb_walls[player] > 0:
                value, action = self.h_alphabeta_search(board, player, step,time_left)
                print(value, action)
            else:
                try:
                    (x, y) = board.get_shortest_path(player)[0]
                except NoPath:
                    print("NO PATH 2 play()")
                action = ('P', x, y)
        return action
    
    def cutoff_depth(d):
        """A cutoff function that searches to depth d."""
        #TODO ameliorer
        def cutoff(game, state, step, depth, start_time, time_left):
            current_time = time.time()
            # 5 seconds to search
            if current_time - start_time >= 5:
                #print("time limit > 5s: ", current_time - start_time)
                return True
            
            #Consider a lower depth if time_left is lower than 100secs or if at start of game
            if step < 7 or time_left < 100:
                return depth >= 2
            return depth > d
        
        return cutoff

    def heuristic():
        #TODO ameliorer

        def estimate_score(game:Board , state: Board, player):
            opponent = (player + 1) % 2
            try:
                 my_score = 10*state.get_score(player) #difference between lengths of my shortest path and of my opponent
            except NoPath:
                print("NO PATH estimate_score")
           
            my_score += 3*((game.nb_walls[player]) - (game.nb_walls[opponent])) 
            
            #If no walls left and player lost
            if game.nb_walls[player] == 0 and my_score < 0:
                my_score -= 100
            if game.nb_walls[opponent] == 0 and my_score > 0:
                my_score += 100

            if state.pawns[player][0] == state.goals[player]: my_score += 1000
            elif state.pawns[opponent][0] == state.goals[opponent]: my_score -= 1000

            return my_score
    
        return estimate_score

    def get_actions():

        def filter_wall_moves(wall_moves, game, state: Board, other_player, threshold=3):
            best_wall_moves = []
            position_opponent = state.pawns[other_player]
            states = game.get_shortest_path(other_player)
            
            for wall_move in wall_moves:
                (_, x, y) = wall_move
                #walls close to opponent
                position_from_opponent = manhattan([x,y], position_opponent)
                if position_from_opponent <= threshold and (x,y) in states:
                    best_wall_moves.append(wall_move)
            
            return best_wall_moves

        def filter_actions(game, state: Board, player):
            actions_to_explore = []
            all_pawn_moves = state.get_legal_pawn_moves(player)
            all_wall_moves = state.get_legal_wall_moves(player)

            other_player = (player + 1) % 2

            if state.nb_walls[player] < 7:
                actions_to_explore.extend(filter_wall_moves(all_wall_moves, game, state, other_player, 6))
            else:
                actions_to_explore.extend(filter_wall_moves(all_wall_moves, game, state, other_player))

            actions_to_explore.extend(all_pawn_moves)
            
            return actions_to_explore 

        return filter_actions

    def h_alphabeta_search(self, game: Board, player, step, time_left, cutoff=cutoff_depth(25), heuristic=heuristic(), actions = get_actions()):
        start = time.time()

        def max_value(state: Board, alpha, beta, depth):
            hash = self.calculate_hash(state)
            if hash in self.max_values_map:
                return self.max_values_map[hash]

            if cutoff(game, state, step, depth, start, time_left):
                return heuristic(game,state, player), None

            if state.is_finished():
                return state.get_score(player), None

            v_star = -math.inf
            m_star = None
            for action in actions(game, state, player):
                clone = state.clone()
                clone.play_action(action, player)
                next_state = clone
                v,_ = min_value(next_state, alpha, beta, depth+1)
                if v > v_star:
                    v_star = v 
                    m_star = action
                    alpha = max(alpha, v_star)
                if v >= beta: 
                    self.max_values_map[hash] = v_star, m_star
                    return v_star,m_star
            self.max_values_map[hash] = v_star, m_star
            return v_star,m_star

        def min_value(state: Board, alpha, beta, depth):
            hash = self.calculate_hash(state)
            if hash in self.min_values_map:
                return self.min_values_map[hash]
            
            if cutoff(game, state, step, depth, start, time_left):
                return heuristic(game,state, player), None

            if state.is_finished():
                return state.get_score(player), None

            v_star = math.inf
            m_star = None
            for action in actions(game, state, player):
                clone = state.clone()
                clone.play_action(action, player)
                next_state = clone
                v,_ = max_value(next_state, alpha, beta, depth+1)
                if v < v_star:
                    v_star = v
                    m_star = action
                    beta = min(beta, v_star)
                if v <= alpha: 
                    self.min_values_map[hash] = v_star, m_star
                    return v_star,m_star
            self.min_values_map[hash] = v_star, m_star
            return v_star,m_star

        return max_value(game, -math.inf, +math.inf, 0)

if __name__ == "__main__":
    agent_main(MyAgent())