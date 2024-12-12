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



def part1(data, is_part2=False):
    visited_locs = set()
    total = 0
    
    for idx, val in np.ndenumerate(data):
        if idx not in visited_locs:
            price_delta, new_locs = explore_region(data, idx, is_part2)
            
            total += price_delta
            visited_locs |= new_locs
    
    return total



def part2(data):
    return part1(data, True)



    
deltas = [[-1, 0],
          [ 0, 1],
          [ 1, 0],
          [ 0,-1]]
def explore_region(board, start, is_part2=False):
    open_list = [start]
    closed_set = set()
    
    area = 0
    perimeter = 0
    border_set = set()
    
    while open_list:
        loc = open_list.pop()
        val = board[loc]
        
        # check we haven't been here
        if loc in closed_set:
            continue
        closed_set.add(loc)
        area += 1
        
        # explore neighbors
        for direc, delt in enumerate(deltas):
            new_loc = advance_point(loc, delt)
            
            # check if <new_loc> is also in region
            in_bounds = 0 <= new_loc[0] < len(board) and 0 <= new_loc[1] < len(board[0])
            
            if in_bounds and board[new_loc] == val:
                open_list.append(new_loc) 
            else:
                # <loc> is on the border and this node is on the other side
                # of the perimeter
                perimeter += 1
                border_set.add( loc + (direc,) )
    
    if is_part2:
        perimeter = find_sides(border_set)
    
    return area * perimeter, closed_set



def find_sides(border_set):
    sides = 0
    while len(border_set) > 0:
        loc = border_set.pop()
        
        # search both directions from <loc> to find all the points, direction pairs 
        # associated with this side and remove them from <border_set>
        border_set = move_along_edge(border_set, loc, True)
        border_set = move_along_edge(border_set, loc, False)
        sides += 1
    
    return sides



def advance_point(loc, delta):
    r, c = loc
    dr, dc = delta
    
    return (r + dr, c + dc)



def move_along_edge(points, loc, is_reversed=False):
    # direc 90 clockwise from current (or counterclockwise if <is_reversed>)
    direc = (loc[2] + (1 if not is_reversed else -1)) % len(deltas)
    
    while True:
        # adjacent point in <direc> direction facing the same was <loc>
        new_loc = advance_point(loc[:2], deltas[direc]) + (loc[2],)
        
        if new_loc in points:
            loc = new_loc
            points.remove(loc)
        else:
            return points  # return <points> minus the locations we've visited



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



puzzles = [['test_case.txt',    [140, 80]],
           ['test_case_2.txt',  [772, 436]],
           ['test_case_3.txt',  [1930, 1206]],
           ['test_case_4.txt',  [None, 236]],
           ['test_case_5.txt',  [None, 368]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)