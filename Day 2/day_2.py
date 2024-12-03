import itertools, re
import numpy as np


def read_file(filename):
    def parse(line):
        num_txts = re.findall('\d+', line)
        return np.array([int(txt) for txt in num_txts])
    
    with open( filename, 'r') as f:
        data = [parse(line) for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    safe_count = 0
    
    for row in data:
        if check_levels(row):
            safe_count += 1
    
    return safe_count



def part2(data):
    safe_count = 0
    
    for row in data:
        if check_levels(row):
            safe_count += 1
        else:
            # try again by removing each level individually
            indices = np.array(list(range(row.size)))
            for idx,val in enumerate(row):
                if check_levels(row[indices != idx]):
                    safe_count += 1
                    break
    
    return safe_count



def check_levels(row):
    diffs = row[1:] - row[:-1]
    
    # Condition 1: all increasing or all decreasing
    if np.all(diffs > 0) or np.all(diffs < 0):
        # Condition 2: change is b/n 1 and 3, inclusive
        # previous line check > 0, so just check <= 3
        if np.all(np.abs(diffs) <= 3):
            return True
    
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



puzzles = [['test_case.txt',    [2, 4]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)