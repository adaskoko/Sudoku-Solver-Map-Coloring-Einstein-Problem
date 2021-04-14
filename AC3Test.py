from CSP import *

country = ["Norweg", "Anglik", "Duńczyk", "Niemiec", "Szwed"]
color = ["czerwony", "zielony", "biały", "żółty", "niebieski"]
tobacco = ["light", "cygaro", "fajka", "bez filtra", "menthol"]
drink = ["herbata", "mleko", "woda", "piwo", "kawa"]
breed = ["koty", "ptaki", "psy", "konie", "rybki"]

variables = country + color + tobacco + drink + breed
house = [1, 2, 3, 4, 5]

problem = Problem()

for variable in variables:
    problem.add_variable(variable, house[:])

single_constraints = [
    (lambda a: a == 1, "Norweg"),
    (lambda a: a == 3, "mleko")
]

double_constraints = [
    (lambda a, b: a == b, ["Anglik", "czerwony"]),
    (lambda a, b: a - b == -1, ["zielony", "biały"]),
    (lambda a, b: a == b, ["Duńczyk", "herbata"]),
    (lambda a, b: abs(a-b) == 1, ["light", "koty"]),
    (lambda a, b: a == b, ["żółty", "cygaro"]),
    (lambda a, b: a == b, ["Niemiec", "fajka"]),
    (lambda a, b: abs(a-b) == 1, ["light", "woda"]),
    (lambda a, b: a == b, ["bez filtra", "ptaki"]),
    (lambda a, b: a == b, ["Szwed", "psy"]),
    (lambda a, b: abs(a-b) == 1, ["Norweg", "niebieski"]),
    (lambda a, b: abs(a-b) == 1, ["konie", "żółty"]),
    (lambda a, b: a == b, ["menthol", "piwo"]),
    (lambda a, b: a == b, ["zielony", "kawa"])
]

double_arcs = [
    (lambda a, b: a == b, "Anglik", "czerwony"),
    (lambda a, b: a == b, "czerwony", "Anglik"),
    (lambda a, b: a - b == -1, "zielony", "biały"),
    (lambda a, b: a - b == 1, "biały", "zielony"),
    (lambda a, b: a == b, "Duńczyk", "herbata"),
    (lambda a, b: a == b, "herbata", "Duńczyk"),
    (lambda a, b: abs(a-b) == 1, "light", "koty"),
    (lambda a, b: abs(a-b) == 1, "koty", "light"),
    (lambda a, b: a == b, "żółty", "cygaro"),
    (lambda a, b: a == b, "cygaro", "żółty"),
    (lambda a, b: a == b, "Niemiec", "fajka"),
    (lambda a, b: a == b, "fajka", "Niemiec"),
    (lambda a, b: abs(a-b) == 1, "light", "woda"),
    (lambda a, b: abs(a-b) == 1, "woda", "light"),
    (lambda a, b: a == b, "bez filtra", "ptaki"),
    (lambda a, b: a == b, "ptaki", "bez filtra"),
    (lambda a, b: a == b, "Szwed", "psy"),
    (lambda a, b: a == b, "psy", "Szwed"),
    (lambda a, b: abs(a-b) == 1, "Norweg", "niebieski"),
    (lambda a, b: abs(a-b) == 1, "niebieski", "Norweg"),
    (lambda a, b: abs(a-b) == 1, "konie", "żółty"),
    (lambda a, b: abs(a-b) == 1, "żółty", "konie"),
    (lambda a, b: a == b, "menthol", "piwo"),
    (lambda a, b: a == b, "piwo", "menthol"),
    (lambda a, b: a == b, "zielony", "kawa"),
    (lambda a, b: a == b, "kawa", "zielony")
]

multiple_constraints = [
    (lambda a, b: a != b, country),
    (lambda a, b: a != b, color),
    (lambda a, b: a != b, tobacco),
    (lambda a, b: a != b, drink),
    (lambda a, b: a != b, breed),
]


for constraint, domain in single_constraints:
    problem.add_single_constraint(constraint, domain)
    # add arcs
    problem.add_arc(constraint, domain)

for constraint, domain in double_constraints:
    problem.add_double_constraint(constraint, domain)

for constraint, domain in multiple_constraints:
    problem.add_multiple_constraint(constraint, domain)
    # add arcs
    for val1 in domain:
        for val2 in domain:
            if val1 != val2:
                problem.add_arc(constraint, val1, val2)
                problem.add_arc(constraint, val2, val1)

# add arcs
for function, var1, var2 in double_arcs:
    problem.add_arc(function, var1, var2)

problem.ac3()
print(problem.variables)
problem.solve_backtracking()
print(problem.solutions)

for i in range(1, 6):
    print(f"\ndomek {i}:")
    for var in problem.solutions[0]:
        if var[1] == i:
            print(var[0])
