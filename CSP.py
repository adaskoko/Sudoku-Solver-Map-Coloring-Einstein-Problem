import time


class Problem:
    def __init__(self):
        self.variables = []

        self.single_constraints = []
        self.double_constraints = []
        self.multiple_constraints = []

        self.solutions = []

        self.arcs = []

        self.variable_heuristic = 0
        self.value_heuristic = 0

        self.nodes_visited = 0
        self.nodes_to_first_sol = 0
        self.start_time = None
        self.end_time = None

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

        self.start_time = time.time()

        self._set_next_node([], self.variables[:],
                            self._select_next_variable(self.variables[:], self.variable_heuristic))

    def solve_forward_check(self):
        self.solutions = []

        self.start_time = time.time()

        variables = self.variables[:]
        for variable in variables:
            for value in variable[1][:]:
                for constraint in self.single_constraints:
                    if constraint[1] == variable[0]:
                        if not constraint[0](value):
                            variable[1].remove(value)

        first_variable = self._select_next_variable(self.variables[:], self.variable_heuristic)

        self._set_next_node_forward_check([], variables, first_variable)

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
        variables.remove(variable)
        for value in self._order_values(variables, variable, self.value_heuristic):
            node = (variable[0], value)
            sol = solution[:]
            variabs = variables[:]
            # variabs.remove(variable)

            self.nodes_visited += 1
            if self.end_time is None:
                self.nodes_to_first_sol += 1

            if self._check_constraints(sol, node):
                sol.append(node)
                if len(sol) == len(self.variables):
                    self.solutions.append(sol)
                    if self.end_time is None:
                        self.end_time = time.time()
                else:
                    new_variable = self._select_next_variable(variabs, self.variable_heuristic)
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
                        return False

        return True

    def _set_next_node_forward_check(self, solution, variables, variable):
        variables.remove(variable)
        for value in self._order_values(variables, variable, self.value_heuristic):
            node = (variable[0], value)
            sol = solution[:]
            variabs = variables[:]
            # variabs.remove(variable)

            self.nodes_visited += 1
            if self.end_time is None:
                self.nodes_to_first_sol += 1

            self._set_domains_forward_check(variables, node)

            sol.append(node)
            if len(sol) == len(self.variables):
                self.solutions.append(sol)
                if self.end_time is None:
                    self.end_time = time.time()

            else:
                new_variable = self._select_next_variable(variabs, self.variable_heuristic)
                self._set_next_node(sol, variabs, new_variable)

    def _set_domains_forward_check(self, variables, node):
        for second_node in variables:
            for value in second_node[1]:
                value_can_be_used = True
                for constraint in self.double_constraints:
                    if second_node[0] == constraint[1][0] and node[0] == constraint[1][1]:
                        if not constraint[0](value, node[1]):
                            value_can_be_used = False
                    elif node[0] == constraint[1][0] and second_node[0] == constraint[1][1]:
                        if not constraint[0](node[1], value):
                            value_can_be_used = False
                if not value_can_be_used:
                    second_node[1].remove(value)

        for second_node in variables:
            for value in second_node[1]:
                value_can_be_used = True
                for constraint in self.multiple_constraints:
                    if node[0] in constraint[1] and second_node[0] in constraint[1]:
                        if not constraint[0](node[1], value):
                            value_can_be_used = False
                if not value_can_be_used:
                    second_node[1].remove(value)

    def _select_next_variable(self, variables, heuristic=0):
        # domyślne wybieranie - kolejnosc dodania zmiennych
        if heuristic == 0:
            return variables[0]

        # najbardziej ograniczona zmienna
        if heuristic == 1:
            index = 0
            length = len(variables[0][1])
            for i in range(len(variables)):
                if len(variables[i][1]) < length:
                    index = i
                    length = len(variables[i][1])
            return variables[index]

        # najbardziej ograniczająca zmienna
        if heuristic == 2:
            index = 0
            constraints = 0
            for i in range(len(variables)):
                var_constraints = 0
                for constr in self.single_constraints:
                    if variables[i][0] == constr[1]:
                        var_constraints += 1
                for constr in self.double_constraints:
                    if variables[i][0] in constr[1]:
                        var_constraints += 1
                for constr in self.multiple_constraints:
                    if variables[i][0] in constr[1]:
                        var_constraints += 1

                if var_constraints > constraints:
                    constraints = var_constraints
                    index = i

            return variables[index]

    def _order_values(self, variables, variable, heuristic):
        # domyślne wybieranie - kolejnosc dodania wartości
        if heuristic == 0:
            return variable[1]

        # najmniej ograniczająca wartość
        if heuristic == 1:
            values = []
            for value in variable[1]:
                constrs = 0
                for constr in self.single_constraints:
                    if variable[0] == constr[1]:
                        if not constr[0](value):
                            constrs += 1

                for constr in self.double_constraints:
                    if variable[0] == constr[1][0]:
                        for variable2 in variables:
                            if variable2[0] == constr[1][1]:
                                for value2 in variable2[1]:
                                    if not constr[0](value, value2):
                                        constrs += 1
                    elif variable[0] == constr[1][1]:
                        for variable2 in variables:
                            if variable2[0] == constr[1][0]:
                                for value2 in variable2[1]:
                                    if not constr[0](value2, value):
                                        constrs += 1

                for constr in self.multiple_constraints:
                    if variable[0] in constr[1]:
                        for variable2 in variables:
                            if variable2[0] in constr[1]:
                                for value2 in variable2[1]:
                                    if not constr[0](value, value2):
                                        constrs += 1
                values.append((value, constrs))

            values = sorted(values, key=lambda a: a[1])
            result = []
            for val, num in values:
                result.append(val)
            return result
