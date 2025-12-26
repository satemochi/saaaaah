from ortools.sat.python import cp_model


def enumerate_solutions():
    model = cp_model.CpModel()

    # 1. Define Variables
    x1 = model.NewIntVar(0, 10, 'x1')
    x2 = model.NewIntVar(0, 10, 'x2')
    x3 = model.NewIntVar(0, 10, 'x3')
    x4 = model.NewIntVar(0, 10, 'x4')

    # 2. Define Equation: 2x + 3y - z = 5
    model.Add(27*x1 + 17*x2 - 64*x3 + x4 == 203)

    # 3. Callback to print solutions
    class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self, variables):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._variables = variables
            self._solution_count = 0

        def on_solution_callback(self):
            self._solution_count += 1
            _x1 = self.Value(self._variables[0])
            _x2 = self.Value(self._variables[1])
            _x3 = self.Value(self._variables[2])
            _x4 = self.Value(self._variables[3])
            print(f'${self._solution_count}$ & '
                  f'${_x1}$ & ${_x2}$ & ${_x3}$ & ${_x4}$ &'
                  f' ${_x1 + 4*_x2 + _x3 + _x4}$ \\\\')

    # 4. Search for all solutions
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([x1, x2, x3, x4])
    solver.SearchForAllSolutions(model, solution_printer)

print(r'\begin{tabular}{c|rrrr|c}')
print(r'\# & $x_1$ & $x_2$ & $x_3$ & $x_4$ & $x_1 + 4x_2 + x_3 + x_4$ \\')
print(r'\hline')
enumerate_solutions()
print(r'\hline')
print(r'\end{tabular}')
