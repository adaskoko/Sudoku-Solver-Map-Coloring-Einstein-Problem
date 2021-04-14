def _select_next_variable(variables):
    '''can_be_chosen = []
    for var in self.variables:
        already_assigned = False
        for node in solution:
            if node[0] == var[0]:
                already_assigned = True
        if not already_assigned:
            can_be_chosen.append(var)

    return random.choice(can_be_chosen)'''
    return variables[0]


class Problem:
    def __init__(self):
        self.variables = []

        self.single_constraints = []
        self.double_constraints = []
        self.multiple_constraints = []

        self.solutions = []

        self.arcs = []

    def add_variable(self, variable, domain):
        self.variables.append((variable, domain))

    def add_single_constraint(self, function, variable):
        self.single_constraints.append((function, variable))

    def add_double_constraint(self, function, variables):
        self.double_constraints.append((function, variables))

    def add_multiple_constraint(self, function, variables):
        self.multiple_constraints.append((function, variables))

    def add_arc(self, function, var1, var2=None):
        self.arcs.append((function, var1, var2))

    def solve_backtracking(self):
        self.solutions = []

        self._set_next_node([], self.variables[:], _select_next_variable(self.variables[:]))

    def ac3(self):
        variables = self.variables[:]
        arcs_queue = self.arcs[:]

        while len(arcs_queue) > 0:
            arc = arcs_queue[0]
            function, var1, var2 = arc

            # single arc
            if var2 is None:
                for variable in variables:
                    if variable[0] == var1:
                        for value in variable[1][:]:
                            if not function(value):
                                variable[1].remove(value)
            # double arc
            else:
                for variable1 in variables:
                    domain_changed = False
                    if variable1[0] == var1:
                        for variable2 in variables:
                            if variable2[0] == var2:
                                for value1 in variable1[1][:]:
                                    value_can_be_used = False
                                    for value2 in variable2[1]:
                                        if function(value1, value2):
                                            value_can_be_used = True
                                    if not value_can_be_used:
                                        variable1[1].remove(value1)
                                        domain_changed = True
                    if domain_changed:
                        for arc in self.arcs:
                            if arc[2] == variable1[0]:
                                arcs_queue.append(arc)
            del arcs_queue[0]

        self.variables = variables

    def _set_next_node(self, solution, variables, variable):
        # print(solution)
        for value in variable[1]:
            node = (variable[0], value)
            sol = solution[:]
            variabs = variables[:]
            variabs.remove(variable)

            # TODO: Forward check tutaj

            if self._check_constraints(sol, node):
                sol.append(node)
                if len(sol) == len(self.variables):
                    self.solutions.append(sol)
                else:
                    new_variable = _select_next_variable(variabs)
                    self._set_next_node(sol, variabs, new_variable)

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

    def solve_forward_check(self):
        pass

    def _set_next_node_forward_check(self, solution, variables, variable):
        # print(solution)
        for value in variable[1]:
            node = (variable[0], value)
            sol = solution[:]
            variabs = variables[:]
            variabs.remove(variable)

            # TODO: Forward check tutaj

            if self._check_constraints(sol, node):
                sol.append(node)
                if len(sol) == len(self.variables):
                    self.solutions.append(sol)
                else:
                    new_variable = _select_next_variable(variabs)
                    self._set_next_node(sol, variabs, new_variable)