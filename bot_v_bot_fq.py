import time
from collections import defaultdict
import random
from fq import agent
from fq import four_board
from fq import four_types
from fq.utils import print_board, print_move

def main():
    l = defaultdict(int)
    nr_rows = 6
    nr_cols = 7
    game = four_board.GameState.new_game(nr_rows,nr_cols)
    bots = {
        four_board.Player.red: agent.naive.RandomBot(),
        four_board.Player.yellow: agent.naive.RandomBot(),
    }
    
    #print_board(game.board)
    
    
    while not game.board._is_full():
        time.sleep(0.5)
        
        player = game.next_player
        bot_move = bots[player].select_move(game)
        print_move(game.next_player, bot_move)
        if game.board.is_victory(bot_move.point,player):
            game = game.apply_move(bot_move)
            l[player]+=1
            print_board(game.board)
            print('Winner is ',player)
            break
        game = game.apply_move(bot_move)
        print_board(game.board)



if __name__ == '__main__':
    main()