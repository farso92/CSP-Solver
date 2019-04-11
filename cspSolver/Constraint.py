import copy

class Constraint:
    def __init__(self, n):
        self.n = n

    def constAndNeighNotAss(self, assignedId, problem):
        constraint = []
        for c in problem.constraintList:
            if (c.get('index')[0] == assignedId and c.get('index')[1] in problem.notAssigned) or \
                    (c.get('index')[0] == assignedId and problem.variables[c.get('index')[1]].tipo == 'aggiuntiva'):
                constraint.append(c)
        return constraint

    def constAndNeighAss(self, assignedId, problem):
        constraint = []
        for c in problem.constraintList:
            if c.get('index')[0] == assignedId and c.get('index')[1] not in problem.notAssigned:
                constraint.append(c)
        return constraint

    def allConstAndNeigh(self, assignedId, problem):
        constraint = []
        for c in problem.constraintList:
            if c.get('index')[0] == assignedId and c.get('index')[1]:
                constraint.append(c)
        return constraint

    def check(self, assignedValue, nearValue, condition, assignedId, nearId, problem):
        if condition == 'notEqual':
            if self.areEqual(assignedValue, nearValue):
                return True
            else:
                return False
        if condition == 'notEqualDiagDX':
            if self.areEqualDiagDX(assignedValue, nearValue, assignedId, nearId):
                return True
            else:
                return False
        if condition == 'notEqualDiagSX':
            if self.areEqualDiagSX(assignedValue, nearValue, assignedId, nearId):
                return True
            else:
                return False
        if condition == 'position1':
            if self.position1(assignedValue, nearValue, assignedId, nearId):
                return True
            else:
                return False
        if condition == 'position2':
            if self.position2(assignedValue, nearValue, assignedId, nearId):
                return True
            else:
                return False
        if condition == 'minor':
            if self.a_isminor_b(assignedValue, nearValue):
                return False
            else:
                return True

        if condition == 'greater':
            if self.a_isgreater_b(assignedValue, nearValue):
                return False
            else:
                return True

        if condition == 'a_isInVect_b':
            if self.a_isInVect_b(assignedValue, nearValue, assignedId):
                return False
            else:
                return True

    def createAllDiff(self, con, n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    c = {'index': (i, j), 'condition': 'notEqual'}
                    con.append(c)

    def createDiagDX(self, con, n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    c = {'index': (i, j), 'condition': 'notEqualDiagDX'}
                    con.append(c)

    def createDiagSX(self, con, n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    c = {'index': (i, j), 'condition': 'notEqualDiagSX'}
                    con.append(c)

    def createSumRange(self, con, n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    c = {'index': (i, j), 'condition': 'sumRange'}
                    con.append(c)

    def createPosition(self, con, n):
        for i in range(n):
            if i != n - 1 and i != (n / 2) - 1:
                c = {'index': (i, i + 1), 'condition': 'position1'}
                con.append(c)

    def createPosition2(self, con, n):
        for i in range(n):
            if i != 0 and i != (n / 2) + 1:
                c = {'index': (i, i - 1), 'condition': 'position2'}
                con.append(c)

    def areEqual(self, a, b):
        if a is None and b is None:
            return False
        if a != b:
            return False
        return True

    def areEqualDiagDX(self, a, b, a_index, b_index):
        if a is None and b is None:
            return False
        if b != a + abs(a_index - b_index):
            return False
        return True

    def areEqualDiagSX(self, a, b, a_index, b_index):
        if a is None and b is None:
            return False
        if b != a - abs(a_index - b_index):
            return False
        return True

    def position1(self, a, b, a_index, b_index):
        if a is None or b is None:
            return False
        if a <= b and a_index < b_index:
            return False
        return True

    def position2(self, a, b, a_index, b_index):
        if a is None or b is None:
            return False
        if a >= b and a_index > b_index:
            return False
        return True

    def a_isminor_b(self, a, b):
        if a is None or b is None:
            return False
        if a >= b:
            return False
        return True

    def a_isgreater_b(self, a, b):
        if a is None or b is None:
            return False
        if a <= b:
            return False
        return True

    def a_isInVect_b(self, a, b, a_index):
        if a is False or b is False:
            return False
        if b[a_index] != a:
            return False
        return True

    def sumWithOrder(self, i, domainVar, temp, newDomainVar, limit, sommatoria):
        if i < len(domainVar):
            a = len(temp)-1
            for v in domainVar[i]:
                if v not in temp and (a == -1 or (a != -1 and v > temp[a])):
                    temp.append(v)
                    sommatoria += v
                    if sommatoria > limit:
                        sommatoria -= temp[i]
                        temp.pop(i)
                    else:
                        x = copy.deepcopy(self.sumWithOrder(i + 1, domainVar, temp, newDomainVar, limit, sommatoria))
                        if x is not False:
                            newDomainVar.append(x)
                        sommatoria -= temp[i]
                        temp.pop(i)
            return False
        else:
            if sommatoria == limit:
                print('Aggiunto un vincolo di somma')
                return temp
            else:
                return False

    def sumSquaredWithOrder(self, i, domainVar, temp, newDomainVar, limit, sommatoria):
        if i < len(domainVar):
            a = len(temp) - 1
            for v in domainVar[i]:
                if v not in temp and (a == -1 or (a != -1 and v > temp[a])):
                    temp.append(v)
                    sommatoria += v*v
                    if sommatoria > limit:
                        sommatoria -= (temp[i]*temp[i])
                        temp.pop(i)
                    else:
                        x = copy.deepcopy(self.sumSquaredWithOrder(i + 1, domainVar, temp, newDomainVar, limit, sommatoria))
                        if x is not False:
                            newDomainVar.append(x)
                        sommatoria -= (temp[i]*temp[i])
                        temp.pop(i)
            return False
        else:
            if sommatoria == limit:
                print('Aggiunto un vincolo di somma dei quadrati')
                return temp
            else:
                return False

    def fraction(self, i, domainVar, temp, newDomainVar, limit):
        if i < len(domainVar):
            for v in domainVar[i]:
                if v not in temp:
                    temp.append(v)
                    x = copy.deepcopy(self.fraction(i + 1, domainVar, temp, newDomainVar, limit))
                    if x is not False:
                        newDomainVar.append(x)
                    temp.pop(i)
            return False
        else:
            fraction = (temp[0]/((10*temp[1])+temp[2])) + (temp[3]/((10*temp[4])+temp[5])) + \
                       (temp[6]/((10*temp[7])+temp[8]))
            if fraction == limit:
                print('Aggiunto un vincolo di somma dei quadrati')
                return temp
            else:
                return False

    def sumWithoutOrder(self, i, domainVar, temp, newDomainVar, limit, sommatoria):
        if i < len(domainVar):
            for v in domainVar[i]:
                if v not in temp:
                    temp.append(v)
                    sommatoria += v
                    if sommatoria > limit:
                        sommatoria -= temp[i]
                        temp.pop(i)
                    else:
                        x = copy.deepcopy(self.sumWithoutOrder(i + 1, domainVar, temp, newDomainVar,
                                                               limit, sommatoria))
                        if x is not False:
                            newDomainVar.append(x)
                        sommatoria -= temp[i]
                        temp.pop(i)
            return False
        else:
            if sommatoria == limit:
                print('Aggiunto un vincolo di somma')
                return temp
            else:
                return False

    def addBinaryConstraint(self, problem, newDomainVar, c, bigList): #aggiunge un vincolo binario
        vect = []
        for i in range(len((newDomainVar))):
            riga = []
            for r in range(problem.initialDim):
                riga.append(0)
            vect.append(riga)
        indiciRelazione = c.get('index')
        for i in range(len(vect)):
            for r in range(problem.initialDim):
                for indexRel in indiciRelazione:
                    if r == indexRel:
                        v = newDomainVar[i].pop(0)
                        vect[i][r] = v
        print()
        problem.variables[problem.n - 1].domain = vect
        problem.variables[problem.n - 1].newDom = vect
        problem.constraintList.remove(c)
        for index in c.get('index'):
            problem.constraintList.append({'index': (index, problem.n - 1), 'condition': 'a_isInVect_b'})

    def binarization(self, problem, CSP):
        print('crea vincoli binari')
        bigList = list()
        for c in problem.constraintList.copy():
            if len(c.get('index')) > 2:  # per ogni vincolo non binario aggiunge una var
                domainVar = []
                for i in problem.variables:
                    if i.id in c.get('index'):
                        domainVar.append(i.domain)
                problem.n += 1
                problem.variables.append(CSP.Node(problem.n-1))
                problem.variables[problem.n-1].tipo = 'aggiuntiva'
                temp = []
                i = 0
                newDomainVar = []
                if c.get('condition') == 'sumWithOrder':
                    sommatoria = 0
                    self.sumWithOrder(i, domainVar, temp, newDomainVar, problem.somma, sommatoria)
                if c.get('condition') == 'sumSquaredWithOrder':
                    sommatoria = 0
                    self.sumSquaredWithOrder(i, domainVar, temp, newDomainVar, problem.sommaQuad, sommatoria)
                if c.get('condition') == 'fraction':
                    self.fraction(i, domainVar, temp, newDomainVar, 1)
                    finish = False
                if c.get('condition') == 'equazione':
                    self.equazione(i, domainVar, temp, newDomainVar, 1)
                    finish = True
                if c.get('condition') == 'sumWithoutOrder':
                    sommatoria = 0
                    self.sumWithoutOrder(i, domainVar, temp, newDomainVar, problem.somma, sommatoria)
                self.addBinaryConstraint(problem, newDomainVar, c, bigList)
        print('vincoli binari creati')
