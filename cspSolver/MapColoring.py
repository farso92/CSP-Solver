from Constraint import *

class MapColoring:
    def __init__(self):
        self.variables = []
        self.assignement = []
        self.notAssigned = []
        self.storyDom = []
        self.n = 7
        self.constraintList = []
        self.costraintObject = []

    def build_domains(self, id, n, problem):
        domain = list()
        for k in range(3):
            domain.append(k)
        return domain

    def makeConstraint(self, n):
        self.costraintObject = Constraint(n)
        # WA
        self.constraintList.append({'index': (0, 1), 'condition': 'notEqual'})
        self.constraintList.append({'index': (0, 2), 'condition': 'notEqual'})
        # NT
        self.constraintList.append({'index': (1, 0), 'condition': 'notEqual'})
        self.constraintList.append({'index': (1, 2), 'condition': 'notEqual'})
        self.constraintList.append({'index': (1, 3), 'condition': 'notEqual'})
        # SA
        self.constraintList.append({'index': (2, 0), 'condition': 'notEqual'})
        self.constraintList.append({'index': (2, 1), 'condition': 'notEqual'})
        self.constraintList.append({'index': (2, 3), 'condition': 'notEqual'})
        self.constraintList.append({'index': (2, 4), 'condition': 'notEqual'})
        self.constraintList.append({'index': (2, 5), 'condition': 'notEqual'})
        # Q
        self.constraintList.append({'index': (3, 1), 'condition': 'notEqual'})
        self.constraintList.append({'index': (3, 2), 'condition': 'notEqual'})
        self.constraintList.append({'index': (3, 4), 'condition': 'notEqual'})
        # NSW
        self.constraintList.append({'index': (4, 2), 'condition': 'notEqual'})
        self.constraintList.append({'index': (4, 3), 'condition': 'notEqual'})
        self.constraintList.append({'index': (4, 5), 'condition': 'notEqual'})
        # V
        self.constraintList.append({'index': (5, 2), 'condition': 'notEqual'})
        self.constraintList.append({'index': (5, 4), 'condition': 'notEqual'})

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
            a = problem.assignement[i]
            if a is False:
                return False
        for i in range(len(problem.assignement)):
            constraint = problem.costraintObject.allConstAndNeigh(problem.assignement[i], problem)
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
            stateName = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
            for i in range(len(solution)):
                if solution[i] == 0:
                    print(stateName[i], 'red')
                else:
                    if solution[i] == 1:
                        print(stateName[i], 'green')
                    else:
                        print(stateName[i], 'blue')