"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.get_empty_squares() == provided.EMPTY or board.check_win() != None:
        return (SCORES[board.check_win()], (-1, -1))
    else:       
        empty_square = board.get_empty_squares()
        score = []
        move = []
        for square in empty_square:
            newboard = board.clone()
            newboard.move(square[0], square[1], player)
            if player == provided.PLAYERX:
                if newboard.check_win() == provided.PLAYERX:
                    return (SCORES[newboard.check_win()], (square[0],square[1]))
                else:
                    result = mm_move(newboard, provided.switch_player(player))
                    score.append(result[0])
                    move.append((square[0], square[1]))
            elif player == provided.PLAYERO:
                if newboard.check_win() == provided.PLAYERO:
                    return (SCORES[newboard.check_win()], (square[0],square[1]))
                else:
                    result = mm_move(newboard, provided.switch_player(player))
                    score.append(result[0])
                    move.append((square[0], square[1]))
        if player == provided.PLAYERX:
            final_score = max(score)
            final_move = move[score.index(final_score)]
        elif player == provided.PLAYERO:
            final_score = min(score)
            final_move = move[score.index(final_score)]
        return (final_score, final_move)
           

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
## testing to save time.
#import user36_AQLww3W1YBS5oCt as unit_test
#unit_test.test_mm_move(mm_move)
import user37_DPspPq7UVT_2 as testsuite
testsuite.run_tests(mm_move)
##
#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
