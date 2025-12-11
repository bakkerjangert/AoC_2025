from collections import defaultdict

def get_paths_len_dict(s, e):
    current_nodes, finished_paths = {s: 1}, 0
    while current_nodes:
        new_nodes = defaultdict(int)
        for node in current_nodes.keys():
            for c in connections[node]:
                if c == e:
                    finished_paths += current_nodes[node]
                else:
                    new_nodes[c] += current_nodes[node]
        current_nodes = new_nodes
    return finished_paths

file = 'input.txt'
# file = 'test.txt'
with open(file, encoding="utf8") as f:
    data = f.read().splitlines()

connections = defaultdict(list)
reversed_connections = defaultdict(list)
for r in data:
    name, connection = r.split(': ')
    connection = connection.split(' ')
    for c in connection:
        connections[name].append(c)
        reversed_connections[c].append(name)

print(f'Part 1: {get_paths_len_dict("you", "out")}')

n1 = get_paths_len_dict('svr', 'fft')
n2a = get_paths_len_dict('fft', 'dac')
n2b = get_paths_len_dict('dac', 'fft')
if n2a != 0:
    n3 = get_paths_len_dict('dac', 'out')
else:
    n3 = get_paths_len_dict('fft', 'out')
print(f'Part 2: {n1 * max(n2a, n2b) * n3}')
