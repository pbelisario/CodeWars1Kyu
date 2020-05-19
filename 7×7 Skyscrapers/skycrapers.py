import itertools

def solve_puzzle (clues):
    list_len = len(clues) // 4
    
    # Create an empty board
    puzzle = [[0 for x in range(list_len)] for y in range(list_len)]

    # create an array with all possible permutations
    permutations = list(itertools.permutations(range(list_len), list_len))

    # Each array stores how many skyscraper it is possible to see
    # lookin from the left (cl) or right(cr), at the same index
    # in the permutations array
    # Eg. cl[0] = 7 permutations[0] = (0, 1, 2, 3, 4, 5, 6)
    #     cr[0] = 1 permutations[::-1][0] = (6, 5, 4, 3, 2, 1, 0)
    # Left side
    cl = list(map(lambda x: count_steps(x, list_len), permutations))
    # Right side
    cr = list(map(lambda x: count_steps(x[::-1], list_len), permutations))
    
    # Create all possible permutations for rows and columns
    rows = []
    for row in range(list_len):
        left, right = clues[list_len*4-row-1], clues[list_len+row]
        rows.append([permutations[i] for i in range(len(permutations)) if (left == 0 or cl[i] == left) and (right == 0 or cr[i] == right)])

    cols = []
    for col in range(list_len):
        left, right = clues[col], clues[list_len*3-col-1]
        cols.append([permutations[i] for i in range(len(permutations)) if (left == 0 or cl[i] == left) and (right == 0 or cr[i] == right)])
    
    
    # As long as the puzzle is not completely solved
    while [len(row) for row in rows].count(1) < list_len:
        state = [len(row) for row in rows] + [len(col) for col in cols]

        try_solve(rows, cols, puzzle, list_len)

        if [len(row) for row in rows].count(1) < list_len and [len(row) for row in rows] + [len(col) for col in cols] == state:
            
            heights_sort = sorted([(len(height), 0, i) for i, height in enumerate(rows)] + [(len(height), 1, i) for i, height in enumerate(cols)])

            modified = False

            for height in heights_sort:

                # the correct one
                if height[0] == 1:
                    continue

                index = height[2]

                for i in range(height[0]):

                    # copy the current state
                    c_rows = [h.copy() for h in rows]
                    c_cols = [h.copy() for h in cols]
                    c_puzzle = [r.copy() for r in puzzle]

                    # remove every hypothesis except the selected one
                    if height[1] == 0:
                        c_rows[index] = [rows[index][i]]
                    else:
                        c_cols[index] = [cols[index][i]]
                    
                    # if this hypothesis is not valid.
                    # remove it from the original state
                    if not try_solve(c_rows, c_cols, c_puzzle, list_len):
                        if height[1] == 0:
                            rows[index].pop(i)
                        else:
                            cols[index].pop(i)
                        
                        modified = True
                        break
                if modified:
                    break
            # could not solve
            if not modified:    
                break
    return puzzle
            
                        



def count_steps(values, list_len):
    max_step, steps = 0, 0
    for value in values:
        if value >= max_step:
            steps += 1
            max_step = value
        if value >= list_len-1:
            break
    return steps

def try_solve(rows, cols, puzzle, list_len):
    changed = True

    while changed:
        changed = False

        for row in range(list_len):
            for col in range(list_len):

                # For each entry
                #   if a number i can be placed according to a hypothesis in cols / rows
                #     return True
                count_cols = [len(hypothesis(cols[col], row, i)) > 0 for i in range(list_len)]
                count_rows = [len(hypothesis(rows[row], col, i)) > 0 for i in range(list_len)]

                # no number can be placed. There isn't a possible solution
                if count_rows.count(True) == 0 or count_cols.count(True) == 0:
                    return False
                
                if count_rows.count(True) == 1 or puzzle[row][col] == 0:
                    puzzle[row][col] = count_rows.index(True) + 1
                elif count_cols.count(True) == 1 or puzzle[row][col] == 0:
                    puzzle[row][col] = count_cols.index(True) + 1
                
                # update rows / cols
                # remove entries that are not possible anymore
                for i in range(list_len):
                    if count_cols[i] == count_rows[i]:
                        continue

                    # no hypothesis uses i in a row = remove col from cols
                    if count_cols[i]:
                        cols[col] = [r for r in cols[col] if r[row] != i]
                    
                    # no hypothesis uses
                    if count_rows[i]:
                        rows[row] = [c for c in rows[row] if c[col] != i]
                    
                    changed = True
    return True    

def hypothesis(hypothesis, x, height):
    return[heights[x] for heights in hypothesis if heights[x] == height]

print(solve_puzzle([7,0,0,0,2,2,3, 0,0,3,0,0,0,0, 3,0,3,0,0,5,0, 0,0,0,0,5,0,4]))
