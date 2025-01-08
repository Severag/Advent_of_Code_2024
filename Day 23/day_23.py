import numpy as np
from collections import defaultdict


def read_file(filename):
    with open( filename, 'r') as f:
        data = [line.strip().split('-') for line in f]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1, extra = part1(data) if do_1 else [None, None]
    p2 = part2(data, extra) if do_2 else None
    
    return p1, p2



def part1(data):
    connections = defaultdict(set)
    
    for comp1, comp2 in data:
        connections[comp1].add(comp2)
        connections[comp2].add(comp1)
    
    parties = set()
    T_triplet = set()
    for comp1, partners in connections.items():        
        for comp2 in partners:
            common = partners & connections[comp2]
            
            parties.add(tuple(sorted( {comp1, comp2} | common )))
            for comp3 in common:
                new_triplet = tuple(sorted((comp1, comp2, comp3)))
                
                if True in [comp.startswith('t') for comp in new_triplet]:
                    T_triplet.add(new_triplet)
    
    return len(T_triplet), (connections, parties)



def part2(data, extra):
    connections, parties = extra
    totally_connected_parties = []
    
    for party_cand in parties:
        cand_set = set(party_cand)
        
        for comp1 in party_cand:
            partners = connections[comp1]
            
            # if <comp1> is not connected to all the members of this party
            if not cand_set.issubset(partners | {comp1,}):
                break
        else:  # no-break condition: all members of the party connect to all other members
            totally_connected_parties.append(party_cand)
    
    biggest = max(totally_connected_parties, key=len)
    
    return ','.join(biggest)



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



puzzles = [['test_case.txt',    [7, 'co,de,ka,ta']],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)