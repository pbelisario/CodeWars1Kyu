def solvePuzzle(clues):
    list_len = len(clues)//4
    # generate all possible permutations
    # of 1 to the width of the skyscraper grid
    permutations = [elements for elements in generatePermutations(list(range(1, list_len+1)))]

    # Group by seen
    seenMap = dividedIntoGroups(permutations)

    # init Grid
    grid = [[0 for i in range(list_len)] for j in range(list_len)]

    # init Mask
    mask = fillGrid(grid, clues, list_len)

    rowCandidatesList = [[candidates for candidates in getCandidatesForRow(row, clues, permutations, seenMap, list_len)] for row in range(list_len)]
    colCandidatesList = [[candidates for candidates in getCandidatesForCol(col, clues, permutations, seenMap, list_len)] for col in range(list_len)] 
    
    filterCandidatesListByMask(rowCandidatesList, colCandidatesList, grid, mask, list_len)
    '''
    while(True):
        updated = filterCandidatesListByMask(rowCandidatesList, colCandidatesList, grid, mask)
        if (not updated): break

        updateMask(mask, rowCandidatesList, colCandidatesList)
        pruneGridAndMask(grid, mask, list_len)
'''

    pass

# create an array with all permutations
# of a sequence between n and 1
def generatePermutations(elements):
    # Final step
    if len(elements) <= 1:
        yield elements
    # Recursive step
    else:
        for perm in generatePermutations(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]

def filterCandidatesListByMask(rowCandidatesList, colCandidatesList, grid, mask, list_len):
    updated = False
    rowPossibleCombinations = {}
    for row in range(list_len):
        if not rowPossibleCombinations.get(row):
            rowPossibleCombinations[row] = []
        for candidateList in rowCandidatesList[row]:
            count = 0
            for col in range(len(candidateList)):
                if not (mask[row][col] & (1 << candidateList[col]-1)):
                    count += 1
            if count > 6:                
                rowPossibleCombinations[row] += [candidateList]
        if len(rowPossibleCombinations) < len(rowCandidatesList[row]): updated = True
        if len(rowPossibleCombinations) == 1:
            heights = rowPossibleCombinations[0]
            for col in range(list_len):
                grid[row][col] = heights[col]
                maskTheSameLine(mask, row, col, heights[col])
        rowCandidatesList[row] = rowPossibleCombinations
    



def getCandidatesForRow(row, clues, permutations, seenMap, list_len):
    left = getLeftClue(clues, row, len(clues))
    right = getRightClue(clues, row, list_len)

    if left and right:
        candidates = seenMap.get('total')[left][right]
    elif left:
        candidates = seenMap.get('left')[left]
    elif right:
        candidates = seenMap.get('right')[right]
    else:
        candidates = permutations
    return candidates

def getCandidatesForCol(col, clues, permutations, seenMap, list_len):
    top = getTopClue(clues, col)
    bottom = getBotClue(clues, col, list_len)
    if top and bottom:
        candidates = seenMap.get('total')[top][bottom]
    elif top:
        candidates = seenMap.get('left')[top]
    elif bottom:
        candidates = seenMap.get('right')[bottom]
    else:
        candidates = permutations
    return candidates

def dividedIntoGroups(permutations):
    # {Number of Skyscraper possible to see : configurations possible for each number}
    left_map = {}
    right_map = {}
    # {Number of Skyscraper in the left: {Number of Skyscraper in the right : configurations}}
    total_map = {}
    for group in permutations:
        left = howManyElementsICanSee(group)
        if not left_map.get(left):
            left_map[left] = []
        left_map[left] += [group]

        right = howManyElementsICanSee(group[::-1])
        if not right_map.get(right):
            right_map[right] = []
        right_map[right] += [group]

        if not total_map.get(left):
            total_map[left] = {}
        if not total_map.get(left).get(right):
            total_map[left][right] = []
        total_map[left][right] += [group]
    
    return {'left' : left_map, 'right' : right_map, 'total' : total_map}

def fillGrid(grid, clues, n):
    # If it assumes a value X, it means that X can not be the answear
    # in the given position. 1 <= X <= n
    mask = [[0 for i in range(n)] for j in range(n)]
    
    length = len(clues)
    # Check by Row
    for i in range(n):
        left = getLeftClue(clues, i, length)
        right = getRightClue(clues, i, n)
        for j in range(n):
            if (left == 1 and not j) or (right == 1 and j == n-1):
                maskTheSameLine(mask, i, j, n)
                continue

            for k in range(1, n+1):
                behind = n - k + 1
                if (j + behind < left) or (n - 1 - j + behind < right):
                    mask[i][j] |= 1 << k - 1
                
    # Check by Column 
    for j in range(n):
        top = getTopClue(clues, j)
        bot = getBotClue(clues, j, n)
        for i in range(n):
            if (top == 1 and not i) or (bot == 1 and i == n - 1):
                maskTheSameLine(mask, i, j, n)
                continue
            
            for k in range(1, n+1):
                behind = n - k + 1
                if (i + behind < top) or (n - 1 - i + behind < bot):
                    mask[i][j] |= 1 << k - 1

    pruneGridAndMask(grid, mask, n)
    
    return mask


def pruneGridAndMask(grid, mask, n):
    while True:
        if findUniqueBit(grid, mask, n): continue
        if findUniqueCol(grid, mask, n): continue
        if findUniqueRow(grid, mask, n): continue
        break

def maskTheSameLine(mask, i, j, x):
    len_mask = len(mask)
    maskAll = 2**len_mask - 1
    for k in range(len_mask):
        if k != j:
            mask[i][k] |= 1 << x - 1
        if k != i:
            mask[k][j] |= 1 << x - 1
    mask[i][j] = ~(1 << x-1) & maskAll

def findUniqueIndex(n, fn):
    indexes = []
    for i in range(n):
        if (fn(i)):
            indexes.append(i)
    return indexes[0] if len(indexes) == 1 else -1


def findUniqueBit(grid, mask, n):
    for i in range(n):
        for j in range(n):
            if grid[i][j]: 
                continue
            k = findUniqueIndex(n , lambda bit : not(mask[i][j] & (1 << bit)))
            if k >= 0:
                grid[i][j] = k + 1
                maskTheSameLine(mask, i, j, k+1)
                return True
    return False

def findUniqueCol(grid, mask, n):
    for i in range(n):
        for k in range(n):
            j = findUniqueIndex(n, lambda col: not(grid[i][col]) and not(mask[i][col] & (1 << k)))

            if j >= 0:
                grid[i][j] = k + 1
                maskTheSameLine(mask, i, j, k+1)
                return True
    return False

def findUniqueRow(grid, mask, n):
    for j in range(n):
        for k in range(n):
            i = findUniqueIndex(n, lambda row: not(grid[row][j]) and not(mask[row][j] & (1 <<k)))
            if i >= 0:
                grid[i][j] = k + 1
                maskTheSameLine(mask, i, j, k+1)
                return True
    return False


def getLeftClue(clues, row, length):
    return clues[length - 1 - row]

def getRightClue(clues, row, length):
    return clues[length + row]

def getTopClue(clues, column):
    return clues[column]

def getBotClue(clues, column, length):
    return clues[(length*3) - 1 - column]

# given an array, how many elements I can see
# if a bigger number hides the smaller one
# after him
def howManyElementsICanSee(group):
    cur_element = group[0]
    count = 1
    for element in group:
        if element > cur_element:
            cur_element = element
            count += 1
    return count

solvePuzzle([7,0,0,0,2,2,3, 0,0,3,0,0,0,0, 3,0,3,0,0,5,0, 0,0,0,0,5,0,4])