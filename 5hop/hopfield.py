import sys, getopt
from tools import Logger

Logger.debug = False

# encoding hash
charset = {
        "0":[-1,-1,-1],
        "1":[1,-1,-1],
        "2":[-1,1,-1],
        "3":[1,1,-1],
        "4":[-1,-1,1],
        
        "5":[1,-1,1],
        "6":[-1,1,1],
        "7":[1,1,1],
        "8":[-1,-1,-1,1],
        "9":[1,-1,-1,1],

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

    # Logger.log("making bipolar {0}:{1}".format(url,result))
    return result

def unmake_bipolar(bipolar_url, bits):
    """ converts from bipolar to string format """
    a = 0
    b = bits
    bipolar = []
    while b <= len(bipolar_url):
        bipolar.append(bipolar_url[a:b])
        a+= bits
        b+=bits

    #Logger.log("unmaking bipolar {0}:bit state {1}".format(bits, bipolar))

    result = []
    for bp in bipolar:
        for c in charset:
            if charset[c] == bp:
                result.append(c)

    # Logger.log("unmaking bipolar {0}:{1}".format(bipolar_url, result))
    return result

class HopfieldNet:
    """ the Hopfield network """

    def __init__(self, neurons = 40, threshold = -1):
        Logger.output("creating network")
        self.neurons = [Neuron(i, neurons, threshold) for i in range(neurons)]
        Logger.output("created network with {0} neurons".format(len(self.neurons)))

    def _state_vector(self):
        """ network state defined by neurons states """
        return [neuron.state for neuron in self.neurons]
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
        fundamental_memories.append("abcd.efg")
        for fundamental_memory in fundamental_memories:
            Logger.log("testing fundamental memory:{0} with state vector:{1}".format(fundamental_memory, self.state_vector))
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

            response = [n.test(flat_memory) for n in self.neurons]

            Logger.log("{0}: {1}".format(fundamental_memory, unmake_bipolar(response, len(charset[fundamental_memory[0]]))))
            Logger.log("{0}: {1}".format(fundamental_memory, len(corelation)))

    def retrieve(self, probe):
        bipolar = make_bipolar(probe)
        flat_probe = [item for sublist in bipolar for item in sublist]
        Logger.log("retrieving probe:{0}".format(probe))

        # stuff with 0's - incomplete information
        while len(flat_probe) < len(self.neurons):
            flat_probe.append(0)
       
        Logger.log("probe:{0}".format(flat_probe))

        # initial state
        counter = 0
        y = flat_probe
        test = []

        while test != self.state_vector:
            Logger.log("state vector:{0} is not equal to retrieval:{1}".format(unmake_bipolar(self.state_vector, len(charset[probe[0]])), unmake_bipolar(y, len(charset[probe[0]]))))
            import random
            r = random.randint(0, len(self.state_vector)-1)
            self.neurons[r].retrieve(y)
            y = self.state_vector
            test = [neuron.test(self.state_vector) for neuron in self.neurons]
            counter += 1

        Logger.log("stable state after {1}:epochs retrieved:{0}".format(self.state_vector, counter))
        Logger.log("stable state unbipolarized:{0}".format(unmake_bipolar(self.state_vector, len(charset[probe[0]]))))
                

################################################################################################

class Neuron:
    """ the single hopfield neuron """

    def __init__(self, neuron_index, dimension, threshold):
        self.weights = [0 for i in range(dimension)]
        # initial state
        self.neuron_index = neuron_index
        self.threshold = threshold 
        self.state = 0

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
        """ neuron testing function """
        #Logger.log("testing neuron:{0}".format(self.neuron_index))
        result = 0
        weighed_input = map(lambda w, x: w*x, self.weights, input_vector)
        weighed_sum = sum(weighed_input) - self.threshold
        result = a_function(self, weighed_sum, input_vector[self.neuron_index])

        # Logger.log("tested:{0} from neuron:{1}".format(result, self.neuron_index))
        return result

    def retrieve(self, probe, a_function = saturized_activation):
        """ neuron testing function """
        weighed_input = map(lambda w, x: w*x, self.weights, probe)
        weighed_sum = sum(weighed_input) - self.threshold
        self.state = a_function(self, weighed_sum, probe[self.neuron_index])

        #Logger.log("retrieved:{0} from neuron:{1}".format(self.state, self.neuron_index))
        return self.state


def simple(inn, neurons, retrieve):
    if inn == None: inn = ["1","2","3","4"]
    if neurons == None: neurons = 3
    hophop = HopfieldNet(neurons)
    hophop.learn(inn)
    hophop.test(inn)

    if retrieve != None: hophop.retrieve(retrieve)

def intellinet(inn, neurons, retrieve, threshold):
    if inn == None: inn = urls
    if neurons == None: neurons = 40
    hophop = HopfieldNet(neurons, threshold)
    hophop.learn(inn)
    hophop.test(inn)

    if retrieve != None: hophop.retrieve(retrieve)

if __name__ == "__main__":
    """ the main routine """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:r:t:dm", ["input=", "manual", "neurons=", "retrieve=", "threshold="]) 
    except getopt.GetoptError:           
        sys.exit(2)                     

    Logger.output("options: {0}".format(opts))
    Logger.output("arguments: {0}".format(args))

    neurons = None
    inn = None
    retrieve = None
    threshold = -1

    for opt, arg in opts:                
        if opt in ("--manual"):      
            inn = args
        if opt in ("-n", "--neurons"):      
            neurons = int(arg)
        if opt == '-d':                
            Logger.debug = True
        if opt in ("-r", "--retrieve"):
            retrieve = arg
        if opt in ("-t", "--threshold"):
            threshold = arg
            
    for opt, arg in opts:                
        if opt in ("-i", "--input"):      
            if arg == "simple":
                simple(inn, neurons, retrieve)
            elif arg == "intellinet":
                intellinet(inn, neurons, retrieve, threshold)
             

