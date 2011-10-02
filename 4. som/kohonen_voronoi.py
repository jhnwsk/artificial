from self_organising_map import SelfOrganisingMap
from voronoi import Voronoi
from tools import SpacialGenerator, Logger

# the 'main' routine 
if __name__ == "__main__":
   dimensions = [800, 600]

   som = SelfOrganisingMap(dimensions, 100, 0.1, 0.01)
 
   for i in range(10):
      point = SpacialGenerator.line(1, 0, dimensions)
      som.activate(point, i)

   self_organised_points = som.weight_vectors()

   Logger.output("points after som: {0}".format(self_organised_points))

   voronoi = Voronoi(dimensions)
   voronoi.drawMosaic(self_organised_points);
