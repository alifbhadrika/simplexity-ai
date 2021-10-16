import random
from time import time

from src.constant import *
from src.model import *
from src.utility import *

from typing import Tuple, List
from copy import deepcopy


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        # return best_movement

        best = -1000 #init
        bestmove = (-1,-1)

        # Greedy Shape Selection - kalo mau ubah ini ubah aja, biar ngesimulasiin 2 jenis shape per parent
        # Buat skrg cuma prioritasin generate move buat shape preferensi tiap player sampe shape itu abis, baru ganti shape 
        if(n_player == 0):
            nextp = 1
            if(state.players[n_player].quota[GameConstant.PLAYER1_SHAPE] > 0):
                sep = GameConstant.PLAYER1_SHAPE
            elif(state.players[n_player].quota[GameConstant.PLAYER1_SHAPE] == 0 and state.players[n_player].quota[GameConstant.PLAYER2_SHAPE] > 0 ):
                sep = GameConstant.PLAYER2_SHAPE
        elif(n_player == 1):
            nextp = 0
            if(state.players[n_player].quota[GameConstant.PLAYER2_SHAPE] > 0):
                sep = GameConstant.PLAYER2_SHAPE
            elif(state.players[n_player].quota[GameConstant.PLAYER2_SHAPE] == 0 and state.players[n_player].quota[GameConstant.PLAYER1_SHAPE] > 0 ):
                sep = GameConstant.PLAYER1_SHAPE

        found = False
        while(not found and time() < self.thinking_time):
            for c in range(state.board.col): #Check Available Move
                for r in range(state.board.row - 1,-1,-1):
                    if((state.board[r, c].shape == ShapeConstant.BLANK and r == state.board.row - 1) or (state.board[r, c].shape == ShapeConstant.BLANK and state.board[r + 1,c].shape != ShapeConstant.BLANK and r < state.board.row - 1 )) :
                        piece = Piece(sep, GameConstant.PLAYER_COLOR[n_player])
                        ns = deepcopy(state)
                        ns.board.set_piece(r,c,piece)
                        ns.players[n_player].quota[sep] -= 1
                        tmp = minimax(ns,nextp,False,0,-1000,1000,1)
                        if(tmp >= best):
                            best = tmp
                            bestmove = (c,sep)
                        ns.players[n_player].quota[sep] += 1
                        ns.board.set_piece(r,c,ShapeConstant.BLANK)
                    if(c == state.board.col - 1 and r == 0):
                        found = True

        if(not found): #Random move
            bestmove = (random.randint(0, state.board.col - 1), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
            # print("Called Random")
        return bestmove

def minimax(state : State, n_player:int, isMax, depth, a, b, maxDepth) -> int:
    '''
    Minimax Alpha Beta Pruning Algo
    state : game state
    n_player : which player turn (0/1)
    isMax : boolean, maximizing (True) or minimizing(False) turn
    depth : current search depth
    a : alpha constraint (maximizer current best value)
    b : beta constraint (minimizer current best value)
    maxDepth : max search depth
    '''
    # Greedy Shape Selection - kalo mau ubah ini ubah aja, biar ngesimulasiin 2 jenis shape per parent
    # Buat skrg cuma prioritasin generate move buat shape preferensi tiap player sampe shape itu abis, baru ganti shape
    if(n_player == 0):
        nextp = 1
        if(state.players[n_player].quota[GameConstant.PLAYER1_SHAPE] > 0):
            sep = GameConstant.PLAYER1_SHAPE
        elif(state.players[n_player].quota[GameConstant.PLAYER1_SHAPE] == 0 and state.players[n_player].quota[GameConstant.PLAYER2_SHAPE] > 0 ):
            sep = GameConstant.PLAYER2_SHAPE
    elif(n_player == 1):
        nextp = 0
        if(state.players[n_player].quota[GameConstant.PLAYER2_SHAPE] > 0):
            sep = GameConstant.PLAYER2_SHAPE
        elif(state.players[n_player].quota[GameConstant.PLAYER2_SHAPE] == 0 and state.players[n_player].quota[GameConstant.PLAYER1_SHAPE] > 0 ):
            sep = GameConstant.PLAYER1_SHAPE

    if(depth == maxDepth): # Deepest depth
        return (eval(state, n_player)) #enter obj func here

    elif(depth < maxDepth):
        if(isMax):
            best = -1000
            for c in range(state.board.col): #Check Available Move
                for r in range(state.board.row - 1,-1,-1):
                    if((state.board[r, c].shape == ShapeConstant.BLANK and r == state.board.row - 1) or (state.board[r, c].shape == ShapeConstant.BLANK and state.board[r + 1,c].shape != ShapeConstant.BLANK and r<state.board.row - 1 )):
                        piece = Piece(sep, GameConstant.PLAYER_COLOR[n_player])
                        ns = deepcopy(state)
                        ns.board.set_piece(r,c,piece)
                        ns.players[n_player].quota[sep] -= 1
                        tmp = minimax(ns,nextp,False,depth + 1,a,b,maxDepth)
                        if(tmp >= best):
                            best = tmp
                        a = max(a,best)
                        ns.players[n_player].quota[sep] += 1
                        ns.board.set_piece(r,c,ShapeConstant.BLANK)
                        if(b <= a):
                            break
            return best

        else : # minimizing
            best = 1000
            for c in range(state.board.col):
                for r in range(state.board.row - 1,-1,-1):
                    if((state.board[r, c].shape == ShapeConstant.BLANK and r == state.board.row - 1) or (state.board[r, c].shape == ShapeConstant.BLANK and state.board[r + 1,c].shape != ShapeConstant.BLANK and r<state.board.row - 1 )):
                        piece = Piece(sep, GameConstant.PLAYER_COLOR[n_player])
                        ns = deepcopy(state)
                        ns.board.set_piece(r,c,piece)
                        ns.players[n_player].quota[sep] -= 1
                        tmp = minimax(ns,nextp,True,depth + 1,a,b,maxDepth)
                        if(tmp <= best):
                            best = tmp
                        b = min(b,best)
                        ns.players[n_player].quota[sep] += 1
                        ns.board.set_piece(r,c,ShapeConstant.BLANK)
                        if(b <= a):
                            break
            return best

def eval(state : State, n_player: int) -> int: #obj func
    board = state.board
    players = state.players
    player1_id = n_player
    player2_id = int(not n_player)
    player1 = players[player1_id]
    player2 = players[player2_id]
    player1_shape = player1.shape
    player1_color = player1.color
    player2_shape = player2.shape
    player2_color = player2.color

    # get horizontal
    # get vertical
    # get diagonal+
    # get diagonal-