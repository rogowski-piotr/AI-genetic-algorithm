import random
import math
import matplotlib.pyplot as plt

tmp_x = 0
x_best_global = []
y_best_global = []


'''
    Represents single solution and one element od all population
'''


class Individual:
    def __init__(self):
        self.chromosomesArray = []
        self.value = None
        self.function_value = None

    def init_rand_chromosom(self):
        for i in range(10):
            self.chromosomesArray.append(random.randint(0, 1))

    def decode_value(self):
        self.chromosomesArray.reverse()
        tmp = 1
        value = 0
        for i in self.chromosomesArray:
            if i == 1:
                value += tmp
            tmp *= 2
        self.chromosomesArray.reverse()
        self.value = value

    def decode_function_value(self):
        self.function_value = pow(self.value, 2) - 10 * math.cos(2 * math.pi * self.value)

    def mutation(self, probability):
        for i in range(len(self.chromosomesArray)):
            if random.randint(0, 100) < probability:
                if self.chromosomesArray[i] == 1:
                    self.chromosomesArray[i] = 0
                else:
                    self.chromosomesArray[i] = 1

    def details(self):
        print(self.chromosomesArray)
        print(self.value)
        print(self.function_value)
        print()


'''
    Represents all population of solutions
'''


class Population:
    def __init__(self):
        self.populationArray = []
        self.best_value = None
        self.best_individual = None

    def population_init(self, size):
        for i in range(size):
            individual = Individual()
            individual.init_rand_chromosom()
            self.populationArray.append(individual)

    def population_rate(self):
        for individual in self.populationArray:
            individual.decode_value()
            individual.decode_function_value()
            if self.best_value is None or self.best_value > individual.function_value:
                self.best_value = individual.function_value
                self.best_individual = individual
        global tmp_x
        tmp_x += 1
        y_best_global.append(self.best_value)
        x_best_global.append(tmp_x)

    def population_rulette_selection(self):
        population_new = []
        sum = 0
        for individual in self.populationArray:
            sum += individual.function_value
        for i in range(len(self.populationArray)):
            random_value = random.randint(0, 100)
            tmp = 0
            for individual in self.populationArray:
                delta = ((sum - individual.function_value) / sum) * 100
                if tmp <= random_value <= tmp + delta:
                    population_new.append(individual)
                tmp += delta
        self.populationArray = population_new

    def population_mutation(self, probability):
        for individual in self.populationArray:
            individual.mutation(probability)

    def population_cross(self):
        length = len(self.populationArray[0].chromosomesArray)
        for index_of_individual in range(0, len(self.populationArray) - 1, 2):
            cut_index = random.randint(0, length - 1)
            for index_of_chromosom in range(0, length):
                if index_of_chromosom < cut_index:
                    tmp = self.populationArray[index_of_individual].chromosomesArray[index_of_chromosom]
                    self.populationArray[index_of_individual].chromosomesArray[index_of_chromosom] = \
                    self.populationArray[index_of_individual + 1].chromosomesArray[index_of_chromosom]
                    self.populationArray[index_of_individual + 1].chromosomesArray[index_of_chromosom] = tmp


# MAIN GA
generations = 50
population_amount = 6
mutation_probability = 10

population = Population()
population.population_init(population_amount)
for gen in range(generations):
    population.population_rate()
    population.population_rulette_selection()
    population.population_cross()
    population.population_mutation(mutation_probability)



# PLOT

plt.plot(x_best_global, y_best_global)

plt.xlabel('generation number')
plt.ylabel('function value')
plt.title('genetic algorithm \n searching for the minimum rastrigine function')
plt.legend()
plt.show()
