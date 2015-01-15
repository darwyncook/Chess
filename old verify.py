__author__ = 'cook'

        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        cp = self.pieces[FEN].position()
        move = [x - cp[0], y - cp[1]]
        if move == [0, 0]:  # no move
            return False
        normalized_move, num_moves = self.normalize_move(move)
        if not(self.pieces[FEN].is_pawn() or self.pieces[FEN].is_king()):
            if num_moves > self.pieces[FEN].max_moves:
                return False
            if self.endanger_king(FEN, x, y):
                return False
            if (self.pieces[FEN].color == Pieces.color_in_check and self.can_remove_check(FEN, x, y)) or \
                    not(self.pieces[FEN].color == Pieces.color_in_check):
#                print('checking ' + FEN + ' [' + str(x) + ',' + str(y) + '] ' + ' [' + str(cp[0]) + ',' + str(cp[1]) + '] ' + '[' + str(move[0]) + ',' + str(move[1]) + ']' + ' num moves ', str(num_moves))
                for vector in self.pieces[FEN].directions:
                    if vector == normalized_move:
                        for piece in self.pieces:  # for a move in a possible direction, check to see if anything is
                            if self.pieces[piece].position() == [x, y] and not(self.pieces[piece].captured)\
                                    and self.pieces[FEN].color == self.pieces[piece].color:  # is already there on our side
                                return False
                            if not self.pieces[FEN].is_knight():  # check to see if we are jumping over other pieces,
                                for i in range(1, num_moves):  # which doesn't apply to knights
                                    in_between_pos = [cp[0]+i*normalized_move[0], cp[1]+i*normalized_move[1]]
                                    if self.pieces[piece].position() == in_between_pos and not(self.pieces[piece].captured):
                                        return False
                            # If we move will our king be in check?
                        return True
            return False
        # Special cases
        # pawns take diagonally, but not forwards
        elif self.pieces[FEN].is_pawn():
            if self.endanger_king(FEN, x, y):
                return False
            if move[1] == 0:  # no vertical movement, a move without taking
                if self.pieces[FEN].num_moves == 0 and num_moves > 2:
                # On the first move you can move more than one space
                    return False
                elif self.pieces[FEN].num_moves != 0 and num_moves > 1:
                    return False
                if Pieces.color_in_check is not None:  # if we are in check we must take the last piece
                    if not(self.can_remove_check(FEN, x, y)):
#                        print("crap"+ FEN)
                        return False
                possible_direction_found = False
                for vector in self.pieces[FEN].directions:
                    if vector == normalized_move:
                        possible_direction_found = True
                if possible_direction_found:
                    for piece in self.pieces:
                        for i in range(1, num_moves+1):
                            in_between_pos = [cp[0]+i*normalized_move[0], cp[1]+i*normalized_move[1]]
                            if self.pieces[piece].position() == in_between_pos and not(self.pieces[piece].captured):
                                return False
                    return True
                else:
                    return False
            else:  # move by taking
                if (self.pieces[FEN].color == Pieces.color_in_check and self.can_remove_check(FEN, x, y)) or \
                        not(self.pieces[FEN].color == Pieces.color_in_check):
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
#                    print("move", str(move[0]), str(move[1]))
            if possible_direction_found:
                for piece in self.pieces:
                    if (self.pieces[piece].color == self.pieces[FEN].color) and self.pieces[piece].position() == [x,y] \
                            and not(self.pieces[piece].captured):
                        return False
                    # are we moving in to check?
                    elif self.pieces[FEN].opponent(self.pieces[piece]) and not(self.pieces[piece].captured):
                        if self.pieces[piece].is_king():
                            other_king_pos = self.pieces[piece].position()
                            if max(abs(x - other_king_pos[0]), abs(y - other_king_pos[1])) == 1:
                                return False  # We would be in check by the other king
                        else:
                            [tempx, tempy] = self.pieces[FEN].position()
                            self.pieces[FEN].x = x
                            self.pieces[FEN].y = y
                            good_move = True
                            for piece in self.pieces:  # for a move in a possible direction, check to see if anything is
                                if self.pieces[piece].position() == [x, y] and not(self.pieces[piece].captured)\
                                    and self.pieces[FEN].color == self.pieces[piece].color:
                                    good_move = False
                                elif self.verify_move(piece, x, y) and not(self.pieces[piece].captured):
                                    good_move = False
                            self.pieces[FEN].x = tempx
                            self.pieces[FEN].y = tempy
                            return good_move  # the king would move into check or another player
                return True
            else:
 #               print("bad direction"+str(x)+str(y) )
                return False




                        # If the piece is at [x,y] we can take it, so we don't worry about those pieces
                        # next we test to see if the piece can move to (x,y). If the piece is a pawn it must be
                        # executing a taking move.




