import itertools, re
import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        machines = []
        info = []
        for line in f:
            if len(line) < 3:
                machines.append(info)
                info = []
            else:
                nums = [int(val) for val in re.findall(r'\d+', line.strip())]
                info.append(nums)
    
    machines.append(info)
    
    return machines



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data, offset=0):
    tokens = 0
    cost = np.array([[3, 1]])
    
    for button_A, button_B, prize in data:
        A = np.array([button_A, button_B]).T
        b = np.array([prize]).T + offset
        
        # solve system of equations
        soln = np.linalg.inv(A) @ b  # <@> is matrix multiplication
        
        # button presses are even integers
        if np.all(A @ np.round(soln, 0) == b):
            # calculate number of tokens needed
            [[price]] = cost @ soln
            tokens += price
        
    return tokens



def part2(data):
    return part1(data, 10_000_000_000_000)



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



puzzles = [['test_case.txt',    [480, None]],
           ['puzzle_input.txt', []]]  # 11115 is too low

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)