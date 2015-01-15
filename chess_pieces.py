__author__ = 'cook'
import board as bd
from PIL import ImageTk
from tkinter import *

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
    turn = 'black'
    def __init__(self, x, y, color, directions, max_moves, name, FEN, image, cb):
        self.x = x
        self.y = y
        self.color = color
        self.directions = directions
        self.max_moves = max_moves   #  maximum number of moves in a direction in a turn
        self.num_moves = 0
        self.possible_moves = []
        self.move_history = []
        self.name = name        #  color and type of piece
        self.FEN = FEN          #  type of piece in FEN notation, followed by start row in caps A-H
        if self.is_pawn():      # take pawns is only necessary for those blasted pawns
            if self.is_white():
                self.take_moves = [[1, 1], [1, -1]]
            else:
                self.take_moves = [[-1, 1], [-1, -1]]
        else:
            self.take_moves = None
        self.captured = False   # has the piece been captured or not?
        self.image = ImageTk.PhotoImage(file=image)
        self.chess_board = cb
#        self.draw = self.chess_board.canvas.\
#            create_text(self.x*self.chess_board.dim_square+self.chess_board.dim_square / 2,
#                        self.y*self.chess_board.dim_square+self.chess_board.dim_square / 2, text=self.FEN)
        self.draw = self.chess_board.canvas.create_image(self.x*self.chess_board.dim_square+self.chess_board.dim_square / 2,
                        self.y*self.chess_board.dim_square+self.chess_board.dim_square / 2, image=self.image)
        self.change_sides()
        self.move_history.append(self.position())

    def __str__(self):
        return self.name + ' at position [' + str(self.x) + ',' + str(self.y) + ']'

    def move(self, x, y):
        """
        Move is responsible for updating the coordinates of the piece and for the chessboard.
        """
        self.x = x
        self.y = y
        self.move_history.append(self.position())
        if not self.captured:
            self.num_moves += 1
            self.chess_board.canvas.coords(self.draw, self.x*self.chess_board.dim_square+self.chess_board.dim_square / 2,
                            self.y*self.chess_board.dim_square+self.chess_board.dim_square / 2 )

    def position(self):
        return [self.x, self.y]

    def capture(self, winner):
        self.captured = True
        px = self.move_history[0][0] # start position for this piece
        py = self.move_history[0][1]
        if self.is_white():  # position the piece in the taken board
            px = 1 - px
        else:
            px = 7 - px
        self.chess_board.canvas.delete(self.draw)
        self.move(px, py)

    def is_white(self):
        return self.color == 'white'

    def is_black(self):
        return self.color == 'black'

    def is_king(self):
        if 'king' in self.name.lower():
            return True
        else:
            return False

    def is_knight(self):
        if 'knight' in self.name.lower():
            return True
        else:
            return False

    def is_pawn(self):
        if 'pawn' in self.name.lower():
            return True
        else:
            return False

    def opponent(self, p):
        return not(self.color == p.color)

    def opposite_color(self):
        if self.is_white():
            return 'black'
        else:
            return 'white'

    def is_turn(self):
        return Piece.turn == self.color

    def change_sides(self):
        Piece.turn = self.opposite_color()
        self.chess_board.whose_turn.config(text=Piece.turn.title() + "'s turn")


