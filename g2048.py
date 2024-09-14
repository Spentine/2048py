import random
import LehmerRNG
import base64 # for replays

# generates iterative reversed arrays
# n = 4:
# 1 | 2 1 | 3 2 1 without divider
def sweepingMovementArray(n):
  array = []
  for i in range(1, n):
    while i > 0:
      array.append(i)
      i -= 1
  return array

class G2048:
  def __init__(self, width=4, height=4, seed=None):
    # restrict seed range
    if (seed == None):
      seed = random.randint(0, 2147483647)
    else:
      seed = seed % 2147483647
    
    # initialize values
    self.width = width
    self.height = height
    
    # make width x height board full of 0
    self.board = [[0 for j in range(width)] for i in range(height)]
    
    self.playing = True
    
    self.initialSeed = seed # in case we need a replay
    self.rng = LehmerRNG.RNG(self.initialSeed)
    self.replay = []
  
  def __str__(self):
    # return str(self.board)
    sBoard = "" # string board
    for i in self.board:
      for j in i:
        sBoard += "|" + str(j).zfill(2)
      sBoard += "|\n"
    return sBoard
  
  def move(self, direction):
    moved = False
    
    # negative numbers means it holds the abosolute value but it can't move
    def singleMove(self, iRow, iColumn, tRow, tColumn):
      if self.board[iRow][iColumn] == 0: return False # moving nothing
      if self.board[tRow][tColumn] < 0: return False # moving to a space that can't move
      if self.board[tRow][tColumn] == 0: # if the destination is free
        self.board[tRow][tColumn] = self.board[iRow][iColumn]
        self.board[iRow][iColumn] = 0
        return True
      if self.board[iRow][iColumn] != self.board[tRow][tColumn]: return False # if they are different tiles
      self.board[tRow][tColumn] = - (1 + self.board[iRow][iColumn]) # increment and make it negative
      self.board[iRow][iColumn] = 0
      return True
    
    match direction:
      # sweepingMovementArray provides movement values
      # each case will map it onto the correct movements
      case "up":
        for row in sweepingMovementArray(self.height):
          for column in range(self.width):
            moved = singleMove(self, row, column, row - 1, column) or moved
      case "down":
        for row in sweepingMovementArray(self.height):
          for column in range(self.width):
            moved = singleMove(self, self.height - row - 1, column, self.height - row, column) or moved
      case "left":
        for column in sweepingMovementArray(self.width):
          for row in range(self.height):
            moved = singleMove(self, row, column, row, column - 1) or moved
      case "right":
        for column in sweepingMovementArray(self.width):
          for row in range(self.height):
            moved = singleMove(self, row, self.width - column - 1, row, self.width - column) or moved
      case _:
        print(f"invalid case! ({direction})")
    
    # make it all positive again
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        self.board[i][j] = abs(self.board[i][j])
    
    return moved
  
  def generateTile(self):
    # get all positions with 0
    validPositions = []
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        if self.board[i][j] == 0:
          validPositions.append([i, j])
    
    if (len(validPositions) == 0): return False # no free positions
    randomIndex = self.rng.randInt(0, len(validPositions) - 1) # choose a random position
    
    chosenTile = 1 + (1 * int(0.9 < self.rng.randFloat())) # 10% chance of 2^2
    
    self.board[validPositions[randomIndex][0]][validPositions[randomIndex][1]] = chosenTile
    return True
  
  def checkValidity(self):
    # check for any empty tiles
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        if self.board[i][j] == 0:
          return True
    
    # check for equal adjacent up/down tiles
    for i in range(len(self.board) - 1):
      for j in range(len(self.board[i])):
        if self.board[i][j] == self.board[i + 1][j]:
          return True
    
    # check for equal adjacent left/right tiles
    for i in range(len(self.board)):
      for j in range(len(self.board[i]) - 1):
        if self.board[i][j] == self.board[i][j + 1]:
          return True
    
    return False
  
  # generate replay
  def generateReplay(self):
    
    replay = ((1).to_bytes(2, 'big') + # version
              self.initialSeed.to_bytes(4, 'big') + # seed
              self.height.to_bytes(2, 'big') + # height
              self.width.to_bytes(2, 'big') + # width
              len(self.replay).to_bytes(4, 'big')) # length
    originalLength = len(self.replay)
    
    while len(self.replay) % 4 != 0:
      self.replay.append(0)
    
    for i in range(len(self.replay) >> 2):
      replay += ((self.replay[4 * i]) |
                 (self.replay[4 * i + 1] << 2) |
                 (self.replay[4 * i + 2] << 4) |
                 (self.replay[4 * i + 3] << 6)).to_bytes(1, 'big')
    
    while len(self.replay) != originalLength:
      self.replay.pop()
    
    return base64.standard_b64encode(replay).decode("utf-8")
  
  # read replay
  def readReplay(self, replay):
    data = base64.standard_b64decode(replay.encode("utf-8"))
    
    version = int.from_bytes(data[0:2], 'big')
    self.initialSeed = int.from_bytes(data[2:6], 'big')
    self.rng = LehmerRNG.RNG(self.initialSeed)
    self.height = int.from_bytes(data[6:8], 'big')
    self.width = int.from_bytes(data[8:10], 'big')
    replayLength = int.from_bytes(data[10:14], 'big')
    self.replay = []
    
    byteIndex = 14
    while (byteIndex < len(replay)):
      byte = int.from_bytes(data[byteIndex:byteIndex+1], 'big')
      for i in range(4):
        self.replay.append(byte & 0b11)
        byte = byte >> 2
      byteIndex += 1
    
    while len(self.replay) != replayLength:
      self.replay.pop()
    
    self.generateTile()
    for movement in self.replay:
      self.move(["up", "down", "left", "right"][movement])
      self.generateTile()
    self.playing = self.checkValidity()
  
  def addToReplay(self, move):
    m = {"up": 0, "down": 1, "left": 2, "right": 3} # direction to number
    if not move in m: return False # if direction invalid
    self.replay.append(m[move]) # add it to the replay
    return True