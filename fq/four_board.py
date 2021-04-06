import copy
from fq.four_types import Player, Point
from collections import defaultdict

class Move():
    '''
    All possible actions that a player can do:
    - play a disk on the board

    To construct an instace of a move you call Move.play
    '''
    def __init__(self, point = None):
        assert (point is not None) 
        self.point = point
        # To play you actually need to pass a Point for a stone to be placed 
        self.is_play = (self.point is not None)    
        
    @classmethod
    def play(cls, point):
        # Place a disk on the board
        return Move(point=point)

class Board():
    '''
    A board is initialized as an empty grid with the specified number of
    rows and columns.
    '''
    def __init__(self,num_rows,num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}
        self._grid_v2 = defaultdict(list) #private dict to store strings of stone
        for i in range(1,num_cols+1):
            self._grid_v2[i] = list()
    
    def _is_full(self):
        return True if sum([len(i) for i in self._grid_v2.values()]) == self.num_rows*self.num_cols else False

    def retrieve_point(self,column):
        if column not in self._grid_v2:
            return Point(column,1)
        return Point(column,len(self._grid_v2[column]))

    def place_disk(self,player,point):

        assert self.is_on_grid(point) # Check if the point is on the board
        assert self.is_legal_move(point) # Check if column is already full
        assert self._grid.get(point) is None
        self._grid_v2[point.col].append(player)
        self._grid[point] = player

    def is_legal_move(self, point):
        return True if (point.row <= self.num_rows) and (1 <= point.col <= self.num_cols) else False

    def is_on_grid(self,point):
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def is_full(self):
        print(self._grid_v2)
        return True if self.num_cols * self.num_rows == sum([len(row) for _,row in self._grid_v2.items()]) else False
    
    def is_victory(self,point,player):
        return True if self.longest_line(point,player) >= 3 else False

    def longest_line(self,point,player):
        row,col = point.row-1,point.col
        directions = ['vertical','horizontal','oblique_r','oblique_l']
        #print([self.find_neighbors(direction,row,col,player) for direction in directions])
        return max([self.find_neighbors(direction,row,col,player) for direction in directions])

    def get(self,point):
        '''
        Returns the content of a point on the board:
        - A player is a stone is on that point
        - or else None
        '''
        v = self._grid.get(point)
        if v is None:
            return None
        return v


    def find_neighbors(self,direction,row,col,player):
        number_neighbors = 0
        if direction == 'vertical':
            row -= 1
            while row >= 0:
                try:
                    if self._grid_v2[col][row] == player:
                        number_neighbors += 1
                    else:
                        break
                    row -= 1
                except:
                    break
        elif direction == 'horizontal':
            l_col, r_col = col, col
            l_col -= 1
            r_col += 1
            while l_col >= 1:
                try:
                    if self._grid_v2[l_col][row] == player:
                        number_neighbors +=1
                    else:
                        break
                    l_col -= 1
                except:
                    break
            while r_col <= self.num_cols:
                try:
                    if self._grid_v2[r_col][row] == player:
                        number_neighbors +=1
                    else:
                        break
                except:
                    break
                r_col += 1
        
        elif direction == 'oblique_r':
            
            l_col, r_col = col, col
            d_row, u_row = row, row
            l_col -= 1
            r_col += 1
            d_row -= 1
            u_row += 1

            while l_col >= 1 and d_row >= 0:
                try:
                    if self._grid_v2[l_col][d_row] == player:
                        number_neighbors +=1
                    else:
                        break
                    l_col -= 1
                    d_row -= 1
                except:
                    break
            while r_col <= self.num_cols and u_row <= self.num_rows:
                try:
                    if self._grid_v2[r_col][u_row] == player:
                        number_neighbors +=1
                    else:
                        break
                except:
                    break
                r_col += 1
                u_row += 1

        elif direction == 'oblique_l':
            
            l_col, r_col = col, col
            d_row, u_row = row, row
            l_col -= 1
            r_col += 1
            d_row -= 1
            u_row += 1

            while l_col >= 1 and u_row <= self.num_rows:
                try:
                    if self._grid_v2[l_col][u_row] == player:
                        number_neighbors +=1
                    else:
                        break
                    l_col -= 1
                    u_row += 1
                except:
                    break
            while r_col <= self.num_cols and d_row >= 0:
                try:
                    if self._grid_v2[r_col][d_row] == player:
                        number_neighbors +=1
                    else:
                        break
                except:
                    break
                r_col += 1
                d_row -= 1        
        return number_neighbors





class GameState():
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    def apply_move(self,move):
        '''
        Return the new GameState after applying the move
        '''
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_disk(self.next_player,move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, move)
    
    @classmethod
    def new_game(cls, num_rows,num_cols):
        '''
        If new game, initialise the board and first player is black
        '''
        board = Board(num_rows, num_cols)
        return GameState(board, Player.red, None)

    def is_over(self,point,player):

        if self.board.is_victory(point,player):
            return True
        if self.board._is_full():
            return True
        return False

    @property
    def situation(self):
        return (self.next_player,self.board)
    

    def is_valid_move(self, move,player):
    #    if self.is_over(move.point,player):
    #        return False
        return self.board.get(move.point) is None
    

    