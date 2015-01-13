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
    white_captured = []
    black_captured = []
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
        self.image = image
        self.chess_board = cb
        self.draw = self.chess_board.canvas.\
            create_text(self.x*self.chess_board.dim_square+self.chess_board.dim_square / 2,
                        self.y*self.chess_board.dim_square+self.chess_board.dim_square / 2, text=self.FEN)
        self.change_sides()

    def __str__(self):
        return self.name + ' from row ' + self.FEN + ' '

    def move(self, x, y):
        """
        Move is responsible for updating the coordinates of the piece and for the chessboard.
        """
        self.x = x
        self.y = y
        self.move_history.append(self.position())
        self.num_moves += 1
        if not self.captured:
            self.chess_board.canvas.coords(self.draw, self.x*self.chess_board.dim_square+self.chess_board.dim_square / 2,
                            self.y*self.chess_board.dim_square+self.chess_board.dim_square / 2 )
        else:
            self.chess_board.canvas.delete(self.draw)

    def position(self):
        return [self.x, self.y]

    def capture(self, winner):
        self.captured = True
        if self.is_white():
            self.move(8, 0)   # put white pieces off the board on the right
            Piece.white_captured.append(self)
        else:
            self.move(-1, 0)  # put black pieces off the board on the left
            Piece.black_captured.append(self)
        cw = ''
        for piece in Piece.white_captured:
            cw += piece.FEN + ' '
        cb = ''
        for piece in Piece.black_captured:
            cb += piece.FEN + ' '
        self.chess_board.blackcaptured.itemconfig(self.chess_board.captbwin, text=cb)
        self.chess_board.whitecaptured.itemconfig(self.chess_board.captwwin, text=cw)
        print("\n" + str(winner) + " captured " + str(self) + " at [" + str(winner.x) + ',' + str(winner.y) + ']' + "\n")

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
    piece_chosen = None
    def __init__(self, cb):
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
        bking = Piece(7, 3, 'black',
                      [[0, 1], [1, 1], [1, 0], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]],
                      1, 'Black King', 'k', 'pieces_image/kblack.png', cb)
        bqueen = Piece(7, 4, 'black',
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
                       [[0, -1]], 1, 'Black Pawn', 'pG', 'pieces_image/pblack.png', cb)
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
        self.cb = cb
        self.cb.canvas.bind("<Button-1>", self.clicked)

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

    def check_move(self, FEN,  x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        cp = self.pieces[FEN].position()
        move = [x - cp[0], y - cp[1]]
        if move == [0, 0]:  # no move
            return True
        normalized_move, num_moves = self.normalize_move(move)
 #       print('checking ' + FEN + ' [' + str(x) + ',' + str(y) + '] ' + ' [' + str(cp[0]) + ',' + str(cp[1]) + '] ' + '[' + str(move[0]) + ',' + str(move[1]) + ']' + ' num moves ', str(num_moves))
        if not(self.pieces[FEN].is_pawn() or self.pieces[FEN].is_king()):
            if num_moves > self.pieces[FEN].max_moves:
                return False
            for vector in self.pieces[FEN].directions:
                if vector == normalized_move:
                    for piece in self.pieces:  # for a move in a possible direction, check to see if anything is
                        if self.pieces[piece].position() == [x, y]\
                                and self.pieces[FEN].color == self.pieces[piece].color:  # is already there on our side
                            return False
                        if not self.pieces[FEN].is_knight():  # check to see if we are jumping over other pieces,
                            for i in range(1, num_moves):  # which doesn't apply to knights
                                in_between_pos = [cp[0]+i*normalized_move[0], cp[1]+i*normalized_move[1]]
                                if self.pieces[piece].position() == in_between_pos:
                                    return False
                    return True
            return False
        # Special cases
        # pawns take diagonally, but not forwards
        elif self.pieces[FEN].is_pawn():
            if move[1] == 0:  # no vertical movement, a move without taking
                if self.pieces[FEN].num_moves == 0 and num_moves > 2:
                # On the first move you can move more than one space
                    return False
                elif self.pieces[FEN].num_moves != 0 and num_moves > 1:
                    return False
                possible_direction_found = False
                for vector in self.pieces[FEN].directions:
                    if vector == normalized_move:
                        possible_direction_found = True
                if possible_direction_found:
                    for piece in self.pieces:
                        for i in range(1, num_moves+1):
                            in_between_pos = [cp[0]+i*normalized_move[0], cp[1]+i*normalized_move[1]]
                            if self.pieces[piece].position() == in_between_pos:
                                return False
                    return True
                else:
                    return False
            else:  # move by taking
                for piece in self.pieces:
                    if move in self.pieces[FEN].take_moves and self.pieces[piece].position() == [x, y]\
                            and self.pieces[FEN].opponent(self.pieces[piece]):
                        return True
                return False
        else:  # we must be moving a king
            possible_direction_found = False
            for vector in self.pieces[FEN].directions:
                if vector == move:
                    possible_direction_found = True
            if possible_direction_found:
                for piece in self.pieces:
                    if (self.pieces[piece].color == self.pieces[FEN].color) and self.pieces[piece].position() == [x,y]:
                        return False
                    if not(self.pieces[piece].is_king()) and self.pieces[piece].opponent(self.pieces[FEN]):
                        if self.check_move(self.pieces[piece].FEN, x, y):
                            print('check found' + piece)
                            return False  # the king would move into check
                    elif self.pieces[piece].opponent(self.pieces[FEN]):
                        other_king_pos = self.pieces[piece].position()
                        if max(abs(x - other_king_pos[0]), abs(y - other_king_pos[1])) == 1:
                            return False
                return True
            else:
                return False

    def move(self, FEN, x, y):
        if self.check_move(FEN, x, y) and self.pieces[FEN].is_turn():
            self.pieces[FEN].move(x, y)
#            print(str(self.pieces[FEN]) + 'moved to [' + str(x) + ',' + str(y) + ']')
            for piece in self.pieces:
                if piece != FEN and self.pieces[piece].position() == [x, y]:
                    self.pieces[piece].capture(self.pieces[FEN])
            if self.pieces[FEN].is_pawn:
                if (self.pieces[FEN].is_white() and x == 7) or \
                        (self.pieces[FEN].is_black() and x == 0):
                    self.trade_in_pawn(FEN)
            check = self.check(FEN)
            if check:
                checkmate = self.check_mate(self.opponent_king(FEN))
                if self.pieces[FEN].is_white():
                    clr = 'black'
                else:
                    clr = 'white'
                if checkmate:
                    self.cb.checkmate.config(text=clr + " is in checkmate")
                else:
                    self.cb.checkmate.config(text=clr + " is in check")
            self.pieces[FEN].change_sides()
            return True
        else:
            return False

    def trade_in_pawn(self, FEN):
        print('trade in pawn', FEN)

    def opponent_king(self, FEN):
        if self.pieces[FEN].is_white():
            return 'k'
        else:
            return 'K'

    def check(self, last_moved):
        opponent_color = self.pieces[last_moved].color
        FEN = self.opponent_king(last_moved)
        for piece in self.pieces:
            if self.pieces[piece].color == opponent_color:
                if self.check_move(piece, self.pieces[FEN].x, self.pieces[FEN].y):
 #                   print('check', 'opponent color', opponent_color, self.pieces[FEN], self.pieces[piece])
                    return True
        return False

    def check_mate(self, FEN):
        x = self.pieces[FEN].position()[0]
        y = self.pieces[FEN].position()[1]
        return not(self.check_move(FEN, x+1, y) or self.check_move(FEN, x+1, y+1) or self.check_move(FEN, x+1, y-1) or \
               self.check_move(FEN, x, y+1) or self.check_move(FEN, x, y-1) or \
               self.check_move(FEN, x-1, y) or self.check_move(FEN, x-1, y+1) or self.check_move(FEN, x-1, y-1))

    def possible_moves(self, FEN):
        pm = []
        for x in range(8):
            for y in range(8):
                if self.check_move(FEN, x, y) and [x,y] != self.pieces[FEN].position():
                    pm.append([x,y])
        return pm

    def clicked(self, event):
        """
        Works with the input boxes
        """
        row = event.x//self.cb.dim_square
        col = event.y//self.cb.dim_square
        if Pieces.piece_chosen is None:
            for piece in self.pieces:
                if (self.pieces[piece].position() == [row, col]) and self.pieces[piece].is_turn():
                        Pieces.piece_chosen=piece
                        self.pieces[piece].possible_moves = self.possible_moves(piece)
                        self.draw_board_pm(self.pieces[piece].possible_moves)
                        print("chose"+piece)
                        return
        else:
            if [row, col] in self.pieces[Pieces.piece_chosen].possible_moves:
                self.move(Pieces.piece_chosen, row, col)
                self.draw_board()
                Pieces.piece_chosen = None
                return

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
                if [x,y] == self.pieces[self.piece_chosen].position():
                    position_color = color
                else:
                    self.cb.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="area")
                color = temp
                color = self.cb.swap_colors(color)
        [x, y] = self.pieces[self.piece_chosen].position()
        x1 = (x * self.cb.dim_square)
        y1 = (y * self.cb.dim_square)
        x2 = x1 + self.cb.dim_square
        y2 = y1 + self.cb.dim_square
        self.cb.canvas.create_rectangle(x1, y1, x2, y2, fill=position_color, width=3, tags="area")
        for piece in self.pieces:
            p = self.pieces[piece]
            if not p.captured:
                self.cb.canvas.create_text(p.x*self.cb.dim_square+self.cb.dim_square / 2,
                        p.y*self.cb.dim_square+self.cb.dim_square / 2, text=p.FEN)

    def draw_board(self):
        color = self.cb.color1
        for x in range(self.cb.rows):
            color = self.cb.swap_colors(color)
            for y in range(self.cb.columns):
                x1 = (x * self.cb.dim_square)
                y1 = (y * self.cb.dim_square)
                x2 = x1 + self.cb.dim_square
                y2 = y1 + self.cb.dim_square
                self.cb.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="area")
                color = self.cb.swap_colors(color)
        for piece in self.pieces:
            p = self.pieces[piece]
            if not p.captured:
                self.cb.canvas.create_text(p.x*self.cb.dim_square+self.cb.dim_square / 2,
                        p.y*self.cb.dim_square+self.cb.dim_square / 2, text=p.FEN)

#chess_set = Pieces()

