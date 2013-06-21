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
        '''
        Naive random choice.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[random.randrange(len(pieces_available))])
        indices = [i for i, x in enumerate(in_play) if x == -1]
        index = indices[random.randrange(len(indices))]
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        move = Move(index,next_piece,pieces_available[random.randrange(len(pieces_available))])
        return move
    
    def next_move(self,board):
        move = self.test_next_move(board)
        i = 0
        while(self.is_suicide_move(move,board) and i < 5):
            move = self.test_next_move(board)
            i += 1
        return move
        
    def is_suicide_move(self,move,board):
        original_after_my_move = copy.deepcopy(board)
        original_after_my_move.make_move(move)
        other_player = Algo4("hash")
        for i in range(5):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            if(test_board.is_winning_arrangement()):
                return True
        return False
        
        
    def __repr__(self):
        return "Algo3"+str(self.identifier)

class Algo3_with_how_deep(Player):
    '''
    Ply 1 strategy 3.
    '''

    def __init__(self,identifier,how_deep):
        self.identifier = identifier
        self.how_deep = how_deep

    def test_next_move(self,board):
        '''
        Naive random choice.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[random.randrange(len(pieces_available))])
        indices = [i for i, x in enumerate(in_play) if x == -1]
        index = indices[random.randrange(len(indices))]
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        move = Move(index,next_piece,pieces_available[random.randrange(len(pieces_available))])
        return move

    def next_move(self,board):
        move = self.test_next_move(board)
        i = 0
        while(self.is_suicide_move(move,board) and i < self.how_deep):
            move = self.test_next_move(board)
            i += 1
        return move

    def is_suicide_move(self,move,board):
        original_after_my_move = copy.deepcopy(board)
        original_after_my_move.make_move(move)
        other_player = Algo4("hash")
        for i in range(self.how_deep):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            if(test_board.is_winning_arrangement()):
                return True
        return False


    def __repr__(self):
        return "Algo3_with_how_deep"+str(self.identifier)


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
    Ply 3 strategy 5.
    '''

    def __init__(self,identifier):
        self.identifier = identifier

    def test_next_move(self,board):
        '''
        Naive random choice.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[random.randrange(len(pieces_available))])
        indices = [i for i, x in enumerate(in_play) if x == -1]
        index = indices[random.randrange(len(indices))]
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        move = Move(index,next_piece,pieces_available[random.randrange(len(pieces_available))])
        return move

    def next_move(self,board):
        indices = [i for i, x in enumerate(board.in_play) if x == -1]
        num_moves_left = len(indices)
        how_deep = min(14,max(2,16-int(num_moves_left*2)))
        move = self.test_next_move(board)
        saved_move = move
        i = 0
        while(i < how_deep):
            #print "test_move",i
            move_type = self.type_of_move(move,board,how_deep)
            if(move_type == "winning_move"):
                return move
            if(move_type == "neutral_move"):
                saved_move = move
            move = self.test_next_move(board)
            i += 1
        return saved_move

    def type_of_move(self,move,board,how_deep):
        original_after_my_move = copy.deepcopy(board)
        #print "now              ",original_after_my_move
        original_after_my_move.make_move(move)
        if(original_after_my_move.is_winning_arrangement()):
            return "winning_move"
        #print "one move ahead   ",original_after_my_move
        other_player = Algo4("hash")
        my_inner_player = Algo3_with_how_deep("hash",how_deep/2)
        for i in range(how_deep):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            #print "two moves ahead  ",test_board
            if(test_board.is_winning_arrangement()):
                return "losing_move"
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            #print "three moves ahead",test_board
            if(test_board.is_winning_arrangement()):
                return "winning_move"      
        return "neutral_move"


    def __repr__(self):
        return "Algo5"+str(self.identifier)


