import itertools, re
import numpy as np


def read_file(filename):
    def parse(line):
        strings = re.findall(r"(-?\d+)", line)
        
        # swap x's and y's so that pos(0, 1) is in (row, col) order
        return [[int(val) for val in subset[::-1]] for subset in [strings[:2], strings[2:]]]
    
    with open( filename, 'r') as f:
        data = [parse(line) for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    states = np.array(data)

    shape = np.array([7, 11] if len(data) < 15 else [103, 101])

    quadrants = np.zeros([2, 2])
    halves = shape // 2
    
    for second in range(100):
        for pos, vel in states:
            pos += vel
            pos %= shape
                        
            if second == 99:  # last iteration
                if not np.any(pos == halves):  # nothing on the quadrant boundary
                    quad_idx = (0 if pos[0] < halves[0] else 1,
                                0 if pos[1] < halves[1] else 1)
                    quadrants[quad_idx] += 1
    
    return np.product(quadrants)



def part2(data):
    states = np.array(data)

    shape = np.array([7, 11] if len(data) < 15 else [103, 101])
    board = np.zeros(shape)
    best = [-1, np.inf]
    
    with open('matrix_log.txt', 'w') as f:
        for second in range(1, 10001):
            states[:, 0] += states[:, 1]  # pos += vel
            states[:, 0] %= shape         # pos %= shape
            
            positions = states[:, 0]
            distance_comp = positions[:, np.newaxis] - positions  # N x N x 2 array
            distances = np.sum(np.abs(distance_comp), axis=2)  # N x N array (manhattan distance)
            
            total = distances.sum()
            if total < best[1]:
                best = [second, total]
                f.write(f"{second: >10d} \t {total: >10,d}\n")
                
                indices = (states[:, 0, 0], states[:, 0, 1])
                board[indices] = 1
                np.savetxt(f, board, '%1.f', '', footer='\n\n')
                board[indices] = 0
    
    return best[0]



def cleanup():
    with open('matrix_log_2.txt', 'w') as out:
        with open('matrix_log.txt', 'r') as f:
            for line in f:
                out.write(line.replace('0', ' '))



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



puzzles = [['test_case.txt',    [12, None]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)