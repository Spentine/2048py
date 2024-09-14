import math

# Lehmer RNG Implementation
class RNG:
  def __init__(self, seed=1, modulus=2147483647, a=16807):
    # ensure seed is in range
    seed = seed % modulus
    if (seed == 0): # 0 is bad
      seed = 1
    
    # initalize values
    self.seed = seed
    self.modulus = modulus
    self.a = a # multiplier
  
  # generate next number
  def random(self):
    # X_k+1 = a * X_k mod m
    self.seed = (self.a * self.seed) % self.modulus
    return self.seed
  
  # generate random float
  def randFloat(self):
    return self.random() / self.modulus
  
  # generate random int between a and b inclusive
  def randInt(self, a, b):
    return math.floor(self.randFloat() * (1 + b - a)) + a