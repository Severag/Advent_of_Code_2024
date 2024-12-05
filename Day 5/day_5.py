import numpy as np
from collections import defaultdict


def read_file(filename):
    with open( filename, 'r') as f:
        orders = defaultdict(set)
        pages = []
        is_section_1 = True
        
        for line in f:
            if line == '\n':
                is_section_1 = False
            elif is_section_1:
                pair = [int(val) for val in line.strip().split('|')]
                orders[pair[0]].add(pair[1])
            else:
                pages.append([int(val) for val in line.strip().split(',')])
        
    return orders, pages



def solve(data, do_1=True, do_2=True):
    p1, invalids = part1(data) if do_1 else (None, None)
    p2 = part2(data, invalids) if do_2 else None
    
    return p1, p2



def part1(data):
    orders, pages = data
    invalids = []
    mids = []
    
    for row in pages:
        for idx, val in enumerate(row[1:], start=1):
            # does the list prior to <idx> share any values with the numbers
            # that must go after <val>
            incorrect_order = bool(set(row[:idx]) & orders[val])
                        
            if incorrect_order:
                invalids.append(row)
                break
        else:  # the <no break> condition
            mids.append(row[len(row)//2])
    
    return sum(mids), invalids



def part2(data, invalids):
    orders, pages = data
    total = 0
    
    for row in invalids:
        # iterate through the list backwards, that way once we move a number backwards,
        # we check that the numbers now behind it are in the proper order
        idx = len(row) - 1
        while idx > 0:
            val = row[idx]
            post_order = orders[val]
            for pos, subval in enumerate(row[:idx]):
                # found a number <val> needs to be before
                if subval in post_order:
                    row.pop(idx)
                    row.insert(pos, val)
                    break
            else:  # if we didn't move <val>, advance up the list
                idx -= 1
        
        total += row[len(row) // 2]
    
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



puzzles = [['test_case.txt',    [143, 123]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)