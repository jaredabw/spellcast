r, c = (2, 2)
surroundings = []
for i in (-1, 0, 1):
    for j in (-1, 0, 1):
        if 0 <= r + i <= 4 and 0 <= c + j <= 4 and not (i == 0 and j == 0):
            surroundings.append((r + i, c + j))

print(surroundings)