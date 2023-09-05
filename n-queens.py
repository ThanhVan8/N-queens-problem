import random
import heapq
import time
import tracemalloc

# MIN-CONFLICT heuristic: “the number of ATTACKING pairs of queens”
def conflict(state):
    res = 0         # number of attacking pairs of queens
    n = len(state)  # number of queens
    for i in range(n - 1):
        for j in range(i + 1, n):
            if state[i] == state[j] or (abs(state[i] - state[j]) == j - i): # same row or same diagonal
                res += 1
    return res

# display the board
def drawBoard(state):
    n = len(state)
    for i in range(n):
        for j in range(n):
            if i == state[j]:   
                print('Q', end = ' ')
            else:
                print('*', end = ' ')
        print()

# init a state with random positions of queens
def initState(n):
    state = []
    for _ in range(n):
        a = random.randint(0, n - 1)
        state.append(a)
    return state

# Graph search A*
def A(state):
    n = len(state)  # number of queens
    frontier = [[conflict(state), conflict(state), 0, state]] # f, h (heuristic), g (path-cost), state [f = h + g]
    exploredSet = []
    while True:
        f, h, g, expanded = heapq.heappop(frontier)
        if h == 0:   # goal-test
            return expanded
        exploredSet.append(expanded)
        for i in range(n):
            for j in range(n):
                if expanded[i] != j:    # generate successors
                    successor = expanded.copy()
                    successor[i] = j

                    frontierTemp = [f[3] for f in frontier] # list of states in frontier
                    if successor not in exploredSet and successor not in frontierTemp:
                        heapq.heappush(frontier, [conflict(successor) + g + 1, conflict(successor), g + 1, successor])
                    elif successor in frontierTemp:
                        index = frontierTemp.index(successor)
                        newCost = conflict(successor) + g + 1
                        if(frontier[index][0] > newCost):   # if have a better cost
                            frontier[index][0] = newCost    # update cost
                            heapq.heapify(frontier)         # heapify to maintain heap structure

# Uniform Cost Search
def UCS(state):
    n = len(state)  # number of queens
    frontier = [[0, state]]   # pathCost, state
    exploredSet = []
    while True:
        if not frontier:
            return None
        pathCost, expanded = heapq.heappop(frontier)
        if conflict(expanded) == 0:   # goal-test
            return expanded
        exploredSet.append(expanded)
        # successors = successor(node)

        for i in range(n):
            for j in range(n):
                if expanded[i] != j:    # generate successors
                    successor = expanded.copy()
                    successor[i] = j

                    frontierTemp = [f[1] for f in frontier] # list of states in frontier
                    if successor not in exploredSet and successor not in frontierTemp:
                        heapq.heappush(frontier, [pathCost + 1, successor])
                    elif successor in frontierTemp:
                        index = frontierTemp.index(successor)
                        if(frontier[index][0] > pathCost + 1):  # if have a better cost
                            frontier[index][0] = pathCost + 1   # update cost
                            heapq.heapify(frontier)             # heapify to maintain heap structure

# init a population of n random states
def initPopulation(n):
    res = []
    for _ in range(0, n):
        state = initState(n)
        heapq.heappush(res, [conflict(state), state])
    return res

# crossover 2 parents p1 and p2
def crossover(p1, p2):
    n = len(p1) # number of queens
    pos = random.randint(0, n-2)
    return p1[:pos] + p2[pos:], p2[:pos] + p1[pos:]

# mutate a state with a probability
def mutate(state):
    n = len(state)  # number of queens
    if random.random() < 0.8:
        col = random.randint(0, n-1)
        pos = random.randint(0, n-1)
        state[col] = pos
    return state

# selection 2 parents to reproduce
def selection(population):
    n = len(population[0][1])   # number of queens
    return [random.choice(population[:int(n*5/10)]), random.choice(population[int(n*5/10):])]

# genetic algorithm
def Genetic(population):
    size = len(population) # size of population
    while True:
        flag = heapq.nsmallest(1, population)   # get the best state
        if flag[0][0] == 0:
            return flag[0][1]

        cnt = 0
        while cnt < size:   # generate new population with the size of the initial population
            parents = selection(population)
            c1, c2 = crossover(parents[0][1], parents[1][1])
            childList = [mutate(s) for s in [c1, c2]]

            for child in childList:
                if cnt < size and child not in [s[1] for s in population]:
                    heapq.heappush(population, [conflict(child), child])
                    cnt += 1

        population = heapq.nsmallest(int(size/2), population) + heapq.nlargest(int(size/2), population) # re-select the population
        heapq.heapify(population)

def solution():
    n = int(input("Number of queens: "))
    print("1. UCS")
    print("2. Graph search A*")
    print("3. Genetic algorithm")
    alg = int(input("Algorithm: "))

    state = []  # initial state
    population = []
    res = []    # goal state

    if alg == 1 or alg == 2:
        state = initState(n)
    elif alg == 3:
        population = initPopulation(n)
    
    tracemalloc.start()
    start = time.time()
    if alg == 1:
        res = UCS(state)
    elif alg == 2:
        res = A(state)
    elif alg == 3:
        res = Genetic(population)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    end = time.time()
    
    drawBoard(res)
    print("Running time:", (end-start) * 10**3, "ms")
    print("Memory:", peak / 1024**2, "MB")

solution()