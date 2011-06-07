import random
from termcolor import colored

class Logger:
   """
   logs messages to user
   """

   debug = False

   @classmethod
   def log(cls, value, color = None):
      """
      output only if DEBUG
      """
      if color == None: msg = value
      else: msg = colored(value, color)
      if cls.debug:
         print msg

   @classmethod
   def output(cls, value, color = None):
      """
      output always
      """
      if color == None: msg = value
      else: msg = colored(value, color)
      print msg

class SpacialGenerator:
   """
   class for generating points in a 2 dimensional uniform space 0..1
   """
   @classmethod
   def line(cls, a, b, dimensions = [1,1]):
      """
      returns random points on line defined by f(x) = ax + b
      """
      x = random.uniform(0, dimensions[0])
      y = a * x + b

      result = [x, y]

      scale = [x/dimensions[0], y/dimensions[1]]

      if any(s > 1 for s in scale):
         scale = max(scale)
         result = [x/scale, y/scale]

      
      Logger.log("random point on line {0}".format(result))

      return result

   @classmethod
   def circle(cls, center, radius, dimensions = [1,1], full = False):
      """
      returns random points in circle with center and radius
      circle can optionally be full
      """


      pass
   
   @classmethod
   def triangle(cls, a, b, c):
      pass

   @classmethod
   def rectangle(cls, a, b, c, d):
      pass

   @classmethod
   def sum(cls, *spaces):
      pass

