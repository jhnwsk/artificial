import random
from termcolor import colored

DEBUG = True
# the multi layer perceptron class
class MultiLayerPerceptron:

   def __init__(self, layers, threshold = 0):
      """ initialize a new network
      
      :param layers: list containing number of neurons in each layer with optionally associated weights
      """
      self.layers = []
      self.threshold = threshold
      layer_number = 0
      self.outputs = []
      
      # initialize input layer
      input_layer = layers[0]
      inputs = 1
      if isinstance(input_layer , int):
         print colored("appending {0} neurons to input layer", "green").format(input_layer)
         self.layers.append([])
         for x in range(input_layer ):
            self.layers[0].append(Neuron(inputs, self.threshold, 0))
      
      # initialize all hidden and output layers
      inputs = len(self.layers[0])
      for (layer_number, layer) in enumerate(layers[1:]):
         if isinstance(layer, int):
            print colored("appending {0} neurons to layer {1}".format(layer, layer_number+1), "green")
            self.layers.append([])
            for x in range(layer):
               self.layers[-1].append(Neuron(inputs, self.threshold))
            inputs = layer

   def assignInput(self, input_values = None):
      """ assign input values, potentially usefull only for input layer """
      for input_neuron in self.layers[0]:
         input_neuron.assignInput([random.randint(1, 10)])
         
      # just for tests
      if DEBUG:
         for input_neuron in self.layers[0]:
            input_neuron.output()
      
   def activate(self, inputs = None):
      """ calculate the network's output, this is the first step in backpropagation learning """
      
      if inputs != None: 
         self.assignInput(inputs)
         inputs = None
      
      for (index, layer) in enumerate(self.layers):
         self.outputs = []
         self.outputs.extend(neuron.output(inputs) for neuron in layer)
         inputs = self.outputs
         if DEBUG: print "layer {0} output = {1} \n".format(index, self.outputs)
         
      return self.outputs
      
   
   def trainWeights(self):
      pass
   
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
		
   def __init__(self, inputs, threshold = 0, weight = None, activation = None, input_values = None ):
      """ initialize the Neuron """
      print "initializing neuron with {0} inputs".format(inputs)
      
      self.weights = []
      self.input_values = []
      if activation == None:
         self.activate = self.__activateSign
      else:
         self.activate = activation
      self.threshold = threshold
      
      w = 0
      if(weight == None):
         # Set all the weights and threshold levels of the network to random numbers uniformly distributed inside a small range (Haykin, 1999):
         # meaning only one random number / number of inputs
         w = random.uniform(-0.5, 0.5)
         w = round(w / float(inputs), 2)
      else:
         w = round(weight / float(inputs), 2)
       
      for x in range(inputs):
         self.weights.append(w)

   def assignInput(self, input_values):
         self.input_values.extend(input_values)
      
   def __combineInputs(self, inputs):
      """ lineary combine the neurons input """
      x = sum(int(value) * float(self.weights[index]) for (index, value) in enumerate(inputs))
      x -= self.threshold
      if DEBUG: print "activation x = " + str(x) + ", threshold: " + str(self.threshold) + ", weight: " + str(self.weights)
      return x
   
   def output(self, inputs = None):
      if inputs == None: inputs = self.input_values
      return self.activate(inputs)
      
   def __activateSign(self, inputs):
      """ sigmoid activation function -> 
            f(x) = 1 if X - threshold >= 0
            f(x) = -1 if X - threshold < 0
      """
      combined_input = self.__combineInputs(inputs)
      result = 0
      if combined_input >= 0: result = 1
      else: result = -1
      return result
      
   def __activateThreshold(self):
      pass
   
   def __activateHyperbolic(self):
      pass      

   def __str__(self):
      """ magical function toString """
      result = "neuron weights: " + str(self.weights)
      if(len(self.input_values) > 0):
         result += "\n" + "neuron input values " + str(self.input_values)
      return result

# the 'main' routine 
if __name__ == "__main__":
   mlp = MultiLayerPerceptron([3, 4, 3])
   # mlp.assignInput()
   print str(mlp)
   print str(mlp.activate([1, 0, 1]))

