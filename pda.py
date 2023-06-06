import random

class EOF:
    def __repr__(self):
        return "EOF"
    def __str__(self):
        return "EOF"

EOF = EOF()

class EOS:
    def __repr__(self):
        return "$"
    def __str__(self):
        return "$"
EOS = EOS()

class RejectedException(Exception):
    pass

class Engine:
  def __init__(self, seed, alpha):
      self.counter = 0
      self.rnd = random.Random(seed)
      self.data = list(alpha) + [EOF]
      self.finished = False
      self.processed = []
      self.stack = []
      self.stack_start = "$"

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
      
  def pop(self):
    if not self.stack:
        raise RejectedException()
    return self.stack.pop()

  def push(self, input):
    self.stack.append(input)
        
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

def example_palindrome(e): #palindrome PDA doesn't work for odd number of characters
    input = e.read()
    e.push(EOS)
    while(e.flip_coin()):
        e.push(input)
        input = e.read()
    top = e.pop()
    while(input == top):
        input = e.read()
        top = e.pop()
    return top == EOS and input == EOF

def example_as_then_bs(e): #parse same number of as then bs
    input = e.read()
    e.push(EOS)
    e.ensure(input == "a") #Can it be the empty string?
    while(input == "a"):
        e.push("a")
        input = e.read()
    top = e.pop()
    while(input == "b" and top == "a"):
        input = e.read()
        top = e.pop()

    return top == EOS and input == EOF


seed = 1
while True:
    accepted, result = run(example_as_then_bs, ["a", "b"])
    seed+=1
    if accepted:
        print("accepted", " ", seed, " ", result)
        break
    else:
        print("rejected", " ", seed, " ", result)