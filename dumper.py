from src.ai import *
from src.constant import Path
from src.utility import dump

def dumper(path_b1, path_b2, path_pvb):
    model = MinimaxGroup44()
    model2 = LocalSearch()
    dump(model, Path.BVB_P1.format(path_b1))
    dump(model2, Path.BVB_P2.format(path_b2))
    dump(model, Path.PVB.format(path_pvb))

if __name__ == '__main__':
    bot1_filename = 'nitra59_minimax.pkl' 
    bot2_filename = 'nitra59_localsearch.pkl'
    pvp_bot_filename = 'nitra59_minimax.pkl'
    dumper(bot1_filename, bot2_filename, pvp_bot_filename)
