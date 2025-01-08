import numpy as np
from collections import defaultdict


def read_file(filename):
    with open( filename, 'r') as f:
        data = [int(line.strip()) for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1, results = part1(data) if do_1 else None
    p2 = part2(data, results) if do_2 else None
    
    return p1, p2



def mix(secret, value):
    return np.bitwise_xor(secret, value)



def prune(secret):
    return secret % 16777216



def evolve(secret):
    '''Step 1'''
    temp = secret * 64
    secret = mix(secret, temp)
    secret = prune(secret)
    
    '''Step 2'''
    temp = secret // 32
    secret = mix(secret, temp)
    secret = prune(secret)
    
    '''Step 3'''
    temp = secret * 2048
    secret = mix(secret, temp)
    secret = prune(secret)
    
    return secret



def part1(data):
    results = np.zeros([2_001, len(data)], dtype=np.int64)
    results[0] = data
    
    for idx in range(1, len(results)):
        results[idx] = evolve(results[idx - 1])
    
    return np.sum(results[-1]), results



def part2(data, results):
    prices = results % 10
    diffs = np.zeros_like(prices)
    diffs[1:] = prices[1:] - prices[:-1]
    
    market_total = defaultdict(int)
    
    for m_idx, diff_seq in enumerate(diffs.T):
        closed_set = set()  # only record the first occurence of <window>
        # for each monkey
        
        for w_idx, window in enumerate(zip(diff_seq[1:], diff_seq[2:], 
                                           diff_seq[3:], diff_seq[4:])):
            if window not in closed_set:
                closed_set.add(window)
                num_idx = w_idx + 4  # index of the last element in <window>
                market_total[window] += prices[num_idx, m_idx]
    
    return max(market_total.values())



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



puzzles = [['test_case.txt',    [37327623, None]],
           ['test_case_3.txt',  [1110806, 9]],
           ['test_case_2.txt',  [37990510, 23]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)