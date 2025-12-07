import math

file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()
data_pt2 = data[:]
data = [r.strip().split() for r in data]
grand_total = 0
for i in range(len(data[0])):
    if data[-1][i] == '+':
        grand_total += sum(map(int, [data[j][i] for j in range(len(data) - 1)]))
    else:
        grand_total += math.prod(map(int, [data[j][i] for j in range(len(data) - 1)]))
print(f'Part 1: {grand_total}')

# Part 2 - Order doesn't matter since only addition and multiplication are used
data = data_pt2[:]
grand_total = 0

# add column with ' ' at end:
max_len = max(len(data[i]) for i in range(len(data)))
for i in range(len(data)):
    data[i] = data[i] + ' ' * (1 + max_len - len(data[i]))
indexes = [i for i in range(len(data[0])) if all(data[j][i] == ' ' for j in range(len(data)))]

start_index = 0
for end_index in indexes:
    numbers = []
    for i in range(start_index, end_index):
        numbers.append(int(''.join(data[j][i] for j in range(len(data) - 1)).strip()))
    # print(numbers)
    if '+' in data[-1][start_index:end_index]:
        grand_total += sum(numbers)
        # print(sum(numbers))
    else:
        grand_total += math.prod(numbers)
        # print(math.prod(numbers))
    start_index = end_index + 1
print(f'Part 2: {grand_total}')
