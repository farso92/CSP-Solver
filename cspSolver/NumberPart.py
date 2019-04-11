from Constraint import *

class NumberPart:
    def __init__(self):
        self.variables = []
        self.assignement = []
        self.notAssigned = []
        self.storyDom = []
        n = 0
        while n == 0 or n < 8 or n % 4 != 0:
            n = int(input('Inserisci la dimensione, deve essere maggiore/uguale a 8 e multiplo di 4 :'))
        self.n = n
        self.initialDim = n
        somma = 0
        sommaQuad = 0
        for i in range(1, self.n+1):
            somma += i
            sommaQuad += (i*i)
        self.somma = int(somma/2)
        self.sommaQuad = int(sommaQuad/2)
        self.constraintList = []
        self.costraintObject = []

    def build_domains(self, id, n, problem):
        domain = list()
        for k in range(n):
            domain.append(k+1)
        return domain

    def makeConstraint(self, n):
        self.costraintObject = Constraint(n)
        self.costraintObject.createAllDiff(self.constraintList, n)
        mid = int((n / 2) - 1)
        a = ()
        b = ()
        for i in range(n):
            if i != mid and i != n-1:
                self.constraintList.append({'index': (i, i+1), 'condition': 'minor'})
                self.constraintList.append({'index': (i+1, i), 'condition': 'greater'})
            if i < mid+1:
                a += (i,)   # prima metà di numeri
            else:
                b += (i,)   # seconda metà di numeri
        self.constraintList.append({'index': a, 'condition': 'sumWithOrder'})
        self.constraintList.append({'index': a, 'condition': 'sumSquaredWithOrder'})
        self.constraintList.append({'index': b, 'condition': 'sumWithOrder'})
        self.constraintList.append({'index': b, 'condition': 'sumSquaredWithOrder'})

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
        somma1 = 0
        somma2 = 0
        sommaQuad1 = 0
        sommaQuad2 = 0
        l = len(problem.assignement)
        for i in range(l):
            if i < l/2:
                somma1 += problem.assignement[i]
                sommaQuad1 += problem.assignement[i]*problem.assignement[i]
            else:
                somma2 += problem.assignement[i]
                sommaQuad2 += problem.assignement[i] * problem.assignement[i]
        if somma1 == problem.somma and somma2 == problem.somma \
                and sommaQuad1 == problem.sommaQuad and sommaQuad2 == problem.sommaQuad:
           return True
        else:
           return False

    def printSolution(self, solution, problem):
        if solution == False:
            print('errore')
        else:
            a = []
            b = []
            for i in range(len(solution)):
                if i < len(solution) / 2:
                    a.append(solution[i])
                else:
                    b.append(solution[i])
            print(sorted(a), sorted(b))
            print('\nSomma = ', problem.somma)
            print('Somma quadrati = ', problem.sommaQuad)
