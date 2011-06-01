import random
import math
from termcolor import colored

DEBUG = True

def log(value, color = None):
   """
   output only if DEBUG
   """
   if color == None: color = "cyan"
   if DEBUG:
      print colored(value, color)

def output(value, color = None):
   """
   output always
   """
   if color == None: color = "cyan"
   print colored(value, color)

#########################################################################################################

class SelfOrganisingMap:
   
   dimensions = []

   def __init__(self, dimensions, input_vector_length, kohonen_neurons = None, learning_rate = None):
      """
      Initializes SOM with learning_rate
      """
      print colored("initializing SOM", "green");

      if learning_rate == None:
         self.learning_rate = random.uniform(0.01, 0.2)
      else:
         self.learning_rate = learning_rate
     
      print colored("learning rate {0}", "green").format(self.learning_rate)

      self.kohonen_neurons = []

      # or if you supplied a tuple with weights
      if kohonen_neurons != None and isinstance(kohonen_neurons, (list, tuple)):
         try:
            for k_n in kohonen_neurons:
               self.kohonen_neurons.append(Neuron(dimensions, k_n))
         except:
            print colored("invalid kohonen_neurons variable {} supplied!", "red").format(kohonen_neurons)

      # you could've supplied just a number of neurons
      else:
          for k_n in range(input_vector_length):
            self.kohonen_neurons.append(Neuron(dimensions))

   def activate(self, input_vector):
      """
      activates SOM
      """

      self.input_vector = input_vector
      print colored("input vector {0}", "blue").format(self.input_vector)

      euclidean = {} 
      for kv in self.kohonen_neurons:
         euclidean[kv.euclidean_distance(self.input_vector)] = kv

      win = min(euclidean.keys());

      log("and the winner is: {0}".format(win))

      winner = euclidean[win]
      winner.learn(self.learning_rate, self.input_vector)

   def weight_vectors(self):
      result = [kn.weight for kn in self.kohonen_neurons]
      return result
         

#########################################################################################################

class Neuron:

   def __init__(self, dimension, weight = None):
      """
      Initializes a new neuron with weight vector
      """
      print colored("initializing neuron", "green");

      self.weight = []

      if weight == None:
         for d in dimension:
            self.weight.append(random.uniform(0, d))
      else:
         self.weight = weight

      print colored("neuron weight vector : {0}", "blue").format(self.weight)

   def euclidean_distance(self, vector):
      """
      calculates the euclidian distance between vector and the weight vector of the neuron
      """
      if(len(vector) != len(self.weight)):
         raise SOMError("input {0} and weight {1} vector dimension mismatch".format(len(vector), len(self.weight))) 

      result = 0
      for i, xi in enumerate(vector):
         result = result + (xi - self.weight[i])**2
      
      log("euclidean before sqrt = {0}".format(result), "cyan")

      result = math.sqrt(result)
      
      log("euclidean = {0}".format(result), "cyan") 
      
      return result

   def learn(self, learning_rate, vector):
      """
      implements the standard competitive learning rule
      """
      if(len(vector) != len(self.weight)):
         raise SOMError("input {0} and weight {1} vector dimension mismatch".format(len(vector), len(self.weight))) 
      
      delta_weight = [learning_rate * (xi - self.weight[i]) for i, xi in enumerate(vector)]
      
      log("delta weights = {0}".format(delta_weight), "magenta")

      self.weight = [wi + delta_weight[i] for i, wi in enumerate(self.weight)]
         
      log("weights after learning = {0}".format(self.weight), "magenta")


#########################################################################################################

class SOMError(Exception):
   def __init__(self, value):
      self.value = value
   def __str__(self):
      return repr(self.value)


