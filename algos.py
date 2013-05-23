import copy
import random
from board import Move,Board

class Player():
    '''
    Abstract class of a player.
    '''
    identifier = -1
    
    def __init__(self,identifier):
        self.identifier = identifier
        
    def next_move(self,board):
        pass

class Algo1(Player):
    '''
    Naive strategy 1.
    '''
    
    def __init__(self,identifier):
        self.identifier = identifier
        
    def next_move(self,board):
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[0])
        index = in_play.index(-1)
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        return Move(index,next_piece,pieces_available[0])
        
    def __repr__(self):
        return "Algo1"+str(self.identifier)


class Algo2(Player):
    '''
    Naive strategy 2.
    '''
    
    def __init__(self,identifier):
        self.identifier = identifier
        
    def next_move(self,board):
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[len(pieces_available)-1])
        index = len(in_play) - in_play[::-1].index(-1) - 1
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        return Move(index,next_piece,pieces_available[len(pieces_available)-1])

    def __repr__(self):
        return "Algo2"+str(self.identifier)


class Algo3(Player):
    '''
    Ply 1 strategy 3.
    '''
    
    def __init__(self,identifier):
        self.identifier = identifier
        
    def test_next_move(self,board):
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[0])
        index = in_play.index(-1)
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        #check other player doesnt win    
        move = Move(index,next_piece,pieces_available[0])
        return move
    
    def next_move(self,board):
        move = self.test_next_move(board)
        i = 0
        while(self.is_suicide_move(move,board) and i < 10):
            move = self.test_next_move(board)
            i += 1
        return move
        
    def is_suicide_move(self,move,board):
        original = copy.deepcopy(board)
        original_after_my_move = copy.deepcopy(original)
        original_after_my_move.make_move(move)
        other_player = Algo4("hash")
        for i in range(10):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            if(test_board.is_winning_arrangement()):
                return True
        return False
        
        
    def __repr__(self):
        return "Algo3"+str(self.identifier)


class Algo4(Player):
    '''
    Random strategy 4.
    '''
    
    def __init__(self,identifier):
        self.identifier = identifier
        
    def next_move(self,board):
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[random.randrange(len(pieces_available))])
        indices = [i for i, x in enumerate(in_play) if x == -1]
        index = indices[random.randrange(len(indices))]
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        return Move(index,next_piece,pieces_available[random.randrange(len(pieces_available))])

    def __repr__(self):
        return "Algo4"+str(self.identifier)


class Algo5(Player):
    '''
    Ply 2 strategy 5.
    '''

    def __init__(self,identifier):
        self.identifier = identifier

    def test_next_move(self,board):
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[0])
        index = in_play.index(-1)
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        #check other player doesnt win    
        move = Move(index,next_piece,pieces_available[0])
        return move

    def next_move(self,board):
        move = self.test_next_move(board)
        saved_move = move
        i = 0
        while(i < 10):
            move_type = self.type_of_move(move,board)
            if(move_type == "winning_move"):
                return move
            if(move_type == "neutral_move"):
                saved_move = move
            move = self.test_next_move(board)
            i += 1
        return saved_move

    def type_of_move(self,move,board):
        original = copy.deepcopy(board)
        original_after_my_move = copy.deepcopy(original)
        original_after_my_move.make_move(move)
        other_player = Algo4("hash")
        my_inner_player = Algo3("hash")
        for i in range(10):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            if(test_board.is_winning_arrangement()):
                return "losing_move"
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            if(test_board.is_winning_arrangement()):
                return "winning_move"      
        return "neutral_move"


    def __repr__(self):
        return "Algo5"+str(self.identifier)

class Algo6(Player):
    '''
    Ply 2 strategy 6.
    '''

    def __init__(self,identifier):
        self.identifier = identifier

    def test_next_move(self,board):
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[0])
        index = in_play.index(-1)
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        #check other player doesnt win    
        move = Move(index,next_piece,pieces_available[0])
        return move

    def next_move(self,board):
        move = self.test_next_move(board)
        saved_move = move
        i = 0
        while(i < 10):
            move_type = self.type_of_move(move,board)
            if(move_type == "winning_move"):
                return move
            move = self.test_next_move(board)
            i += 1
        return saved_move

    def type_of_move(self,move,board):
        original = copy.deepcopy(board)
        original_after_my_move = copy.deepcopy(original)
        original_after_my_move.make_move(move)
        other_player = Algo4("hash")
        my_inner_player = Algo3("hash")
        for i in range(10):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            if(test_board.is_winning_arrangement()):
                return "losing_move"
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            if(test_board.is_winning_arrangement()):
                return "winning_move"      
        return "neutral_move"


    def __repr__(self):
        return "Algo6"+str(self.identifier)
