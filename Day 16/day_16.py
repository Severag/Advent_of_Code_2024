import heapq
import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        data = [list(line.strip()) for line in f]
    
    return np.array(data)



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2


deltas = [[-1, 0],
          [ 0, 1],
          [ 1, 0],
          [ 0,-1]]
def part1(data, is_part2=False):
    start = tuple(np.squeeze(np.where(data == 'S')))
    end = tuple(np.squeeze(np.where(data == 'E')))
    
    open_list = [(0, start, 1, [start])]  # (points, location, direction [NESW=0123], path)
    closed_set = set()
    
    best_paths = set()
    best_score = np.inf
    
    while open_list:
        score, loc, direc, path = heapq.heappop(open_list)
        
        if score > best_score:  # out of contention for best score
            continue
        elif loc == end:  # end condition
            if is_part2:
                best_score = score
                best_paths |= set(path)
            else:
                return score
        closed_set.add((loc, direc))
        
        # find neighbors
        rev_direc = (direc + 2) % len(deltas)
        for idx, [dr, dc] in enumerate(deltas):
            cand = (loc[0] + dr, loc[1] + dc)
            
            # not returning to <loc> and not a wall and new location
            if idx != rev_direc and data[cand] != '#' and (cand, idx) not in closed_set:
                cost = 1 if idx == direc else 1001  # moving or moving + turning cost
                
                heapq.heappush(open_list, (score + cost, cand, idx, path + [cand]))
    
    return len(best_paths)



def part2(data):
    return part1(data, True)



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



puzzles = [['test_case.txt',    [7036, 45]],
           ['test_case_2.txt',  [11048, 64]],
           ['puzzle_input.txt', []]]  # 72432 is too low

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)