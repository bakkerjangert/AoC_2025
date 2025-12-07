def check_ingredient(i):
    for a, b in ranges:
        if a <= i <= b:
            return True
    return False

file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()
ranges = [tuple(map(int, r.split('-'))) for r in data if '-' in r]
ingredients = tuple(map(int, data[len(ranges) + 1:]))

print(f'Part 1: {sum(check_ingredient(i) for i in ingredients)}')

ranges.sort(key=lambda r: r[0])
merged_ranges = [ranges[0]]
for a, b in ranges[1:]:
    if merged_ranges[-1][1] < a - 1:
        # gap between ranges, add new range
        merged_ranges.append((a, b))
    else:
        # merge ranges
        merged_ranges[-1] = (merged_ranges[-1][0], max(b, merged_ranges[-1][1]))

print(f'Part 2: {sum(b - a + 1 for a, b in merged_ranges)}')