import random
from termcolor import colored

class Logger:
   """
   logs messages to user
   """

   debug = True

   @classmethod
   def log(cls, value, color = None):
      """
      output only if DEBUG
      """
      if color == None: color = "cyan"
      if cls.debug:
         print colored(value, color)
   @classmethod
   def output(cls, value, color = None):
      """
      output always
      """
      if color == None: color = "cyan"
      print colored(value, color)

class SpacialGenerator:
   """
   class for generating points in a 2 dimensional uniform space 0..1
   """
   @classmethod
   def line(cls, a, b, dimensions = [1,1]):
      """
      returns points on line defined by f(x) = ax + b
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
   def circle(cls, full = False):
      pass
   
   @classmethod
   def triangle(cls):
      pass

   @classmethod
   def rectangle(cls):
      pass

   @classmethod
   def sum(cls, *spaces):
      pass