class Algo6(Player):
    '''
    Ply 3 strategy 6, with random inner move.
    '''

    def __init__(self,identifier):
        self.identifier = identifier

    def test_next_move(self,board):
        '''
        Naive random choice.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[random.randrange(len(pieces_available))])
        indices = [i for i, x in enumerate(in_play) if x == -1]
        index = indices[random.randrange(len(indices))]
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        move = Move(index,next_piece,pieces_available[random.randrange(len(pieces_available))])
        return move

    def next_move(self,board):
        indices = [i for i, x in enumerate(board.in_play) if x == -1]
        num_moves_left = len(indices)
        how_deep = min(14,max(2,16-int(num_moves_left*2)))
        move = self.test_next_move(board)
        saved_move = move
        i = 0
        while(i < how_deep):
            #print "test_move",i
            move_type = self.type_of_move(move,board,how_deep)
            if(move_type == "winning_move"):
                return move
            if(move_type == "neutral_move"):
                saved_move = move
            move = self.test_next_move(board)
            i += 1
        return saved_move

    def type_of_move(self,move,board,how_deep):
        original_after_my_move = copy.deepcopy(board)
        #print "now              ",original_after_my_move
        original_after_my_move.make_move(move)
        if(original_after_my_move.is_winning_arrangement()):
            return "winning_move"
        #print "one move ahead   ",original_after_my_move
        other_player = Algo4("hash")
        my_inner_player = Algo4("hash")
        for i in range(how_deep):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            #print "two moves ahead  ",test_board
            if(test_board.is_winning_arrangement()):
                return "losing_move"
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            #print "three moves ahead",test_board
            if(test_board.is_winning_arrangement()):
                return "winning_move"      
        return "neutral_move"


    def __repr__(self):
        return "Algo6"+str(self.identifier)


class Algo7(Player):
    '''
    Ply 3 strategy 7, with probabilistic.
    '''

    def __init__(self,identifier):
        self.identifier = identifier

    def test_next_move(self,board):
        '''
        Naive random choice.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[random.randrange(len(pieces_available))])
        indices = [i for i, x in enumerate(in_play) if x == -1]
        index = indices[random.randrange(len(indices))]
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        move = Move(index,next_piece,pieces_available[random.randrange(len(pieces_available))])
        return move

    def next_move(self,board):
        indices = [i for i, x in enumerate(board.in_play) if x == -1]
        num_moves_left = len(indices)
        how_deep = min(14,max(2,16-int(num_moves_left*2)))
        move = self.test_next_move(board)
        saved_move = move
        i = 0
        current_probability = -1
        while(i < how_deep):
            #print "test_move",i
            move_type = self.type_of_move(move,board,how_deep)
            if(move_type == "winning_move"):
                return move
            if(move_type > current_probability):
                saved_move = move
                current_probability = move_type
            move = self.test_next_move(board)
            i += 1
        return saved_move

    def type_of_move(self,move,board,how_deep):
        original_after_my_move = copy.deepcopy(board)
        #print "now              ",original_after_my_move
        original_after_my_move.make_move(move)
        if(original_after_my_move.is_winning_arrangement()):
            return "winning_move"
        #print "one move ahead   ",original_after_my_move
        other_player = Algo4("hash")
        my_inner_player = Algo4("hash")
        losers = 0
        winners = 0
        for i in range(how_deep):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            #print "two moves ahead  ",test_board
            if(test_board.is_winning_arrangement()):
                losers += 1
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            #print "three moves ahead",test_board
            if(test_board.is_winning_arrangement()):
                winners += 1      
        return 1.0 * (winners-losers) / how_deep


    def __repr__(self):
        return "Algo7"+str(self.identifier)


