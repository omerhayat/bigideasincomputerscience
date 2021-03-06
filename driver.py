import sys
import os

# #####
# What it is going to be done is taking inputs
# Inputs are n, i, j, numberGeneration
# #####

n = sys.argv[1]
n = int(n)

x = sys.argv[2]
x = int(x)
while (x > n):
    print("X axis cannot bigger than table size.")
    os._exit()

y = sys.argv[3]
y = int(y)
while (y > n):
    print("Y axis cannot bigger than table size.")
    os._exit()

numberOfGenerations = sys.argv[4]
numberOfGenerations = int(numberOfGenerations)

constants = ['RU', 'RD', 'DR', 'DL', 'UR', 'UL', 'LU', 'LD']

#  This variables up to programmer
populationSize = 3000
survivalRatio = 0.5

# delete that later what we are going to is elite would be true
# If elite is true then only the best solutions survive, instead of also some random ones.
# elite = False

# It prints the best solution of every generation
printValues = True

######
# Don't change code below here, unless you really want to :p
######

###############################################################################################

# The maximum number of moves knight do.
maxNumberOfMoves = n * n


# Create a first random population of solutions
def make_population():
    population = []
    for i in range(populationSize):
        population.append(Individual())
    return population

# This function executes one generation of dying solutions and new solutions being born.
def generation(population):
    # Sort the solutions by merit (they've already calculated their own fitness upon being created)
    population.sort(key=lambda x: x.numberOfMoves, reverse=True)

    # Determine the number of solutions allowed to survive from the given survival ratio
    # and how many room that leaves for children.

    survivors = int(len(population) * survivalRatio)

    #bestFromPopulation = population[0:(survivors - 1)]

    bestFromPopulation = []
    for i in range (survivors -1):
        bestFromPopulation.append((population[i]).gene)

    from Reproduction import reproduce
    genomes = reproduce(bestFromPopulation, len(population))
    population = [None] * len(population)

    for i,genome in enumerate(genomes):
        population[i] = Individual(genome)

    return population


# Returns the best solution in a population (sorted or not)
def findbest(population):
    return population[0]


# Class for individual solutions in a population of solutions to a TSP
class Individual:
    # The solutions's genome, a permutation of cities to visit
    gene = list()

    # Create a new solution. If no gene is given, it wil give itself a random one.
    # It immediately computes it's own fitness.
    def __init__(self, gene=None):
        if gene is None:
            self.gene = self.create()
        else:
            if len(gene) != maxNumberOfMoves:
                raise Exception
            self.gene = gene
        self.numberOfMoves = self.evaluate()

    def create(self):
        created_list = list()

        from random import randint
        for i in range(maxNumberOfMoves):
            position = randint(0, (len(constants) - 1))
            created_list.append(constants[position])
            # print(created_list[i])

        return created_list

    def evaluate(self):
        from fitnessfunction import calculateLengthOfPossibleMoves
        numberOfMoves = calculateLengthOfPossibleMoves(self.gene, [x, y], n )
        # that can possible done with that individual

        # numberOfMoves = fitness function will give me the length
        return numberOfMoves


# This method governs the passing of generations, and lets us know what the best solution is every generation.
def run():
    # ind1 = Individual()
    # print (len(ind1.gene))
    if populationSize < 2:
        print("Reproducing solo doesn't work")
        exit()
    population = make_population()
    best = findbest(population)
    from fitnessfunction import possibleMoves
    print("Best solution in population 1: the Length of Possible Moves: " + str(best.numberOfMoves) + ", solution: "
          + str(possibleMoves(best.gene, [x, y], n)))
    for i in range(numberOfGenerations - 1):
        population = generation(population)
        if printValues is True:
            best = findbest(population)
            print("Best solution in population " + str(i + 2) + ": the Length of Possible Moves: " + str(
                best.numberOfMoves) + ", solution: " + str(possibleMoves(best.gene, [x, y], n)))
    return findbest(population)


def main():
    best = run()
    from fitnessfunction import possibleMoves
    print("Best solution found: the Length of Possible Moves: " + str((best.numberOfMoves)) + ", solution: " + str(
            possibleMoves(best.gene, [x, y], n)))

if __name__ == '__main__':
    main()
