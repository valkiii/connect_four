import time
from collections import defaultdict
import random
from fq import agent
from fq import four_board
from fq import four_types
from fq.utils import print_board, print_move, point_from_coords
from six.moves import input

def possible_moves(game,move,point,player):
    candidates = []
    for c in range(1, game.board.num_cols +1):
        candidate = four_types.Point(row=len(game.board._grid_v2[c])+1,col=c)
        if valid_move(game,move,point,player):
            candidates.append(candidate)
    return candidates

def valid_move(game,move,point,player):
    return game.is_valid_move(move,player) and game.board.is_legal_move(point)

def main():
    nr_rows = 6
    nr_cols = 7
    game = four_board.GameState.new_game(nr_rows,nr_cols)
    bot = agent.RandomBot()
    
    print_board(game.board)
    while not game.board._is_full():
        time.sleep(0.1)

        #print(chr(27) + "[2J")
        player = game.next_player
        if player == four_types.Player.yellow:
            flag = True
            while flag:
                human_move = input('')
                point = point_from_coords(human_move.strip())
                if point in possible_moves(game,four_board.Move.play(point),point,player):
                    move = four_board.Move.play(point)
                    flag = False
                else:
                    print('Sorry, the move selected is not permitted. Try again')
        else:
            move = bot.select_move(game)
        
        print_move(player, move)
        if game.board.is_victory(move.point,game.next_player):
            game = game.apply_move(move)
            print_board(game.board)
            print('Winner is ',player)
            break
        game = game.apply_move(move)
        print_board(game.board)


if __name__ == '__main__':
    main()