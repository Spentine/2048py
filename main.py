import g2048

game = g2048.G2048(4, 4) # create game
userInput = input("Would you like to:\n- play (any key)\n- enter a replay (r)\n- load board state (b)\n>> ")
if userInput == "r":
  game.readReplay(input("input replay >> ")) # reads the replay into the game
  print(game) # prints the game state
  quit()
elif userInput == "b":
  game.importGameState(input("input board state >> ")) # imports the game state
game.generateTile() # generates a tile
print(game)

while game.checkValidity(): # while the game is still running
  x = False
  decision = None
  while not x:
    decision = None
    while not (decision in ["up", "down", "left", "right"]):
      decision = input("enter a direction (up, down, left, right) \n>> ")
    x = game.move(decision) # try to move a certain direction, will return True if successful
  game.addToReplay(decision) # add the decision to the replay
  game.generateTile() # generates a tile
  print(game) # prints the game state
  print(game.exportGameState()) # exports the game state

game.playing = False # redundant but whatever
print(f"Replay: \n{game.generateReplay()}") # generates replay