import numpy as np
from collections import defaultdict
from functools import lru_cache


def read_file(filename):
    with open( filename, 'r') as f:
        data = [line.strip().split(' ') for line in f]
    
    return data[0]



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    line = [int(val) for val in data]
    
    for blink in range(25):
        idx = 0
        while idx < len(line):
            val = line[idx]
            
            if val == 0:
                line[idx] = 1
            else:
                val_str = str(val)
                digits = len(val_str)
                
                if digits % 2 == 0:
                    val1 = int(val_str[:digits // 2])
                    val2 = int(val_str[digits // 2:])
                    
                    line[idx] = val1
                    line.insert(idx + 1, val2)
                    
                    idx += 1  # skip inserted value
                else:
                    line[idx] *= 2024
            
            idx += 1
    
    return len(line)



def part2(data, cycles=75):
    
    num_dict = defaultdict(int)
    
    for val in data:
        num_dict[val] += 1
    
    for blink in range(cycles):
        next_dict = defaultdict(int)
        
        for key,val in num_dict.items():
            for new_key in get_evolution(key):
                next_dict[new_key] += val
        
        num_dict = next_dict
    
    total = 0
    for key,val in num_dict.items():
        total += val
    
    return total



@lru_cache
def get_evolution(val_str):
    if val_str == '0':
        return ['1',]
    if len(val_str) % 2 == 0:
        half_digits = len(val_str) // 2
        return [str(int(val)) for val in [val_str[:half_digits], val_str[half_digits:]]]
    else:
        return [str(int(val_str) * 2024),]



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



puzzles = [['test_case.txt',    [55312, None]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)