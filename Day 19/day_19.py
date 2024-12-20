import functools, re
import numpy as np
from collections import defaultdict


def read_file(filename):
    with open( filename, 'r') as f:
        towels = next(f).strip().split(', ')
        designs = [line.strip() for line in f if line != '\n']
    
    return sorted(towels, key=len, reverse=True), designs



def solve(data, do_1=True, do_2=True):
    p1, keeps = part1(data) if do_1 else [None, None]
    p2 = part2(data, keeps) if do_2 else None
    
    return p1, p2



def part1(data):
    towels, designs = data
    regex = rf"(^(?:{'|'.join(towels)})+$)"
    
    keeps = []
    for stripes in designs:
        if re.match(regex, stripes) is not None:
            keeps.append(stripes)
    
    return len(keeps), keeps



def part2(data, keeps):
    towels, designs = data
    
    total = 0
    for stripes in keeps:
        matches = [1] + [0] * len(stripes)
        
        for idx in range(len(stripes)):
            for towel in towels:
                # if <stripes>[idx] starts with <towel>
                # i.e. if this towel can cover the colors we need here
                if stripes.startswith(towel, idx):
                    # then the towel coming after it will have as many 
                    # possible combinations as this spot does
                    width = len(towel)
                    matches[idx + width] += matches[idx]
        
        total += matches[-1]
    
    return total



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



puzzles = [['test_case.txt',    [6, 16]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)