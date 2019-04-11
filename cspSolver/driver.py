import copy
from timeit import default_timer as timer
from NQueen import NQueen
from MapColoring import MapColoring
from NumberPart import NumberPart
from NFractions import NFractions

possibleProblems = ['nRegine', 'Number Part', 'NFractions', 'MapColoring']


class CSP:
    def __init__(self, tipo):
        self.tipo = tipo
        if self.tipo == 0:
            self.problemObj = NQueen()
        if self.tipo == 1:
            self.problemObj = NumberPart()
        if self.tipo == 2:
            self.problemObj = NFractions()
        if self.tipo == 3:
            self.problemObj = MapColoring()
        self.n = self.problemObj.n
        self.prepare_game(self.n, self.problemObj)

    def prepare_game(self, n, problem):
        temp = []
        for id in range(n):
            problem.variables.append(CSP.Node(id))
            problem.variables[id].domain = problem.build_domains(id, n, problem)  # dominio della variabile
            problem.variables[id].newDom = problem.build_domains(id, n, problem)  # dominio aggiornato di volta in volta
            problem.assignement.append(False)  #  nessuna variabile assegnata
            problem.notAssigned.append(id)    #  valore id perchè inizialmente nessuna var è assegnata
        problem.makeConstraint(n)   # crea i vincoli
        problem.costraintObject.binarization(problem, self)  # controlla se ce ne sono n-ari
        for id in range(problem.n):
            temp.append(problem.variables[id].domain)
        problem.storyDom.append(copy.deepcopy(temp))  # inizializza lo storico

    class Node:
        def __init__(self, id):
            self.id = id
            self.value = None
            self.domain = []
            self.newDom = []
            self.tipo = 'base'


def control(XjDom, XiValue, condition, Xj, Xi, problem):
    inconsistence = False
    for XjValue in XjDom:
        if problem.costraintObject.check(XjValue, XiValue, condition, Xj, Xi, problem):
            inconsistence = True  # XjValue e XiValue non hanno rispettato condition
        else:
            return False  # esiste un XjValue che rispetta condition dato XiValue, non annulla il dominio
    return inconsistence


def revise(problem, Xi, Xj, condition):
    revised = False
    for XiValue in problem.variables[Xi].newDom.copy():
        if control(problem.variables[Xj].newDom, XiValue, condition, Xj, Xi, problem): #se true => c'è inconsistenza
            problem.variables[Xi].newDom.remove(XiValue)
            revised = True
    return revised


def ac3(problem, assignedId): #esegui AC3
    queue = problem.costraintObject.constAndNeighNotAss(assignedId, problem)
    problem.noEmptyList = False
    while queue:
        problem.noEmptyList = True
        temp = queue.pop(0)
        Xi = temp.get('index')[1]
        Xj = temp.get('index')[0]
        condition = temp.get('condition')
        if revise(problem, Xi, Xj, condition):
            if len(problem.variables[Xi].newDom) == 0:
                print('La scelta azzera un dominio')
                return False
            neighbors = problem.costraintObject.constAndNeighNotAss(Xi, problem)
            for n in neighbors:
                queue.append(n)
    return True


def isComplete(problem):
    print('controllo completezza di', problem.assignement, '\n')
    found = problem.checkComplete(problem)
    if found:
        print('trovata la soluzione \n \n')
        return True
    else:
        print('soluzione non trovata \n \n')


def isConsistent(problem, assignedId, assignedValue):
    print('controllo consistenza della scelta sulla variabile', assignedId, 'con valore', assignedValue, ':')
    found = problem.checkConsistent(assignedId, assignedValue, problem)
    return found


def restoreDom(problem, assegnedDom, assignedId):
    v = copy.deepcopy(problem.storyDom[len(problem.storyDom) - 1])
    for i in range(problem.n):
        problem.variables[i].newDom = v[i]
    problem.variables[assignedId].newDom = assegnedDom


def addInferences(problem):
    if problem.noEmptyList:
        bigList = []
        for i in range(problem.n):
            copyList = copy.deepcopy(problem.variables[i].newDom[:])
            bigList.append(copyList)
        problem.storyDom.append(copy.deepcopy(bigList))
        print(problem.storyDom[len(problem.storyDom) - 1], '\n')


