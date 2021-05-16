from CSP import *
from Map import *
import time


problem = Problem()
problem2 = Problem()
problem3 = Problem()

new_map = Map()
new_map.generate_points(13)
new_map.connect_points()

color = [1, 2, 3, 4]

for i in range(len(new_map.points)):
    problem.add_variable(i, color[:])
    problem2.add_variable(i, color[:])
    problem3.add_variable(i, color[:])

for line in new_map.lines:
    problem.add_double_constraint(lambda p1, p2: p1 != p2,
                                  (new_map.points.index(line.point1), new_map.points.index(line.point2)))
    problem2.add_double_constraint(lambda p1, p2: p1 != p2,
                                  (new_map.points.index(line.point1), new_map.points.index(line.point2)))
    problem3.add_double_constraint(lambda p1, p2: p1 != p2,
                                   (new_map.points.index(line.point1), new_map.points.index(line.point2)))

start = time.time()

problem.variable_heuristic = 0
problem.value_heuristic = 0
problem.solve_backtracking()
# print(problem.solutions)

end = time.time()
print(f"czas: {end - start}\nnodes: {problem.nodes_visited}")
print(f"czas pierwsze rozwiązanie: {problem.end_time - problem.start_time}\nnodes: {problem.nodes_to_first_sol}")

start = time.time()

problem2.variable_heuristic = 0
problem2.value_heuristic = 0
problem2.solve_forward_check()
# print(problem.solutions)

end = time.time()
print(f"czas: {end - start}\nnodes: {problem2.nodes_visited}")
print(f"czas pierwsze rozwiązanie: {problem2.end_time - problem2.start_time}\nnodes: {problem2.nodes_to_first_sol}")


start = time.time()

problem3.variable_heuristic = 0
problem3.value_heuristic = 1
problem3.solve_forward_check()
# print(problem.solutions)

end = time.time()
print(f"czas: {end - start}\nnodes: {problem3.nodes_visited}")
print(f"czas pierwsze rozwiązanie: {problem3.end_time - problem3.start_time}\nnodes: {problem3.nodes_to_first_sol}")


solutions = problem.solutions
print(f"Znaleziono {len(solutions)} rozwiązań:")

print(solutions[0])
for key, value in solutions[0]:
    new_map.points[key].color = value

# new_map.draw()
