from tools import Logger

patterns = [[1,0,0,0],[1,0,0,0]], [[0,1,0,0],[0,1,0,0]], [[0,0,1,0],[0,0,1,0]], [[0,0,0,1],[0,0,0,1]]

##############################################
# Multi Layer Perceptron
##############################################
class MLP:
    """ the MLP class """
    def __init__(self, layers):
        Logger.log("initializing MLP with {0} layers".format(len(layers)))
# sum of all neurons in the mlp
        self.F = sum(layers)
        self.layers = [Layer(neurons, self.F) for neurons in layers]

    def initialize(self):
        """ initializes the neuron weights """
        for i, layer in enumerate(self.layers):
            try:
                layer.assign_weights(self.layers[i+1], self.F)
                Logger.log("assigned weights to layer {0}".format(i+2))
            except IndexError:
                Logger.log("finished assigning weights")

        for i, layer in enumerate(self.layers):
            Logger.log("initialized layer {0}".format(i+1))
            for j, n in enumerate(layer.neurons):
                Logger.log("neuron {0}:{1} weights {2}".format(i+1, j+1, n.weights))

    def activate(self, pattern):
        """ activates the mlp using the patterns """
        Logger.log("activating input layer")
        self.layers[0].activate(pattern[0])
        for layer in self.layers[1:]:
            layer.activate


##############################################
# Neuron
##############################################
class Layer:
    """ the Neuron class """
    def __init__(self, neurons, F, bias = False):
        Logger.log("initializing Layer with {0} neurons".format(neurons))
        self.neurons = [Neuron(F) for neuron in range(neurons)]

    def _output(self):
        return [n.output for n in self.neurons]
    output = property(_output)

    def assign_weights(self, layer, F):
        """ generate random weights based on neurons in self and assign to each neuron in layer """
        for neuron in layer.neurons:
            import random
            """ Haykin - uniform weight and threshold distribution """
            weights = [random.uniform(-2.4/F, 2.4/F) for n in self.neurons]
            neuron.weights = weights

    def activate(self, pattern):
        """ activates the mlp using the patterns """
        for i, neuron in enumerate(self.neurons):
            if not neuron.weights:
                neuron.output = pattern[i]

        Logger.log("activated layer: {0}".format(self.output))


##############################################
# Neuron
##############################################
class Neuron:
    """ the Neuron class """

    def __init__(self, F, bias = False):
        """
        F - number of all neurons in the network
        """
        self.bias = bias
        self.weights = []
        import random
        self.threshold = random.uniform(-2.4/F, 2.4/F) 
        self.output = None
        Logger.log("initializing Neuron")

    def sigmoid_activate(self, x):
        """ 
        sigmoid (logistic) activation function 
        1 / (1 + e^(-x))
        """
        from math import e
        result = e ** (-x)
        result += 1
        result = 1/result
        self.output = result
        return result

if __name__ == "__main__":
    import getopt, sys
    opts, args = getopt.getopt(sys.argv[1:], "d", ["help", "output="])

    for o, a in opts:
        if o == "-d":
            Logger.debug = True
        elif o in ("-o", "--output"):
            output = a

    mlp = MLP([4,2,4])
    mlp.initialize()
    mlp.activate(patterns[0])
