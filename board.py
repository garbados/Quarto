import copy


class Move():
    index = -1
    current_piece = -1
    next_piece = -1

    def __init__(self, index, current_piece, next_piece):
        self.index = index
        self.current_piece = current_piece
        self.next_piece = next_piece

    def __repr__(self):
        return "Move[ index:" + str(self.index) + "\tcurrent_piece:" + str(self.current_piece) + "\tnext_piece:" + str(self.next_piece) + " ]"


class Board():

    '''
    Track all pieces in the game, main game opperations.
    '''
    in_play = []
    next_piece = -1
    pieces_available = []

    ALL_PIECES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    ATTRIBUTES = [[0, 1, 2, 3, 4, 5, 6, 7],   [8, 9, 10, 11, 12, 13, 14, 15],
                  [0, 1, 2, 3, 8, 9, 10, 11], [4, 5, 6, 7, 12, 13, 14, 15],
                  [0, 1, 4, 5, 8, 9, 12, 13], [2, 3, 6, 7, 10, 11, 14, 15],
                  [0, 2, 4, 6, 8, 10, 12, 14], [1, 3, 5, 7, 9, 11, 13, 15]]

    def __init__(self):
        self.in_play = [-1, -1, -1, -1, -1, -1,
                        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.next_piece = -1
        self.pieces_available = [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def four_match(self, a, b, c, d):
        total = 15
        if(a < 0 or b < 0 or c < 0 or d < 0):
            return False
        a_opp = total - a
        b_opp = total - b
        c_opp = total - c
        d_opp = total - d
        return ((a & b & c & d) > 0 or (a_opp & b_opp & c_opp & d_opp) > 0)

    def __deepcopy__(self, memo):
        result = Board()
        result.in_play = self.in_play[::]
        result.next_piece = self.next_piece
        result.pieces_available = self.pieces_available[::]
        return result

    def __repr__(self):
        return "Board: [in_play:" + str(self.in_play) + "\tnext_piece:" + str(self.next_piece) + "\tpieces_available" + str(self.pieces_available) + " ]"

    def make_move(self, move):
        '''
        Check the move is valid, then move pieces accordingly.
        '''
        if(self.check_move_valid(move)):
            self.in_play[move.index] = move.current_piece
            if(move.next_piece != -1):
                self.pieces_available.remove(move.next_piece)
            self.next_piece = move.next_piece
            return True
        else:
            return False

    def check_move_valid(self, move):
        '''
        Check if the space is clear, and the next piece is available.
        '''
        if(self.in_play[move.index] == -1 and (move.next_piece in self.pieces_available or move.next_piece == -1)):
            return True
        return False

    def game_over(self):
        return self.is_winning_arrangement() or -1 not in self.in_play

    def is_winning_arrangement(self):
        '''
        Check if there is a winning arrangement on board.
        '''
        in_play = self.in_play
        winning = False
        for i in range(4):
            winning = winning or self.four_match(in_play[
                                                 4 * i], in_play[4 * i + 1], in_play[4 * i + 2], in_play[4 * i + 3])
            winning = winning or self.four_match(in_play[
                                                 i], in_play[i + 4], in_play[i + 8], in_play[i + 12])
        winning = winning or self.four_match(in_play[
                                             0], in_play[5], in_play[10], in_play[15])
        winning = winning or self.four_match(in_play[
                                             3], in_play[6], in_play[9], in_play[12])
        return winning


def check_all_pieces(attributes_one, attributes_two, attributes_all):
    '''
    Check two opposite attributes add to be full set of pieces.
    '''
    attributes_possible = set(attributes_one).union(set(attributes_two))

    return set(attributes_all) == attributes_possible


def check_all_pieces_accounted_for(board, next_piece, pieces_available, ALL_PIECES):
    '''
    Check all portions of game, the board, next piece, and pieces available will add to be full set of pieces.
    '''
    all_pieces = set()
    for r in range(4):
        for c in range(4):
            if(board[r][c] != -1):
                all_pieces.add(board[r][c])

    if(next_piece != -1):
        all_pieces.add(next_piece)

    for i in range(len(pieces_available)):
        all_pieces.add(pieces_available[i])

    return set(ALL_PIECES) == all_pieces
