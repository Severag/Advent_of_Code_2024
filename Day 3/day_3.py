import itertools, re
import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        data = [line.strip() for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    combined = ''.join(data)
    mult_strs = re.findall(r'mul\(\d+,\d+\)', combined)
    
    total = 0
    for string in mult_strs:
        coeffs = [int(val) for val in re.findall(r'\d+', string)]
        total += coeffs[0] * coeffs[1]
    
    return total



def part2(data):
    combined = ''.join(data)
    mult_strs = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", combined)
    
    total = 0
    is_do = True
    for string in mult_strs:
        if "don't" in string:
            is_do = False
        elif 'do' in string:
            is_do = True
        elif is_do:
            try:
                coeffs = [int(val) for val in re.findall(r'\d+', string)]
            except TypeError as e:
                print(string)
                print('stop')
            coeffs = [int(val) for val in re.findall(r'\d+', string)]
            total += coeffs[0] * coeffs[1]
    
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



puzzles = [['test_case.txt',    [161, None]],
           ['test_case_2.txt',  [None, 48]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)