import random
from termcolor import colored

DEBUG = True

class SelfOrganisingMap:
   
   def __init__(self, input_neurons, kohonen_neurons, learning_rate = None):
      """
      Initializes SOM with learning_rate
      """
      print colored("initializing SOM", "green");

      if learning_rate == None:
         self.learning_rate = random.uniform(0.01, 0.2)
      else:
         self.learning_rate = learning_rate
     
      print colored("learning rate {0}", "green").format(self.learning_rate)

      self.input_neurons = []
      self.kohonen_neurons = []

      for i_n in input_neurons:
         self.input_neurons.append(Neuron(i_n))

      # or if you supplied a tuple with weights
      if isinstance(kohonen_neurons, (int, long)):
         for k_n in range(kohonen_neurons):
            self.kohonen_neurons.append(Neuron())
      # you could've supplied just a number of neurons
      else:
         try:
            for k_n in kohonen_neurons:
               self.kohonen_neurons.append(Neuron(k_n))
         except:
            print colored("invalid kohonen_neurons variable {} supplied!", "red").format(kohonen_neurons)

class Neuron:

   def __init__(self, weight = None):
      """
      Initializes a new neuron with weight vector
      """
      print colored("initializing neuron", "green");

      if weight == None:
         self.weight = random.uniform(0, 1)
      else:
         self.weight = weight

      print colored("neuron weight vector : {0}").format(self.weight)

      pass

# the 'main' routine 
if __name__ == "__main__":
   input_neurons = [[0.1, 0.1], [0, -0.1]]
   kohonen_neurons = [[0.5, 0.5], [0.2, 0.3]]

   som = SelfOrganisingMap(input_neurons, kohonen_neurons, 0.1)
   som = SelfOrganisingMap(input_neurons, 4, 0.1)
