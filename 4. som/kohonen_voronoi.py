from self_organising_map import SelfOrganisingMap
from voronoi import Voronoi

# the 'main' routine 
if __name__ == "__main__":
   
   # voronoi
   dimensions = [800, 600]
   input_vectors = [[100, 100], [700, 100], [100, 500], [700, 500]]

   som = SelfOrganisingMap(dimensions, len(input_vectors))
 
   for i in range(2000):
      for iv in input_vectors:
         som.activate(iv)

   self_organised_points = som.weight_vectors()
   print "points after som: {0}".format(self_organised_points)

   voronoi = Voronoi(dimensions)
   voronoi.drawMosaic(self_organised_points);
