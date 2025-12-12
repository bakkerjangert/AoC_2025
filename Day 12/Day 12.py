from collections import defaultdict

from numpy.ma.extras import column_stack

file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()

number_of_blocks = sum(1 for row in data if row.strip() == '')
blocks = defaultdict(list)
for i in range(number_of_blocks):
    rows = data[1 + 5 * i: 4 + 5 * i]
    for row in rows:
        for col in row:
            if col == '#':
                blocks[i].append((row, col))

does_not_fit, maybe_fits, fits_for_sure = 0, 0, 0

for r in data[number_of_blocks * 5:]:
    h, b = map(int, r.split(':')[0].split('x'))
    required_blocks = tuple(map(int, r.split(': ')[1].split(' ')))
    parts = sum(len(blocks[i]) * val for i, val in enumerate(required_blocks))
    if h * b < parts:
        does_not_fit += 1
    elif h // 3 * b // 3 >= sum(required_blocks):
        fits_for_sure +=1
    else:
        maybe_fits += 1

print(f'Part 1: {fits_for_sure}')
print(f'Maybe fits: {maybe_fits}')
print(f'Does not fit: {does_not_fit}')


