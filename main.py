import g2048

game = g2048.G2048(4, 4)
userInput = input("Would you like to:\n- play (any key)\n- enter a replay (r)\n- load board state (b)\n>> ")
if userInput == "r":
  game.readReplay(input("input replay >> "))
  print(game)
  quit()
elif userInput == "b":
  game.importGameState(input("input board state >> "))
game.generateTile()
print(game)

while game.checkValidity():
  x = False
  decision = None
  while not x:
    decision = None
    while not (decision in ["up", "down", "left", "right"]):
      decision = input("enter a direction (up, down, left, right) \n>> ")
    x = game.move(decision)
  game.addToReplay(decision)
  game.generateTile()
  print(game)
  print(game.exportGameState())

game.playing = False
print(f"Replay: \n{game.generateReplay()}")