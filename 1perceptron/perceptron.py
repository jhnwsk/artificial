from tools import Logger

patterns = [[1,0,0,0],[1,0,0,0]], [[0,1,0,0],[0,1,0,0]], [[0,0,1,0],[0,0,1,0]], [[0,0,0,1],[0,0,0,1]]

##############################################
# Multi Layer Perceptron
##############################################
class MLP:
    """ the MLP class """
    def __init__(self, layers, learning_rate = 1, threshold = None):
        Logger.log("initializing MLP with {0} layers".format(len(layers)))
# sum of all neurons in the mlp
        self.F = sum(layers)
        self.layers = [Layer(neurons, self.F, learning_rate, threshold) for neurons in layers]

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
        for i, layer in enumerate(self.layers[1:]):
            layer.activate(self.layers[i].output)

    def backpropagate(self, pattern):
        Logger.log("beginning backpropagation of pattern {0}".format(pattern[1]))

        Logger.log("training output layer")
        self.layers[-1].backpropagate(pattern[1], self.layers[-2], True)
        current = self.layers[-1]

        backward = self.layers[1:-1]
        backward.reverse()
        for i, layer in enumerate(backward):
            Logger.log("training hidden layer {0}".format(len(self.layers)-i-1))
            layer.backpropagate(None, current)
            current = layer
    
        for layer in self.layers[1:]:
            for neuron in layer.neurons:
                neuron.update_weight()

##############################################
# Neuron
##############################################
class Layer:
    """ the Neuron class """
    def __init__(self, neurons, F, learning_rate, threshold):
        Logger.log("initializing Layer with {0} neurons".format(neurons))
        self.neurons = [Neuron(F, learning_rate, threshold) for neuron in range(neurons)]

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
        """ activates the layer using the patterns """
        for i, neuron in enumerate(self.neurons):
            # input layer
            if not neuron.weights:
                neuron.output = pattern[i]
            # processing layers
            else:
                neuron.activate(pattern)

        Logger.log("activated layer: {0}".format(self.output))

    def backpropagate(self, pattern, layer, output = False):
        """ 
        weight training on potentially output layer
        """
        if output: map(lambda n,p: n.weight_train(p, layer.neurons, output), self.neurons, pattern)
        else:
            for i, neuron in enumerate(self.neurons):
                error_signal = sum([n.weights[i] * n.error_gradient for j,n in enumerate(layer.neurons)])
                neuron.weight_train(error_signal, layer.neurons, output)

##############################################
# Neuron
##############################################
class Neuron:
    """ the Neuron class """

    def __init__(self, F, learning_rate, threshold):
        """
        F - number of all neurons in the network
        """
        self.weights = []

        import random
        if not threshold:
            self.threshold = random.uniform(-2.4/F, 2.4/F) 
        else:
            self.threshold = threshold
        
        self.output = None
        self.learning_rate = learning_rate
        Logger.log("initializing Neuron")

    def sigmoid_activate(self, x):
        """ 
        sigmoid (logistic) activation function 
        1 / (1 + e^(-x))
        """
        from math import exp
        result = exp(-x)
        result += 1
        result = 1/result
        self.output = result
        return result

    def activate(self, pattern, activate = sigmoid_activate):
        """ activates the neuron using the patterns """
        weighed_input = map(lambda x,y:x*y, self.weights, pattern)
        weighed_sum = sum(weighed_input)
        weighed_sum -= self.threshold
        self.output = activate(self, weighed_sum)
        return self.output

    def weight_train(self, desired, layer, output):
        """ 
        calculates the error gradient 
        desired is either the desired pattern or the error gradient 
        """
        if output:
            self.error_signal = desired - self.output
            self.error_gradient = self.output * (1 - self.output) * self.error_signal
            # dont apply them yet, we need them for further backpropagation
            self.weight_corrections = [self.learning_rate * y.output * self.error_gradient for y in layer]
        else:
            self.error_signal = desired
            self.error_gradient = self.output * (1 - self.output) * self.error_signal
            self.weight_corrections = [self.learning_rate * y.output * self.error_gradient for y in layer]

        Logger.log("trained output Neuron to signal:{0}, gradient:{1} and delta:{2}".format(self.error_signal, self.error_gradient, self.weight_corrections))

    def update_weight(self):
        """ updates the weights of neurons """
        self.weights = map(lambda w, dw: w + dw, self.weights, self.weight_corrections)
        self.weight_corrections = None

if __name__ == "__main__":
    import getopt, sys
    opts, args = getopt.getopt(sys.argv[1:], "e:p:d", ["help", "epochs=", "pattern="])

    epochs = 1
    pattern = patterns[0]
    for o, a in opts:
        if o == "-d":
            Logger.debug = True
        elif o in ("-e", "--epochs"):
            epochs = int(a)
        elif o in ("-p", "--pattern"):
            pattern = patterns[int(a)]

    mlp = MLP([4,2,4])
    mlp.initialize()
    for e in range(epochs):
        mlp.activate(pattern)
        mlp.backpropagate(pattern)
