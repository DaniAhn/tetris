import pygame
import random

# Default dimensions of the game window
SCR_WIDTH = 800
SCR_HEIGHT = 700
# Dimensions of the tetris grid
PLAY_WIDTH = 300
PLAY_HEIGHT = 600

# X, Y coordinates of the top left corner of the grid
TL_X = (SCR_WIDTH - PLAY_WIDTH) // 2
TL_Y = SCR_HEIGHT - PLAY_HEIGHT - 10
# Size of a single tile
BLOCK_SIZE = 30

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
    (12, 255, 12),
    (255, 12, 12),
    (12, 255, 255),
    (255, 255, 12),
    (12, 12, 255), 
    (255, 128, 12), 
    (255, 12, 255)
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

    def rotate_cw(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def rotate_ccw(self):
        self.rotation = (self.rotation - 1) % len(self.shape)

    def move_rgt(self):
        self.x += 1
    
    def move_lft(self):
        self.x -= 1
    
    def move_down(self):
        self.y += 1

    def move_up(self):
        self.y -= 1

def main():
    """
    Main entry point of the program.
    """
    pygame.font.init()

    win = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption("Tetris")
    game_loop(win)

def create_grid(locked={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (col, row) in locked:
                c = locked[(col, row)]
                grid[row][col] = c

    return grid

def draw_grid(surface, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(surface, grid[row][col], 
                             (TL_X + col * BLOCK_SIZE,
                              TL_Y + row * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE), 0)
    
    for row in range(len(grid)):
        pygame.draw.line(surface, (32,32,32), 
                         (TL_X, TL_Y + row * BLOCK_SIZE),
                         (TL_X + PLAY_WIDTH, TL_Y + row * BLOCK_SIZE))
        for col in range(len(grid[row])):
            pygame.draw.line(surface, (32,32,32), 
                             (TL_X + col * BLOCK_SIZE, TL_Y), 
                             (TL_X + col * BLOCK_SIZE, TL_Y + PLAY_HEIGHT))
            

def draw_window(surface, grid):
    surface.fill((0,0,0))

    font = pygame.font.SysFont("Georgia", 60)
    label = font.render("TETRIS", True, (255,255,255))

    surface.blit(label, (TL_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 20))
            
    pygame.draw.rect(surface, (128,128,128), (TL_X - 5, TL_Y - 5, 
                                              PLAY_WIDTH + 10, 
                                              PLAY_HEIGHT + 10), 5)
    
    draw_grid(surface, grid)
    pygame.display.update()

def game_loop(win):
    run = True
    global grid

    change_piece = False

    locked = {}

    clock = pygame.time.Clock()
    piece_queue = [get_shape() for x in range(5)]

    curr_piece = get_shape()

    fall_time = 0
    fall_speed = 0.27

    while run:
        grid = create_grid(locked)

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            curr_piece.y += 1
            if not valid_space(curr_piece, grid) and curr_piece.y > 0:
                curr_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    curr_piece.move_lft()
                    if not valid_space(curr_piece, grid):
                        curr_piece.move_rgt()

                if event.key == pygame.K_RIGHT:
                    curr_piece.move_rgt()
                    if not valid_space(curr_piece, grid):
                        curr_piece.move_lft()

                if event.key == pygame.K_DOWN:
                    curr_piece.move_down()
                    if not valid_space(curr_piece, grid):
                        curr_piece.move_up()

                if event.key == pygame.K_UP:
                    curr_piece.rotate_cw()
                    if not valid_space(curr_piece, grid):
                        curr_piece.rotate_ccw()

                if event.key == pygame.K_z:
                    curr_piece.rotate_ccw()
                    if not valid_space(curr_piece, grid):
                        curr_piece.rotate_cw()
                        
                if event.key == pygame.K_c:
                    pass
                if event.key == pygame.K_SPACE:
                    pass

        shape_pos = convert_shape_format(curr_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = curr_piece.colour

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked[p] = curr_piece.colour

            curr_piece = piece_queue.pop(0)
            piece_queue.append(get_shape())
            change_piece = False

        draw_window(win, grid)

    pygame.quit()

def get_shape():
    shape_index = random.randint(0, len(shapes) - 1)
    shape = Piece(5, 0, shapes[shape_index])
    return shape

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] 
                    for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False    
    return True

def convert_shape_format(shape):
    positions = []
    shape_format = shape.shape[shape.rotation]
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, col in enumerate(row):
            if col == "0":
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
        
    return False

if __name__ == "__main__":
    main()