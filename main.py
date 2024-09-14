import g2048

game = g2048.G2048(4, 4)
if (input("Would you like to play (any key) or enter a replay (r)?") == "r"):
  game.readReplay(input("input replay >>"))
  print(game)
else:
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

  game.playing = False
  print(f"Replay: \n{game.generateReplay()}")