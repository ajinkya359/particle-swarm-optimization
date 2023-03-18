#------------------------------------------------------------------------------+
#
#	Nathan A. Rooy
#	Simple Particle Swarm Optimization (PSO) with Python
#	Last update: 2018-JAN-26
#	Python 3.6
#
#------------------------------------------------------------------------------+

#--- IMPORT DEPENDENCIES ------------------------------------------------------+

from random import random
from random import uniform
import numpy as np
import matplotlib.pyplot as plt
import math

#--- MAIN ---------------------------------------------------------------------+
#TODO: Apply the same stopping condition as in other
class Particle:
    def __init__(self, bounds):
        self.position_i=[]          # particle position
        self.velocity_i=[]          # particle velocity
        self.pos_best_i=[]          # best position individual
        self.err_best_i=-1          # best error individual
        self.err_i=100               # error individual
        self.fitness=0
        for i in range(0,num_dimensions):
            self.velocity_i.append(uniform(-1,1))
            self.position_i.append(uniform(bounds[i][0],bounds[i][1]))

    # evaluate current fitness
    def evaluate(self,costFunc,plaintext):
        self.err_i=costFunc(self.position_i,plaintext)
        self.fitness=100-self.err_i
        # check to see if the current position is an individual best
        if self.err_i<self.err_best_i or self.err_best_i==-1:
            self.pos_best_i=self.position_i.copy()
            self.err_best_i=self.err_i
                    
    # update new particle velocity
    def update_velocity(self,pos_best_g,current_gen,max_gen):
        w=1       # constant inertia weight (how much to weigh the previous velocity)
        c1=5        # cognative constant
        c2=10        # social constant
        # kappa=(max_gen-current_gen)/max_gen #[0,1]
        # kappa=0.1 
        # kappa=0.4 
        kappa=0.5
        # kappa=0.1 

        for i in range(0,num_dimensions):
            r1=random()
            r2=random()
            phi1=c1*r1
            phi2=c2*r2
            phi=phi1+phi2
            chi=(2*kappa)/abs(2-phi-math.sqrt(abs(phi*(phi-4))))
            vel_cognitive=c1*r1*(self.pos_best_i[i]-self.position_i[i])
            vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
            self.velocity_i[i]=chi*(w*self.velocity_i[i]+vel_cognitive+vel_social)
            # print("chi" , chi)
    # update the particle position based off new velocity updates
    def update_position(self,bounds):
        for i in range(0,num_dimensions):
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]
            
            # adjust maximum position if necessary
            if self.position_i[i]>bounds[i][1]:
                self.position_i[i]=bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i]<bounds[i][0]:
                self.position_i[i]=bounds[i][0]
        
        
def minimize(costFunc,plaintext, x0, bounds, num_particles, maxiter, verbose=False):
    global num_dimensions

    num_dimensions=len(x0)
    err_best_g=-1                   # best error for group
    pos_best_g=[]                   # best position for group
    # pos_best_g_fitness=0
    # establish the swarm
    swarm=[]
    for i in range(0,num_particles):
        swarm.append(Particle(bounds))

    # begin optimization loop
    i=0
    plt.ion()
    fig, ax = plt.subplots()
    x, y = [],[]
    sc = ax.scatter(x,y,cmap="hsv")
    plt.xlim(bounds[0][0],bounds[0][1])
    plt.ylim(bounds[1][0],bounds[1][1])
    while i<maxiter:
        if verbose: print(f'iter: {i:>4d}, best solution: {err_best_g:10.6f}, fintess: {100-err_best_g:10.6f}')
        temp_fitness=[]
        mmax_fitness=-10000

        for j in range(0,num_particles):
            temp_fitness.append(100-swarm[j].err_i)
            mmax_fitness=max(100-swarm[j].err_i,mmax_fitness)
        # count=temp_fitness.count(mmax_fitness)
        threshold=5
        count=0
        for j in range(0,num_particles):
            if 100-swarm[j].err_i>=100-err_best_g-threshold :
                count+=1
        
        if verbose: print(f'iter: {i:>4d}, best solution: {err_best_g:10.6f}, fintess: {100-err_best_g:10.6f},count: {count}')
        if count/num_particles >=0.5 and 100-err_best_g>=95:
            print('\nFINAL SOLUTION:')
            print(f'   > {pos_best_g}')
            print(f'   > {err_best_g}\n')
            print(f'   > {100-err_best_g}\n')
            return err_best_g, pos_best_g
        
        # for
        # cycle through particles in swarm and evaluate fitness
        for j in range(0,num_particles):
            swarm[j].evaluate(costFunc,plaintext)

            # determine if current particle is the best (globally)
            if swarm[j].err_i<err_best_g or err_best_g==-1:
                pos_best_g=list(swarm[j].position_i)
                err_best_g=float(swarm[j].err_i)
        
        # cycle through swarm and update velocities and position
        x=[]
        y=[]
        for j in range(0,num_particles):
            swarm[j].update_velocity(pos_best_g,i,maxiter)
            swarm[j].update_position(bounds)
            x.append(swarm[j].position_i[0])
            y.append(swarm[j].position_i[1])
        x.append(pos_best_g[0])
        y.append(pos_best_g[1])
        sc.set_offsets(np.c_[x, y])
        color=[0]*num_particles
        color.append(1)
        sc.set_array(color)

        fig.canvas.draw_idle()
        
        plt.pause(0.1)



        i+=1

    # print final results
    if verbose:
        print('\nFINAL SOLUTION:')
        print(f'   > {pos_best_g}')
        print(f'   > {err_best_g}\n')
        print(f'   > {100-err_best_g}\n')

    return err_best_g, pos_best_g

#--- END ----------------------------------------------------------------------+
