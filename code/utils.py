import GeneticAlg as ga
import pandas as pd

def get_genes_from(fn, dt):
    df = pd.read_csv(fn)
    pt = pd.read_csv(dt)

    genes = [ga.Gene(row['cidades'], row['criminalidade'])
             for _, row in df.iterrows()]

    for a in genes:
        p = pt[pt['origem']==a.name][['destino', 'km']]
        p.index = p['destino']
        p = p['km']
        a.set_dist_table(p.to_dict())

    return genes

def plot(cost, individual):
    print()
    print('-- Security-GA -- Rota ')

    
    for p in individual.genes:
        print(p.name+"  ")
    print()
    print('------------------------')
    print('Numero de mortos: ', individual.deads)
    print('KM: ', individual.km)
    print('------------------------')

def sum(antn, n):
    sum = 0
    for i in range(antn, n):
        sum += i
    return sum

def calculateDeads(antc, days):
    if antc ==5:
        return days*5
    else:
        if antc+days<5:
            return sum(antc,days)
        else:
            d = sum(antc, 5)
            p = antc + days - 5
            d+= p*5
            return d
