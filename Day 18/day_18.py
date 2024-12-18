import heapq
import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        # reverse x,y to make them row, col
        data = [tuple(int(val) for val in line.strip().split(',')[::-1]) for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



deltas = [[-1, 0],
          [ 0, 1],
          [ 1, 0],
          [ 0,-1]]
def part1(data, time=None):
    if len(data) < 30:  # test case
        board = np.zeros([7, 7])
        init = data[:12]
    else:
        board = np.zeros([71, 71])
        init = data[:1024]
    
    if time is not None:  # for Part 2
        init = data[:time]
    
    for coord in init:
        board[coord] = -1
    end = tuple(val - 1 for val in board.shape)
    
    open_list = [(0, (0, 0))]
    closed_set = set()
    
    while open_list:
        dist, loc = heapq.heappop(open_list)
        
        if loc in closed_set:
            continue
        
        if loc == end:
            return dist
        
        closed_set.add(loc)
        
        for dr, dc in deltas:
            cand = (loc[0] + dr, loc[1] + dc)
            
            in_bounds = (0 <= cand[0] < len(board)) and (0 <= cand[1] < len(board[1]))
            if in_bounds and board[cand] == 0 and cand not in closed_set:  # open, unvisited spot
                heapq.heappush(open_list, (dist + 1, cand))
    
    return -1



def part2(data):
    start = 1 + (12 if len(data) < 30 else 1024)
    
    for idx in range(start, len(data)):
        if part1(data, idx) == -1:  # "no path found" result
            idx -= 1  # <part1> places all the glitches [0, idx), so the most 
            # recently placed glitch that blocked our path is at <idx - 1>
            return f"{data[idx][1]},{data[idx][0]}"
    
    return "None"



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



puzzles = [['test_case.txt',    [22, '6,1']],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)