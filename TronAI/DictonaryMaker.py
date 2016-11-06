counter = 0
map = dict()
for i in range(0, 30, 1):
    for v in range(0, 20, 1):
        map[(i, v)] = False


nodes = {}
for i in range(30):
    for j in range(20):
        neighbours = []
        if i < 29:
            neighbours.append((i + 1, j))
        if i > 0:
            neighbours.append((i - 1, j))
        if j < 19:
            neighbours.append((i, j + 1))
        if j > 0:
            neighbours.append((i, j - 1))
        nodes[(i, j)] = neighbours

print(map)
print("\n")
print(nodes)