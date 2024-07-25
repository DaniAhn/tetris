import pygame
import random
import time

# Default dimensions of the game window
SCR_WIDTH = 800
SCR_HEIGHT = 700
# Dimensions of the tetris grid
PLAY_WIDTH = 300
PLAY_HEIGHT = 600

# X, Y coordinates of the top left corner of the grid
TL_X = (SCR_WIDTH - PLAY_WIDTH) // 2
TL_Y = SCR_HEIGHT - PLAY_HEIGHT - 10
# Size of a single tile on the grid
BLOCK_SIZE = 30

# Default piece fall speed 
FALL_SPD = 0.27

# Input delay for left/right movement and fall speed while holding DOWN key
INPUT_DEL = 0.08
FALL_DEL = 0.025

# Point bonuses awarded based on lines cleared
SGL_PTS = 100
DBL_PTS = 300
TRP_PTS = 500
TTS_PTS = 800

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

I = [['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],
     ['..0..',
      '..0..',
      '..0..',
      '..0..',
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
        shape (list[list[str]]): The shape of the piece.
        colour (tuple[int]): The colour of the piece in RGB values.
        rotation (int): The current rotation of the piece.
    """
    rows = 20
    cols = 10

    def __init__(self, col: int, row: int, shape: list[list[str]])-> None:
        """
        Initializes a new Tetris piece.

        Args:
            col (int): The initial column position of the piece.
            row (int): The initial row position of the piece.
            shape (list[list[str]]): The shape of the piece.
        """
        self.x = col
        self.y = row
        self.shape = shape
        self.colour = shape_colours[shapes.index(shape)]
        self.rotation = 0

    def rotate_cw(self)-> None:
        """
        Rotates the piece clockwise.
        """
        self.rotation = (self.rotation + 1) % len(self.shape)
        if not valid_space(self, grid):
            self.rotation = (self.rotation - 1) % len(self.shape)

    def rotate_ccw(self)-> None:
        """
        Rotates the piece counterclockwise.
        """
        self.rotation = (self.rotation - 1) % len(self.shape)
        if not valid_space(self, grid):
            self.rotation = (self.rotation + 1) % len(self.shape)

    def move_rgt(self)-> None:
        """
        Moves the piece one tile to the right.
        """
        self.x += 1
        if not valid_space(self, grid):
            self.x -= 1
    
    def move_lft(self)-> None:
        """
        Moves the piece one tile to the left.
        """
        self.x -= 1
        if not valid_space(self, grid):
            self.x += 1
    
    def move_down(self)-> None:
        """
        Moves the piece one tile down.
        """
        self.y += 1
        if not valid_space(self, grid):
            self.y -= 1

def main()-> None:
    """
    Main entry point of the program.
    """
    # Creates a pygame Surface object.
    win = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))

    pygame.font.init()
    # Sets the caption for the game window.
    pygame.display.set_caption("Tetris")
    
    game_loop(win)

def game_loop(win: pygame.Surface)-> None:
    """
    Main loop of the game. Handles all game logic.

    Args:
        win (pygame.Surface): Pygame Surface object containing the
        display contents.
    """
    run = True
    clock = pygame.time.Clock()
    score = 0

    # Global representation of the current grid.
    global grid
    # Dictionary representing locked positions in the current grid.
    locked = {}
    
    # Creates a queue for upcoming pieces and sets the current piece.
    piece_queue = [get_shape() for x in range(5)]
    curr_piece = get_shape()

    # Determines if the current piece is locked.
    locked_piece = False

    # Tracks the time elapsed since the last tile the piece has fallen.
    fall_time = 0
    # Tracks the time of the last key press for each key.
    last_key_press = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_DOWN: 0}

    while run:
        clock.tick()
        grid = create_grid(locked)

        # Updates position of the current piece.
        shape_pos = convert_shape_format(curr_piece)

        # Adds the time passed since the last loop iteration to fall_time.
        fall_time += clock.get_rawtime()
        # Descends by one tile if fall_time exceeds the FALL_SPD threshold.
        if fall_time / 1000 > FALL_SPD:
            fall_time = 0
            curr_piece.y += 1
            # Changes piece if the tile below the current piece is locked.
            if not valid_space(curr_piece, grid) and curr_piece.y > 0:
                curr_piece.y -= 1
                locked_piece = True
                                
        # Handles real-time player movement and delays.
        keys = pygame.key.get_pressed()
        curr_time = time.time()
                     
        if keys[pygame.K_LEFT]:
            # Moves current piece if elapsed time passed since last key press
            # exceeds the delay threshold.
            if curr_time - last_key_press[pygame.K_LEFT] > INPUT_DEL:
                curr_piece.move_lft()
                last_key_press[pygame.K_LEFT] = curr_time

        if keys[pygame.K_RIGHT]:
            # Moves current piece if elapsed time passed since last key press
            # exceeds the delay threshold.
            if curr_time - last_key_press[pygame.K_RIGHT] > INPUT_DEL:
                curr_piece.move_rgt()
                last_key_press[pygame.K_RIGHT] = curr_time

        if keys[pygame.K_DOWN]:
            # Moves current piece if elapsed time passed since last key press
            # exceeds the delay threshold.
            if curr_time - last_key_press[pygame.K_DOWN] > FALL_DEL:
                curr_piece.move_down()
                last_key_press[pygame.K_DOWN] = curr_time

        # Handles key press events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                # Rotates current piece clockwise.
                if event.key == pygame.K_UP:
                    curr_piece.rotate_cw()
                if not valid_space(curr_piece, grid):
                    curr_piece.rotate_ccw()

                # Rotates current piece counterclockwise.
                if event.key == pygame.K_z:
                    curr_piece.rotate_ccw()
                    if not valid_space(curr_piece, grid):
                        curr_piece.rotate_cw()
                        
                if event.key == pygame.K_c:
                    pass
                if event.key == pygame.K_SPACE:
                    pass

        # Updates grid with the position of the current piece.
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = curr_piece.colour

        if locked_piece:
            curr_piece = change_piece(curr_piece, shape_pos, 
                                      locked, piece_queue)
            rows_cleared = clear_rows(grid, locked)
            # Awards points based on number of lines cleared
            if rows_cleared == 1:
                score += SGL_PTS
            elif rows_cleared == 2:
                score += DBL_PTS
            elif rows_cleared == 3:
                score += TRP_PTS
            elif rows_cleared == 4:
                score += TTS_PTS

            locked_piece = False

        draw_window(win, grid, piece_queue, score)
        pygame.display.update

        # Ends the game upon player loss.
        if check_lost(locked):
            run = False
            pygame.display.quit()

    pygame.quit()

def create_grid(locked: dict[tuple[int], 
                             tuple[int]]={})-> list[list[tuple[int]]]:
    """
    Creates a representation of the current tetris grid.
    
    Args:
        locked (dict[tuple[int], tuple[int]]): Locked positions on the grid.
    Returns: 
        list[list[tuple[int]]]: Representation of the current grid.
    """
    # Initializes an empty grid.
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    # Assigns the correct colours to display for each locked tile.
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (col, row) in locked:
                tile = locked[(col, row)]
                grid[row][col] = tile

    return grid

def draw_grid(win: pygame.Surface, grid: list[list[tuple[int]]])-> None:
    """
    Draws the grid onto the surface.

    Args:
        win (pygame.Surface): pygame Surface object containing the 
        display contents.
        grid (list[list[tuple[int]]]): Representation of the current grid.
    """

    # Draws the grid lines for each row and column.
    for row in range(len(grid)):
        pygame.draw.line(win, (32,32,32), 
                         (TL_X, TL_Y + row * BLOCK_SIZE),
                         (TL_X + PLAY_WIDTH, TL_Y + row * BLOCK_SIZE))
        for col in range(len(grid[row])):
            pygame.draw.line(win, (32,32,32), 
                             (TL_X + col * BLOCK_SIZE, TL_Y), 
                             (TL_X + col * BLOCK_SIZE, TL_Y + PLAY_HEIGHT))

def draw_window(win: pygame.Surface, grid: list[list[tuple[int]]], 
                queue: list[Piece], score: int=0)-> None:
    """
    Draws the display for the game window.

    Args:
        win (pygame.Surface): Pygame Surface object containing the 
        display contents.
        grid (list[list[tuple[int]]]): Representation of the current grid.
        queue (list[piece]): List of pieces in the current queue.
        score (int): Current score.
    """
    # Creates a blank surface.
    win.fill((0,0,0))

    # Displays the game title.
    title_font = pygame.font.SysFont("Georgia", 60)
    title = title_font.render("TETRIS", True, (255,255,255))
    win.blit(title, (TL_X + PLAY_WIDTH / 2 - (title.get_width() / 2), 20))

    # Displays the current score.
    score_font = pygame.font.SysFont("Georgia", 30)
    score_label = score_font.render(f"SCORE: {score}", True, (255,255,255))
    win.blit(score_label, (TL_X - TL_X / 2 - score_label.get_width() / 2, TL_Y))

    # Draws each tile of the grid onto the display.
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(win, grid[row][col], 
                             (TL_X + col * BLOCK_SIZE,
                              TL_Y + row * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE), 0)
    
    # Draws the outline for the playable grid.
    pygame.draw.rect(win, (128,128,128),
                     (TL_X - 5, TL_Y - 5,
                      PLAY_WIDTH + 10, PLAY_HEIGHT + 10), 5)
    
    draw_grid(win, grid)
    display_queue(win, queue)

    pygame.display.update()

def display_queue(win: pygame.Surface, queue: list[Piece])-> None:
    """
    Draws the piece queue onto the display.

    Args:
        win (pygame.Surface): Pygame Surface object containing the 
        display contents.
        queue (list[Piece]): List of pieces in the current queue.
    """
    # X position of the queue.
    queue_pos = SCR_WIDTH - TL_X / 2

    # Creates the queue label.
    queue_font = pygame.font.SysFont("Georgia", 30)
    queue_label = queue_font.render("NEXT:", True, (255,255,255))
    win.blit(queue_label, (queue_pos - queue_label.get_width() / 2, TL_Y))

    # Variable to maintain spacing uniformity.
    spacing = 1

    # Draws the pieces in the queue onto the screen.
    for shape in queue:
        format = shape.shape[shape.rotation]
        # Adds spacing of one tile between each piece.
        spacing += 1
        for j, line in enumerate(format):
            row = list(line)
            blank_row = True
            for k, col in enumerate(row):
                if col == "0":
                    pygame.draw.rect(win, shape.colour, 
                                     (queue_pos - len(row) * BLOCK_SIZE / 2 
                                      + k * BLOCK_SIZE,
                                      TL_Y + spacing * BLOCK_SIZE, 
                                      BLOCK_SIZE, BLOCK_SIZE), 0)
                    blank_row = False
            # Increases spacing if current row is not a blank row.
            if blank_row == False:
                spacing += 1         

def get_shape()-> Piece:
    """
    Creates and returns a randomized Tetris piece.

    Returns:
        Piece: Object representing the randomly selected Tetris piece.
    """
    # Generates a random shape index.
    shape_index = random.randint(0, len(shapes) - 1)
    # Initializes shape with position at the top middle of the playable area.
    shape = Piece(5, 0, shapes[shape_index])

    return shape

def valid_space(shape: Piece, grid: list[list[tuple[int]]])-> bool:
    """
    Determines if the current shape is in a valid position on the grid.
    Args:
        grid (list[list[tuple[int]]]): Representation of the current grid.
    Returns:
        bool: Determines if the shape is in a valid position.
    """
    # Creates a list of valid positions on the board.
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] 
                    for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    # Creates a list of formatted tile positions of the current shape.
    formatted = convert_shape_format(shape)
    
    # Determines if any tile in the current shape overlaps with a locked tile.
    for pos in formatted:
        x, y = pos
        if pos not in accepted_pos:
            # Bypasses check if shape is in the starting position.
            if y > -1:
                return False
            # Determines if the tile is outside the boundary of the edges.
            elif x < 0 or x > 9:
                return False
            
    return True

def convert_shape_format(shape: Piece)-> list[tuple[int]]:
    """
    Converts the 2D array representation of the current shape to a list of 
    tile positions.

    Args: 
        shape (Piece): The shape being converted.
    Returns:
        list[tuple[int]]: List containing tuples of tile coordinates.
    """
    # Gets the 2D array representation of the current shape and rotation.
    format = shape.shape[shape.rotation]

    # Adds coordinates of each current tile to a list of tile positions.
    positions = []
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == "0":
                positions.append((shape.x + j, shape.y + i))

    # Counteracts offset of each tile.
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def change_piece(curr_piece: Piece, shape_pos: list[tuple[int]], 
                 locked: dict[tuple[int], tuple[int]], 
                 queue: list[Piece])-> Piece:
    """
    Locks the current Tetris piece on the grid and moves on to the next piece.

    Args:
        curr_piece (Piece): Current Tetris piece.
        shape_pos (list[tuple[int]]): Tile coordinates of the current piece.
        locked (dict[tuple[int], tuple[int]]): Locked positions on the grid.
        queue (list[Piece]): List of pieces in the current queue.
    Returns:
        Piece: The new current Tetris piece.
    """
    # Locks each tile in the current piece to the grid.
    for pos in shape_pos:
        p = (pos[0], pos[1])
        locked[p] = curr_piece.colour

    # Moves onto the next piece and adds a new one to the queue.
    curr_piece = queue.pop(0)
    queue.append(get_shape())

    return curr_piece

def clear_rows(grid: list[list[tuple[int]]], 
               locked: dict[tuple[int], tuple[int]])-> int:
    """
    Clears lines that have been filled.

    Args:
        grid (list[list[tuple[int]]]): Representation of the current grid.
        locked (dict[tuple[int], tuple[int]]): Locked positions on the grid.
    Returns:
        int: Number of lines cleared.
    """
    lines_cleared = []

    # Tracks which lines have been filled and adds them to lines_cleared.
    for row in range(len(grid)):
        if (0,0,0) not in grid[row]:
            lines_cleared.append(row)

    # Deletes cleared lines from locked positions.
    for line in lines_cleared:
        for col in range(len(grid[0])):
            try:
                del locked[(col, line)]
            except KeyError:
                continue

    # Moves down each row above the cleared lines.
    for line in lines_cleared:
        for row in range(line, -1, -1):
            for col in range(len(grid[0])):
                if (col, row - 1) in locked.keys():
                    new_tile = locked[(col, row - 1)]
                    locked[(col, row)] = new_tile
                    del locked[col, row - 1]
        
    return len(lines_cleared)               

def check_lost(locked: dict[tuple[int], tuple[int]])-> bool:
    """
    Determines loss state of the game.

    Args: 
        locked (dict[tuple[int], tuple[int]]): Locked positions on the grid.
    Returns: 
        bool: True if the game has been lost.
    """
    # Returns True if any locked piece exceeds the top boundary of the grid.
    for pos in locked:
        x, y = pos
        if y < 0:
            return True
        
    return False

if __name__ == "__main__":
    main()