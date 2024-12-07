import math, re
import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        data = [[int(val) for val in re.findall(r'\d+', line)] for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    valid_totals = []
    
    for eqn in data:
        goal = eqn[0]
        all_subtotals = [eqn[1]]
        
        for val in eqn[2:]:
            all_subtotals = [result for subtotal in all_subtotals for result in 
                             [val + subtotal, val * subtotal] if result <= goal]
            
            # ran out of valid pathways to reach <goal>
            if len(all_subtotals) < 1:
                break
        
        # we found a way to combine all the numbers to equal <goal>
        if goal in all_subtotals:
            valid_totals.append(goal)
        
    return sum(valid_totals)



def part2(data):
    valid_totals = []
    funcs = [lambda x,y: x + y,  # addition
             lambda x,y: x * y,  # multiplication
             # lambda x,y: x * 10**math.ceil(math.log(y, 10) + 1e-15) + y,  # contatenation
             lambda x,y: int(str(x) + str(y))  # contatenation
            ]
    
    for i,eqn in enumerate(data):
        goal = eqn[0]
        all_subtotals = [eqn[1]]
        
        for val in eqn[2:]:
            all_subtotals = [op(subtotal, val) for subtotal in all_subtotals for 
                             op in funcs if subtotal <= goal]
            
            # ran out of valid pathways to reach <goal>
            if len(all_subtotals) < 1:
                break
        
        # we found a way to combine all the numbers to equal <goal>
        if goal in all_subtotals:
            valid_totals.append(goal)
    
    return sum(valid_totals)



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



puzzles = [['test_case.txt',    [3749, 11387]],
           ['puzzle_input.txt', []]]
                                    

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)