#x, y, color, directions, max, name, FEN, image
class Pieces:
    """ 0,0 is the upper left, white on the left column
    """
    color_in_check = None
    last_moved = 'pA'  # FEN of the last piece moved, needs to be initially a black piece
    piece_chosen = None
    checkmate = False
    def __init__(self, cb):
        self.cb = cb
        self.img = {}
        self.captimg = {}
        self.cb.canvas.bind("<Button-1>", self.clicked)
        infinity = 8
        wking = Piece(0, 4, 'white',
                      [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                      1, 'White King', 'K', 'pieces_image/kwhite.png', cb)
        wqueen = Piece(0, 3, 'white',
                       [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                       infinity, 'White Queen', 'Q', 'pieces_image/qwhite.png', cb)
        wrookA = Piece(0, 0, 'white',
                       [[0, 1], [1, 0], [-1, 0], [0, -1]],
                       infinity, 'White Rook', 'RA', 'pieces_image/rwhite.png', cb)
        wrookH = Piece(0, 7, 'white',
                       [[0, 1], [1, 0], [-1, 0], [0, -1]],
                       infinity, 'White Rook', 'RH', 'pieces_image/rwhite.png', cb)
        wknightB = Piece(0, 1, 'white',
                         [[1, 2], [-1, 2], [1, -2], [-1, -2],
                          [2, 1], [-2, 1], [2, -1], [-2, -1]],
                         1, 'White Knight', 'NB', 'pieces_image/nwhite.png', cb)
        wknightG = Piece(0, 6, 'white',
                         [[1, 2], [-1, 2], [1, -2], [-1, -2],
                          [2, 1], [-2, 1], [2, -1], [-2, -1]],
                         1, 'White Knight', 'NG', 'pieces_image/nwhite.png', cb)
        wbishopC = Piece(0, 2, 'white',
                         [[1, 1], [-1, 1], [-1, -1], [1, -1]],
                         infinity, 'White Bishop', 'BC', 'pieces_image/bwhite.png', cb)
        wbishopF = Piece(0, 5, 'white',
                         [[1, 1], [-1, 1], [-1, -1], [1, -1]],
                         infinity, 'White Bishop', 'BF', 'pieces_image/bwhite.png', cb)
        wpawnA = Piece(1, 0, 'white',
                       [[1, 0]], 1, 'White Pawn', 'PA', 'pieces_image/pwhite.png', cb)
        wpawnB = Piece(1, 1, 'white',
                       [[1, 0]], 1, 'White Pawn', 'PB', 'pieces_image/pwhite.png', cb)
        wpawnC = Piece(1, 2, 'white',
                       [[1, 0]], 1, 'White Pawn', 'PC', 'pieces_image/pwhite.png', cb)
        wpawnD = Piece(1, 3, 'white',
                       [[1, 0]], 1, 'White Pawn', 'PD', 'pieces_image/pwhite.png', cb)
        wpawnE = Piece(1, 4, 'white',
                       [[1, 0]], 1, 'White Pawn', 'PE', 'pieces_image/pwhite.png', cb)
        wpawnF = Piece(1, 5, 'white',
                       [[1, 0]], 1, 'White Pawn', 'PF', 'pieces_image/pwhite.png', cb)
        wpawnG = Piece(1, 6, 'white',
                       [[1, 0]], 1, 'White Pawn', 'PG', 'pieces_image/pwhite.png', cb)
        wpawnH = Piece(1, 7, 'white',
                       [[1, 0]], 1, 'White Pawn', 'PH', 'pieces_image/pwhite.png', cb)
        bking = Piece(7, 4, 'black',
                      [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                      1, 'Black King', 'k', 'pieces_image/kblack.png', cb)
        bqueen = Piece(7, 3, 'black',
                       [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                       infinity, 'Black Queen', 'q', 'pieces_image/qblack.png', cb)
        brookA = Piece(7, 0, 'black',
                       [[0, 1], [1, 0], [-1, 0], [0, -1]],
                       infinity, 'Black Rook', 'rA', 'pieces_image/rblack.png', cb)
        brookH = Piece(7, 7, 'black',
                       [[0, 1], [1, 0], [-1, 0], [0, -1]],
                       infinity, 'Black Rook', 'rH', 'pieces_image/rblack.png', cb)
        bknightB = Piece(7, 1, 'black',
                         [[1, 2], [-1, 2], [1, -2], [-1, -2],
                         [2, 1], [-2, 1], [2, -1], [-2, -1]],
                         1, 'Black Knight', 'nB', 'pieces_image/nblack.png', cb)
        bknightG = Piece(7, 6, 'black',
                         [[1, 2], [-1, 2], [1, -2], [-1, -2],
                         [2, 1], [-2, 1], [2, -1], [-2, -1]],
                         1, 'Black Knight', 'nG', 'pieces_image/nblack.png', cb)
        bbishopC = Piece(7, 2, 'black',
                         [[1, 1], [-1, 1], [-1, -1], [1, -1]],
                         infinity, 'Black Bishop', 'bC', 'pieces_image/bblack.png', cb)
        bbishopF = Piece(7, 5, 'black',
                         [[1, 1], [-1, 1], [-1, -1], [1, -1]],
                         infinity, 'Black Bishop', 'bF', 'pieces_image/bblack.png', cb)
        bpawnA = Piece(6, 0, 'black',
                       [[-1, 0]], 1, 'Black Pawn', 'pA', 'pieces_image/pblack.png', cb)
        bpawnB = Piece(6, 1, 'black',
                       [[-1, 0]], 1, 'Black Pawn', 'pB', 'pieces_image/pblack.png', cb)
        bpawnC = Piece(6, 2, 'black',
                       [[-1, 0]], 1, 'Black Pawn', 'pC', 'pieces_image/pblack.png', cb)
        bpawnD = Piece(6, 3, 'black',
                       [[-1, 0]], 1, 'Black Pawn', 'pD', 'pieces_image/pblack.png', cb)
        bpawnE = Piece(6, 4, 'black',
                       [[-1, 0]], 1, 'Black Pawn', 'pE', 'pieces_image/pblack.png', cb)
        bpawnF = Piece(6, 5, 'black',
                       [[-1, 0]], 1, 'Black Pawn', 'pF', 'pieces_image/pblack.png', cb)
        bpawnG = Piece(6, 6, 'black',
                       [[-1, 0]], 1, 'Black Pawn', 'pG', 'pieces_image/pblack.png', cb)
        bpawnH = Piece(6, 7, 'black',
                       [[-1, 0]], 1, 'Black Pawn', 'pH', 'pieces_image/pblack.png', cb)

        self.pieces = {'K': wking, 'Q': wqueen, 'RA': wrookA, 'RH': wrookH,
                       'NB': wknightB, 'NG': wknightG, 'BC': wbishopC, 'BF': wbishopF,
                       'PA': wpawnA, 'PB': wpawnB, 'PC': wpawnC, 'PD': wpawnD,
                       'PE': wpawnE, 'PF': wpawnF, 'PG': wpawnG, 'PH': wpawnH,
                       'k': bking, 'q': bqueen, 'rA': brookA, 'rH': brookH,
                       'nB': bknightB, 'nG': bknightG, 'bC': bbishopC, 'bF': bbishopF,
                       'pA': bpawnA, 'pB': bpawnB, 'pC': bpawnC, 'pD': bpawnD,
                       'pE': bpawnE, 'pF': bpawnF, 'pG': bpawnG, 'pH': bpawnH}
        self.draw_board()

    def normalize_move(self, move):
        if abs(move[0]) == abs(move[1]):  # diagonal move
            num_moves = abs(move[0])
            normalized_move = [move[0]/num_moves, move[1]/num_moves]
        elif abs(move[0]) == 0:   # vertical move
            num_moves = abs(move[1])
            normalized_move = [0, move[1]/num_moves]
        elif abs(move[1]) == 0:   # horizontal move
            num_moves = abs(move[0])
            normalized_move = [move[0]/num_moves, 0]
        else:  # knight
            num_moves = min(abs(move[0]), abs(move[1]))
            normalized_move = [move[0]/num_moves, move[1]/num_moves]
        return normalized_move, num_moves

    def verify_move_empty_board(self, FEN, x, y):
        """
        :param FEN: Piece we are checking
        :param x: x coordinate of where we are moving
        :param y: y coordinate of where we are moving
        :return: if the piece could move to this point if there were no other pieces present
        """
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        cp = self.pieces[FEN].position()
        move = [x - cp[0], y - cp[1]]
        if move == [0, 0]:  # no move
            return False
        normalized_move, num_moves = self.normalize_move(move)
        if self.pieces[FEN].is_pawn():
            if self.pieces[FEN].num_moves == 0 and num_moves > 2:
                # On the first move you can move more than one space
                return False
            elif self.pieces[FEN].num_moves != 0 and num_moves > 1:
                return False
        elif num_moves > self.pieces[FEN].max_moves:
            return False
        for vector in self.pieces[FEN].directions:
            if vector == normalized_move:
                return True
        return False

    def verify_no_teammates(self, FEN, x, y):
        """
        :param FEN: piece we are trying to move
        :param x: x coordinate we are trying to move to
        :param y: y coordinate we are trying to move to
        :return: true if none of our currently active teammates are at this point, false if one is
        """
        for piece in self.pieces:
            if self.pieces[piece].position() == [x, y] and not(self.pieces[piece].captured):
                if  self.pieces[FEN].color == self.pieces[piece].color:  # there is piece already there on our side
                    return False
                elif self.pieces[FEN].is_pawn() and self.pieces[FEN].opponent(self.pieces[piece]):
                    return False                                          # pawns cannot take going horizontal
        return True

    def verify_not_jumping_another_piece(self, FEN, x, y):
        """
        :param FEN: piece we are trying to move
        :param x: x coordinate we are trying to move to
        :param y: y coordinate we are trying to move to
        :return: true if we are not going to jump another piece moving to x,y, false otherwise.
        """
        if not self.pieces[FEN].is_knight(): # the jump other pieces rule doesn't apply to knights
            cp = self.pieces[FEN].position()
            move = [x - cp[0], y - cp[1]]
            normalized_move, num_moves = self.normalize_move(move)
            for piece in self.pieces:
                for i in range(1, num_moves):  # which doesn't apply to knights
                    in_between_pos = [cp[0]+i*normalized_move[0], cp[1]+i*normalized_move[1]]
                    if self.pieces[piece].position() == in_between_pos and not(self.pieces[piece].captured):
                        return False
        return True

    def verify_not_putting_own_king_in_check(self, FEN, x, y):
        """
        :param FEN: piece we are trying to move
        :param x: x coordinate we are trying to move to
        :param y: y coordinate we are trying to move to
        :return: true if by moving to x,y we do not put our king in check, false otherwise
        """
        king = self.king(self.pieces[FEN].color)
        [kx, ky] = self.pieces[king].position()
        tempx = self.pieces[FEN].x
        tempy = self.pieces[FEN].y
#        if FEN == king:
#            [kx, ky] = [x,y]
        self.pieces[FEN].x = x
        self.pieces[FEN].y = y
        for piece in self.pieces:
            if self.pieces[king].opponent(self.pieces[piece]) and self.verify_move_empty_board(piece, kx, ky) and \
                self.verify_not_jumping_another_piece(piece, kx, ky) and not(self.pieces[piece].captured):
                self.pieces[FEN].x = tempx
                self.pieces[FEN].y = tempy
                return False
        self.pieces[FEN].x = tempx
        self.pieces[FEN].y = tempy
        return True

    def verify_pawn_taking(self, FEN, x, y):
        """
            :param FEN: piece we are trying to move
            :param x: x coordinate we are trying to move to
            :param y: y coordinate we are trying to move to
            :return: verify that a pawn is executing a taking move
        """
        if self.pieces[FEN].is_pawn():
            cp = self.pieces[FEN].position()
            move = [x - cp[0], y - cp[1]]
            for piece in self.pieces:
                if move in self.pieces[FEN].take_moves and self.pieces[piece].position() == [x, y]\
                        and self.pieces[FEN].opponent(self.pieces[piece]) and not(self.pieces[piece].captured):
                    return True
        return False

    def verify_move_not_in_check(self, FEN,  x, y):
        if self.verify_move_empty_board(FEN, x, y) and self.verify_no_teammates(FEN, x, y) and \
                self.verify_not_jumping_another_piece(FEN, x, y) and self.verify_not_putting_own_king_in_check(FEN, x, y):
            return True
        elif self.pieces[FEN].is_pawn() and self.verify_pawn_taking(FEN, x, y) and \
                self.verify_not_putting_own_king_in_check(FEN, x, y):
            return True
        else:
            return False

    def verify_move(self, FEN, x, y):
        if self.color_in_check is None:
            return self.verify_move_not_in_check(FEN, x, y)
        else:
            potential_move = False
            if self.verify_move_empty_board(FEN, x, y) and self.verify_no_teammates(FEN, x, y) and \
                    self.verify_not_jumping_another_piece(FEN, x, y):
                potential_move = True
            elif self.pieces[FEN].is_pawn() and self.verify_pawn_taking(FEN, x, y):
                potential_move = True
            if potential_move:
                king = self.king(self.color_in_check)
                [kx, ky] = self.pieces[king].position()
                tempx = self.pieces[FEN].x
                tempy = self.pieces[FEN].y
                if king == FEN:
                    [kx, ky] = [x, y]
                self.pieces[FEN].x = x
                self.pieces[FEN].y = y
                # if there is a piece in the new position on the opposite side we need to capture it.
                # we just better make sure to release it. Do NOT use the capture method, just set the variable.
                captured_piece = None
                for piece in self.pieces:
                    if self.pieces[FEN].opponent(self.pieces[piece]) and self.pieces[piece].position() == [x, y] and \
                            not(self.pieces[piece].captured):
                        if (self.pieces[FEN].is_pawn() and self.verify_pawn_taking(FEN, x, y)) or not(self.pieces[FEN].is_pawn()):
                            captured_piece = piece
                            self.pieces[captured_piece].captured = True
                # if we move to the new position, will anyone be able to take our king?
                for piece in self.pieces:
                    if self.pieces[king].opponent(self.pieces[piece]) and not(self.pieces[piece].captured) and \
                                    self.pieces[piece].position() != [x, y]:
                        if self.verify_move_empty_board(piece, kx, ky) and \
                                self.verify_not_jumping_another_piece(piece, kx, ky):
                            self.pieces[FEN].x = tempx
                            self.pieces[FEN].y = tempy
                            if captured_piece is not None:
                                self.pieces[captured_piece].captured = False
                            print(FEN, "blocked by ", piece, x, y)
                            return False
                        elif self.pieces[piece].is_pawn() and self.verify_pawn_taking(piece, kx, ky) and \
                                        self.pieces[piece].position() != [x, y]:
                            self.pieces[FEN].x = tempx
                            self.pieces[FEN].y = tempy
                            if captured_piece is not None:
                                self.pieces[captured_piece].captured = False
                            print(FEN, "blocked by ", piece, x, y)
                            return False
                self.pieces[FEN].x = tempx
                self.pieces[FEN].y = tempy
                if captured_piece is not None:
                    self.pieces[captured_piece].captured = False
                return True

    def move(self, FEN, x, y):
        if self.verify_move(FEN, x, y) and self.pieces[FEN].is_turn():
            self.pieces[FEN].move(x, y)
            Pieces.last_moved = FEN
#            print(str(self.pieces[FEN]) + 'moved to [' + str(x) + ',' + str(y) + ']')
            for piece in self.pieces:
                if piece != FEN and self.pieces[piece].position() == [x, y]:
                    self.pieces[piece].capture(self.pieces[FEN])
            if self.pieces[FEN].is_pawn():
                if (self.pieces[FEN].is_white() and x == 7) or \
                        (self.pieces[FEN].is_black() and x == 0):
                    self.trade_in_pawn(FEN)
            # If we have made a legal move, we must have eliminated any threat of being in check
            Pieces.color_in_check = None
            if self.in_check(self.pieces[FEN].opposite_color()):
                Pieces.color_in_check = self.pieces[FEN].opposite_color()
                checkmate = self.check_mate(self.king(self.pieces[FEN].opposite_color()))
                if self.pieces[FEN].is_white():
                    clr = 'Black'
                else:
                    clr = 'White'
                if checkmate:
                    self.cb.whose_turn.config(text="")
                    self.cb.checkmate.config(text=clr + " is in checkmate by the " + self.pieces[Pieces.last_moved].name.lower())
                    Pieces.checkmate = True
                else:
                    self.cb.checkmate.config(text=clr + " is in check by the " + self.pieces[Pieces.last_moved].name.lower())
            else:
                self.cb.checkmate.config(text="")  # Clear previous messages
            self.pieces[FEN].change_sides()
            return True
        else:
            return False

    def trade_in_pawn(self, pawn):
        print('trade in pawn', pawn)

    def king(self, color):
        if color == 'white':
            return 'K'
        else:
            return 'k'

    def in_check(self, color):
        """ color is the color of the king you want to check"""
        FEN = self.king(color)
        kings_position = self.pieces[FEN].position()
        return self.verify_move(Pieces.last_moved, kings_position[0], kings_position[1])

    def check_mate(self, king):
        """ This is only called if we already know we are in check.
        """
        for piece in self.pieces:
            if self.pieces[piece].color == self.pieces[king].color and not(self.pieces[piece].captured) and \
                            self.possible_moves(piece) != []:
                return False
        return True

    def print_possible_moves(self, FEN):
        """ For error checking only """
        pos = self.possible_moves(FEN)
        print(FEN )
        for p in pos:
            print('   [' + str(p[0]) + ',' + str(p[1]) + ']')

    def possible_moves(self, FEN):
        pm = []
        for x in range(8):
            for y in range(8):
                if self.verify_move(FEN, x, y):
                    pm.append([x, y])
        return pm

    def clicked(self, event):
        """
        Works with the input boxes
        """
        if Pieces.checkmate:
            return
        row = event.x//self.cb.dim_square
        col = event.y//self.cb.dim_square
        if Pieces.piece_chosen is None:
            for piece in self.pieces:
                if (self.pieces[piece].position() == [row, col]) and self.pieces[piece].is_turn() \
                        and not(self.pieces[piece].captured):
                    Pieces.piece_chosen = piece
                    self.pieces[piece].possible_moves = self.possible_moves(piece)
                    self.print_possible_moves(piece)
                    self.draw_board_pm(self.pieces[piece].possible_moves)
        else:
            if [row, col] in self.possible_moves(Pieces.piece_chosen): #self.pieces[Pieces.piece_chosen].possible_moves:
                self.move(Pieces.piece_chosen, row, col)
            Pieces.piece_chosen = None
            self.draw_board()

    def draw_pieces(self):
        self.img = {}
        self.captimg = {}
        for piece in self.pieces:
            p = self.pieces[piece]
            if not p.captured:
                self.img.update({piece: self.pieces[piece].image})
                self.cb.canvas.create_image(p.x*self.cb.dim_square+self.cb.dim_square / 2,
                                            p.y*self.cb.dim_square+self.cb.dim_square / 2,
                                            image=self.img[piece])
            else:
                self.captimg.update({piece: self.pieces[piece].image})
                if p.is_white():
                    self.cb.whitecaptured.create_image(p.x*self.cb.dim_square+self.cb.dim_square / 2,
                                                       p.y*self.cb.dim_square+self.cb.dim_square / 2,
                                                       image=self.captimg[piece])
                else:
                    self.cb.blackcaptured.create_image(p.x*self.cb.dim_square+self.cb.dim_square / 2,
                                                       p.y*self.cb.dim_square+self.cb.dim_square / 2,
                                                       image=self.captimg[piece])

    def draw_board_pm(self, possible_moves):
        color = self.cb.color1
        for x in range(self.cb.rows):
            color = self.cb.swap_colors(color)
            for y in range(self.cb.columns):
                temp = color
                if [x, y] in possible_moves:
                    color = "yellow"
                x1 = (x * self.cb.dim_square)
                y1 = (y * self.cb.dim_square)
                x2 = x1 + self.cb.dim_square
                y2 = y1 + self.cb.dim_square
                if [x, y] == self.pieces[self.piece_chosen].position():
                    self.cb.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=3)
                else:
                    self.cb.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                color = temp
                color = self.cb.swap_colors(color)

        self.draw_pieces()

    def draw_board(self):
        color = self.cb.color1
        for x in range(self.cb.rows):
            color = self.cb.swap_colors(color)
            for y in range(self.cb.columns):
                x1 = (x * self.cb.dim_square)
                y1 = (y * self.cb.dim_square)
                x2 = x1 + self.cb.dim_square
                y2 = y1 + self.cb.dim_square
                self.cb.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                color = self.cb.swap_colors(color)
        self.draw_pieces()
