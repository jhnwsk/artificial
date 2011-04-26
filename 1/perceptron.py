import random

# the multi layer perceptron class
class MultiLayerPerceptron:

   layers = []

   def __init__(self, layers):
      """ initialize a new network
      
      :param layers: list containing number of neurons in each layer with optionally associated weights
      """
      layer_number = 0
      inputs = 1
      for layer in layers:
         if isinstance(layer, int):
            print "appending ", layer, " neurons to layer ",layer_number
            self.layers.append([])
            for x in range(layer):
               self.layers[layer_number].append(Neuron(inputs))
            inputs = layer
         layer_number += 1

   def __str__(self):
      result = "input layer: \n" 
      for n in self.layers[0]:
         result += str(n) + "\n"
      for l in self.layers[1:-1]:
         result += "hidden layer: \n"
         for n in l:
            result += str(n) + "\n"
 
      result += "output layer: \n"
      for n in self.layers[-1]:
         result += str(n) + "\n"
 
      return str(result)

# the neuron class
class Neuron:

   # threshold = 0
   # weights = []

   def __init__(self, inputs, threshold = 0, weight = None, activation = None ):
      """ initialize the Neuron """
      print "initializing neuron with {0} inputs".format(inputs)

      self.weights = []

      w = 0
      if(weight == None):
         # Set all the weights and threshold levels of the network to random numbers uniformly distributed inside a small range (Haykin, 1999):
         # meaning only one random number / number of inputs
         w = random.uniform(-0.5, 0.5)
         w = w / inputs
      else:
         w = weight / inputs
       
      for x in range(inputs):
         self.weights.append(w)

      self.activation = activation
      self.threshold = threshold

   def __str__(self):
      return "neuron weights: " + str(self.weights)

   def combineInputs(self):
      """ lineary combine the neurons input """
      pass

# the 'main' routine 
if __name__ == "__main__":
   mlp = MultiLayerPerceptron([3, 4, 3])
   print str(mlp)
