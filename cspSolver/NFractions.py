from Constraint import *

class NFractions:
    def __init__(self):
        self.variables = []
        self.assignement = []
        self.notAssigned = []
        self.storyDom = []
        self.n = 9
        self.initialDim = 9
        self.constraintList = []
        self.costraintObject = []

    def build_domains(self, id, n, problem):
        domain = list()
        for k in range(n):
            domain.append(k + 1)
        return domain

    def makeConstraint(self, n):
        self.costraintObject = Constraint(n)
        self.costraintObject.createAllDiff(self.constraintList, n)
        self.constraintList.append({'index': (0, 1, 2, 3, 4, 5, 6, 7, 8), 'condition': 'fraction'})

    def checkConsistent(self, assignedId, assignedValue, problem):
        problem.assignement[assignedId] = assignedValue
        constraint = problem.costraintObject.constAndNeighAss(assignedId, problem)
        for c in constraint:
            if c.get('index')[1] < len(problem.assignement):
                nearValue = problem.assignement[c.get('index')[1]]
                if problem.costraintObject.check(assignedValue, nearValue, c.get('condition'), assignedId,
                                                 c.get('index')[1], problem):
                    problem.assignement[assignedId] = False
                    return False
        return True

    def checkComplete(self, problem):
        for i in range(problem.initialDim):
            for j in range(problem.initialDim):
                if i != j:
                    if problem.assignement[i] != problem.assignement[j] and problem.assignement[j] is not False:
                        found = True
                    else:
                        return False
        add1 = problem.assignement[0] * (10 * problem.assignement[4] + problem.assignement[5]) * (
                    10 * problem.assignement[7] + problem.assignement[8])
        add2 = problem.assignement[3] * (10 * problem.assignement[1] + problem.assignement[2]) * (
                    10 * problem.assignement[7] + problem.assignement[8])
        add3 = problem.assignement[6] * (10 * problem.assignement[1] + problem.assignement[2]) * (
                    10 * problem.assignement[4] + problem.assignement[5])
        sum = (10 * problem.assignement[1] + problem.assignement[2]) * (
                    10 * problem.assignement[4] + problem.assignement[5]) * (
                          10 * problem.assignement[7] + problem.assignement[8])
        if add1 + add2 + add3 == sum:
            return found
        else:
            return False

    def printSolution(self, solution, problem):
        if solution == False:
            print('errore')
        else:
            for i in range(len(solution)):
                print('Variabile:', i, 'valore', solution[i])
            print(
                "(" + str(solution[0]) + " / " + str(solution[1]) + str(solution[2]) + ") + " + \
                "(" + str(solution[3]) + " / " + str(solution[4]) + str(solution[5]) + ") + " + \
                "(" + str(solution[6]) + " / " + str(solution[7]) + str(solution[8]) + ") = 1")
            print()