from collections import defaultdict

file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()

beams = defaultdict(int)
beams[data[0].index('S')] = 1

total_splits = 0
for row_n, r in enumerate(data[:]):
    splitters = [i for i in range(len(r)) if r[i] == '^']
    # print(splitters)
    for s in splitters:
        if beams[s] > 0:
            total_splits += 1
            beams[s - 1] += beams[s]
            beams[s + 1] += beams[s]
            beams[s] = 0
    for k in beams.keys():
        if data[row_n][k] != '^' and beams[k] > 0:
            data[row_n] = data[row_n][:k] + '|' + data[row_n][k + 1:]
print(f'Part 1: {total_splits}')
print(f'Part 2: {sum(beams.values())}')

# for r in data:
#     print(''.join(r))

