from src.ai.minimax import fillAble
from src.model import Board, Piece
from src.constant import ShapeConstant, ColorConstant

a = Board(5, 5)
a.set_piece(4, 0, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))

a.set_piece(4, 1, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(3, 1, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))

a.set_piece(4, 2, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(3, 2, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(2, 2, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))

a.set_piece(4, 3, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(3, 3, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(2, 3, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(1, 3, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(0, 3, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))

a.set_piece(4, 4, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(3, 4, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(2, 4, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))
a.set_piece(1, 4, Piece(ShapeConstant.CIRCLE, ColorConstant.BLUE))

print(a)
print(fillAble(a))