import numpy as np
from collections import defaultdict
from functools import lru_cache


def read_file(filename):
    with open( filename, 'r') as f:
        data = [list(line.strip()) for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def setup_pads():
    num_text = '789, 456, 123, _0A'
    direc_text = '_^A, <v>'
    
    output = []
    for txt in [num_text, direc_text]:
        lines = txt.split(', ')
        array = np.array([list(l) for l in lines])
        
        loc_dict = {str(val):np.array(idx) for idx, val in np.ndenumerate(array)}
        
        output.append(loc_dict)
    
    return output



def get_instr(loc_dict, button_list):
    instructions = []
    forbidden = loc_dict['_']
    
    # start at 'A', move to <button>, press 'A*', move to next <button>, repeat
    # 'A' is 'A' for <loc_dict>
    # 'A*' is 'A' for the next board up
    loc = loc_dict['A']
    for button in button_list:
        dr, dc = loc_dict[button] - loc
        
        next_instr = get_next_i(loc, dr, dc, forbidden)
        
        instructions += list(next_instr + 'A')
        loc = loc_dict[button]
        
    return instructions



def get_next_i(loc, dr, dc, forbidden):
    next_instr = ''
    should_flip = False
    
    if dc < 0:  # col left       
        # if doing this move first would bring us over the forbidden spot, flip the move
        if len(next_instr) == 0 and loc[0] == forbidden[0] and loc[1] + dc == forbidden[1]:
            should_flip = True
        next_instr += '<' * -dc
        
    if dr > 0:  # row down
        if len(next_instr) == 0 and loc[1] == forbidden[1] and loc[0] + dr == forbidden[0]:
            should_flip = True
        next_instr += 'v' * dr
    
    if dr < 0:  # row up        
        if len(next_instr) == 0 and loc[1] == forbidden[1] and loc[0] + dr == forbidden[0]:
            should_flip = True
        next_instr += '^' * -dr
        
    if dc > 0:  # col right        
        if len(next_instr) == 0 and loc[0] == forbidden[0] and loc[1] + dc == forbidden[1]:
            should_flip = True
        next_instr += '>' * dc
    
    if should_flip:
        next_instr = next_instr[::-1]
    
    return next_instr



def get_instr_dict(loc_dict, button_dict):
    instructions = defaultdict(int)
    
    for buttons, count in button_dict.items():
        results = get_instr_dict_helper(buttons)
        
        for seq, sub_count in results.items():
            instructions[seq] += count * sub_count
        
    return instructions



@lru_cache()
def get_instr_dict_helper(button_list):
    loc_dict = direc_pad
    instructions = defaultdict(int)
    forbidden = loc_dict['_']
    
    # start at 'A', move to <button>, press 'A*', move to next <button>, repeat
    # 'A' is 'A' for <loc_dict>
    # 'A*' is 'A' for the next board up
    loc = loc_dict['A']
    for button in button_list:
        dr, dc = loc_dict[button] - loc
        
        next_instr = get_next_i(loc, dr, dc, forbidden)
        
        instructions[next_instr + 'A'] += 1
        loc = loc_dict[button]
        
    return instructions



def part1(data):
    complexities = []
    key_pads = [num_pad, direc_pad, direc_pad]
    
    for code in data:
        number = int(''.join(code[:-1]))
        
        for idx,pad in enumerate(key_pads):
            code = get_instr(pad, code)
        
        complexities.append(number * len(code))
    
    return sum(complexities)



def part2(data):
    complexities = []
    
    for code in data:
        number = int(''.join(code[:-1]))
        
        # do the numerical keypad and setup for extended rounds of directional keypads
        direc_code = get_instr(num_pad, code)
        code_dict = {''.join(direc_code):1}
        
        # run directional keypads with dictionary instead of list
        for idx in range(25):
            code_dict = get_instr_dict(direc_pad, code_dict)
        
        # calculate final length
        length = 0
        for seq, count in code_dict.items():
            length += len(seq) * count
        
        # find complexity
        complexities.append(number * length)
        
    return sum(complexities)



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


num_pad, direc_pad = setup_pads()

puzzles = [['test_case.txt',    [126384, None]],
           ['test_case_2.txt',  [81898, None]],
           ['puzzle_input.txt', []]]  

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)