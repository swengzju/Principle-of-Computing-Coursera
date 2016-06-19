"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result = []
    list1_index = 0
    while list1_index < len(list1):
        result.append(list1[list1_index])
        while list1_index + 1 <len(list1) and list1[list1_index + 1] == list1[list1_index]:
            list1_index += 1
        list1_index += 1
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    for item in list1:
        if item in list2:
            result.append(item)
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """ 
    result = []
    index1 = 0
    index2 = 0
    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] < list2[index2]:
            result.append(list1[index1])
            index1 += 1
        elif list1[index1] > list2[index2]:
            result.append(list2[index2])
            index2 += 1
        else:
            result.append(list1[index1])
            result.append(list1[index1])
            index1 += 1
            index2 += 1
    if index1 < len(list1):
        result += list1[index1 :]
    if index2 < len(list2):
        result += list2[index2 :]
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) == 0:
        return []
    elif len(list1) == 1:
        return list1
    elif len(list1) >1:
        mid = len(list1)//2
        half1 = list1[ :mid]
        half2 = list1[mid: ]
        sort1 = merge_sort(half1)
        sort2 = merge_sort(half2)       
        return merge(sort1, sort2)


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    result = []
    if len(word) == 1:
        result = ["", word]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        for string in rest_strings:
            result.append(string)
            length = len(string) + 1
            for index in range(length):
                if index == 0:
                    newword = first + string
                    result.append(newword)
                elif index < len(string):
                    part1 = string[:index]
                    part2 = string[index:]
                    newword = part1 + first + part2
                    result.append(newword)
                else:
                    newword = string + first
                    result.append(newword)
    return result

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    result = []
    url = codeskulptor.file2url(WORDFILE)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        result.append(line)
    return result

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
