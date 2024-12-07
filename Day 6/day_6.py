import itertools, re
import numpy as np


def read_file(filename):
    def parse(line):
        nums = line.strip().replace('.', '0,').replace('#', '1,').replace('^', '-1,')
        return [int(val) for val in nums.strip(',').split(',')]
    
    with open( filename, 'r') as f:
        data = [parse(line) for line in f]
    
    return np.array(data)



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    start = np.where(data == -1)
    loc = np.squeeze(start)
    board = np.copy(data)
    
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # directions
    facing = 0
    have_ended = False
    
    while not have_ended:
        # move to next roadblock
        new_loc = np.array(loc)
        
        while board[new_loc[0], new_loc[1]] < 1:
            board[new_loc[0], new_loc[1]] = -1  # mark where we've been
            new_loc += dirs[facing]
            
            # if we're going out of bounds
            if np.any([new_loc >= board.shape, new_loc < 0]):
                have_ended = True
                break
        
        # take one step back to not be directly on top of the block
        new_loc = tuple(new_loc - dirs[facing])
        
        loc = new_loc
        facing = (facing + 1) % len(dirs)  # turn 90 degrees right
    
    return np.count_nonzero(board == -1)



def part2(data):
    start = np.where(data == -1)
    loc = np.squeeze(start)
    board = np.copy(data)
    paths = np.zeros(board.shape + (4,), dtype=int)
    
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # directions
    facing = 0
    have_ended = False
    potentials = []
    
    while not have_ended:
        # move to next roadblock
        new_loc = np.array(loc)
        next_facing = (facing + 1) % len(dirs)  # turn 90 degrees right
        
        while board[new_loc[0], new_loc[1]] < 1:
            board[new_loc[0], new_loc[1]] = -1  # mark where we've been
            paths[new_loc[0], new_loc[1], facing] = 1
            
            # advance
            new_loc += dirs[facing]
            
            # if we're going out of bounds
            if np.any([new_loc >= board.shape, new_loc < 0]):
                have_ended = True
                break
            
            # if we haven't been this way before, check if placing a block here
            # would create a cycle
            if board[new_loc[0], new_loc[1]] != -1:
                temp_board = board.copy()
                temp_paths = paths.copy()
                
                # create new block
                temp_board[new_loc[0], new_loc[1]] = 1  # add block here
                
                # reset to just before hitting it
                temp_loc = tuple(new_loc - dirs[facing])
                
                if circles_back(temp_loc, temp_board, temp_paths, facing):
                    potentials.append(temp_loc)
        
        # take one step back to not be directly on top of the block
        new_loc = tuple(new_loc - dirs[facing])
        
        loc = new_loc
        facing = next_facing
    
    return len(potentials)



def circles_back(loc, board, paths, facing):    
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # directions
    have_ended = False
    
    while not have_ended:
        # move to next roadblock
        new_loc = np.array(loc)
        next_facing = (facing + 1) % len(dirs)  # turn 90 degrees right
        
        while board[new_loc[0], new_loc[1]] < 1:
            board[new_loc[0], new_loc[1]] = -1  # mark where we've been
            paths[new_loc[0], new_loc[1], facing] = 1
            
            # advance
            new_loc += dirs[facing]
            
            # if we're going out of bounds
            if np.any([new_loc >= board.shape, new_loc < 0]):
                have_ended = True
                break
            
            # if we've been this way before
            if board[new_loc[0], new_loc[1]] == -1 and paths[new_loc[0], new_loc[1], facing] == 1:
                return True
        
        # take one step back to not be directly on top of the block
        new_loc = tuple(new_loc - dirs[facing])
        
        loc = new_loc
        facing = next_facing
    
    return False
    


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



puzzles = [['test_case.txt',    [41, 6]],
           ['test_case_2.txt',  [None, 1]],
           ['test_case_3.txt',  [None, 3]],
           ['puzzle_input.txt', []]]  

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)