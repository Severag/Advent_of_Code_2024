import itertools, re
import numpy as np


def read_file(filename):
    register = []
    
    with open( filename, 'r') as f:
       for line in f:
           if line.startswith('Register'):
               val = int(line.split(': ')[-1].strip())
               register.append(val)
           elif line.startswith('Program'):
               program = [int(val) for val in re.findall('\d+', line)]
    
    register = [0, 1, 2, 3] + register
    
    return register, program



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    memory = data[0].copy()
    program = data[1]
    
    idx = 0
    output = []
    
    while idx < len(program):
        memory, output, idx = run_IntCode(memory, program, output, idx)
    
    return ','.join([str(val) for val in output])



reg_A, reg_B, reg_C = 4, 5, 6
def run_IntCode(memory, program, output, idx):
    opcode = program[idx]
    operand = program[idx + 1]
    
    if opcode   == 0:
        memory[reg_A] //= 2**memory[operand]
    elif opcode == 1:
        memory[reg_B] ^= operand
    elif opcode == 2: 
        memory[reg_B] = memory[operand] % 8
    elif opcode == 3:
        if memory[reg_A] != 0:
            idx = operand - 2  # end of loop jump will take it the rest of the way
    elif opcode == 4:
        memory[reg_B] ^= memory[reg_C]
    elif opcode == 5:
        output.append(memory[operand] % 8)
    elif opcode == 6:
        memory[reg_B] = memory[reg_A] // 2**memory[operand]
    elif opcode == 7:
        memory[reg_C] = memory[reg_A] // 2**memory[operand]
    
    idx += 2
    
    return memory, output, idx



def other_tests():
    memory = list(range(7))
    
    # test 1
    memory[reg_C] = 9
    memory, _, _ = run_IntCode(memory, [2, 6], [], 0)
    assert memory[reg_B] == 1
    
    # test 2
    memory[reg_A] = 10
    assert part1([memory, [5,0,5,1,5,4]]) == '0,1,2'
    
    # test 3
    memory[reg_A] = 2024
    assert part1([memory, [0,1,5,4,3,0]]) == '4,2,5,6,7,7,7,7,3,1,0'
    # and reg_A == 0
    
    # test 4
    memory[reg_B] = 29
    memory, _, _ = run_IntCode(memory, [1, 7], [], 0)
    assert memory[reg_B] == 26
    
    # test 5
    memory[reg_B] = 2024
    memory[reg_C] = 43690
    memory, _, _ = run_IntCode(memory, [4, 0], [], 0)
    assert memory[reg_B] == 44354
other_tests()



def part2(data):
    memory = data[0].copy()
    program = data[1]
    
    target = ','.join([str(val) for val in program])
    
    end_idx = -3
    with open('log.txt', 'w') as f:
        val = 0
        while -end_idx <= len(target):
            memory[reg_A] = val
            
            output = part1([memory, program])
            if output.startswith(target[end_idx:]):
                f.write(f"{val: >20,d} \t {output: >31s}\n")
                f.write(f"{' ':>20s} \t {target}\n\n\n")
                
                end_idx -= 2
                val *= 8  # <8> determined by analyzing output, makes sense given opcodes
            else:
                val += 1
    
    if output == target:
        return val / 8
    else:
        return -1



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



puzzles = [['test_case.txt',    ['4,6,3,5,6,3,5,2,1,0', None]],
           ['test_case_2.txt',  [None, 117440]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)