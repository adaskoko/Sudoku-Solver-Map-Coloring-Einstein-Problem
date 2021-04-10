from Backtracking import *
from Map import *


problem = Problem()

new_map = Map()
new_map.generate_points(15)
new_map.connect_points()

color = [1, 2, 3, 4]

for i in range(len(new_map.points)):
    problem.add_variable(i, color)

for line in new_map.lines:
    problem.add_double_constraint(lambda p1, p2: p1 != p2,
                                  (new_map.points.index(line.point1), new_map.points.index(line.point2)))

problem.solve()
solutions = problem.solutions

print(f"Znaleziono {len(solutions)} rozwiązań:")

print(solutions[0])
for key, value in solutions[0]:
    new_map.points[key].color = value

new_map.draw()
