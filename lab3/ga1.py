import ga


ga1 = ga.GA(popSize=200, steps=200, generations=500, sessions=100, eltism=0, crossover=1)
ga1.runGA()

