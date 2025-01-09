import itertools
import numpy as np


def read_file(filename):
    locks = []
    keys = []
    with open( filename, 'r') as f:
        shape = []
        line = 'start'
        
        while line:
            line = next(f, '')  # default value is '', which trips the <while> condition
            
            if len(shape) == 0:  # new shape
                is_key = '#' not in line
                # first line is either empty (key) or ignored (lock)
                shape = [0 for char in line.strip()]
            elif len(line.strip()) < 1:  # end of shape
                if is_key:  # remove last solid row from key count
                    shape = [val - 1 for val in shape]
                    keys.append(shape)
                else:
                    locks.append(shape)
                shape = []
                is_key = False
            else:
                shape = [val + (1 if char == '#' else 0) for val, char in zip(shape, line.strip())]
    
    return locks, keys



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    all_locks, all_keys = data
    good_fits = 0
    
    for lock, key in itertools.product(all_locks, all_keys):
        for val1, val2 in zip(lock, key):
            if val1 + val2 > 5:
                break
        else:  # no breaks, ergo all fit
            good_fits += 1
    
    return good_fits



def part2(data):
    return



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



puzzles = [['test_case.txt',    [3, None]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)