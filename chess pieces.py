__author__ = 'cook'
import math
from PIL import ImageTk
from PIL import Image

class Piece:
    """ Upper left is (0,0), the pieces are aligned vertically
and pawns move horizontally. x,y is the current position of the
piece, color is the color of the piece. Directions is a list
of vector directions, each of which are a list [deltax, deltay]
that the piece can move in. At least one of deltax, deltay should
be 1. Pawns are handled separately.
Max_moves is the maximum number of moves the piece
can make in any direction. Name is a string representing the
name of the piece, while FEN is the Forsyth-Edwards notation for the
piece. Captures is whether the piece has been taken or not.
Image is passed in as a filename and converted to a Tkinter
compatible image.
    """
    def __init__(self, x, y, color, directions, max, name, FEN, image):
        self.x = x
        self.y = y
        self.color = color
        self.directions = directions
        self.max_moves = max
        self.name = name
        self.FEN = FEN
        self.captured = False
        self.image = ImageTk.PhotoImage(file=image)

    def move(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return [self.x, self.y]

    def captured(self):
        self.captured = True

    def pawn(self):
        if 'pawn' in self.name.upper():
            return True
        else:
            return False

    def king(self):
        if 'king' in self.name.upper():
            return True
        else:
            return False

    def opponent(self):
        if self.color == 'white':
            return 'black'
        else:
            return 'white'

#x, y, color, directions, max, name, FEN, image
class Pieces:
    """ 0,0 is the upper left, white on the left column
    """
    def __init__(self):
        infinity = 8
        wking = Piece(0, 4, 'white',
                      [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                       1, 'White King', 'K', 'pieces_image/kwhite.png')
        wqueen = Piece(0, 3, 'white',
                       [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                       infinity, 'White Queen', 'Q', 'pieces_image/qwhite.png')
        wrookA = Piece(0, 0, 'white',
                       [[0, 1], [1, 0],[-1, 0], [0, -1]],
                       infinity, 'White Rook', 'RA', 'pieces_image/rwhite.png')
        wrookH = Piece(0, 7, 'white',
                       [[0, 1], [1, 0],[-1, 0], [0, -1]],
                       infinity, 'White Rook', 'RH', 'pieces_image/rwhite.png')
        wknightB = Piece(0, 1, 'white',
                         [[1, 2], [-1, 2], [1, -2], [-1, -2],
                          [2, 1], [-2, 1], [2, -1], [-2, -1]],
                         infinity, 'White Knight', 'NB', 'pieces_image/nwhite.png')
        wknightG = Piece(0, 6, 'white',
                         [[1, 2], [-1, 2], [1, -2], [-1, -2],
                          [2, 1], [-2, 1], [2, -1], [-2, -1]],
                         infinity, 'White Knight', 'NG', 'pieces_image/nwhite.png')
        wbishopC = Piece(0, 2, 'white',
                         [[1, 1], [-1, 1], [-1, -1], [1, -1]],
                         infinity, 'White Bishop', 'BC', 'pieces_image/bwhite.png')
        wbishopF = Piece(0, 5, 'white',
                         [[1, 1], [-1, 1], [-1, -1], [1, -1]],
                         infinity, 'White Bishop', 'BF', 'pieces_image/bwhite.png')
        wpawnA = Piece(1, 0, 'white',
                       [[0, 1]], 1, 'White Pawn', 'PA', 'pieces_image/pwhite.png')
        wpawnB = Piece(1, 1, 'white',
                       [[0, 1]], 1, 'White Pawn', 'PB', 'pieces_image/pwhite.png')
        wpawnC = Piece(1, 2, 'white',
                       [[0, 1]], 1, 'White Pawn', 'PC', 'pieces_image/pwhite.png')
        wpawnD = Piece(1, 3, 'white',
                       [[0, 1]], 1, 'White Pawn', 'PD', 'pieces_image/pwhite.png')
        wpawnE = Piece(1, 4, 'white',
                       [[0, 1]], 1, 'White Pawn', 'PE', 'pieces_image/pwhite.png')
        wpawnF = Piece(1, 5, 'white',
                       [[0, 1]], 1, 'White Pawn', 'PF', 'pieces_image/pwhite.png')
        wpawnG = Piece(1, 6, 'white',
                       [[0, 1]], 1, 'White Pawn', 'PG', 'pieces_image/pwhite.png')
        wpawnH = Piece(1, 7, 'white',
                       [[0, 1]], 1, 'White Pawn', 'PH', 'pieces_image/pwhite.png')
        bking = Piece(7, 3, 'black',
                      [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                      1, 'Black King', 'k', 'pieces_image/kblack.png')
        bqueen = Piece(7, 4, 'black',
                       [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                       infinity, 'Black Queen', 'q', 'pieces_image/qblack.png')
        brookA = Piece(7, 0, 'black',
                       [[0, 1], [1, 0],[-1, 0], [0, -1]],
                       infinity, 'Black Rook', 'rA', 'pieces_image/rblack.png')
        brookH = Piece(7, 7, 'black',
                       [[0, 1], [1, 0],[-1, 0], [0, -1]],
                       infinity, 'Black Rook', 'rH', 'pieces_image/rblack.png')
        bknightB = Piece(7, 1, 'black',
                         [[1, 2], [-1, 2], [1, -2], [-1, -2],
                         [2, 1], [-2, 1], [2, -1], [-2, -1]],
                         infinity, 'Black Knight', 'nB', 'pieces_image/nblack.png')
        bknightG = Piece(7, 6, 'black',
                         [[1, 2], [-1, 2], [1, -2], [-1, -2],
                         [2, 1], [-2, 1], [2, -1], [-2, -1]],
                         infinity, 'Black Knight', 'nG', 'pieces_image/nblack.png')
        bbishopC = Piece(7, 2, 'black',
                         [[1, 1], [-1, 1], [-1, -1], [1, -1]],
                         infinity, 'Black Bishop', 'bC', 'pieces_image/bblack.png')
        bbishopF = Piece(7, 5, 'black',
                         [[1, 1], [-1, 1], [-1, -1], [1, -1]],
                         infinity, 'Black Bishop', 'bF', 'pieces_image/bblack.png')
        bpawnA = Piece(6, 0, 'black',
                       [[0, -1]], 1, 'Black Pawn', 'pA', 'pieces_image/pblack.png')
        bpawnB = Piece(6, 1, 'black',
                       [[0, -1]], 1, 'Black Pawn', 'pB', 'pieces_image/pblack.png')
        bpawnC = Piece(6, 2, 'black',
                       [[0, -1]], 1, 'Black Pawn', 'pC', 'pieces_image/pblack.png')
        bpawnD = Piece(6, 3, 'black',
                       [[0, -1]], 1, 'Black Pawn', 'pD', 'pieces_image/pblack.png')
        bpawnE = Piece(6, 4, 'black',
                       [[0, -1]], 1, 'Black Pawn', 'pE', 'pieces_image/pblack.png')
        bpawnF = Piece(6, 5, 'black',
                       [[0, -1]], 1, 'Black Pawn', 'pF', 'pieces_image/pblack.png')
        bpawnG = Piece(6, 6, 'black',
                       [[0, -1]], 1, 'Black Pawn', 'pG', 'pieces_image/pblack.png')
        bpawnH = Piece(6, 7, 'black',
                       [[0, -1]], 1, 'Black Pawn', 'pH', 'pieces_image/pblack.png')

        self.pieces = {'K': wking, 'Q': wqueen, 'RA': wrookA, 'RH': wrookH,
                       'NB': wknightB, 'NG': wknightG, 'BC': wbishopC, 'BF': wbishopF,
                       'PA': wpawnA, 'PB': wpawnB, 'PC': wpawnC, 'PD': wpawnD,
                       'PE': wpawnE, 'PF': wpawnF, 'PG': wpawnG, 'PH': wpawnH,
                       'k': bking, 'q': bqueen, 'rA': brookA, 'rH': brookH,
                       'nB': bknightB, 'nG': bknightG, 'bC': bbishopC, 'bF': bbishopF,
                       'pA': bpawnA, 'pB': bpawnB, 'pC': bpawnC, 'pD': bpawnD,
                       'pE': bpawnE, 'pF': bpawnF, 'pG': bpawnG, 'pH': bpawnH}

    def check_move(self, FEN,  x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        move = [x - self.pieces[FEN].x, y - self.pieces[FEN].y]
        if move == [0,0]: # no move
            return True
        elif abs(move[0]) == abs(move[1]):  # diagonal move
            num_moves = abs(move[0])
            normalized_move = [move[0]/num_moves, move[1]/num_moves]
        elif abs(move[0]) == 0 :   # vertical move
            num_moves = abs(move[1])
            normalized_move = [0, move[1]/num_moves]
        elif abs(move[1]) == 0 :   # horizontal move
            num_moves = abs(move[0])
            normalized_move = [move[0]/num_moves, 0]
        else:  # rook
            num_moves = min(abs(move[0]), abs(move[1]))
            normalized_move = [move[0]/num_moves, move[1]/num_moves]

        if not(self.pieces[FEN].pawn() or self.pieces[FEN].king()):
            for vector in self.pieces[FEN].directions:
                if vector == normalized_move and num_moves <= self.pieces[FEN].max_moves:
                    for piece in self.pieces:
                        if self.pieces[piece].position() == [x,y]\
                                and self.pieces[FEN].color() == self.pieces[piece].color():
                            return False
                    return True
            return False
        # Special cases
        # pawns take diagonally, but not forwards
        elif self.pieces[FEN].pawn():
            # move without taking
            if self.pieces[FEN].directions[0] == normalized_move and num_moves == 1:
                for piece in self.pieces:
                    if self.pieces[piece].position() == [x,y]:
                        return False
                return True
            # move by taking
            if self.pieces[FEN].color == 'white':
                take_moves = [[1, 1], [1, -1]]
            else:
                take_moves = [[1, 1], [1, -1]]
            for piece in self.pieces:
                if move in take_moves and self.pieces[piece].position() == [x,y]\
                        and self.pieces[piece].color == self.pieces[piece].opponent():
                    return True
            return False
        else:  # we must be moving a king
            if num_moves == 1:
                for piece in self.pieces:
                    if not self.pieces[piece].king():
                        if self.pieces[piece].check_move(self.pieces[piece].FEN, x, y):
                            return False  # the king would move into check
                    elif self.pieces[piece].opponent() == self.pieces[FEN].color:
                        other_king_pos = self.pieces[piece].position()
                        if max(abs(x - other_king_pos[0]),abs(y - other_king_pos)) == 1:
                            return False
                return True
            else:
                return False


    def move(self, FEN, x, y):
        if self.pieces[FEN].check_move(FEN, x, y):
            self.pieces[FEN].move(x, y)
            for piece in self.pieces:
                if piece != FEN and self.pieces[piece].position!= [x,y]:
                    self.pieces[piece].captured()
                if self.pieces[FEN].pawn:
                    if self.pieces[FEN].color == 'white' and x == 7 or \
                       self.pieces[FEN].color == 'black' and x == 0:
                        self.trade_in_pawn(FEN)
            return True
        else:
            return False

    def trade_in_pawn(self, FEN):
        pass