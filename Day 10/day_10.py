import itertools, re
import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        data = [[int(val) for val in line.strip()] for line in f]
    
    return np.array(data)



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    total = 0
    
    for r,c in zip(*np.where(data == 0)):
        total += explore_trailhead(data, (r, c))
    
    return total



def part2(data):
    total = 0
    
    for r,c in np.transpose(np.where(data == 0)):
        total += explore_trailhead(data, (r, c), False)
    
    return total



def explore_trailhead(board, start, is_part1=True):
    open_list = [start]
    closed_set = set()
    score = 0
    
    deltas = [[ 1, 0],
              [-1, 0],
              [ 0, 1],
              [ 0,-1]]
    
    while open_list:
        loc = open_list.pop()
        val = board[loc]
        
        if is_part1:
            # check we haven't been here
            if loc in closed_set:
                continue
            closed_set.add(loc)
        
        # increase score, if we're at a peak
        if val == 9:
            score += 1
        
        # explore neighbors
        for dr, dc in deltas:
            new_loc = (loc[0] + dr, loc[1] + dc)
            
            # check if in bounds
            if 0 <= new_loc[0] < len(board) and 0 <= new_loc[1] < len(board[0]):
                # always move to a spot exactly 1 higher than the current
                if board[new_loc] == val + 1:
                    open_list.append(new_loc)    
    
    return score



def get_rating(board, start):
    open_list = [start]
    rating = 0
    
    deltas = [[ 1, 0],
              [-1, 0],
              [ 0, 1],
              [ 0,-1]]
    
    while open_list:
        loc = open_list.pop()
        val = board[loc]
        
        # increase rating, if we're at a peak
        if val == 9:
            rating += 1
        
        # explore neighbors
        for dr, dc in deltas:
            new_loc = (loc[0] + dr, loc[1] + dc)
            
            # check if in bounds
            if 0 <= new_loc[0] < len(board) and 0 <= new_loc[1] < len(board[0]):
                # always move to a spot exactly 1 higher than the current
                if board[new_loc] == val + 1:
                    open_list.append(new_loc)    
    
    return rating



def check(myanswer, answer):
    if answer:  # compare each pre-known answer with its matching part's answer
        for my_ans, ans in zip(myanswer, answer):
            if ans is not None:
                if np.array_equal(my_ans, ans):
                    print(f"\tCheck passed!   \t{my_ans}")
                else:
                    print(f"\n\t{'ERROR':{'*'}^50}\n" + 
                          f"\tCorrect answer: \t{ans}\n"
                          f"\tReturned answer:\t{my_ans}")
    else:  # don't have a pre-known answer
        print(f"\t{myanswer}")



puzzles = [['test_case.txt',    [1, None]],
           ['test_case_2.txt',  [36, 81]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)