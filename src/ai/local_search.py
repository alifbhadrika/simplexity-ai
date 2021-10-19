import random
from time import time

from src.constant import *
from src.model import *
from src.utility import *

from typing import Tuple, List


class LocalSearch:
    def __init__(self):
        self.currValue = 0

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        curr = state
        board = curr.board

        
        succs = fillAble(board)
        
        #generate col for best move
        foundSucc = False
        i = 0
        while(i < len(succs) and not foundSucc):
            succValue = eval(curr, n_player, succs[i])
            if (succValue > self.currValue):
                foundSucc = True
                self.currValue = succValue
                break
            i+=1
   
        #generate shape for best move
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
    
        if (foundSucc):
            bestMove = (succs[i][1], sep)

        #buat tes masuk foundsucc apa kaga dan ngecek eval tu ngasilin berapa aja si
        s = 0
        for succ in succs:
            s += eval(curr, n_player, succ)
        bestMove = (s, sep)
        return bestMove



def fillAble(board: Board) -> List[Tuple[int, int]]:
    out = dict()
    for x in range(board.row-1, -1, -1):
        if len(out.keys()) == board.col:
            break
        for y in range(board.col):
            if board[x,y] == Piece(ShapeConstant.BLANK, ColorConstant.BLACK):
                if str(y) in out.keys(): 
                    continue
                out[str(y)] = x
            else:
                if x == 0:
                    out[str(y)] = -1
    out2 = []
    for key in out.keys():
        out2.append([out[key], int(key)])
        
    return out2

def eval(state : State, n_player: int, nextMove : Tuple[int, int]) -> int: #heuristic func
    board = state.board
    players = state.players
    player1_id = n_player
    player2_id = int(not n_player)
    player1 = players[player1_id]
    player2 = players[player2_id]

    bisadiisi = []
    bisadiisi.append(nextMove)
    skor = 0

    # get horizontal
    for x,y in bisadiisi:
        if (x==-1): continue #gbs diisi

        #cek kanan
        if y+3<board.col:
            if board[x,y+1] == player1:
                if board[x,y+2] == player1 and board[x,y+3] == player1:
                    skor += 100
                elif board[x,y+2] == player1:
                    skor += 10
                else:
                    skor += 5
            else:
                if board[x,y+1].shape == player2.shape and board[x,y+2].shape == player2.shape and board[x,y+3].shape == player2.shape:
                    skor -= 20
                elif (board[x,y+1].shape == player1.shape and board[x,y+1].color == player2.color and
                    board[x,y+2].shape == player1.shape and board[x,y+3].color == player2.color and
                    board[x,y+3].shape == player1.shape and board[x,y+3].color == player2.color):
                    skor -= 7
        #cek kiri
        if y-3>=0:
            if board[x,y-1] == player1:
                if board[x,y-2] == player1 and board[x,y-3] == player1:
                    skor += 100
                elif board[x,y-2] == player1:
                    skor += 10
                else:
                    skor += 5
            else:
                if board[x,y-1].shape == player2.shape and board[x,y-2].shape == player2.shape and board[x,y-3].shape == player2.shape:
                    skor -= 20
                elif (board[x,y-1].shape == player1.shape and board[x,y-1].color == player2.color and
                    board[x,y-2].shape == player1.shape and board[x,y-3].color == player2.color and
                    board[x,y-3].shape == player1.shape and board[x,y-3].color == player2.color):
                    skor -= 7

    # get vertical
    for x,y in bisadiisi:
        if(x==-1): continue
        #cek bawah
        if x+3<board.row:
            if board[x+1,y] == player1:
                if board[x+2,y] == player1 and board[x+3,y] == player1:
                    skor += 100
                elif board[x+2,y] == player1:
                    skor += 10
                else:
                    skor += 5
            else:
                if board[x+1,y].shape == player2.shape and board[x+2,y].shape == player2.shape and board[x+3,y].shape == player2.shape:
                    skor -= 20
                elif (board[x+1,y].shape == player1.shape and board[x+1,y].color == player2.color and
                    board[x+2,y].shape == player1.shape and board[x+2,y].color == player2.color and
                    board[x+3,y].shape == player1.shape and board[x+3,y].color == player2.color):
                    skor -= 7


    # get diagonal+
    for x,y in bisadiisi:
        if (x==-1): continue #gbs diisi
        if x-3>=0 and y+3<board.col:
            if board[x-1,y+1] == player1:
                if board[x-2,y+2] == player1 and board[x-3,y+3] == player1:
                    skor += 100
                elif board[x-2,y+2] == player1:
                    skor += 10
                else:
                    skor += 5
            else:
                if board[x-1,y+1].shape == player2.shape and board[x-2,y+2].shape == player2.shape and board[x-3,y+3].shape == player2.shape:
                    skor -= 20
                elif (board[x-1,y+1].shape == player1.shape and board[x-1,y+1].color == player2.color and
                    board[x-2,y+2].shape == player1.shape and board[x-2,y+3].color == player2.color and
                    board[x-3,y+3].shape == player1.shape and board[x-3,y+3].color == player2.color):
                    skor -= 7
        if x+3<board.row and y-3>=0:
            if board[x+1,y-1] == player1:
                if board[x+2,y-2] == player1 and board[x+3,y-3] == player1:
                    skor += 100
                elif board[x+2,y-2] == player1:
                    skor += 10
                else:
                    skor += 5
            else:
                if board[x+1,y-1].shape == player2.shape and board[x+2,y-2].shape == player2.shape and board[x+3,y-3].shape == player2.shape:
                    skor -= 20
                elif (board[x+1,y-1].shape == player1.shape and board[x+1,y-1].color == player2.color and
                    board[x+2,y-2].shape == player1.shape and board[x+2,y-3].color == player2.color and
                    board[x+3,y-3].shape == player1.shape and board[x+3,y-3].color == player2.color):
                    skor -= 7
    # get diagonal-
    for x,y in bisadiisi:
        if (x==-1): continue #gbs diisi
        if x+3<board.row and y+3<board.col:
            if board[x+1,y+1] == player1:
                if board[x+2,y+2] == player1 and board[x+3,y+3] == player1:
                    skor += 100
                elif board[x+2,y+2] == player1:
                    skor += 10
                else:
                    skor += 5
            else:
                if board[x+1,y+1].shape == player2.shape and board[x+2,y+2].shape == player2.shape and board[x+3,y+3].shape == player2.shape:
                    skor -= 20
                elif (board[x+1,y+1].shape == player1.shape and board[x+1,y+1].color == player2.color and
                    board[x+2,y+2].shape == player1.shape and board[x+2,y+3].color == player2.color and
                    board[x+3,y+3].shape == player1.shape and board[x+3,y+3].color == player2.color):
                    skor -= 7
        if x-3>=0 and y-3>=0:
            if board[x-1,y-1] == player1:
                if board[x-2,y-2] == player1 and board[x-3,y-3] == player1:
                    skor += 100
                elif board[x-2,y-2] == player1:
                    skor += 10
                else:
                    skor += 5
            else:
                if board[x-1,y-1].shape == player2.shape and board[x-2,y-2].shape == player2.shape and board[x-3,y-3].shape == player2.shape:
                    skor -= 20
                elif (board[x-1,y-1].shape == player1.shape and board[x-1,y-1].color == player2.color and
                    board[x-2,y-2].shape == player1.shape and board[x-2,y-3].color == player2.color and
                    board[x-3,y-3].shape == player1.shape and board[x-3,y-3].color == player2.color):
                    skor -= 7
    return skor
