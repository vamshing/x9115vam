
# coding: utf-8

# In[15]:

import sys
import random
sys.path
sys.path.append('/Users/vamshiguduguntla/Documents/Python-Programs/models/')

from DTLZ1 import *
from DTLZ3 import *
from DTLZ5 import *
from DTLZ7 import *


# In[13]:

class GA:
    
    def __init__(self,model,num_candidates = 100,num_generations = 10,mutation_prob = 0.05):
        self.num_objectives = model.num_objectives
        self.num_decisions = model.num_decisions
        self.num_candidates = num_candidates
        self.num_generations = num_generations
        self.mutation_prob = mutation_prob
        self.lives = 5
        self.frontier = []
        self.frontier_new = []
        self.base_frontier = []
        self.main(model)
        
    def binary_domination(self,x,y):
        """
        Type I comparison
        Returns whether candidate x dominates candidate y (Binary domination)
        """
        x_obj_vec = model.function_value(x)
        y_obj_vec = model.function_value(y)
        
        for i in range(model.num_objectives):
            if x_obj_vec[i] < y_obj_vec[i]:
                return False
        return True
    
    
    def select(self,box):
        """
        Return the candidate which has binary dominated candidates in the box
        """
        fr = []
        for x in box:
            selection = -1
            for y in box:
                if self.binary_domination(x,y):
                    selection = 1
                    break
            if selection == 1:
                fr.append(x)
        return fr
    
    
    def crossover(self,parent_1,parent_2,child):
        """
        Picks a random decision, take all dad's decisions up to that point, take alll mum's decisions after that point
        """
        while True:
            rand_int = random.randint(0,model.num_decisions)
            child.dec = list(np.array(parent_1)[:rand_int])+list(np.array(parent_2)[rand_int:])
            if child.ok():
                return child
        
    def mutate(self,child):
        """
        Picks a candidate, returns the random decisions to create a new candidate
        """
        child.randomstate()
        return child
        
        
    def penalize_lives(self):
        
        """
        Type II comparison
        Compares between current frontier and the previous frontier
        if atleast one is better in the current frontier - dont penalize
        """
        for x in self.frontier_new:
            penalty = -1
            for y in self.frontier:
                if self.binary_domination(x,y):
                    return 5
        return self.lives-1
    
                    
    def main(self,model):
        
        box =  [model.randomstate() for _ in range(self.num_candidates)]
        self.base_frontier = self.select(box)
        self.frontier = self.select(box)
        
        for i in range(self.num_generations):
            newbox = []
            for j in range(self.num_candidates):
                
                child = model
                sample = np.random.randint(0, len(self.frontier), size=2)
                parent_1 = self.frontier[sample[0]]
                parent_2= self.frontier[sample[1]]
                self.crossover(parent_1,parent_2,child)
                if random.random() < self.mutation_prob :
                    self.mutate(child)
                    
                newbox.append(child.dec)
            
            self.frontier_new = []
            self.frontier_new = self.select(newbox)
            self.lives = self.penalize_lives()
            
            if self.lives == 0:
                break
            
            box = newbox
            self.frontier = self.frontier_new
            
            print '### Generation:',i,'No. of lives',self.lives
            
        return self.frontier_new


# In[14]:

model = DTLZ1(2,10)
state = model.randomstate()
GA(model)


# In[ ]:


