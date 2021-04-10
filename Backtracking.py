import random


class Problem:
    def __init__(self):
        self.variables = []

        self.single_constraints = []
        self.double_constraints = []
        self.multiple_constraints = []

        self.solutions = []

    def add_variable(self, variable, domain):
        self.variables.append((variable, domain))

    def add_single_constraint(self, function, variable):
        self.single_constraints.append((function, variable))

    def add_double_constraint(self, function, variables):
        self.double_constraints.append((function, variables))

    def add_multiple_constraint(self, function, variables):
        self.multiple_constraints.append((function, variables))

    def solve(self):
        self.solutions = []
        self._set_next_node([], self._select_next_variable([]))

    def _set_next_node(self, solution, variable):
        # print(solution)
        for value in variable[1]:
            node = (variable[0], value)
            sol = solution[:]

            if self._check_constraints(sol, node):
                sol.append(node)
                if len(sol) == len(self.variables):
                    self.solutions.append(sol)
                else:
                    new_variable = self._select_next_variable(sol)
                    self._set_next_node(sol, new_variable)

    def _check_constraints(self, solution, node):
        for constraint in self.single_constraints:
            if constraint[1] == node[0]:
                if not constraint[0](node[1]):
                    return False

        for constraint in self.double_constraints:
            for second_node in solution:
                if second_node[0] == constraint[1][0] and node[0] == constraint[1][1]:
                    if not constraint[0](second_node[1], node[1]):
                        return False
                elif node[0] == constraint[1][0] and second_node[0] == constraint[1][1]:
                    if not constraint[0](node[1], second_node[1]):
                        return False

        for constraint in self.multiple_constraints:
            for second_node in solution:
                if node[0] in constraint[1] and second_node[0] in constraint[1]:
                    if not constraint[0](node[1], second_node[1]):
                        # print(f"constraint {node} elo {second_node}")
                        return False

        return True

    def _select_next_variable(self, solution):
        '''can_be_chosen = []
        for var in self.variables:
            already_assigned = False
            for node in solution:
                if node[0] == var[0]:
                    already_assigned = True
            if not already_assigned:
                can_be_chosen.append(var)

        return random.choice(can_be_chosen)'''
        return self.variables[len(solution)]
