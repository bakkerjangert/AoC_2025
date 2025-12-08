import math
from collections import defaultdict

class Box:
    def __init__(self, string):
        x, y, z = list(map(int, string.split(',')))
        self.x, self.y, self.z = x, y, z
    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
    def __repr__(self):
        return f'Box at {self.x},{self.y},{self.z}'

file = 'input.txt'
to_be_paired = 1000
# file = 'test.txt'
# to_be_paired = 10
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()
data = list(map(Box, data))

distances = list()
for i, b1 in enumerate(data[:-1]):
    for b2 in data[i + 1:]:
        distances.append([b1, b2, b1.distance(b2)])
distances.sort(key=lambda x: x[2])

circuits, box_circuits = defaultdict(list), defaultdict(int)
new_circuit = 1
i = 0
for b1, b2, dist in distances:
    i += 1
    if box_circuits[b1] == box_circuits[b2] == 0:
        # print('New Circuit')
        circuits[new_circuit].append(b1)
        circuits[new_circuit].append(b2)
        box_circuits[b1] = new_circuit
        box_circuits[b2] = new_circuit
        new_circuit += 1
    elif box_circuits[b1] == box_circuits[b2]:
        # print('Already in circuit')
        pass
    elif box_circuits[b1] == 0:
        # print(f'Added {b1} to circuit {box_circuits[b2]}')
        circuits[box_circuits[b2]].append(b1)
        box_circuits[b1] = box_circuits[b2]
    elif box_circuits[b2] == 0:
        # print(f'Added {b2} to circuit {box_circuits[b1]}')
        circuits[box_circuits[b1]].append(b2)
        box_circuits[b2] = box_circuits[b1]
    else:
        # print('\nMerging')
        c1, c2 = box_circuits[b1], box_circuits[b2]
        circuits[box_circuits[b1]] += circuits[box_circuits[b2]]
        for b in circuits[c2]:
            box_circuits[b] = c1
        del circuits[c2]
    if i == to_be_paired:
        longest_circuit = sorted(list(circuits.values()), key=len, reverse=True)
        print(f'Part 1: {math.prod(len(i) for i in longest_circuit[:3])}')
    if len(circuits) == 1 and all(box_circuits[b] > 0 for b in data):
        print(f'Part 2: {b1.x * b2.x}')
        break
