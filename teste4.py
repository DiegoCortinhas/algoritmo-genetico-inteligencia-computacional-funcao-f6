from numpy.random import rand, randint
import numpy as np
import matplotlib.pyplot as plt
import math
from random import choices
import sys
from decimal import Decimal

# Parametros de entrada do GA
bounds = [[-100, 100], [-100, 100]]
iteration = 40
half_genome = 22
bits = 44  #numero de bits do Genoma
pop_size = 100
crossover_rate = 0.65
mutation_rate = 0.08
genome = []

def function_f6(I):
    x = I[0]
    y = I[1]
    x_y_pow = float(x ** 2 + y ** 2)
    square_of_pow = math.sqrt(x_y_pow)
    sin_pow = (math.sin(square_of_pow) ** 2)
    fraction = (((sin_pow) - (0.5))) / (((1 + (float(0.001) * (x_y_pow)))) ** 2)
    result = (0.5) - fraction
    return result

# -----------------------------------------------------------------------------------------------#

def mutation(pop, mutation_rate):
    _,pop_bin = pop[0],pop[1]
    #print(pop_bin)
    #sys.exit()
    offspringX = list()
    offspringY = list()
    population_mutaded = []
    for i in range(len(pop_bin)):
        p1x = pop_bin[i]['x'] #parent X
        p1y = pop_bin[i]['y'] #parent y
        c1x = meio_mutation(p1x,mutation_rate,offspringX)
        c1y = meio_mutation(p1y,mutation_rate,offspringY)
        individual_bit_mutaded = {
            "x": c1x[0],
            "y": c1y[0]
        }
        population_mutaded.append(individual_bit_mutaded)
    #print(population_mutaded)

    return population_mutaded

def meio_mutation(p1,mutation_rate,offspring):
    if rand() < mutation_rate:
        cp = randint(0, len(p1))  # gera gene aleatorio
        c1 = p1
        c = list(c1)

        if c[cp] == "1":
            c[cp] = "0"  # flip
        else:
            c[cp] = "1"
        c_aux = ''.join([str(elem) for elem in c])
        offspring.append(c_aux)
    else:
        offspring.append(p1)
    return offspring

def crossover(pop_bin, crossover_rate):

    offspring = []
    for i in range(len(pop_bin)-1):
        p1x = pop_bin[i]['x']  # parent 1
        p2x = pop_bin[i+1]['x']  # parent 2
        p1y = pop_bin[i]['y']  # parent 1
        p2y = pop_bin[i+1]['y']  # parent 2
        rand_variable = rand()
        if rand_variable < crossover_rate:
            #print("aleatorio",rand_variable)
            cp = randint(1,len(pop_bin)-1,size=2)
            #print(cp)

            while cp[0] == cp[1]:
                cp = randint(1,len(pop_bin)-1,size=2)
            cp = sorted(cp)
            c1 = p1x[:cp[0]] + p2x[cp[0]:cp[1]] + p1x[cp[1]:]
            c2 = p2y[:cp[0]] + p1y[cp[0]:cp[1]] + p2y[cp[1]:]
            c = {
                'x': c1,
                'y': c2
            }
            offspring.append(c)
            '''
            if i == len(pop_bin) - 2:
                offspring.append(c2)
            '''
        else:
            c1 = {
                'x':p1x,
                'y':p1y
            }

            c2 = {
                'x':p2x,
                'y':p2y
            }
            offspring.append(c1)

        if i == len(pop_bin) - 2:
            offspring.append(c2)




    print(pop_bin,"teste")
    print(offspring,"offspring")
    sys.exit()
    return offspring


# Seleção do metodo da roleta
def selection(pop, fitness, pop_size):
    _, pop_bin = pop[0], pop[1]
    next_generation = list()
    elite = np.argmax(fitness)


    next_generation.append(pop_bin[elite])     #mantem o melhor
    P = [f/sum(fitness) for f in fitness]  #seleção da prob
    index = list(range(int(len(pop_bin))))
    index_selected = np.random.choice(index,size=pop_size-1,replace=False,p=P)
    s=0
    for j in range(pop_size-1):
        next_generation.append(pop_bin[index_selected[s]])
        s+=1
    return next_generation

#Cria a população de 44bits para real
def inicializa_pop(bounds,bits,genome):
    lower_x_boundary, upper_x_boundary = bounds[0]
    lower_y_boundary, upper_y_boundary = bounds[1]
    half_genome = bits/2
    population = []
    population_bit = []

    for i in range(pop_size):
        cromossomox = ""
        cromossomoy = ""

        for j in range(len(genome)):
            if j < half_genome:
                cromossomox += str(genome[j])

            else:
                cromossomoy += str(genome[j])

        individual_bit = {
            "x": cromossomox,
            "y": cromossomoy
        }
        if cromossomox != '' and cromossomoy != '':
            b = int(cromossomox,2)
            cromossomox_float = float(b)
            c = (int(cromossomoy, 2))
            cromossomoy_float = float(c)
            if type(cromossomox_float) == float and type(cromossomoy_float) == float:
                cromossomox_decimal = cromossomox_float * float((upper_x_boundary - lower_x_boundary) / (pow(2, half_genome) - 1)) + float(lower_x_boundary)
                cromossomoy_decimal = cromossomoy_float * float((upper_y_boundary - lower_y_boundary) / (pow(2, half_genome) - 1)) + float(lower_y_boundary)
                individual = {
                    "x": cromossomox_decimal,
                    "y": cromossomoy_decimal
                }
                population.append(individual)
                population_bit.append(individual_bit)

                genome = generate_genome(bits)
            else:
                break

    return population,population_bit


def generate_genome(length: int):
    choices_selected = choices([0, 1], k=length)
    return choices_selected

# ---------------------------------Programa Principal-----------------------------------------------#

genome = generate_genome(bits)
pop_real,pop_bin = inicializa_pop(bounds,bits,genome)
#print(pop_bin,"teste")
#sys.exit()

best_fitness = []
for gen in range(iteration):

    offspring = crossover(pop_bin, crossover_rate)
    offspring = mutation(offspring, mutation_rate)

    for p in offspring:
        pop_bin.append(p)
    print(pop_bin)
    sys.exit()

    real_chromossome = [inicializa_pop(bounds,bits,p) for p in pop_bin]

    for d in real_chromossome:
        fitness = function_f6(d)   #fitness value

    index = np.argmax(fitness)
    current_best = pop_bin[gen]
    best_fitness.append(1/max(fitness)-1)
    pop_bin = selection(pop_bin,fitness,pop_size)


# ---------------------------------Gerando os Gráficos-----------------------------------------------#

#Falta Acertar o grafico para fazer a media dos experimentos

fig = plt.figure()
plt.plot(best_fitness)
fig.subtitle('Evolução')
plt.xlabel('Iteração')
plt.ylabel('Function F6 Values')
print("Solução Otima",inicializa_pop(bounds,bits,current_best))