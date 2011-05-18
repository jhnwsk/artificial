import random
import math
from termcolor import colored

DEBUG = True

def log(value, color):
   if DEBUG:
      print colored(value, color)

#########################################################################################################

class SelfOrganisingMap:

   def __init__(self, input_vector, kohonen_neurons, learning_rate = None):
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

      self.input_vector = input_vector
      print colored("input vector {0}", "blue").format(self.input_vector)

      # or if you supplied a tuple with weights
      if isinstance(kohonen_neurons, (int, long)):
         for k_n in range(kohonen_neurons):
            self.kohonen_neurons.append(Neuron(len(input_vector)))
      # you could've supplied just a number of neurons
      else:
         try:
            for k_n in kohonen_neurons:
               self.kohonen_neurons.append(Neuron(k_n))
         except:
            print colored("invalid kohonen_neurons variable {} supplied!", "red").format(kohonen_neurons)

   def activate(self):
      """
      activates SOM
      """
      euclidian = []
      for kv in self.kohonen_neurons:
         euclidian.append(kv.euclidianDistance(self.input_vector))

      # TODO map the euclidian distances, and make'em smallest learn
         
#########################################################################################################

class Neuron:

   def __init__(self, dimension, weight = None):
      """
      Initializes a new neuron with weight vector
      """
      print colored("initializing neuron", "green");

      self.weight = []

      if weight == None:
         for d in range(dimension):
            self.weight.append(random.uniform(0, 1))
      else:
         self.weight = weight

      print colored("neuron weight vector : {0}", "blue").format(self.weight)

   def euclidianDistance(self, vector):
      """
      calculates the euclidian distance between vector and the weight vector of the neuron
      """
      if(len(vector) != len(self.weight)):
         raise SOMError("input {0} and weight {1} vector dimension mismatch".format(len(vector), len(self.weight))) 

      result = 0
      for i, xi in enumerate(vector):
         result = result + (xi - self.weight[i])**2
      
      log("result before sqrt = {0}".format(result), "cyan")

      result = math.sqrt(result)
      
      return result

   def learn(self, learning_rate, vector):
      """
      implements the standard competitive learning rule
      """
      if(len(vector) != len(self.weight)):
         raise SOMError("input {0} and weight {1} vector dimension mismatch".format(len(vector), len(self.weight))) 
      
      delta_weight = []
      for i, xi in vector:
         delta_weight.append(learning_rate * (xi - self.weight[i]))
      
      log("delta weights = {0}".format(delta_weight), "magenta")

      for i, wi in self.weight:
         wi = wi + delta_weight[i]

      log("weights after learning = {0}".format(self.weight), "magenta")


#########################################################################################################

class SOMError(Exception):
   def __init__(self, value):
      self.value = value
   def __str__(self):
      return repr(self.value)

# the 'main' routine 
if __name__ == "__main__":
   input_neuron = [0.1, 0.1]
   kohonen_neurons = [[0.5, 0.5], [0.2, 0.3]]

   som = SelfOrganisingMap(input_neuron, 4, 0.1)
   som.activate()
