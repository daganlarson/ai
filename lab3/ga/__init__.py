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

def uniform_crossover(parent1: Strategy, parent2: Strategy):
    genome1 = ""
    genome2 = ""

    for i in range(243):
        if random.randint(0,1) == 0:
            genome1 += parent1.genome[i]
            genome2 += parent2.genome[i]
        else:
            genome1 += parent2.genome[i]
            genome2 += parent1.genome[i]
    
    return (Strategy(genome1), Strategy(genome2))

class GA():
    def __init__(self, popSize=200, crossover=1, steps=200, generations=500, sessions=100, eltism=0.1):
        self.popSize = popSize
        self.steps = steps
        self.generations = generations
        self.crossover = crossover
        self.sessions = sessions
        self.elitism = eltism

        self.filename = f"output/GAoutput_{str(round(time.time()))[-4:]}.txt"

        self.rw = robby.World(10,10)
        self.rw.graphicsEnabled = False
        self.rw.graphicsOff()

        self.population = [Strategy() for x in range(popSize)]
    
    def sessionFitness(self, s: Strategy):
        self.rw.distributeCans()
        self.rw.goto(0,0)
        fitness = 0
        for i in range(self.steps):
            p = self.rw.getPerceptCode()
            actionIndex = int(s.genome[p])
            action = POSSIBLE_ACTIONS[actionIndex]

            fitness += self.rw.performAction(action)
           
        return fitness
    
    def strategyFitness(self, s: Strategy) -> int:
        totalFitness = 0
        for x in range(self.sessions):
            totalFitness += self.sessionFitness(s)

        return totalFitness/self.sessions
    
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

        #Elitism
        offspring.extend(parents[self.popSize-round(self.elitism*self.popSize):])

        while len(offspring) < self.popSize:
            parent1 = parents[random.randrange(0, len(parents))]
            parent2 = parents[random.randrange(0, len(parents))]

            if random.randint(0,1) < self.crossover:
                offspring1, offspring2 = single_point_crossover(parent1, parent2)
            else:
                offspring1, offspring2 = uniform_crossover(parent1, parent2)

            offspring1.mutate()
            offspring2.mutate()
            offspring.extend([offspring1, offspring2])
        
        assert(len(offspring) == len(self.population))
        self.population = offspring

        avgFitness = sum(f) / len(f)
        return (avgFitness, f[self.popSize - 1], s[self.popSize - 1])
    
    def runGA(self):
        with open(self.filename, "a") as f:
            f.write(f"Population: {self.popSize}\nGenerations: {self.generations}\nSteps: {self.steps}\nSessions: {self.sessions}\nElitism: {self.elitism}\nCrossover: {self.crossover}\n")

        for g in range(self.generations + 1):
            output = self.runGeneration()
            if g % 10 == 0:
                output = (g, output[0], output[1], output[2])
                with open(self.filename, 'a') as f:
                    output = str(output[0]) + " " + str(output[1]) + " " + str(output[2]) + " " + str(output[3].genome) + "\n"
                    f.write(output)

def main():
    rw = robby.World(10, 10)
    with open("bestStrategy.txt", 'r') as f:
        strat = f.readline()

    rw.demo(strat)



if __name__ == "__main__":
    main()