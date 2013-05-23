import copy
import datetime
from algos import Player,Algo4,Algo3,Algo5,Algo6
from board import Move,Board

 

if __name__=="__main__":
    tic = datetime.datetime.now()
    num_games = 1000
    
    player_1 = "a"
    player_2 = "b"
    player_1_wins = 0
    player_2_wins = 0
    stalemates = 0
    
    for j in range(num_games):
        board = Board()

        player_a = Algo6(player_1)
        player_b = Algo4(player_2)
        
        current_player = player_a
        i = 0
        while(not board.game_over()):
            #print "Round:",str(i),"  Player:",current_player
            board_for_player = copy.deepcopy(board)
            move = current_player.next_move(board_for_player)
            #print "before_move",board
            #print move
            board.make_move(move)
            #print "after_move ",board
            if(not board.game_over()):
                if current_player == player_a:
                    current_player = player_b
                else:
                    current_player = player_a
                i += 1
        if(board.is_winning_arrangement()):
            if player_1 in str(current_player):
                player_1_wins += 1
            else:
                player_2_wins += 1
        else:
            stalemates += 1
            
    print "p1_wins:",player_1_wins
    print "p2_wins:",player_2_wins
    print "stalemates:",stalemates
    toc = datetime.datetime.now()
    print toc-tic