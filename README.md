# Purpose
This project's main purpose is to provide a Python class that runs a 2048 game. This project was made to be integrated with my recreational Discord bot to provide a more interactive and fun bot.

# Attributes

`.width` (`int`)
The width, or number of columns, of the board. Given `self.board[i][j]`, `0` <= `j` < `width`.

`.height` (`int`)
The height, or number of rows, of the board. Given `self.board[i][j]`, `0` <= `i` < `height`.

`.board` (`int[][]`)
A matrix of the current board state. `0`s represent empty cells, and any numbers larger represent the number `2^n` where `n` is the value.

`.score` (`int`)
The current score of the game.

`.playing` (`bool`)
Whether the game is active and/or can be played on. It is currently redundant and doesn't do anything.

`.initialSeed` (`int`)
The seed at initialization. It may be used when generating a replay, in which case, knowing the initial seed is necessary.

`.rng` (`RNG`)
The RNG class that determines the positions of new tiles.
- `.rng.randInt(a, b)` generates a random number from `a` to `b`, inclusive.
- `.rng.randFloat()` generates a random floating point number from 0 to 1, exclusive of 1.

`.replay` (`int[]`)
Stores the replay of the past moves that occurred. Each item in the list uses different values for directions.
- `0` = `up`
- `1` = `down`
- `2` = `left`
- `3` = `right`

# Methods

`__init__(width=4, height=4, seed=None)` => `G2048`
Creates a new `G2048` instance with the specified parameters.
- `width` specifies the width, or number of columns, of the board.
- `height` specifies the height, or number of rows, of the board.
- `seed` specifies the seed for the random number generator used to generate new tiles. If left unspecified, a random value will be chosen instead.

`.generateTile()`
Generates a tile on the board with a 90% chance of it being a 2 (interally 1) and a 10% chance of it being a 4 (interally 2)

`.move(direction)` => `bool`
Will move the board's tiles in the specified direction. It will return whether any pieces have moved.
- Direction may be `up`, `down`, `left`, or `right`.

`.__str__()` => `str`
Will return a stringified representation of the board so that it's viewable in a console or terminal.

`checkValidity()` => `bool`
Determines whether it is possible to continue playing on the board; whether it is possible to make any moves.

`generateReplay()` => `str`
Will generate a replay of the entire game's history. It also includes all the data about the object itself. The resultant data is a base64-encoded string.

`readReplay(replay, simulate=True)`
Will load a replay into the object.
- `replay` will be read from as a base64-encoded string.
- If `simulate` is `True`, it will also simulate the history of the game to reach the current board state. It may be left `False` if used in conjunction with `importGameState`, which will provide the current board state anyways.

`addToReplay(direction)`
Will add the movement direction to the replay. The direction should ideally be verified to affect the board.
- Direction may be `up`, `down`, `left`, or `right`.

`exportGameState()` => `str`
Will generate a string of the entire game's data except for its history. The resultant data is a base64-encoded string.

`importGameState(gameState)`
- `gameState` will be read from as a base64-encoded string.
Will import a game state into the object. It will overwrite all values except for `self.initialSeed`, `self.playing`, and `self.replay`.

# Example

```py
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
```