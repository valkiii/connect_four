import random
from fq.agent.base import Agent
from fq.four_board import Move
from fq.four_types import Point

class RandomBot(Agent):
    def select_move(self, game_state):
        '''
        Choose a random valid move 
        '''
        candidates = []
        for c in range(1, game_state.board.num_cols +1):
            candidate = Point(row=len(game_state.board._grid_v2[c])+1,col=c)
            if game_state.is_valid_move(Move.play(candidate),game_state.next_player) \
            and game_state.board.is_legal_move(candidate):
                candidates.append(candidate)
        if len(candidates) == 0:
            exit()
        return Move.play(random.choice(candidates))
        