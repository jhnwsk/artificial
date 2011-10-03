import math
from tools import Logger

Logger.debug = True

# encoding hash
charset = {
        "1":[1,1,1],
        "2":[-1,-1,-1],
        "3":[1,-1,1],
        "4":[-1,1,-1],
        
        "5":[1,1,1,1],
        "6":[-1,-1,-1,1],
        "7":[1,-1,1,1],
        "8":[-1,1,-1,1],
        "9":[-1,1,-1,-1],

        "_":[-1,-1,-1,-1,-1],
        "/":[1,-1,-1,-1,-1],
        ".":[-1,1,-1,-1,-1],
        "?":[1,1,-1,-1,-1],
        "=":[-1,-1,1,-1,-1],
        "&":[1,-1,1,-1,-1],
        "a":[-1,1,1,-1,-1],
        "b":[1,1,1,-1,-1],
        "c":[-1,-1,-1,1,-1],
        "d":[1,-1,-1,1,-1],
        "e":[-1,1,-1,1,-1],
        "f":[1,1,-1,1,-1],
        "g":[-1,-1,1,1,-1],
        "h":[1,-1,1,1,-1],
        "i":[-1,1,1,1,-1],
        "j":[1,1,1,1,-1],
        "k":[-1,-1,-1,-1,1],
        "l":[1,-1,-1,-1,1],
        "m":[-1,1,-1,-1,1],
        "n":[1,1,-1,-1,1],
        "o":[-1,-1,1,-1,1],
        "p":[1,-1,1,-1,1],
        "q":[-1,1,1,-1,1],
        "r":[1,1,1,-1,1],
        "s":[-1,-1,-1,1,1],
        "t":[1,-1,-1,1,1],
        "u":[-1,1,-1,1,1],
        "v":[1,1,-1,1,1],
        "w":[-1,-1,1,1,1],
        "x":[1,-1,1,1,1],
        "y":[-1,1,1,1,1],
        "z":[1,1,1,1,1]}

# reverse for conversion
#tesrach = {}
#for key in charset:
#    tesrach[charset[key]] = key
#    Logger.output(key)
#    pass

urls = ["ai.eu?b=", "op.pl/ab", "onet.pl/", "beer.com"]

def make_bipolar(url):
    """ makes an url bipolar """
    result = []
    for s in url:
        result.append(charset[s])    

    Logger.log(result)
    return result

def unmake_bipolar(bipolar_url):
    """ converts from bipolar to string format """
    result = []
    for bp in bipolar_url:
        for c in charset:
            if charset[c] == bp:
                result.append(c)

    Logger.log(result)
    return result

class HopfieldNet:
    """ the Hopfield network """

    def __init__(self, neurons = 40):
        Logger.output("creating network")
        self.neurons = [Neuron(i, neurons) for i in range(neurons)]
        Logger.output("created network with {0} neurons".format(len(self.neurons)))
        pass

    def _state_vector(self):
        """ network state defined by neurons states """
        pass
    state_vector = property(_state_vector)

    def learn(self, M, epochs=1, learning_rate = .1, forgetting_factor = .01):
        """
        a method for network learning
        M - the patterns
        """
        for e in range(epochs):
            for m in M:
                for i, neuron in enumerate(self.neurons):
                    bipolar = make_bipolar(m)
                    flat_input = [item for sublist in bipolar for item in sublist] 
                    neuron.learn(flat_input, i, flat_input[i])

            Logger.log("I've learned:")
            for i, neuron in enumerate(self.neurons):
                Logger.log("w{0}: {1}".format(i, neuron.weights))

    def test(self, fundamental_memories):
        for fundamental_memory in fundamental_memories:
            corelation = []
            bipolar = make_bipolar(fundamental_memory)    
            flat_memory = [item for sublist in bipolar for item in sublist]
            Logger.log("{0} length: {1}".format(fundamental_memory, len(flat_memory)))
            for i in flat_memory:
                x_mi = i
# there is no sign function in python... :D
                y_mi = self.neurons[i].test(flat_memory)
                if x_mi == y_mi:
                    corelation.append(True)

            Logger.log("{0}: {1}".format(fundamental_memory, len(corelation)))


################################################################################################

class Neuron:
    """ the single hopfield neuron """

    def __init__(self, neuron_index, dimension):
        self.weights = [0 for i in range(dimension)]
        # initial state
        self.neuron_index = neuron_index

    def saturized_activation(self, x, y):
        """ saturized linear activation function """
        result = y
        if x >= 1: result = 1
        elif x <= -1: result = -1

        return result

    def activate(self, input_vector, a_function = saturized_activation):
        """ 
        neurons activation function
        there is no need to remove the item at neuron_index as its weight will always be 0
        """
        weighed_input_vector = map(lambda x,y : x*y, input_vector, self.weights)
        weighed_input = sum(weighed_input_vector)
        return a_function(weighed_input)

    def learn(self, input_vector, neuron_index, state):
        """ generalized hebbian learning rule """
        for j, weight in enumerate(self.weights):
            if j != neuron_index: 
                dw = 0
                if state == input_vector[j]: dw = 1
                else: dw = -1
                self.weights[j] += dw
                Logger.log("for weight i:{0} j:{1} - dw = {2} and weight = {3}".format(neuron_index, j, dw, self.weights[j]))

    def test(self, input_vector, a_function = saturized_activation):
        result = 0
        weighed_input = map(lambda w, x: w*x, self.weights, input_vector)
        weighed_sum = sum(weighed_input)
        result = a_function(self, weighed_sum, input_vector[self.neuron_index])

        return result

if __name__ == "__main__":
    
# ksiazkowo, koncertowo!
    simple=["1","2","3","4"]
    hophop = HopfieldNet(3)
    hophop.learn(simple)
    hophop.test(simple)

    simple=["5","6","7","8","9"]
    hophop = HopfieldNet(4)
    hophop.learn(simple)
    hophop.test(simple)

# z zadania
#    hophop = HopfieldNet(40)
 #   hophop.learn(urls)
  #  hophop.test(urls)

