import itertools, re
import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        data = [list(line.strip()) for line in f]
    
    return np.array(data)



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    board = np.zeros_like(data, dtype=int)
    antennas = [val for val in np.unique(data) if val != '.']
    ant_locs = [np.array(np.where(data == val)).T for val in antennas]
    
    # calculate antinodes
    for freq in ant_locs:
        for p1, p2 in itertools.combinations(freq, 2):
            diff = p1 - p2
            
            for node in [diff + p1, p2 - diff]:
                if in_bounds(node, board):
                    board[tuple(node)] = 1
    
    return board.sum()



def part2(data):
    board = np.zeros_like(data, dtype=int)
    antennas = [val for val in np.unique(data) if val != '.']
    ant_locs = [np.array(np.where(data == val)).T for val in antennas]
    
    # calculate antinodes
    for freq in ant_locs:
        for p1, p2 in itertools.combinations(freq, 2):
            diff = p1 - p2
            
            # p1 backwards
            node = p1.copy()
            while in_bounds(node, board):
                board[tuple(node)] = 1
                
                node += diff
            
            # p2 forwards
            node = p2.copy()
            while in_bounds(node, board):
                board[tuple(node)] = 1
                
                node -= diff
    
    return board.sum()



def in_bounds(loc, array):
    return 0 <= loc[0] < len(array) and 0 <= loc[1] < len(array[0])



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



puzzles = [['test_case.txt',    [14, 34]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)