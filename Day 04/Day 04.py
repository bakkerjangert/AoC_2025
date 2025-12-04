file = 'input.txt'
# file = 'test.txt'
with open(file, 'r') as f:
    grid = [list(line.strip()) for line in f if line.strip()]

# Add empty outer ring to grid to simplify calculations
for r in range(len(grid)):
    grid[r] = ['.'] + grid[r] + ['.']
grid = [['.'] * len(grid[0])] + grid + [['.'] * len(grid[0])]

pt1_solved = False
rolls_accessible, removed_rolls = set(), 0
while len(rolls_accessible) > 0 or not pt1_solved:
    rolls_accessible = set()
    for r in range(1, len(grid) - 1): # omit outer ring
        for c in range(1, len(grid[0]) - 1): # omit outer ring
            if grid[r][c] == '@':
                rolls = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if grid[r + dr][c + dc] in '@':
                            rolls += 1
                if rolls <= 4:  # roll in center is counted
                    rolls_accessible.add((r, c))
    if not pt1_solved:
        print(f'Part 1: {len(rolls_accessible)}')
        pt1_solved = True
    removed_rolls += len(rolls_accessible)
    for r, c in rolls_accessible:
        grid[r][c] = '.'
print(f'Part 2: {removed_rolls}')

# for r in grid[1:-1]:
#     print(''.join(r[1:-1]))