def fisrtAssignement(assignement):
    first = False
    for a in assignement:
        if not a or a == 0:
            first = True
    return first


def selectFirstVar(problem):
    count = []
    idList = []
    for i in range(problem.initialDim):
        count.append(0)
        idList.append(i)
        for c in problem.constraintList:
            if i == c.get('index')[0]:
                count[i] += 1
    z = zip(count, idList)
    return z


def selectVar(problem):
    minId = 0
    minDom = len(problem.variables[problem.notAssigned[0]].newDom)
    for i in range(len(problem.notAssigned)):
        if minDom > len(problem.variables[problem.notAssigned[i]].newDom) and \
                problem.variables[problem.notAssigned[i]].tipo == 'base':
            minDom = len(problem.variables[problem.notAssigned[i]].newDom)
            minId = i
    return minId


def orderDomainValue(assignedTempId, problem):
    count = []
    idList = []
    for i in range(len(problem.variables[assignedTempId].newDom)):
        count.append(0)
        idList.append(-1)
    id = -1
    constraintAndNeighbors = problem.costraintObject.constAndNeighNotAss(assignedTempId, problem)
    for assignedTempValue in problem.variables[assignedTempId].newDom.copy():
        id += 1
        idList[id] = id
        problem.assignement[assignedTempId] = assignedTempValue
        for c in constraintAndNeighbors:
            nearTempId = c.get('index')[1]
            for nearTempValue in problem.variables[nearTempId].newDom:
                consistence = problem.costraintObject.check(problem.assignement[assignedTempId], nearTempValue, c.get('condition'), assignedTempId, nearTempId, problem)
                if consistence == False:
                    count[id] += 1
        problem.assignement[assignedTempId] = False
    z = [i for _, i in sorted(zip(count, idList))]
    return z


def addAssignement(assignedId, assignedValue, problem):
    problem.assignement[assignedId] = assignedValue
    assignedDom = problem.variables[assignedId].newDom
    problem.variables[assignedId].newDom = [assignedValue]
    return assignedDom


def backtrack(problem, assignement):
    if isComplete(problem):
        return assignement
    if problem.notAssigned:
        #if not fisrtAssignement(assignement):
        #    z = selectFirstVar(problem)
        #    assignedId = z.pop(0)
        #    problem.notAssigned.pop(assignedId)
        #else:
        assignedId = problem.notAssigned.pop(selectVar(problem))    # assignedId = seleziona una variabile non assegnata
        orderedDomainList = [x for _, x in sorted(zip(orderDomainValue(assignedId, problem),
                                                      problem.variables[assignedId].newDom))]

        for assignedValue in orderedDomainList.copy():
        #for assignedValue in problem.variables[assignedId].newDom.copy():     # for each value in order domain of var
            if isConsistent(problem, assignedId, assignedValue):
                assignedDom = addAssignement(assignedId, assignedValue, problem)
                inferences = ac3(problem, assignedId)
                if inferences:                  # se inferences è true la scelta var= value ha aggiornato un dominio
                    addInferences(problem)
                    result = backtrack(problem, assignement)
                    if result:
                        return result
            result = False                      #  ripristinare i domini
            restoreDom(problem, assignedDom, assignedId)
            assignement[assignedId] = False
        if assignedId not in problem.notAssigned:
            problem.notAssigned.insert(0, assignedId)
        count = len(problem.storyDom)
        del problem.storyDom[count - 1]
        restoreDom(problem, assignedDom, assignedId)
    return False


if __name__ == '__main__':
    for i in range(len(possibleProblems)):
        print('(', i, ')', possibleProblems[i])
    tipo = int(input('\nScegli il tipo di problema:'))
    start = timer()
    problem = CSP(tipo)
    solution = backtrack(problem.problemObj, problem.problemObj.assignement)
    end = timer()
    time = end - start
    problem.problemObj.printSolution(solution, problem.problemObj)
    print('Eseguito in:', time)
    del problem
