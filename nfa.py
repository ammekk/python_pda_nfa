import random

class EOF:
    def __repr__(self):
        return "EOF"
    def __str__(self):
        return "EOF"

EOF = EOF()

class RejectedException(Exception):
    pass

class Engine:
  def __init__(self, seed, alpha):
      self.counter = 0
      self.rnd = random.Random(seed)
      self.data = list(alpha) + [EOF]
      self.finished = False
      self.processed = []

  def flip_coin(self):
      if self.finished:
          raise RejectedException()
      result = self.rnd.choice([True, False])
      return result

  def has_next(self):
      return self.finished

  def read(self):
      if self.finished:
          raise RejectedException()
      result = self.rnd.choice(self.data)
      if result is not EOF:
          self.processed.append(result)
      self.finished = result is EOF
      return result

  def _get_processed(self):
      while not self.finished:
          self.read()
      return self.processed

  def ensure(self, cond):
      if not cond:
          raise RejectedException()

def run(func, alpha, seed=None): # Why pass this alpha and not use it
    e = Engine(seed, alpha)
    try:
        result = func(e)

        return result, e._get_processed()
    except RejectedException:
        return False, e._get_processed()

def accepts_all(e):
    return True

def rejects_all(e):
    return False

def example1(e):
    input = e.read()
    while e.flip_coin():
        input = e.read()
    if input == 0:
        input = e.read()
        e.ensure(input == 0)
        return True

def example2(e):
    input = e.read()
    while e.flip_coin():     # I think one of the potential problems with this is it will read inputs for a random 
        input = e.read()    # amount of time possibly consuming all the inputs even if it ends in 0 and 1
    e.ensure(input == 0)
    input = e.read()
    e.ensure(input == 1)
    return e.read() == EOF

def example3(e):
    input = e.read()
    while e.flip_coin():
        input = e.read()
    e.ensure(input == 0)
    input = e.read()
    return e.read() == EOF

def example4(e):
    input = e.read()
    while e.flip_coin():
        e.ensure(input == "a" or input == "b")
        input = e.read()
    e.ensure(input == "a")
    input = e.read()
    e.ensure(input == "c")
    return e.read() == EOF

def example5(e):    #https://cogumbreiro.github.io/teaching/cs420/f21/lecture12.pdf
    input = e.read()
    while (e.flip_coin()):   # if there is a loop that contains all the input characters is this the right way to represent it
         input = e.read()
    e.ensure(input == "a")
    input = e.read()
    if (e.flip_coin() or input == "b"):
        input = e.read()
    e.ensure(input == "a")
    while (e.flip_coin() and not input == EOF):
        input = e.read()
    return e.read() == EOF

def example6(e): #https://lh6.ggpht.com/_W1dLiLjFqdw/SaTJLtvDBfI/AAAAAAAAAfU/7ZULjntgraY/NFA%5B11%5D.png?imgmax=800
    input = e.read()
    if (input == "a"):
        input = e.read()
        while (e.flip_coin()):
            input = e.read()
        e.ensure(input == "a")
    if (input == "b"):
        input = e.read()
        while (e.flip_coin()):
            input = e.read()
        e.ensure(input == "b")
    return e.read() == EOF

def example7(e): #https://condor.depaul.edu/glancast/444class/docs/images/dfa2gnfa2.gif
    input = e.read()
    while (input == 0):
        input = e.read()
    e.ensure(input == 1)
    input = e.read()
    while (input == 0):
        input = e.read()
        while (input == 0):
            input = e.read()
        e.ensure(input == 1)  # this line isn't realy nescessary but I feel like it should be included for legibility
        input = e.read()      # but its pretty much the only option it can be? I don't know just seems a bit awkward 
    e.ensure(input == 1)
    input = e.read()
    while(input == 1):
        input = e.read()
    e.ensure(input == 0)
    input = e.read()
    while (input == 0):
        input = e.read()
        while (input == 0):
            while (input == 0):
                input = e.read()
            e.ensure(input == 1)  
            input = e.read()       
        e.ensure(input == 1)
        input = e.read()
        while(input == 1):
            input = e.read()
        e.ensure(input == 0)
        input = e.read()
    e.ensure(input == 1)
    input = e.read()
    while(input == 1 or input == 0): #This is preferable to while(input != EOF ) because I think it represents the NFA more
        input == e.read()
    return input == EOF #Again by this point the input is obviously going to equal EOF
    

def example8(e): #https://media.geeksforgeeks.org/wp-content/uploads/20200217172951/1406-3.png
    input = e.read()
    while(input == 1):
        input = e.read()
        e.ensure(input == 1)
        input = e.read()
    while(input == 1 or input == 0):
        if input == 0:
            input = e.read()
            e.ensure(input == 0)
            input = e.read()
        if input == 1:
            input = e.read()
            e.ensure(input == 0)
            input = e.read()
    return True #Or should it be return input == EOF. I think clarity in syntax is important

        
def example9(e): #https://grrinchas.github.io/resources/images/automata_6.svg
    input = e.read()
    e.ensure(input == "a") # a little awkward cause you have to have that line before the transition which
    while(input == "a"): #doesn't match the diagram
        if e.flip_coin():
            input = e.read()
            e.ensure(input == "b")
        input = e.read()
    return input == EOF



seed = 1
while True:
    accepted, result = run(example9, ["a", "b"])
    seed+=1
    if accepted:
        print("accepted", " ", seed, " ", result)
        break
    else:
        print("rejected", " ", seed, " ", result)

