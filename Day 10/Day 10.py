import itertools
from collections import Counter


def minimum_pushes(string, buttons):
    lights = [i for i in range(len(string)) if string[i] == '#']
    pushes, solved = 1, False
    while not solved:
        # No need for multiple pushes of a button; pushing button twice reverts a step back
        combinations = itertools.combinations(buttons, pushes)
        for c in combinations:
            numbers = sum(c, ())
            counts = Counter(numbers)
            current_lights = sorted([num for num, cnt in counts.items() if cnt % 2 == 1])
            if lights == current_lights:
                solved = True
                # print(f'Solved in {pushes} pushes!')
                return pushes
        pushes += 1
    return None

def minimum_pushes_pt2(jolts, buttons, current_jolts=None):
    if current_jolts is None:
        current_jolts = [0,] * len(jolts)
    if not buttons:
        return None

    i =
    for i in

file = 'input.txt'
file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()

total_pushes_pt1, total_pushes_pt2 = 0, 0
for r in data:
    lights = r.split('[')[1].split(']')[0]
    jolts = list(map(int, r.split('{')[1].split('}')[0].split(',')))
    buttons = r.split('] ')[1].split(' {')[0]
    buttons = buttons.replace(' ', ', ')
    buttons = buttons.replace(')', ',)')
    buttons = eval(f'({buttons})')
    total_pushes_pt1 += minimum_pushes(lights, buttons)
    dfs(buttons, jolts)
print(f'Part 1: {total_pushes_pt1}')