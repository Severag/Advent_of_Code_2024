import itertools, re
import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        board = []
        instructions = []
        
        in_section1 = True
        
        for line in f:
            if in_section1:
                if line == '\n':
                    in_section1 = False
                else:
                    board.append(line.strip())
            else:
                instructions.append(line.strip())
        
    return board, ''.join(instructions)



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    board = np.array([list(line) for line in data[0]])
    instructions = data[1]
    
    start = np.where(board == '@')    
    loc = tuple(np.transpose(start)[0])
    
    for instr in instructions:
        loc = do_move(board, loc, instr)
    
    boulder_locs = np.where(board == 'O')
    total = np.sum(100 * boulder_locs[0] + boulder_locs[1])
    
    return total


direc = {'^':[-1,  0],
         '>':[ 0,  1],
         'v':[ 1,  0],
         '<':[ 0, -1]}
def do_move(board, loc, instr, is_part2=False):
    dr, dc = direc[instr]
    
    new_loc = (loc[0], loc[1])
    
    while board[new_loc] != '.':  # while we haven't found an empty space
        new_loc = (new_loc[0] + dr, new_loc[1] + dc)
        
        if board[new_loc] == '#':  # found a wall before empty spot
            break
    else:  # we found an empty spot before we found a wall
        # move robot
        board[loc] = '.'
        loc = (loc[0] + dr, loc[1] + dc)
        board[loc] = '@'
        
        # move boulders into empty space    
        if is_part2:
            char = '[' if instr == '<' else ']'
            
            while new_loc != loc:
                board[new_loc] = char
                
                new_loc = (new_loc[0] - dr, new_loc[1] - dc)
                char = '[' if char == ']' else ']'
        else:
            if new_loc != loc:
                board[new_loc] = 'O'
    
    return loc



def part2(data):
    # convert to upscaled version
    converter = lambda x: x.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
    board = np.array([list(converter(line)) for line in data[0]])
    
    instructions = data[1]
    
    start = np.where(board == '@')    
    loc = tuple(np.transpose(start)[0])
    
    for idx,instr in enumerate(instructions):
        if instr == '>' or instr == '<':
            loc = do_move(board, loc, instr, True)
        else:
            loc = do_move2(board, loc, instr)
    
    boulder_locs = np.where(board == '[')
    total = np.sum(100 * boulder_locs[0] + boulder_locs[1])
    
    return total



def do_move2(board, loc, instr):
    dr, _ = direc[instr]
    
    new_loc = (loc[0] + dr, loc[1])
    
    # easy cases
    if board[new_loc] == '.':  # just move into empty space
        board[loc] = '.'
        board[new_loc] = '@'
        return new_loc
    elif board[new_loc] == '#':  # don't move at all
        return loc
    elif board[new_loc] == '[' :
        boulder = (new_loc, (new_loc[0], new_loc[1] + 1))
    elif board[new_loc] == ']':
        boulder = ((new_loc[0], new_loc[1] - 1), new_loc)
    else:
        raise ValueError('Not a valid character on board')
    
    # found a boulder (hard case)
    all_clear, left_spots, right_spots = check_move(board, boulder, dr)
    
    # we can move the boulders
    if all_clear:  # move it all
        moved_set = set()
        
        for boulder in zip(reversed(left_spots), reversed(right_spots)):
            for side, char in zip(boulder, '[]'):
                if side not in moved_set:
                    board[side] = '.'
                    board[side[0] + dr, side[1]] = char
                    moved_set.add(side)
        
        # move robot
        board[loc] = '.'
        board[new_loc] = '@'
        return new_loc
    else:
        return loc  # don't move



'''
    Can the boulder located at <locs> move in direction <dr>?
    Parameters
        <board> 
        <locs> a 2D tuple of (left location (r,c), right location(r,c))
    Returns 
        boolean: can move yes/no
        list: of all the "[" that will be moved
        list: of all the "]" that will be moved
'''
def check_move(board, locs, dr):
    all_clear = True
    left_spots = [locs[0]]
    right_spots = [locs[1]]
    
    # check [
    new_loc = (locs[0][0] + dr, locs[0][1])
    val = board[new_loc]
    if val == '.':  # empty spot
        pass  # don't do anything yet
    elif val == '[':  # another boulder aligned with this one
        next_locs = (new_loc, (new_loc[0], new_loc[1] + 1))
        output = check_move(board, next_locs, dr)
        all_clear &= output[0]
        left_spots += output[1]
        right_spots += output[2]
        return all_clear, left_spots, right_spots
    elif val == ']':  # another boulder offset with this one
        next_locs = ((new_loc[0], new_loc[1] - 1), new_loc)
        output = check_move(board, next_locs, dr)
        all_clear &= output[0]
        left_spots += output[1]
        right_spots += output[2]
    elif val == '#':  # a wall
        return False, [], []
    else:
        raise ValueError('Not a valid character on board')
    
    # check ]
    new_loc = (locs[1][0] + dr, locs[1][1])
    val = board[new_loc]
    if val == '.':
        return all_clear, left_spots, right_spots
    elif val == '[':  # another boulder offset with this one
        next_locs = (new_loc, (new_loc[0], new_loc[1] + 1))
        output = check_move(board, next_locs, dr)
        all_clear &= output[0]
        left_spots += output[1]
        right_spots += output[2]
        return all_clear, left_spots, right_spots
    elif val == '#':  # a wall
        return False, [], []
    else:
        raise ValueError('Not a valid character on board')



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



puzzles = [['test_case.txt',    [2028,  None]],
           ['test_case_2.txt',  [10092, 9021]],
           ['test_case_3.txt',  [None,   618]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)