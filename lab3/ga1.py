import ga


ga1 = ga.GA(popSize=500, steps=200, generations=150, sessions=100, eltism=0.1, crossover=1)
ga1.runGA()