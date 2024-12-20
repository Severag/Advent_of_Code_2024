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



def part1(data, cheat_dist=2):
    dist, path = dijkstra(data)
    
    path_arr = np.array(path)
    dists_3D = np.abs(path_arr - path_arr[:, np.newaxis, :])
    dists = np.sum(dists_3D, axis=2)  # manhattan distance
    
    path_idx = np.arange(0, len(path_arr))
    path_dists  = np.abs(path_idx - path_idx[:, np.newaxis])
    
    if data.size < 300:  # test case
        shortcuts = (dists <= cheat_dist) & (path_dists > cheat_dist)
        
        cheats = dict()
        for p1, p2 in zip(*np.where(shortcuts)):
            loc = (p1, p2) if p1 < p2 else (p2, p1)
            time_saved = path_dists[loc] - dists[loc]
            cheats[loc] = time_saved
        
        top_cheats = sorted(list(cheats.values()), reverse=True)
        
        return top_cheats[:5]
    else:
        time_saved = path_dists - dists
        shortcuts = (dists <= cheat_dist) & (time_saved >= 100)
        return np.count_nonzero(shortcuts) // 2



deltas = [[-1, 0],
          [ 0, 1],
          [ 1, 0],
          [ 0,-1]]
def dijkstra(board):
    start = tuple(np.squeeze(np.where(board == 'S')))
    end = tuple(np.squeeze(np.where(board == 'E')))
    
    open_list = [(0, start, [start])]
    closed_set = set()
    
    while open_list:
        dist, loc, path = heapq.heappop(open_list)
        
        # end condition
        if loc == end:
            return dist, path
        
        # check for repeat
        if loc in closed_set:
            raise ValueError
        closed_set.add(loc)
        
        # advance
        for dr, dc in deltas:
            cand = (loc[0] + dr, loc[1] + dc)
            
            if cand not in closed_set and board[cand] != '#':
                new_state = (dist + 1, cand, path + [cand,])
                heapq.heappush(open_list, new_state)
    
    return -1



def part2(data):
    return part1(data, 20)



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



puzzles = [['test_case.txt',    [[64, 40, 38, 36, 20], [76, 76, 76, 74, 74]]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)