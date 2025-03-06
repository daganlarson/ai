import robby 
import random, time

POSSIBLE_ACTIONS = ["MoveNorth", "MoveSouth", "MoveEast", "MoveWest", "StayPut", "PickUpCan", "MoveRandom"]

class Strategy():
    length = 243

    def __init__(self, init=None, mutationRate=0.005):
        if init == None:
            self.genome = ""
            for x in range(0, 243):
                self.genome += str(random.randint(0,6))
        else:
            self.genome = init      

        for char in self.genome:
            if char not in "0123456":
                raise Exception("strategy contains a bad character: '%s'" % char)    
        
        self.mutationRate = mutationRate

    def mutate(self):
        for gene in self.genome:
            if random.uniform(0, 1) < self.mutationRate:
                newGene = random.randint(0, 6)
                while(newGene == gene):
                    newGene = random.randint(0, 6)
                gene = newGene

def single_point_crossover(parent1: Strategy, parent2: Strategy):
    loc = random.randint(0, 242)
    offspring1 = Strategy(parent1.genome[:loc] + parent2.genome[loc:])
    offspring2 = Strategy(parent2.genome[:loc] + parent1.genome[loc:])
    return (offspring1, offspring2)
    
class GA():
    def __init__(self, popSize=200, crossover=1, steps=200, generations=500):
        self.popSize = popSize
        self.population = [Strategy() for x in range(popSize)]
        self.crossover = crossover
        self.steps = steps
        self.generations = generations
        self.rw = robby.World(10,10)
        self.rw.graphicsOff()
    
    def sessionFitness(self, s: Strategy):
        self.rw.distributeCans()
        self.rw.goto(0,0)
        fitness = 0
        for i in range(self.steps):
            p = self.rw.getPerceptCode()
            actionIndex = int(s.genome[p])
            action = POSSIBLE_ACTIONS[actionIndex]

            fitness += self.rw.performAction(action)
            
            # This section checks to see if Robby is going in circles,
            # and speeds up the simulation if a repetitive pattern of
            # behavior is detected. It works reasonably well most of
            # the time, but there is still some room for improvement.
            '''
            if not cycleDetected:
                # skip after having detected a cycle
                time.sleep(PAUSE)
                state = [action, self.robbyRow, self.robbyCol, self._gridContents()]
                if action != "MoveRandom":
                    period = self._checkForCycle(state, history, CYCLE_LIMIT)
                    if period > 0:
                        #print "cycle of period %d detected" % period
                        cycleDetected = True
                        if period == 1:
                            runFastUntil = i + FAST_STEPS/2
                        else:
                            runFastUntil = i + FAST_STEPS
                history.append(state)
            
            elif self.graphicsEnabled and i > runFastUntil:
                # disable graphics after running for FAST_STEPS
                self.graphicsEnabled = False
            if not self.rw.graphicsEnabled:
                self.rw.graphicsEnabled = True
                self.rw._updateGrid()
            '''
            # it's better for the demo method to return None instead of a
            # reward value, so that students will be forced to write their
            # own method to compute a strategy's cumulative reward.
           
        return fitness
    
    def strategyFitness(self, s: Strategy) -> int:
        avgNum = 100
        totalFitness = 0
        for x in range(avgNum):
            totalFitness += self.sessionFitness(s)

        return totalFitness/avgNum
    
    def sortByFitness(self, genomes : list[Strategy]):
        tuples = [(self.strategyFitness(g), g) for g in genomes]
        tuples.sort(key=lambda t: t[0])
        sortedFitnessValues = [f for (f, g) in tuples]
        sortedGenomes = [g for (f, g) in tuples]
        return sortedGenomes, sortedFitnessValues
    
    def runGeneration(self):
        s, f = self.sortByFitness(self.population)
        parents = list[Strategy]()
        # Rank Selection
        for i in range(len(s)):
            if random.randint(0, self.popSize - 1) < i:
                parents.append(s[i])
        
        #Offspring
        offspring = list[Strategy]()
        while len(offspring) < self.popSize:
            parent1 = parents[random.randrange(0, len(parents))]
            parent2 = parents[random.randrange(0, len(parents))]
            offspring1, offspring2 = single_point_crossover(parent1, parent2)
            offspring.extend([offspring1, offspring2])

        for child in offspring:
            child.mutate()
        
        assert(len(offspring) == len(self.population))
        self.population = offspring

        avgFitness = sum(f) / len(f)
        return (avgFitness, f[self.popSize - 1], s[self.popSize - 1])


    def rankSelection(self, strategy, index):
        randint = int(random.randint(0, 199))
        if randint < index:
            print(randint, index, self.popSize)
            return strategy


def main():
    ga = GA(popSize=200)
    for g in range(500):
        output = ga.runGeneration()
        if g % 10 == 0:
            print(g, output[0], output[1], output[2])

if __name__ == "__main__":
    main()



