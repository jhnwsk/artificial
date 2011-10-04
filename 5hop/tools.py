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


