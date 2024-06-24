import pygame
import random

# Default dimensions of the game window
scr_width = 800
scr_height = 700
# Dimensions of the tetris grid
play_width = 300
play_height = 600

# X, Y coordinates of the top left corner of the game window
top_left_x = (scr_width - play_width) // 2
top_left_y = scr_height - play_height
# Size of a single tile
block_size = 30

# Tetris pieces represented as lists of 2D arrays with rotations
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# List of all possible shapes
shapes = [S, Z, I, O, J, L, T]
# Colours corresponding to each shape in the list order
shape_colours = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0), 
    (0, 0, 255), 
    (128, 0, 128)
]

class Piece:
    """
    Represents a Tetris piece.
    
    Attributes:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        x (int): X position of the piece in the grid.
        y (int): Y position of the piece in the grid.
        shape (list): The shape of the piece.
        colour (tuple): The colour of the piece.
        rotation (int): The current rotation of the piece.
    """
    rows = 20
    cols = 10

    def __init__(self, col: int, row: int, shape: list):
        self.x = col
        self.y = row
        self.shape = shape
        self.colour = shape_colours[shapes.index(shape)]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def move_rgt(self):
        self.x += 1
    
    def move_lft(self):
        self.x -= 1

def main():
    """
    Main entry point of the program.
    """
    pygame.font.init()

if __name__ == "__main__":
    main()