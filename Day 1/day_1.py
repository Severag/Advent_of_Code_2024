import itertools, re
import numpy as np


def read_file(filename):
    def parse(line):
        text_list = re.findall('(\d+)', line)
        return [int(val) for val in text_list]
    
    with open( filename, 'r') as f:
        data = [parse(line) for line in f]
    
    return np.array(data)



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    left = np.sort(data[:, 0])
    right = np.sort(data[:, 1])
    
    return np.sum(np.abs(left - right))



def part2(data):
    left = np.sort(data[:, 0])
    left_uniqs, left_counts = np.unique(left, return_counts=True)
    
    right = np.sort(data[:, 1])
    right_uniqs, right_counts = np.unique(right, return_counts=True)
    right_dict = {val:count for val, count in zip(right_uniqs, right_counts)}
    
    score = 0
    
    for val, count in zip(left_uniqs, left_counts):
        score += val * count * right_dict.get(val, 0)
    
    return score



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



puzzles = [['test_case.txt',    [11, 31]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)