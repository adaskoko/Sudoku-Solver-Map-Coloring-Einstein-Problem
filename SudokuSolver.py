from Backtracking import *
import time

problem = Problem()

'''fields = [
    [5, 4, 0, 0, 2, 0, 8, 0, 6],
    [0, 1, 9, 0, 0, 7, 0, 0, 3],
    [0, 0, 0, 3, 0, 0, 2, 1, 0],
    [9, 0, 0, 4, 0, 5, 0, 2, 0],
    [0, 0, 1, 0, 0, 0, 6, 0, 4],
    [6, 0, 4, 0, 3, 2, 0, 8, 0],
    [0, 6, 0, 0, 0, 0, 1, 9, 0],
    [4, 0, 2, 0, 0, 9, 0, 0, 5],
    [0, 9, 0, 0, 7, 0, 4, 0, 2]
]'''

fields = [
    [0, 7, 0, 0, 2, 0, 9, 0, 0],
    [0, 4, 0, 8, 0, 6, 0, 0, 0],
    [0, 1, 2, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 7, 0],
    [0, 6, 0, 9, 7, 2, 0, 5, 0],
    [0, 2, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 2, 9, 0],
    [0, 0, 0, 5, 0, 4, 0, 3, 0],
    [0, 0, 7, 0, 6, 0, 0, 1, 0]
]

'''fields = [
    [0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 8, 0, 0, 0, 7, 0, 9, 0],
    [6, 0, 2, 0, 0, 0, 5, 0, 0],
    [0, 7, 0, 0, 6, 0, 0, 0, 0],
    [0, 0, 0, 9, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 4, 0],
    [0, 0, 5, 0, 0, 0, 6, 0, 3],
    [0, 9, 0, 4, 0, 0, 0, 7, 0],
    [0, 0, 6, 0, 0, 0, 0, 0, 0]
]'''

for row in fields:
    print(row)

indexes = []
for i in range(9):
    indexes.append([i * 9 + j for j in range(9)])

domain = [i for i in range(1, 10)]

for i in range(9):
    for j in range(9):
        if fields[i][j] != 0:
            problem.add_variable(i * 9 + j, [fields[i][j]])

for i in range(9):
    for j in range(9):
        if fields[i][j] == 0:
            problem.add_variable(i * 9 + j, domain)

for i in range(9):
    problem.add_multiple_constraint(lambda a, b: a != b, [indexes[i][j] for j in range(9)])
# print(problem.multiple_constraints)

for i in range(9):
    problem.add_multiple_constraint(lambda a, b: a != b, [indexes[j][i] for j in range(9)])
# print(problem.multiple_constraints[9::])

squares = [
    [[], [], []],
    [[], [], []],
    [[], [], []]
]
for i in range(9):
    for j in range(9):
        squares[int(i / 3)][int(j / 3)].append(indexes[i][j])
# print(squares)

for row in squares:
    for square in row:
        problem.add_multiple_constraint(lambda a, b: a != b, square)
# print(problem.multiple_constraints[18::])


start = time.time()
problem.solve()
end = time.time()

print(f"czas: {end - start}")
for i in range(9):
    row = []
    for j in range(9):
        for value in problem.solutions[0]:
            if value[0] == i * 9 + j:
                row.append(value[1])
    print(row)
