#pyeasyga functions were used as guidance
#pyeasyga site: https://github.com/remiomosowon/pyeasyga

import random

#List to store each generation's population
current_generation = []

#create individual solution
def create_individual():
    return [random.randint(0, 1) for _ in range(20)]

#create initial population
def create_initial_population(amount):
    for _ in range(amount):
        current_generation.append(create_individual())
    return current_generation

#Evaluates fitness of an individual solution
def fitness(individual):
    fit = 0
    for i in individual:
        if( i == 1):
            fit =fit+1
    return fit

#Finds the average fitness of a generation
def average_fitness(pop):
    fitness_sum = 0
    for i in pop:
        fitness_sum = fitness_sum + fitness(i)
    
    return fitness_sum/len(pop)

#roulette wheel selection
def roulette_selection(pop):
    fitness_sum = 0
    for i in pop:
        fitness_sum =fitness_sum + fitness(i)
    pick = random.randint(0,fitness_sum)
    current = 0
    for i in pop:
        current = current + fitness(i)
        if(current >= pick):
            return i

# crossover function
def crossover(parent1,parent2):
    index = random.randrange(1, len(parent1))
    child_1 = parent1[:index] + parent2[index:]
    child_2 = parent2[:index] + parent1[index:]
    return child_1, child_2

#mutation function
def mutation(individual):
    mutate_index = random.randrange(len(individual))
    individual[mutate_index] = (0, 1)[individual[mutate_index] == 0]


#Creates the next generations population, refrenced pyeasyga's function create_new_population for guidance
def create_new_gen(cross_prob,mutate_prob):
    global current_generation
    new_pop = []

    can_mutate = random.random() < mutate_prob
    can_crossover = random.random() < cross_prob

    while len(new_pop) < len(current_generation):
        parent_1 = roulette_selection(current_generation)
        parent_2 = roulette_selection(current_generation)

        child_1 = parent_1
        child_2 = parent_2

        can_mutate = random.random() < mutate_prob
        can_crossover = random.random() < cross_prob

        if can_crossover:
            child_1, child_2 = crossover(parent_1, parent_2)

        if can_mutate:
            mutation(child_1)
            mutation(child_2)
        
        new_pop.append(child_1)
        if len(new_pop) < 20:
            new_pop.append(child_2)
    current_generation = new_pop
 
    return current_generation

#Finds each fitness of a current generation and then sorts into a list by highest fitness - lowest fitness
#Returns the highest fitness
def best_individual_fitness():
    fitnesses = []
    for i in current_generation:
        fitnesses.append(fitness(i))
    fitnesses.sort(reverse=True)
    best = fitnesses[0]
    return best
    
#GA run loop
def runGA(pop_size, cross_prob, mutate_prob,file):
    gen = 0
    sourceFile = open(file, 'w')
    print("Population size: "+ str(pop_size)+"\n")
    print("Genome Length: 20\n")
    create_initial_population(pop_size)
    print(str(gen)+" "+str(average_fitness(current_generation))+" "+str((best_individual_fitness())), file=sourceFile)
    print("Generation: " +str(gen)+ " Average Fitness: "+ str(average_fitness(current_generation))+" Best fitness: "+str(best_individual_fitness())+"\n")
    for _ in range(50):
        gen = gen+1
        a = create_new_gen(cross_prob,mutate_prob)
        print(str(gen)+" "+str(average_fitness(current_generation))+" "+str((best_individual_fitness())), file=sourceFile)
        print("Generation: " +str(gen)+ " Average Fitness: "+ str(average_fitness(current_generation))+" Best fitness: "+str(best_individual_fitness())+"\n")
        if(best_individual_fitness()==20):
            break
    sourceFile.close()
    print("results saved.")
    print(gen)

runGA(100,.7,.001, "results.txt")