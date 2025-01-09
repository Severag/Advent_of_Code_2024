import re
import numpy as np
from collections import defaultdict


def read_file(filename):
    wires = dict()
    in_wires = True
    
    gates = []
    regex = r"(\w+) (\w+) (\w+) -> (\w+)"
    
    with open( filename, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) < 1:
                in_wires = False
            elif in_wires:
                wire_id, val = line.split(':')
                wires[wire_id] = int(val)
            else:
                gates.append(re.findall(regex, line)[0])
    
    return wires, gates



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def do_op(intput1, op, input2):    
    if op == 'AND':
        return intput1 and input2
    elif op == 'OR':
        return intput1 or input2
    elif op == 'XOR':
        return intput1^input2
    else:
        raise ValueError



def get_num(wire_states, start_str):
    char_ids = sorted([wire_id for wire_id in wire_states.keys() if wire_id.startswith(start_str)], reverse=True)
    char_vals = ''.join([str(wire_states[wire_id]) for wire_id in char_ids])
    
    return int(char_vals, 2)



def part1(data):
    wire_states = data[0].copy()
    gates = data[1]
    
    gate_states = [0] * len(gates)
    gate_still_open = True
    
    # let everything calculate
    while gate_still_open:
        gate_still_open = False
        for idx, (state, instr) in enumerate(zip(gate_states, gates)):
            if state == 0:  # still open, check if it can resolve
                wire1, op, wire2, wire_out = instr
                
                if wire1 in wire_states and wire2 in wire_states:
                    # update wire state
                    wire_states[wire_out] = do_op(wire_states[wire1], op, wire_states[wire2])
                    # update gate state
                    gate_states[idx] = 1
                else:  # can't resolve, must do another pass through the list
                    gate_still_open = True
    
    # determine the z-values
    z_num = get_num(wire_states, 'z')
    
    return z_num



def sort_gates(gates):  # sotring is not strictly necessary, but was helpful to grasp the problem
    new_gates = []
    # inputs to the pairs of AND and XOR gates that add in the previous column's remainder
    mid_gate_inputs = set()  
    # inputs to the OR gate that determines if we need to "carry a one"
    OR_gate_inputs = set()
    
    for instr in gates:
        wire1, op, wire2, wire_out = instr
        
        if wire2 < wire1:  # wires are out of alphabetical order
            instr = (wire2, op, wire1, wire_out)
            wire1, op, wire2, wire_out = instr
        
        new_gates.append(instr)
        
        if op == 'OR':
            OR_gate_inputs |= {wire1, wire2}
        elif not wire1.startswith('x'):
            mid_gate_inputs |= {wire1, wire2}
        
    return sorted(new_gates), mid_gate_inputs, OR_gate_inputs



def part2(data):
    gates, mid_gate_inputs, OR_gate_inputs = sort_gates(data[1])
    last = f"z{int(gates[-1][0][1:]) + 1}"
    
    wrong_outs = []
    wrong_instr = []  # is not strictly necessary, but was helpful to grasp the problem
    
    for instr in gates:
        wire1, op, wire2, wire_out = instr
        
        is_edge_case = wire_out == 'z00' or wire_out == last
        should_flag = False
        
        # neither starting gates nor OR gates should have 'z' outputs
        if wire1.startswith('x') or op == 'OR':
            if wire_out.startswith('z') and not is_edge_case:
                should_flag = True
        # of the remaining gates, the AND gates should lead to a non-z wire
        # and the XOR gates should lead to z wires
        elif (op == 'AND' and wire_out.startswith('z')) or (
              op == 'XOR' and not wire_out.startswith('z')):
            should_flag = True
        
        # with erroneous z's out of the way, move on to mundane checks
        if wire1 != 'x00' and not should_flag:
            if op == 'AND' and wire_out not in OR_gate_inputs:
                # this wire should be headed to an OR gate, check if it matches one that does
                should_flag = True
            elif wire1.startswith('x') and op == 'XOR' and wire_out not in mid_gate_inputs:
                should_flag = True
        
        if should_flag:
            wrong_outs.append(wire_out)
            wrong_instr.append(instr)
    
    return ','.join(sorted(wrong_outs))



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



puzzles = [['test_case.txt',    [4, None]],
           ['test_case_2.txt',  [2024, None]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)