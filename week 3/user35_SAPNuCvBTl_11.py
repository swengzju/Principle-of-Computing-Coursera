"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """   
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    dice_sum = list()
    for dice_num in range(1, max(hand)+1):
        temp_sum = 0
        for dice_hand in hand:
            if dice_num == dice_hand:
                temp_sum += dice_hand
        dice_sum.append(temp_sum)
    return max(dice_sum)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = range(1, num_die_sides+1)
    possible_outcome = gen_all_sequences(outcomes, num_free_dice)
    expectvalue = 0.0
    num_outcome = len(possible_outcome)
    for one_outcome in possible_outcome:
        this_hand = held_dice + one_outcome
        expectvalue += float(score(this_hand)) / num_outcome
    return expectvalue


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    dice_hold = set([()])
    index = gen_all_sequences((0, 1), len(hand))
    for item in index:
        subset_hold = tuple()
        for dummy_item in range(len(item)):
            if list(item)[dummy_item] == 1:
                subset_hold += (list(hand)[dummy_item],)
        dice_hold.add(subset_hold)
    return dice_hold


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    tohold = tuple()
    best_expect = 0
    dice_inhand = gen_all_holds(hand)
    for choice in dice_inhand:
        expected = expected_value(choice, num_die_sides, len(hand)-len(choice))
        if expected >= best_expect:
            best_expect = expected
            tohold = choice
    return (best_expect, tohold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)