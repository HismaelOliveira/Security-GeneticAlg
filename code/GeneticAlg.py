from sys import maxsize
from time import time
from math import ceil
from random import random, randint, sample
import utils

class Gene: #Cada cidade é descrita como um gene e possui um nome, índice de criminalidade e uma matriz de distância para outras cidades
    def __init__(self, name, crim):
        self.name = name
        self.crim = crim
        self._distance_table = {}

    def set_dist_table(self, dist_table):
        self._distance_table = dist_table

    def get_distance_to(self, dest):
        return self._distance_table[dest.name]

    def set_crim(self, days): #Feita a alteração do índice de criminalidade
        crim = self.crim + days
        if crim<5:
            self.crim = crim
        else:
            self.crim = 5

class Individual: #Um índividuo pe uma rota completa entre todas as cidades
    def __init__(self, genes):
        assert(len(genes)>3)
        self.genes = genes
        self.deads = 0
        self.km = 0
        self.__reset_params()

    def __reset_params(self):
        self.__travel_cost = 0.0
        self.__fitness = 0.0
        self.deads = 0
        self.km = 0

    def swap(self, gene1, gene2):
        self.genes[0]
        a, b, = self.genes.index(gene1), self.genes.index(gene2)
        self.genes[b], self.genes[a] = self.genes[a], self.genes[b]
        self.__reset_params()

    def add(self, gene):
        self.genes.append(gene)
        self.__reset_params()

    @property
    def fitness(self): #A função fitness é expressa como: 1/((distancia)*0.3 + (numMortos)*0.7). Escolhemos essa função por ser normalizada e segundo o estado da arte, obter bons resultados
        if self.__fitness == 0.0:
            self.__fitness =1/ self.travel_cost
        return self.__fitness

    @property
    def travel_cost(self):
        if self.__travel_cost == 0:
            deads = 0
            deadsAnt = 0
            for i in range(len(self.genes)):
                origin = self.genes[i]
                days = ceil(origin.crim/3)
                if i==len(self.genes) -1:
                    self.__travel_cost += ((deads-deadsAnt)*0.6)
                else:
                    #Calcular a quantidade de mortos para as proximas cidades
                    for j in range(i+1, len(self.genes)):
                        auxg = self.genes[j]
                        antc = auxg.crim
                        auxg.set_crim(days+1)
                        deads += utils.calculateDeads(antc, days)
                    dest = self.genes[i+1]
                    self.__travel_cost += (origin.get_distance_to(dest)*0.3 + (deads-deadsAnt)*0.7)
                    self.km += origin.get_distance_to(dest)
                    deadsAnt= deads
            self.deads = deads
        return self.__travel_cost

class Population:
    def __init__(self, individuals):
        self.individuals = individuals

    @staticmethod
    def gen_individuals(sz, genes):
        individuals = []
        for _ in range(sz):
            individuals.append(Individual(sample(genes, len(genes))))
        return Population(individuals)

    def add(self, route):
        self.individuals.append(route)

    def rmv(self, route):
        self.individuals.remove(route)

    #Retornar a melhor individuo a população
    def get_fittest(self):
        fittest = self.individuals[0]
        for route in self.individuals:
            if route.fitness > fittest.fitness:
                fittest = route
        return fittest

#METODOS DO ALGORITMO GENÉTICO

def evolve(pop, tourn_size, mut_rate):
    new_generation = Population([])
    pop_size = len(pop.individuals)
    elitism_num = pop_size//2

    for _ in range(elitism_num):
        fittest = pop.get_fittest()
        new_generation.add(fittest)
        pop.rmv(fittest)

    for _ in range(elitism_num, pop_size):
        parent1 = selection(new_generation, tourn_size)
        parent2 = selection(new_generation, tourn_size)
        child = crossover(parent1, parent2)
        new_generation.add(child)

    for i in range(elitism_num, pop_size):
        mutate(new_generation.individuals[i], mut_rate)

    return new_generation

def crossover(parent1, parent2):
    def fill_with_parent1_genes(child, parent, genes_n):
        start_at = randint(0, len(parent.genes)-genes_n-1)
        finish_at = start_at + genes_n
        for i in range(start_at, finish_at):
            child.genes[i] = parent1.genes[i]

    def fill_with_parent2_genes(child, parent):
        j = 0
        for i in range(0, len(parent.genes)):
            if child.genes[i] == None:
                while parent.genes[j] in child.genes:
                    j += 1
                child.genes[i] = parent.genes[j]
                j += 1

    genes_n = len(parent1.genes)
    child = Individual([None for _ in range(genes_n)])
    fill_with_parent1_genes(child, parent1, genes_n // 2)
    fill_with_parent2_genes(child, parent2)

    return child

def mutate(individual, rate):
    for _ in range(len(individual.genes)):
        if random() < rate:
            sel_genes = sample(individual.genes, 2)
            individual.swap(sel_genes[0], sel_genes[1])

def selection(population, competitors_n):
    return Population(sample(population.individuals, competitors_n)).get_fittest()

def run_ga(genes, pop_size, n_gen, tourn_size, mut_rate):
    population = Population.gen_individuals(pop_size, genes)
    history = {'cost': [population.get_fittest().travel_cost]}
    counter, generations, min_cost = 0, 0, maxsize

    print("-- Security-GA -- Inicializando Evolução...")
    start_time = time()
    while generations < n_gen:
        population = evolve(population, tourn_size, mut_rate)
        cost = population.get_fittest().travel_cost

        if cost < min_cost:
            counter, min_cost = 0, cost
        else:
            counter += 1

        generations += 1
        history['cost'].append(cost)

    total_time = round(time() - start_time, 6)
    print("-- Security-GA -- Evolução finalizada após {} gerações em {} s".format(generations, total_time))
    #print("-- Security-GA -- Custo Mínimo {} ".format(min_cost))

    history['generations'] = generations
    history['total_time'] = total_time
    history['route'] = population.get_fittest()

    return history
