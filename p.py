from pso import pso_simple
import random
from pso.cost_functions import encrypt_cost_function,encrypt


class Agent:

    def __init__(self, length):

        self.params = [random.uniform(1,4),random.uniform(0.1,4)] #(a,d) 
        self.fitness = -1

    def __str__(self):

        return 'Params: ' + str(self.params) + ' Fitness: ' + str(self.fitness)


def init_agents(population, length):
    return [Agent(length) for _ in range(population)]


in_str = None
in_str_len = None
population = 20
generations = 100000

initial=[0,0]
bounds=[(1,4),(0.1,4)]
# bounds=[(1,400),(1,400)]
# plaintext = input("Enter message : ")

plaintext = "Hello there my name is Ajinkya Shinde"
err,pos=pso_simple.minimize(encrypt_cost_function,plaintext, initial, bounds, num_particles=20, maxiter=1000, verbose=True)
print(encrypt(plaintext,pos[0],pos[1]))