"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided


# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 10    # Number of trials to run
MCMATCH = 2.0  # Score for squares played by the machine player
MCOTHER = 2.0  # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    """
    while board.check_win() == None:
        empty_list = board.get_empty_squares()
        pick_position = random.choice(empty_list)
        board.move(pick_position[0], pick_position[1], player)
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    """
    score the completed board and update the scores grid
    """
    if board.check_win() == provided.DRAW:
        scores = [ [0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    elif board.check_win() == player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
                elif board.square(row, col) == player:
                    scores[row][col] += MCMATCH                
                elif board.square(row, col) != player:
                    scores[row][col] += -MCOTHER                   
    elif board.check_win() != player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
                elif board.square(row, col) == player:
                    scores[row][col] += -MCMATCH
                elif board.square(row, col) != player:
                    scores[row][col] += MCOTHER
          
def get_best_move(board, scores):
    """
    find all of the empty squares with the maximum score and randomly return one of them
    """
    if board.get_empty_squares() == []:
        pass
    else:
        empty_list2 = board.get_empty_squares()
        alist = list()
        max_score_list = list()
        for position in empty_list2:
            alist.append(scores[position[0]][position[1]])
            max_num = max(alist)
        for position2 in empty_list2:
            if scores[position2[0]][position2[1]] == max_num:
                max_score_list.append(position2)
        return random.choice(max_score_list)
    
def mc_move(board, player, trials):
    """
    return a move for the machine player 
    """
    scores = [ [0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    for dummy_num in range(trials):
        class_copy = provided.TTTBoard(board.get_dim(), reverse = False, board = None)
        board_trial = class_copy.clone()
        mc_trial(board_trial, player)
        mc_update_scores(scores, board_trial, player)
    return get_best_move(board, scores)
       

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
