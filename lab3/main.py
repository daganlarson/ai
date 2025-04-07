import robby

def main():
    rw = robby.World(10, 10)
    with open("bestStrategy.txt", 'r') as f:
        strat = f.readline()

    rw.demo(strat)



if __name__ == "__main__":
    main()