import random
import math
from tools import Logger

#########################################################################################################

class SelfOrganisingMap(Logger):

   debug = False

   def __init__(self, dimensions, input_vector_length, kohonen_neurons = None, learning_rate = None):
      """
      Initializes SOM with learning_rate
      """
      self.output("initializing SOM", "green")

      self.dimensions = dimensions

      if learning_rate == None:
         self.learning_rate = random.uniform(0.01, 0.2)
      else:
         self.learning_rate = learning_rate
     
      self.output("learning rate {0}".format(self.learning_rate), "green")

      self.kohonen_neurons = []

      # or if you supplied a tuple with weights
      if kohonen_neurons != None and isinstance(kohonen_neurons, (list, tuple)):
         try:
            self.kohonen_neurons = [Neuron(dimensions, k_n) for k_n in kohonen_neurons]
         except:
            self.output("invalid kohonen_neurons variable {0} supplied!".format(kohonen_neurons), "red")

      # you could've supplied just a number of neurons
      else:
          for k_n in range(input_vector_length):
            self.kohonen_neurons.append(Neuron(len(dimensions)))

   def activate(self, input_vector):
      """
      activates SOM
      """

      # normalize the input vector
      self.input_vector = [iv / float(self.dimensions[i]) for i, iv in enumerate(input_vector)]
      self.log("input vector {0}".format(self.input_vector), "blue")

      euclidean = {} 
      for kv in self.kohonen_neurons:
         euclidean[kv.euclidean_distance(self.input_vector)] = kv

      win = min(euclidean.keys());

      self.log("and the winner is: {0}".format(win))

      winner = euclidean[win]
      winner.learn(self.learning_rate, self.input_vector)

   def weight_vectors(self):
      result = [map(lambda w, dim: w * dim, kn.weight, self.dimensions) for kn in self.kohonen_neurons]
      self.log("map {0}".format(result))
      return result
         

#########################################################################################################

class Neuron(Logger):
   debug = False
   def __init__(self, dimension, weight = None):
      """
      Initializes a new neuron with weight vector
      """
      self.output("initializing neuron", "green");

      self.weight = []

      if weight == None:
         for d in range(dimension):
            self.weight.append(random.uniform(0, 1))
      else:
         self.weight = weight

      self.log("neuron weight vector : {0}".format(self.weight), "blue")

   def euclidean_distance(self, vector):
      """
      calculates the euclidian distance between vector and the weight vector of the neuron
      """
      if(len(vector) != len(self.weight)):
         raise SOMError("input {0} and weight {1} vector dimension mismatch".format(len(vector), len(self.weight))) 

      result = 0
      for i, xi in enumerate(vector):
         result = result + (xi - self.weight[i])**2
      
      self.log("euclidean before sqrt = {0}".format(result), "cyan")

      result = math.sqrt(result)
      
      self.log("euclidean = {0}".format(result), "cyan") 
      
      return result

   def learn(self, learning_rate, vector):
      """
      implements the standard competitive learning rule
      """
      if(len(vector) != len(self.weight)):
         raise SOMError("input {0} and weight {1} vector dimension mismatch".format(len(vector), len(self.weight))) 
      
      delta_weight = [learning_rate * (xi - self.weight[i]) for i, xi in enumerate(vector)]
      
      self.log("delta weights = {0}".format(delta_weight), "magenta")

      self.weight = [wi + delta_weight[i] for i, wi in enumerate(self.weight)]
         
      self.log("weights after learning = {0}".format(self.weight), "magenta")


#########################################################################################################

class SOMError(Exception):
   def __init__(self, value):
      self.value = value
   def __str__(self):
      return repr(self.value)


