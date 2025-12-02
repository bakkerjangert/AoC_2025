from collections import deque

file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()
    data = data[0].split(',')
    print(type(data), data)

invalid_IDs_pt1 = 0
for d in data:
    n1, n2 = map(int, d.split('-'))
    if len(str(n1)) != len(str(n2)):
        # checked --> maximum 1 digit difference between n1 and n2
        # rewrite to two even length numbers (example 1000 - xxxx or xxxx - 9999)
        if len(str(n1)) % 2 == 1:
            n1 = int('1' + len(str(n1)) * '0')
        else:
            n2 = int('9' * (len(str(n2)) - 1))
    if len(str(n1)) % 2 == 1:
        # uneven length; no repeating sequence possible
        continue
    s1, s2 = int(str(n1)[:len(str(n1)) // 2]), int(str(n2)[:len(str(n2)) // 2])
    # print(n1, n2, s1, s2)
    for n in range(s1, s2 + 1):
        if n1 <= int(str(n) + str(n)) <= n2:
            # print(f'Invalid found {str(n) + str(n)}')
            invalid_IDs_pt1 += int(str(n) + str(n))
print(f'Part 1: {invalid_IDs_pt1}')

sorted_data = []  # ranges split so start and end have the same digit length
for d in data:
    n1, n2 = d.split('-')
    split = False
    if len(n1) == len(n2) == 1:
        # single digit is never invalid
        continue
    elif len(n1) == len(n2):
        sorted_data.append(d)
    elif len(n1) == 1:
        sorted_data.append(f'10-{n2}')
    else:
        # Assume never more than a single digit difference between n1 and n2
        sorted_data.append(f'{n1}-{"9" * len(n1)}')
        sorted_data.append(f'{"1"}{"0" * len(n1)}-{n2}')
        split = True


invalid_IDs_pt2 = 0
for d in sorted_data:
    n1, n2 = d.split('-')
    invalids = set()
    for sequence_len in range(1, len(n1) // 2 + 1):
        if len(n1) % sequence_len != 0:
            continue
        sequences = len(n1) // sequence_len
        for n in range(int(n1[:sequence_len]), int(n2[:sequence_len]) + 1):
            if int(n1) <= int(str(n) * sequences) <= int(n2):
                invalids.add(int(str(n) * sequences))
    invalid_IDs_pt2 += sum(invalids)
print(f'Part 2: {invalid_IDs_pt2}')

# 4174379265