class Algo8(Player):
    '''
    Ply 3 strategy 8, with probabilistic.
    '''

    def __init__(self,identifier):
        self.identifier = identifier

    def test_next_move(self,board):
        '''
        Naive random choice.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[random.randrange(len(pieces_available))])
        indices = [i for i, x in enumerate(in_play) if x == -1]
        index = indices[random.randrange(len(indices))]
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        move = Move(index,next_piece,pieces_available[random.randrange(len(pieces_available))])
        return move

    def all_next_moves(self,board):
        '''
        All moves possible.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            moves = list()
            for i in range(len(pieces_available)):
                moves.append(Move(-1,-1,pieces_available[i]))
            return moves
        indices = [i for i, x in enumerate(in_play) if x == -1]
        moves = list()
        for index in indices:
            if len(pieces_available) == 0:
                pieces_available.append(-1)
            for i in range(len(pieces_available)):
                moves.append(Move(index,next_piece,pieces_available[i]))
        return moves

    def next_move(self,board):
        indices = [i for i, x in enumerate(board.in_play) if x == -1]
        num_moves_left = len(indices)
        how_deep = min(14,max(2,16-int(num_moves_left*2)))
        moves = self.all_next_moves(board)
        saved_move = moves[0]
        current_probability = -1
        if len(moves) > 100:
            random.shuffle(moves)
        i = 0
        for move in moves:
            move_type = self.type_of_move(move,board,how_deep)
            if(move_type == "winning_move"):
                return move
            if(move_type > current_probability):
                saved_move = move
                current_probability = move_type
            i += 1
            if i > 100:
                break
        return saved_move

    def type_of_move(self,move,board,how_deep):
        original_after_my_move = copy.deepcopy(board)
        #print "now              ",original_after_my_move
        original_after_my_move.make_move(move)
        if(original_after_my_move.is_winning_arrangement()):
            return "winning_move"
        #print "one move ahead   ",original_after_my_move
        other_player = Algo3_with_how_deep("hash",how_deep/2)
        my_inner_player = Algo3_with_how_deep("hash",how_deep/2)
        losers = 0
        winners = 0
        for i in range(how_deep):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            #print "two moves ahead  ",test_board
            if(test_board.is_winning_arrangement()):
                losers += 1
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            #print "three moves ahead",test_board
            if(test_board.is_winning_arrangement()):
                winners += 1      
        return 1.0 * (winners-losers) / how_deep


    def __repr__(self):
        return "Algo8"+str(self.identifier)


class Algo9(Player):
    '''
    Ply 3 strategy 9, with probabilistic, with inner players of 8.
    '''

    def __init__(self,identifier):
        self.identifier = identifier

    def test_next_move(self,board):
        '''
        Naive random choice.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            return Move(-1,-1,pieces_available[random.randrange(len(pieces_available))])
        indices = [i for i, x in enumerate(in_play) if x == -1]
        index = indices[random.randrange(len(indices))]
        if len(pieces_available) == 0:
            pieces_available.append(-1)
        move = Move(index,next_piece,pieces_available[random.randrange(len(pieces_available))])
        return move

    def all_next_moves(self,board):
        '''
        All moves possible.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            moves = list()
            for i in range(len(pieces_available)):
                moves.append(Move(-1,-1,pieces_available[i]))
            return moves
        indices = [i for i, x in enumerate(in_play) if x == -1]
        moves = list()
        for index in indices:
            if len(pieces_available) == 0:
                pieces_available.append(-1)
            for i in range(len(pieces_available)):
                moves.append(Move(index,next_piece,pieces_available[i]))
        return moves

    def next_move(self,board):
        indices = [i for i, x in enumerate(board.in_play) if x == -1]
        num_moves_left = len(indices)
        how_deep = min(14,max(2,16-int(num_moves_left*2)))
        moves = self.all_next_moves(board)
        saved_move = moves[0]
        current_probability = -1
        if len(moves) > 100:
            random.shuffle(moves)
        i = 0
        for move in moves:
            move_type = self.type_of_move(move,board,how_deep)
            if(move_type == "winning_move"):
                return move
            if(move_type > current_probability):
                saved_move = move
                current_probability = move_type
            i += 1
            if i > 100:
                break
        return saved_move

    def type_of_move(self,move,board,how_deep):
        original_after_my_move = copy.deepcopy(board)
        #print "now              ",original_after_my_move
        original_after_my_move.make_move(move)
        if(original_after_my_move.is_winning_arrangement()):
            return "winning_move"
        #print "one move ahead   ",original_after_my_move
        other_player = Algo6("hash")
        my_inner_player = Algo6("hash")
        losers = 0
        winners = 0
        for i in range(how_deep):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            #print "two moves ahead  ",test_board
            if(test_board.is_winning_arrangement()):
                losers += 1
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            #print "three moves ahead",test_board
            if(test_board.is_winning_arrangement()):
                winners += 1      
        return 1.0 * (winners-losers) / how_deep


    def __repr__(self):
        return "Algo9"+str(self.identifier)


