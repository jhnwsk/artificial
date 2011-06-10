import random
import math
from tools import Logger

#########################################################################################################

class SelfOrganisingMap(Logger):

   debug = False

   def __init__(self, dimensions, kohonen_neurons,
         learning_rate = random.uniform(0.01, 0.2), 
         min_euclidean_distance = random.uniform(0.01, 0.1)):
      """
      Initializes SOM which can scale input vectors from dimensions space two a uniform space and kohonen_neurons number of neurons
      learning rate is optional
      min_euclidean_distance is the euclidean distance at which the winner neuron will no longer be activated
      """
      self.output("initializing SOM", "green")

      self.dimensions = dimensions
      self.learning_rate = learning_rate
      self.output("learning rate {0}".format(self.learning_rate), "green")
      
      self.min_euclidean_distance = min_euclidean_distance
      self.output("min euclidean distance {0}".format(self.min_euclidean_distance), "green")

      self.kohonen_neurons = []

      # or if you supplied a tuple with weights
      if kohonen_neurons != None and isinstance(kohonen_neurons, (list, tuple)):
         try:
            self.kohonen_neurons = [Neuron(dimensions, k_n) for k_n in kohonen_neurons]
         except:
            self.output("invalid kohonen_neurons variable {0} supplied!".format(kohonen_neurons), "red")

      # you could've supplied just a number of neurons
      elif kohonen_neurons != None and isinstance(kohonen_neurons, (long, int)):
          for k_n in range(kohonen_neurons):
            self.kohonen_neurons.append(Neuron(len(dimensions)))

   def activate(self, input_vector, epoch):
      """
      activates SOM with input_vector
      """
      # normalize the input vector
      self.input_vector = [iv / float(self.dimensions[i]) for i, iv in enumerate(input_vector)]
      self.log("input vector {0}".format(self.input_vector), "blue")

      # dictionary comprehensions available in python 2.7 and 3+
      # euclidean = {kn.euclidean_distance(self.input_vector) : kn for kn in self.kohonen_neurons}

      # generate euclidean dictionary of neurons keyed by their distances
      euclidean = dict((kn.euclidean_distance(self.input_vector), kn) for kn in self.kohonen_neurons)
      
      win = min(euclidean.keys());

      self.log("and the winner is: {0}".format(win))

      # pop the winner for later gaussian learning
      winner = euclidean.pop(win)
      
      # activate according to neighborhood function
      if math.fabs(win) > self.min_euclidean_distance:
         for neuron in euclidean.values():
            neuron.learn(neuron.gaussian_neighborhood(self.learning_rate, winner.weight, self.shrink_learning_radius(epoch)), self.input_vector)
         # winner learns last
         self.log("winner learns")
         winner.learn(self.learning_rate, self.input_vector)

      self.output("neurons after epoch {0}".format([str(kn) for kn in self.kohonen_neurons]))

      # the learning rate should shrink over time
      self.shrink_learning_rate(epoch)

   def weight_vectors(self):
      """
      returns the weight vectors of all neurons in the network
      """
      result = [map(lambda w, dim: w * dim, kn.weight, self.dimensions) for kn in self.kohonen_neurons]
      self.log("map {0}".format(result))
      return result
   
   def shrink_learning_radius(self, epoch, time_constant = 1, initial_learning_radius = 0.1, minimal_learning_radius = 0.0001):
      """
      calculates the learning_radius decreasing over epoch's by time constant from initial_learning_radius  to minimal_learning_radius values
      """
      result = initial_learning_radius * math.exp(-epoch/time_constant)

      if result < minimal_learning_radius: result = minimal_learning_radius
      self.log("shrunk learning radius: {0}".format(result))

      return result

   def shrink_learning_rate(self, epoch, time_constant = 1, minimal_learning_rate = 0.001):
      """
      shrinks the self.learning_rate over epoch's using time_constant
      """
      result = self.learning_rate * math.exp(-epoch/time_constant)

      if result < minimal_learning_rate: result = minimal_learning_rate
      self.log("shrunk learning rate: {0}".format(result))

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
   
   def gaussian_neighborhood(self, unity, winner, learning_radius):
      """
      f(x) = unity * e^(-(x - winner)^2 / (2 * learning_radius^2))
      calculates the gaussian neighborhood function from winner with peak in unity and width of learning radius

      the length of the winner tuple is used as dimensions for the function
      """
      # TODO - how to augment learning radius over time? 
      # initial idea - euclidean distance of winner from input vector - sucks! ;)
      # idea from "Neural Networks a comprehensive foundation" in learning_radius method

      dividends = map(lambda x, b: -(x - b)**2, self.weight, winner)
      self.log("dividends {0}".format(dividends))

      divisor = 2 * learning_radius**2
      self.log("divisor {0}".format(divisor))

      result = [unity * math.exp(div/divisor) for div in dividends]
      self.log("gaussian neighborhood {0}".format(result))
      return result

   def learn(self, learning_rate, vector):
      """
      implements the standard competitive learning rule
      """
      if(len(vector) != len(self.weight)):
         raise SOMError("input {0} and weight {1} vector dimension mismatch".format(len(vector), len(self.weight))) 
     
      self.log("neuron learns at rate {0} with input {1}".format(learning_rate, vector))

      # winner learns with global learning rate
      if isinstance(learning_rate, (int, float)):
         delta_weight = [learning_rate * (xi - self.weight[i]) for i, xi in enumerate(vector)]
      # looser learn with individual learning rates in each dimension
      elif isinstance(learning_rate, (list, tuple)):
         adjusted_weights = [(xi - self.weight[i]) for i, xi in enumerate(vector)]
         self.log("adjusted weights = {0}".format(adjusted_weights))
         delta_weight = map(lambda lr, aw: lr * aw, learning_rate, adjusted_weights)
      
      self.log("delta weights = {0}".format(delta_weight))

      self.weight = [wi + delta_weight[i] for i, wi in enumerate(self.weight)]
         
      self.log("weights after learning = {0}".format(self.weight))

   def __str__(self):
      return str(self.weight)

#########################################################################################################

class SOMError(Exception):
   def __init__(self, value):
         self.value = value
   def __str__(self):
      return repr(self.value)


