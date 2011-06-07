from self_organising_map import SelfOrganisingMap
from voronoi import Voronoi
from tools import SpacialGenerator, Logger

# the 'main' routine 
if __name__ == "__main__":
   
   # voronoi
   dimensions = [600, 600]
   # old tests with set of input vectors 
   # input_vectors = [[100, 100], [700, 100], [100, 500], [700, 500]]

   som = SelfOrganisingMap(dimensions, 10, 0.1, 0.01)
 
   for i in range(100000):
      point = SpacialGenerator.line(1, 0, dimensions)
      som.activate(point, i)

   self_organised_points = som.weight_vectors()

   Logger.output("points after som: {0}".format(self_organised_points))

   voronoi = Voronoi(dimensions)
   voronoi.drawMosaic(self_organised_points);
