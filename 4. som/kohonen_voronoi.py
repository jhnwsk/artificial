from self_organising_map import SelfOrganisingMap
from voronoi import *

# the 'main' routine 
if __name__ == "__main__":
   
   # voronoi
   dimensions = [800, 600]
   input_vectors = [[750, 599], [100, 100], [500, 500], [250, 250], [300, 10]]
   som = SelfOrganisingMap(dimensions, len(input_vectors))
 
   for iv in input_vectors:
      for i in range(1000):
         som.activate(iv)

   self_organised_points = som.weight_vectors()
   print "points after som: {0}".format(self_organised_points)

   voronoi = Voronoi(dimensions)
   voronoi.drawMosaic(self_organised_points);
