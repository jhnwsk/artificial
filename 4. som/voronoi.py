# Voronoi diagram
# FB - 201008087
import random
import math
import Image

class Voronoi:

   def __init__(self, dimensions):
      self.imgx = dimensions[0]
      self.imgy = dimensions[1]
      self.image = Image.new("RGB", (self.imgx, self.imgy))

   def drawMosaic(self, points = None):
      n = 0
      nx = []
      ny = []
      nr = []
      ng = []
      nb = []

      if points == None:
         n = random.randint(50, 100) # of cells
         for i in range(n):
            nx.append(random.randint(0, imgx - 1))
            ny.append(random.randint(0, imgy - 1))
            nr.append(random.randint(0, 255))
            ng.append(random.randint(0, 255))
            nb.append(random.randint(0, 255))
      else:
         n = len(points)
         for p in points:
            nx.append(int(p[0]))
            ny.append(int(p[1]))
            nr.append(random.randint(0, 255))
            ng.append(random.randint(0, 255))
            nb.append(random.randint(0, 255))

      for y in range(self.imgy):
         for x in range(self.imgx):
            # find the closest cell center
            dmin = math.hypot(self.imgx - 1, self.imgy - 1)
            j = -1
            for i in range(n):
               d = math.hypot(nx[i] - x, ny[i] - y)
               if d < dmin:
                  dmin = d
                  j = i

            self.image.putpixel((x, y), (nr[j], ng[j], nb[j]))

      # mark the cell centers
      for i in range(n):
         self.image.putpixel((nx[i], ny[i]),(255 - nr[i], 255 - ng[i], 255 - nb[i]))

      self.image.save("Voronoi.png", "PNG")
