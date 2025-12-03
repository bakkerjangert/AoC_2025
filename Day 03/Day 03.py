file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()

joltage_pt1 = 0
for d in data:
    numbers = list(map(int, list(d)))
    battery_1 = max(numbers[:-1])
    index_1 = numbers.index(battery_1)
    battery_2 = max(numbers[index_1 + 1:])
    joltage_pt1 += int(f'{battery_1}{battery_2}')
print(f'Part 1: {joltage_pt1}')

joltage_pt2 = 0
for d in data:
    numbers = list(map(int, list(d)))
    numbers.append('foo')  # just a placeholder to allow index -1 to point at last number
    joltage, start_index = '', 0
    for i in range(12):
        n = max(numbers[start_index:-12 + i])
        joltage += str(n)
        start_index += numbers[start_index:].index(n) + 1
    # print(joltage)
    joltage_pt2 += int(joltage)
print(f'Part 2: {joltage_pt2}')
