from Constraint import *

class NQueen:
    def __init__(self):
        self.variables = []
        self.assignement = []
        self.notAssigned = []
        self.storyDom = []
        n = 0
        while n == 0 or n < 4:
            n = int(input('Inserisci la dimensione:'))
        self.n = n
        self.initialDim = n
        self.constraintList = []
        self.costraintObject = []

    def build_domains(self, id, n, problem):
        domain = list()
        for k in range(n):
            domain.append(k)
        return domain

    def makeConstraint(self, n):
        self.costraintObject = Constraint(n)
        self.costraintObject.createAllDiff(self.constraintList, n)
        self.costraintObject.createDiagDX(self.constraintList, n)
        self.costraintObject.createDiagSX(self.constraintList, n)

    def checkConsistent(self, assignedId, assignedValue, problem):
        problem.assignement[assignedId] = assignedValue
        constraint = problem.costraintObject.constAndNeighAss(assignedId, problem)
        for c in constraint:
            nearValue = problem.assignement[c.get('index')[1]]
            if problem.costraintObject.check(assignedValue, nearValue, c.get('condition'), assignedId,
                                             c.get('index')[1], problem):
                problem.assignement[assignedId] = False
                return False
        return True

    def checkComplete(self, problem):
        for i in range(problem.n):
            if problem.assignement[i] is False:
                return False
        for i in range(len(problem.assignement)):
            constraint = problem.costraintObject.allConstAndNeigh(i, problem)
            for c in constraint:
                nearId = c.get('index')[1]
                if problem.costraintObject.check(problem.assignement[i], problem.assignement[nearId],
                                                 c.get('condition'), i, nearId, problem):
                    return False
        return True

    def printSolution(self, solution, problem):
        if solution == False:
            print('errore')
        else:
            out = '+---' * len(solution) + '+\n'
            for q in solution:
                out += ('|   ' * q + '| Q |' + '   |' * (len(solution) - 1 - q) + '\n' + '+---' * len(
                    solution) + '+\n')
            print(out)
        return out