class Algo10(Player):
    '''
    Ply 3 strategy 10, with probabilistic.
    '''

    def __init__(self,identifier):
        self.identifier = identifier

    def all_next_moves(self,board):
        '''
        All moves possible.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            moves = list()
            for i in range(len(pieces_available)):
                moves.append(Move(-1,-1,pieces_available[i]))
            return moves
        indices = [i for i, x in enumerate(in_play) if x == -1]
        moves = list()
        for index in indices:
            if len(pieces_available) == 0:
                pieces_available.append(-1)
            for i in range(len(pieces_available)):
                moves.append(Move(index,next_piece,pieces_available[i]))
        return moves

    def next_move(self,board):
        indices = [i for i, x in enumerate(board.in_play) if x == -1]
        num_moves_left = len(indices)
        how_deep = min(100,max(2,15*(16-int(num_moves_left))))
        moves = self.all_next_moves(board)
        saved_move = moves[0]
        current_probability = -1
        if len(moves) > how_deep:
            random.shuffle(moves)
        i = 0
        for move in moves:
            move_type = self.type_of_move(move,board,max(2,min(10,how_deep/15)))
            if(move_type == "winning_move"):
                return move
            if(move_type > current_probability):
                saved_move = move
                current_probability = move_type
            i += 1
            if i > how_deep:
                break
        return saved_move

    def type_of_move(self,move,board,how_deep):
        original_after_my_move = copy.deepcopy(board)
        #print "now              ",original_after_my_move
        original_after_my_move.make_move(move)
        if(original_after_my_move.is_winning_arrangement()):
            return "winning_move"
        #print "one move ahead   ",original_after_my_move
        other_player = Algo3_with_how_deep("hash",how_deep/2)
        my_inner_player = Algo3_with_how_deep("hash",how_deep/2)
        losers = 0
        winners = 0
        for i in range(how_deep):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            #print "two moves ahead  ",test_board
            if(test_board.is_winning_arrangement()):
                losers += 1
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            #print "three moves ahead",test_board
            if(test_board.is_winning_arrangement()):
                winners += 1      
        return 1.0 * (winners-losers) / how_deep


    def __repr__(self):
        return "Algo10"+str(self.identifier)

class AlgoMiniMax(Player):
    '''
    Minimax strategy, with depth specified.
    '''

    def __init__(self,identifier,depth):
        self.identifier = identifier
        self.depth = depth

    def all_next_moves(self,board):
        '''
        All moves possible.
        '''
        in_play = board.in_play
        next_piece = board.next_piece
        pieces_available = board.pieces_available
        if(next_piece == -1):
            moves = list()
            for i in range(len(pieces_available)):
                moves.append(Move(-1,-1,pieces_available[i]))
            return moves
        indices = [i for i, x in enumerate(in_play) if x == -1]
        moves = list()
        for index in indices:
            if len(pieces_available) == 0:
                pieces_available.append(-1)
            for i in range(len(pieces_available)):
                moves.append(Move(index,next_piece,pieces_available[i]))
        return moves

    def next_move(self,board):
        
        indices = [i for i, x in enumerate(board.in_play) if x == -1]
        num_moves_left = len(indices)
        how_deep = min(100,max(2,15*(16-int(num_moves_left))))
        moves = self.all_next_moves(board)
        saved_move = moves[0]
        current_probability = -1
        if len(moves) > how_deep:
            random.shuffle(moves)
        i = 0
        for move in moves:
            move_type = self.type_of_move(move,board,max(2,min(10,how_deep/15)))
            if(move_type == "winning_move"):
                return move
            if(move_type > current_probability):
                saved_move = move
                current_probability = move_type
            i += 1
            if i > how_deep:
                break
        return saved_move

    def type_of_move(self,move,board,how_deep):
        original_after_my_move = copy.deepcopy(board)
        #print "now              ",original_after_my_move
        original_after_my_move.make_move(move)
        if(original_after_my_move.is_winning_arrangement()):
            return "winning_move"
        #print "one move ahead   ",original_after_my_move
        other_player = Algo3_with_how_deep("hash",how_deep/2)
        my_inner_player = Algo3_with_how_deep("hash",how_deep/2)
        losers = 0
        winners = 0
        for i in range(how_deep):
            test_board = copy.deepcopy(original_after_my_move)
            other_player_move = other_player.next_move(test_board)
            test_board.make_move(other_player_move)
            #print "two moves ahead  ",test_board
            if(test_board.is_winning_arrangement()):
                losers += 1
            my_inner_move = my_inner_player.next_move(test_board)
            test_board.make_move(my_inner_move)
            #print "three moves ahead",test_board
            if(test_board.is_winning_arrangement()):
                winners += 1      
        return 1.0 * (winners-losers) / how_deep


    def __repr__(self):
        return "Algo10"+str(self.identifier)

