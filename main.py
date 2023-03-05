import random


def chromosome_generator(size):  # generate random chromosome
    return [random.randint(1, size) for _ in range(size)]


def reproduce(c1, c2):  # perform cross_over between two given chromosomes
    n = len(c1)
    c = random.randint(0, n - 1)
    return c1[0:c] + c2[c:n]


def mutation(c1):  # mutate the indexes of a chromosome
    n = len(c1)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    c1[c] = m
    return c1


def fitness_function(chromosomes):  # finds the fitness of given chromosome
    horizontal_Collision = sum([chromosomes.count(queen) - 1 for queen in chromosomes]) / 2

    n = len(chromosomes)
    l_diagonal = [0] * 2 * n
    r_diagonal = [0] * 2 * n
    for i in range(n):
        l_diagonal[i + chromosomes[i] - 1] += 1
        r_diagonal[len(chromosomes) - i + chromosomes[i] - 2] += 1

    diagonal_Collision = 0
    for i in range(2 * n - 1):
        counter = 0
        if l_diagonal[i] > 1:
            counter += l_diagonal[i] - 1
        if r_diagonal[i] > 1:
            counter += r_diagonal[i] - 1
        diagonal_Collision += counter / (n - abs(i - n + 1))

    return int(max_fitness - (horizontal_Collision + diagonal_Collision))


def probability_function(chromosome, fitness):  # finds the probability of a given chromosome with the fitness
    return fitness(chromosome) / max_fitness


def randomly_pick_choromosome(pop, probab):  # return the best chromosome form the given population
    popWithProbab = zip(pop, probab)
    total = sum(w for c, w in popWithProbab)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(pop, probab):
        if upto + w >= r:
            return c
        upto += w
    assert False, "not found!"


def Genetic_Queen(pop, fitness):
    default_mutation_probability = 0.03
    new_pop = []
    probab = [probability_function(n, fitness) for n in pop]
    for i in range(len(pop)):
        best1 = randomly_pick_choromosome(pop, probab)  # getting 1st best chromosome
        best2 = randomly_pick_choromosome(pop, probab)  # getting sec best chromosome
        child = reproduce(best1, best2)  # generating two new Chromosomes from the above best 2 chromosomes
        if random.random() < default_mutation_probability:
            child = mutation(child)
        Display_Chromosome(child)
        new_pop.append(child)
        if fitness(child) == max_fitness: break
    return new_pop


def Display_Board(board):
    for row in board:
        print(" ".join(row))


def Display_Chromosome(chrom):
    print("Chromosome = {},  Chromosome_Fitness = {}"
          .format(str(chrom), fitness_function(chrom)))


if __name__ == "__main__":
    n_queue = int(input("Enter number of queens: "))  # input from user
    max_fitness = int((n_queue * (n_queue - 1)) / 2)  # find max fitness
    print("Max Chromosome Fitness: ", max_fitness)
    pop = [chromosome_generator(n_queue) for _ in range(50)]  # generate pop of size 50
    generation = 1  # generation is set to 1

    while not max_fitness in [fitness_function(chrom) for chrom in pop]:
        print("<===> Generation {} <===>".format(generation))
        pop = Genetic_Queen(pop, fitness_function)
        print("\nMaximum Fitness = ", format(max([fitness_function(n) for n in pop])))
        generation += 1
    chrom_out = []
    print("solution found in Generation ", format(generation - 1))
    for chrom in pop:
        if fitness_function(chrom) == max_fitness:
            print("")
            print("One of the best solutions: ")
            chrom_out = chrom
            Display_Chromosome(chrom)

    board = []

    for x in range(n_queue):
        board.append(["x"] * n_queue)

    for i in range(n_queue):
        board[n_queue - chrom_out[i]][i] = "Q"

    print()
    Display_Board(board)
