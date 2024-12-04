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
    count = 0
    # forwards
    count += find_xmas(data)
    
    # backwards
    back = [row[::-1] for row in data]
    count += find_xmas(back)
    
    # top-to-bottom
    transpose = [''.join([row[idx] for row in data]) for idx,_ in enumerate(data) ]
    count += find_xmas(transpose)
    
    # bottom-to-top
    back_trans = [row[::-1] for row in transpose]
    count += find_xmas(back_trans)
    
    # diagonal (top left to bottom right)
    diag1 = []
    for col1 in range(-1, -len(data) - 1, -1):
        temp = [data[r][c] for r, c in enumerate(range(col1, 0))]
        diag1.append(''.join(temp))
    for row1 in range(1, len(data)):
        temp = [data[r][c] for c, r in enumerate(range(row1, len(data)))]
        diag1.append(''.join(temp))
    count += find_xmas(diag1)
    
    # diagonal (previous, backwards)
    count += find_xmas([row[::-1] for row in diag1])
    
    # diagonal (bottom left to top right)
    diag2 = []
    for row1 in range(0, len(data)):
        temp = [data[r][c] for r,c in enumerate(range(row1, -1, -1))]
        diag2.append(''.join(temp))
    for col1 in range(1, len(data)):
        temp = [data[len(data) - r][c] for r,c in enumerate(range(col1, len(data)), start=1)]
        diag2.append(''.join(temp))
    count += find_xmas(diag2)
    
    # diagonal (previous, backwards)
    count += find_xmas([row[::-1] for row in diag2])
    
    return count



def part2(data):
    count = 0
    
    for r_idx, row in enumerate(data):
        for c_idx, ltr in enumerate(row):
            # check 'A's not in the border of the data
            if ltr == 'A' and 0 < r_idx < len(data) - 1 and 0 < c_idx < len(row) - 1:
                top_left = data[r_idx-1][c_idx-1]
                top_right = data[r_idx-1][c_idx+1]
                bot_left = data[r_idx+1][c_idx-1]
                bot_right = data[r_idx+1][c_idx+1]
                
                diag1 = (top_left == 'M' and bot_right == 'S') or (
                         top_left == 'S' and bot_right == 'M')
                diag2 = (top_right == 'M' and bot_left == 'S') or (
                         top_right == 'S' and bot_left == 'M')
                
                if diag1 and diag2:
                    count += 1
    
    return count



def find_xmas(str_list):
    count = 0
    for row in str_list:
        count += row.count('XMAS')
    
    return count



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



puzzles = [['test_case.txt',    [18, 9]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)