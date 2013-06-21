import copy
import datetime
from algos import Player,Algo4,Algo3,Algo5,Algo6,Algo7,Algo8,Algo9,Algo10
from board import Move,Board

def drive():
    num_games = 5
    
    player_1 = "a"
    player_2 = "b"
    player_1_wins = 0
    player_2_wins = 0
    stalemates = 0
    
    for j in range(num_games):
        board = Board()

        player_a = Algo10(player_1)
        player_b = Algo7(player_2)
        if j % 2 == 0:
            current_player = player_a
        else:
            current_player = player_b
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
            
    print player_a,"_wins:",player_1_wins
    print player_b,"_wins:",player_2_wins
    print "stalemates:",stalemates


if __name__=="__main__":
    tic = datetime.datetime.now()
    drive()
    toc = datetime.datetime.now()
    print toc-tic