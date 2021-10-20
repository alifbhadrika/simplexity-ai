import random
from time import time

from src.constant import *
from src.model import *
from src.utility import *

from typing import Tuple, List
from copy import deepcopy


class LocalSearchGroup44:
    def __init__(self):
        self.currValue = 0

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        timeout = self.thinking_time < time()
        temp = self.currValue

        curr = state
        board = curr.board

        
        succs = fillAble(board)
        
        #generate col for best move
        foundSucc = False
        i = 0

        neighbor = []
        while(i < len(succs) and not foundSucc and not timeout):
            succValue = eval(curr, n_player, succs[i])
            neighbor.append([succValue, succs[i][1], succs[i][0]])
            i+=1
            timeout = self.thinking_time < time()
        
        neighbor.sort(key=lambda x: x[0])

        succValue = neighbor[-1][0]

        if (succValue >= self.currValue and neighbor[-1][2] != -1):
            foundSucc = True
            self.currValue = succValue
            i = -1
        else:
            foundSucc = True
            i = len(neighbor)-2
            while (i >= 0 and neighbor[i][2] == -1):
                i-=1
            self.currValue = neighbor[i][0]

   
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
            bestMove = (neighbor[i][1], sep)
        if (timeout):
            bestMove = (random.randint(0, board.col-1), sep)
            # print("calledrandom")
        
        if self.currValue == 696969:
            self.currValue = temp
            
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

    [x,y] = nextMove

    boardjadijadian = deepcopy(board)
    boardjadijadian.set_piece(x, y, player1)

    isFull = is_full(boardjadijadian)
    if (isFull): return 0

    isWin = is_win(boardjadijadian)
    if isWin is not None:
        if Piece(isWin[0], isWin[1]) == player1:
            return 9999999999999999

    out = []

    horizontal1 = [0]
    horizontal2 = [0]
    horizontalval = 0

    #cek kanan
    if y+3<board.col:
        if board[x,y+1] == player1:
            if board[x,y+2] == player1:
                horizontal1.append(100)
            else:
                horizontal1.append(50)
        else: # player2
            if board[x,y+1] == player2 or board[x,y+1].color == player2.color:
                if board[x,y+2].color == player2.color or board[x,y+2].shape == player2.shape:
                    if board[x,y+3].color == player2.color or board[x,y+3].shape == player2.shape:
                        return 696969
                    else:
                        horizontal1.append(150)
                else:
                    horizontal1.append(50)
            else:
                horizontal1.append(50)
    
    #cek kiri
    if y-3>=0:
        if board[x,y-1] == player1:
            if board[x,y-2] == player1:
                horizontal2.append(100)
            else:
                horizontal2.append(50)
        else: # player2
            if board[x,y-1] == player2 or board[x,y-1].color == player2.color:
                if board[x,y-2].color == player2.color or board[x,y-2].shape == player2.shape:
                    if board[x,y-3].color == player2.color or board[x,y-3].shape == player2.shape:
                        return 696969
                    else:
                        horizontal2.append(150)
                else:
                    horizontal2.append(50)
            else:
                horizontal2.append(50)

    horizontal1.sort()
    horizontal2.sort()
    horizontalval = max(horizontal1[-1], horizontal2[-1])
    
    #cek antara 1
    if y-1>=0 and y+2<board.col:
        if ((board[x,y-1].color == player2.color or board[x,y-1].shape == player2.shape)
            and (board[x,y+1].color == player2.color or board[x,y+1].shape == player2.shape)
            and (board[x,y+2].color == player2.color or board[x,y+2].shape == player2.shape)):
            return 696969
    
    #cek antara 2
    if y-2>=0 and y+1<board.col:
        if ((board[x,y-2].color == player2.color or board[x,y-2].shape == player2.shape)
            and (board[x,y-1].color == player2.color or board[x,y-1].shape == player2.shape)
            and (board[x,y+1].color == player2.color or board[x,y+1].shape == player2.shape)):
            return 696969

    vertikalval = 0
    #cek bawah
    if x+3<board.row:
        if board[x+1,y] == player1:
            if board[x+2,y] == player1:
                vertikalval = 100
            else:
                vertikalval = 50
        else:
            if board[x+1, y] == player2 or board[x+1, y].color == player2.color:
                if board[x+2,y].color == player2.color or board[x+2,y].shape == player2.shape:
                    if board[x+3,y].color == player2.color or board[x+3,y].shape == player2.shape:
                        return 696969
                    else:
                        vertikalval = 150
                else:
                    vertikalval = 50
            else:
                vertikalval = 50

    diagonalplus1 = [0]
    diagonalplus2 = [0]
    diagonalplus = 0
    if x-3>=0 and y+3<board.col:
        if board[x-1,y+1] == player1:
            if board[x-2,y+2] == player1:
                diagonalplus1.append(100)
            else:
                diagonalplus1.append(50)
        else: # player2
            if board[x-1, y+1] == player2 or board[x-1, y+1].color == player2.color:
                if board[x-2,y+2].color == player2.color or board[x-2,y+2].shape == player2.shape:
                    if board[x-3,y+3].color == player2.color or board[x-3,y+3].shape == player2.shape:
                        return 696969
                    else:
                        diagonalplus1.append(150)
                else:
                    diagonalplus1.append(50)
            else:
                diagonalplus1.append(50)

    if x+3<board.row and y-3>=0:
        if board[x+1,y-1] == player1:
            if board[x+2,y-2] == player1:
                diagonalplus2.append(100)
            else:
                diagonalplus2.append(50)
        else: # player2
            if board[x+1, y-1] == player2 or board[x+1, y-1].color == player2.color:
                if board[x+2,y-2].color == player2.color or board[x+2,y-2].shape == player2.shape:
                    if board[x+3,y-3].color == player2.color or board[x+3,y-3].shape == player2.shape:
                        return 696969
                    else:
                        diagonalplus2.append(150)
                else:
                    diagonalplus2.append(50)
            else:
                diagonalplus2.append(50)

    diagonalplus1.sort()
    diagonalplus2.sort()
    diagonalplus = max(diagonalplus1[-1], diagonalplus2[-1])

    # cek antara 1
    if y-2>=0 and x+2<board.row and y+1<board.col and x-1>=0:
        if ((board[x-1,y+1].color == player2.color or board[x-1,y+1].shape == player2.shape)
            and (board[x+1,y-1].color == player2.color or board[x+1,y-1].shape == player2.shape)
            and (board[x+2,y-2].color == player2.color or board[x+2,y-2].shape == player2.shape)):
            return 696969
    # cek antara 2
    if y-1>=0 and x+1<board.row and y+2<board.col and x-2>=0:
        if ((board[x+1,y-1].color == player2.color or board[x+1,y-1].shape == player2.shape)
            and (board[x-1,y+1].color == player2.color or board[x-1,y+1].shape == player2.shape)
            and (board[x-2,y+2].color == player2.color or board[x-2,y+2].shape == player2.shape)):
            return 696969

    diagonalmin1 = [0]
    diagonalmin2 = [0]
    diagonalmin = 0    
    if x+3<board.row and y+3<board.col:
        if board[x+1,y+1] == player1:
            if board[x+2,y+2] == player1:
                diagonalmin1.append(100)
            else:
                diagonalmin1.append(50)
        else: # player2
            if board[x+1, y+1] == player2 or board[x+1, y+1].color == player2.color:
                if board[x+2,y+2].color == player2.color or board[x+2,y+2].shape == player2.shape:
                    if board[x+3,y+3].color == player2.color or board[x+3,y+3].shape == player2.shape:
                        return 696969
                    else:
                        diagonalmin1.append(150)
                else:
                    diagonalmin1.append(50)
            else:
                diagonalmin2.append(50)


    if x-3>=0 and y-3>=0:
        if board[x-1,y-1] == player1:
            if board[x-2,y-2] == player1:
                diagonalmin2.append(100)
            else:
                diagonalmin2.append(50)
        else: # player2
            if board[x-1, y-1] == player2 or board[x-1, y-1].color == player2.color:
                if board[x-2,y-2].color == player2.color or board[x-2,y-2].shape == player2.shape:
                    if board[x-3,y-3].color == player2.color or board[x-3,y-3].shape == player2.shape:
                        return 696969
                    else:
                        diagonalmin2.append(150)
                else:
                    diagonalmin2.append(50)
            else:
                diagonalmin2.append(50)


    diagonalmin1.sort()
    diagonalmin2.sort()
    diagonalmin = max(diagonalmin1[-1], diagonalmin2[-1])

    # cek antara 1
    if y-2>=0 and x-2>=0 and y+1<board.col and x+1<board.row:
        if ((board[x+1,y+1].color == player2.color or board[x+1,y+1].shape == player2.shape)
            and (board[x-1,y-1].color == player2.color or board[x-1,y-1].shape == player2.shape)
            and (board[x-2,y-2].color == player2.color or board[x-2,y-2].shape == player2.shape )):
            return 696969
    # cek antara 2
    if y+2<board.col and x+2<board.row and y-1>=0 and x-1>=0:
        if ((board[x-1,y-1].color == player2.color or board[x-1,y-1].shape == player2.shape)
            and (board[x+1,y+1].color == player2.color or board[x+1,y+1].shape == player2.shape)
            and (board[x+2,y+2].color == player2.color or board[x+2,y+2].shape == player2.shape)):
            return 696969

    out = [horizontalval, vertikalval, diagonalplus, diagonalmin]
    out.sort()

    return out[-1]

def countmypiece(board: Board, color: int) -> int:
    out = 0
    for x in range(board.row):
        for y in range(board.col):
            if board[x,y].color == color:
                out+=1
    return out
