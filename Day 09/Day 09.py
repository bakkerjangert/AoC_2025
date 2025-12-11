from copy import deepcopy

import matplotlib.pyplot as plt

class StraightLine:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.vert = True if self.x1 == self.x2 else False
        self.hor = True if self.y1 == self.y2 else False
        if not self.hor and not self.vert:
            print(f'Warning: Not a Straight Line: ({x1},{y1}) -> ({x2},{y2})')
        # if self.hor and self.vert:
        #     print(f'Warning: Line in one point! ({x1},{y1}) -> ({x2},{y2})')
    def checkIntersection(self, other):
        if (self.hor and other.hor) or (self.vert and other.vert):
            # checked lines never at same x or y coordinate
            return False
        l1_xmax, l1_xmin = max(self.x1, self.x2), min(self.x1, self.x2)
        l1_ymax, l1_ymin = max(self.y1, self.y2), min(self.y1, self.y2)
        l2_xmax, l2_xmin = max(other.x1, other.x2), min(other.x1, other.x2)
        l2_ymax, l2_ymin = max(other.y1, other.y2), min(other.y1, other.y2)
        if self.hor:
            if (l1_xmin < l2_xmin < l1_xmax) and (l2_ymin < l1_ymin < l2_ymax):
                return True
            return False
        elif self.vert:
            if (l1_ymin < l2_ymin < l1_ymax) and (l2_xmin < l1_xmin < l2_xmax):
                return True
            return False
        print('Warning: Shouldnt be here in intersection check!')
        return None

    def __repr__(self):
        return f'({"vertical" if self.vert else "horizontal"} line with coordinates ({self.x1},{self.y1}) -> ({self.x2},{self.y2})'

file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()
data = [list(map(int, r.split(','))) for r in data]

areas = []
for i, (x1, y1) in enumerate(data[:-1]):
    for x2, y2 in data[i + 1:]:
        areas.append(((x1, y1), (x2, y2), (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)))
areas.sort(key=lambda x: x[2], reverse=True)
print(f'Part 1: {areas[0][2]}')

boundaries = list()
for (x1, y1), (x2, y2) in zip(data, data[1:] + [data[0],]):
    boundaries.append(StraightLine(x1, y1, x2, y2))
original_boundaries = deepcopy(boundaries)

# Move initial boundary outside by 0.5 to prevent unwanted intersections
max_x = max(l.x1 for l in boundaries)
most_right_vertical = [l for l in boundaries if l.vert and l.x1 == max_x][0]
i = boundaries.index(most_right_vertical)
move_hor, move_vert = 'r', None # None, r(ight), l(eft); None, u(p), d(own)

delta = 0.5
# for i, (_l, l1, l_) in enumerate(zip([boundaries[-1]] + boundaries[:-1], boundaries, boundaries[1:] + [boundaries[0]])):
for i, (_l, l1, l_) in enumerate(
            zip(boundaries[i-1:] + boundaries[:i-1], boundaries[i:] + boundaries[:i], boundaries[i+1:] + boundaries[:i+1])):
    if move_hor:
        # print(_l == boundaries[i - 1], l1 == boundaries[i], l_ == boundaries[i + 1])
        # Adjust boundaries
        factor = 1 if move_hor == 'r' else -1
        _l.x2 += delta * factor
        l1.x1 += delta * factor
        l1.x2 += delta * factor
        l_.x1 += delta * factor
        # determine next move direction
        if l1.y1 < l1.y2: # move up
            if move_hor == 'r':
                move_vert = 'd' if l_.x1 < l_.x2 else 'u'
            else:
                move_vert = 'u' if l_.x1 < l_.x2 else 'd'
        else: # move down
            if move_hor == 'r':
                move_vert = 'u' if l_.x1 < l_.x2 else 'd'
            else:
                move_vert = 'd' if l_.x1 < l_.x2 else 'u'
        move_hor = None
    elif move_vert:
        # Adjust boundaries
        factor = 1 if move_vert == 'u' else -1
        _l.y2 += delta * factor
        l1.y1 += delta * factor
        l1.y2 += delta * factor
        l_.y1 += delta * factor
        # determine next move direction
        if l1.x1 < l1.x2: # move right
            if move_vert == 'u':
                move_hor = 'l' if l_.y1 < l_.y2 else 'r'
            else:
                move_hor = 'r' if l_.y1 < l_.y2 else 'l'
        else: # move left
            if move_vert == 'u':
                move_hor = 'r' if l_.y1 < l_.y2 else 'l'
            else:
                move_hor = 'l' if l_.y1 < l_.y2 else 'r'
        move_vert = None
    else:
        print('Error: No move direction!!')

# sort shifted boundaries on length to improve speed (longest line has highset chang to be crossed)
sorted_boundaries = sorted(boundaries, key=lambda x: abs(x.x1 - x.x2) + abs(x.y1 - x.y2))
# boundaries.sort(key=lambda x: abs(x.x1 - x.x2) + abs(x.y1 - x.y2), reverse=True)

for rectangle in areas:
    x1, y1 = rectangle[0]
    x2, y2 = rectangle[1]
    valid_rectangle = True
    for l1 in (StraightLine(x1, y1, x2, y1), StraightLine(x1, y1, x1, y2), StraightLine(x2, y1, x2, y2), StraightLine(x1, y2, x2, y2)):
        for l2 in sorted_boundaries:
            if l1.checkIntersection(l2):
                valid_rectangle = False
                break
        if not valid_rectangle:
            break
    if valid_rectangle:
        print(f'Part 2: {rectangle[2]}')
        r_pt2 = rectangle
        break


# Plot initial Boundary
x = [b.x1 for b in original_boundaries + [original_boundaries[0]]]
y = [b.y1 for b in original_boundaries + [original_boundaries[0]]]
plt.plot(x, y, color='blue')
# Plot shifted Boundary
x = [l.x1 for l in boundaries + [boundaries[0]]]
y = [l.y1 for l in boundaries + [boundaries[0]]]
plt.plot(x, y, color='red')
plt.axis('equal')
x_rct = (r_pt2[0][0], r_pt2[1][0])
y_rct = (r_pt2[0][1], r_pt2[1][1])
plt.fill_between(x_rct, y_rct[0], y_rct[1], color='green')
plt.show()
