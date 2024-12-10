import numpy as np


def read_file(filename):
    with open( filename, 'r') as f:
        data = [int(val) for line in f for val in line.strip()]
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    # expand disk map out to a full block representation
    disk = [idx // 2 if idx % 2 == 0 else '.' for idx,size in enumerate(data) for _ in range(size)]
    
    def get_byte():
        for neg_idx, val in enumerate(disk[::-1]):
            if val != '.':
                idx = len(disk) - 1 - neg_idx
                disk[idx] = '.'
                yield idx, val
    
    back_byte = get_byte()
    back_idx, back_val = next(back_byte)
    
    check_sum = 0
    
    for front_idx, val in enumerate(disk):
        if back_idx <= front_idx:  # crossed the pointers
            # reset <back_val>
            disk[back_idx] = back_val
            
            # make sure this value still gets added to checksum
            if disk[front_idx] != '.':
                check_sum += front_idx * disk[front_idx]
            
            break
        elif val == '.':  # fill empty space
            disk[front_idx] = back_val
            back_idx, back_val = next(back_byte)
        
        check_sum += front_idx * disk[front_idx]  # disk[front_idx] may not equal val anymore
    
    return check_sum



def part2(data):
    # expand disk map out to a full block representation
    disk = [idx // 2 if idx % 2 == 0 else '.' for idx,size in enumerate(data) for _ in range(size)]
    
    # create record of free space
    # each row is (ending index, size) for each free space
    free_map = [[-1, size] for size in data[1::2]]
    cumlative = 0
    for idx, size in enumerate(data):
        cumlative += size
        
        if idx % 2 == 1:
            free_map[(idx - 1) // 2][0] = cumlative
    
    # shift all files forward, if possible
    disk_idx = len(disk)
    for neg_data_idx, size in enumerate(data[:0:-1]):
        data_idx = len(data) - 1 - neg_data_idx
        new_disk_idx = disk_idx - size
                
        if data_idx % 2 == 0:  # if it's a file
            file_id = disk[new_disk_idx]
            disk_range = range(new_disk_idx, disk_idx) 
            
            # find an open spot forward of this file
            for f_idx, (free_end, free_size) in enumerate(free_map):
                # we're now looking behind this file, so just stop
                if free_end >= disk_idx:
                    free_range = range(0, 0)  # don't move it
                    break
                if size <= free_size:
                    # resize the record to account for the space we're taking
                    free_map[f_idx][1] = free_size - size
                    free_range = range(free_end - free_size, free_end)
                    break
            else:
                # if there aren't any valid moving locations, don't move this file
                free_range = range(0, 0)
            
            # reassign file addres to new location
            for new_idx, old_idx in zip(free_range, disk_range):
                disk[new_idx] = file_id
                disk[old_idx] = '.'
        
        disk_idx = new_disk_idx
    
    check_sum = 0
    for idx, val in enumerate(disk):
        check_sum += idx * val if val != '.' else 0
    
    return check_sum



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



puzzles = [['test_case.txt',    [1928, 2858]],
           ['test_case_2.txt',  [60, None]],
           ['test_case_3.txt',  [None, 169]],
           ['test_case_4.txt',  [None, 73]],
           ['puzzle_input.txt', []]]

for problem in puzzles:
    filename, answers = problem
    data = read_file(filename)
    
    do_parts = [ans is not None for ans in answers] if answers else [True, True]    
    print(f"\n\n{filename}")
    results = solve(data, *do_parts)
    check(results, answers)