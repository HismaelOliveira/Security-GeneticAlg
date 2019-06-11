import utils
import random
import argparse
import GeneticAlg as ga
from datetime import datetime

cidades = 'cidades.csv'
distancia = 'distancia.csv'
pop_size = 500
n_gen = 200
tourn_size = 25
mut_rate = 0.02

genes = utils.get_genes_from(cidades, distancia)
history = ga.run_ga(genes, pop_size, n_gen, tourn_size, mut_rate)

utils.plot(history['cost'][0], history['route'])
