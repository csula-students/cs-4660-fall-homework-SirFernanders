counter = 0
map = dict()
for i in range(0, 32, 1):
    for v in range(0, 22, 1):
        counter += 1
        if (i == 0) or (i == 21) or (v == 0) or (v == 31):
            map[str(i) + "-" + str(v)] = True
        else:
            map[str(i) + "-" + str(v)] = False
print(map)
print(map["0-0"])
