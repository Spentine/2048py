# Purpose
This project's main purpose is to provide an easy-to-use Python class that runs a 2048 game. This project was made to be integrated with my recreational Discord bot to provide a more interactive and fun bot.

# Methods

`.generateTile(self)`
Generates a tile in a random position on the board. Chooses "2" 90% of the time and "4" 10% of the time.

`.__str__(self)`
Renders the board in a console-friendly manner.

`.move(self, direction)`
Moves the board in the specified direction. If the board remained the same, it will return `False`. If it moved, it returns `True`. If the specified `direction` is invalid, it will return `False`.
`direction` is in `["up", "right", "down", "left"]`

`.toString(self)`
Converts the object into a string that can be converted back into the object.

`.fromString(self, string)`
Converts the specified `string` back into an object.

`.canMove(self)`
Returns whether a movement is possible in the current board position. A use for this would be for detecting when a game is over.

# Example

```py
game = G2048() # Initialize game

while game.canMove(): # While the user can move and interact with the board
  print(game) # Display board
  print(f"Score: {game.score}") # Display score
  awaitingInput = True
  while awaitingInput: # While a move hasn't been made
    awaitingInput = not game.move(input(">> ")) # If the user moved, set awaitingInput to False and end the cycle.
  game.generateTile() # generate a new tile

# Game over
print(game)
print(f"Final Score: {game.score}")
```
