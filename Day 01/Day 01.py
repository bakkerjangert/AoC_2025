from collections import deque

dail = deque(range(100))
dail.rotate(-50) # left = positive, right = negative

file = 'input.txt'
# file = 'aoc-2025-day-1-challenge-1.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()

password_pt1 = 0
for instruction in data:
    factor = 1 if instruction[0] == 'L' else -1
    dail.rotate(factor * int(instruction[1:]))
    if dail[0] == 0:
        password_pt1 += 1
print(f'Part 1: {password_pt1}')

password_pt2 = 0
dail = deque(range(100))
dail.rotate(-50)
for instruction in data:
    factor = 1 if instruction[0] == 'L' else -1
    number = int(instruction[1:])
    password_pt2 += number // 100
    number %= 100
    if number == 0:
        continue
    prev_number = dail[0]
    dail.rotate(factor * int(instruction[1:]))
    if dail[0] == 0:
        password_pt2 += 1
        continue
    if prev_number == 0:
        continue
    if (instruction[0] == 'L' and dail[0] > prev_number) or (instruction[0] == 'R' and dail[0] < prev_number):
        password_pt2 += 1
print(f'Part 2: {password_pt2}')
