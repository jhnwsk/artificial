from self_organising_map import SelfOrganisingMap
from voronoi import Voronoi
from tools import SpacialGenerator, Logger
import sys, getopt

# the 'main' routine 
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                "x:y:n:l:m:s:e:d", 
                ["dim_x=", "dim_y=", "neurons=", "learning=", "min_euclidean=", "spacial=", "epochs="]) 
    except getopt.GetoptError:           
        sys.exit(2)                     

    Logger.output("options: {0}".format(opts))
    Logger.output("arguments: {0}".format(args))

    neurons = 10
    x = 800
    y = 600
    learning_rate = 0.1
    min_euclidean = 0.01
    epochs = 1000
    spacial = SpacialGenerator.line

    for opt, arg in opts:                
        if opt in ("-x", "--dim_x"):      
            x = int(arg)
        if opt in ("-y", "--dim_y"):      
            y = int(arg)
        if opt in ("-n", "--neurons"):      
            neurons = int(arg)
        if opt in ("-l", "--learning"):      
            learning_rate = float(arg)
        if opt in ("-m", "--min_euclidean"):      
            min_euclidean = float(arg)
        if opt in ("-s", "--spacial"):      
            if arg == "line":
                spacial = SpacialGenerator.line
            if arg == "circle":
                spacial = SpacialGenerator.circle
        if opt in ("-e", "--epochs"):      
            epochs = int(arg)

    dimensions = [x, y]
    som = SelfOrganisingMap(dimensions, neurons, learning_rate, min_euclidean)
 
    for i in range(epochs):
        if spacial == SpacialGenerator.line:
            point = spacial(1, 0, dimensions)
        elif spacial == SpacialGenerator.circle:
            point = spacial(dimensions)
            

        som.activate(point, i)

    self_organised_points = som.weight_vectors()

    Logger.output("points after som: {0}".format(self_organised_points))

    voronoi = Voronoi(dimensions)
    voronoi.drawMosaic(self_organised_points);
