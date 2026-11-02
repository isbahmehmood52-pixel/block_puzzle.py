# import pygame
# import random
# import sys

# # Pygame initialize karein
# pygame.init()

# # --- CONFIGURATION & CONSTANTS ---
# SCREEN_WIDTH = 500
# SCREEN_HEIGHT = 650
# GRID_SIZE = 30
# GRID_WIDTH = 10   # 10 columns
# GRID_HEIGHT = 20  # 20 rows

# # Offsets for centering grid
# GRID_OFFSET_X = 50
# GRID_OFFSET_Y = 30

# # High-Quality Neon Colors (RGB)
# COLOR_BG = (18, 18, 24)
# COLOR_GRID_BG = (28, 28, 38)
# COLOR_GRID_LINE = (40, 40, 55)
# COLOR_WHITE = (240, 240, 240)
# COLOR_PANEL = (35, 35, 48)

# # Block Colors
# SHAPE_COLORS = [
#     (0, 240, 240),   # Cyan (I)
#     (240, 240, 0),   # Yellow (O)
#     (160, 0, 240),   # Purple (T)
#     (0, 240, 0),     # Green (S)
#     (240, 0, 0),     # Red (Z)
#     (0, 0, 240),     # Blue (J)
#     (240, 160, 0)    # Orange (L)
# ]

# # Tetromino Shapes (Puzzles)
# SHAPES = [
#     [[1, 1, 1, 1]],                              # I
#     [[1, 1], [1, 1]],                            # O
#     [[0, 1, 0], [1, 1, 1]],                      # T
#     [[0, 1, 1], [1, 1, 0]],                      # S
#     [[1, 1, 0], [0, 1, 1]],                      # Z
#     [[1, 0, 0], [1, 1, 1]],                      # J
#     [[0, 0, 1], [1, 1, 1]]                       # L
# ]

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Neon Falling Block Puzzle")
# clock = pygame.time.Clock()

# # --- PIECE CLASS ---
# class Piece:
#     def __init__(self, x, y, shape):
#         self.x = x
#         self.y = y
#         self.shape = shape
#         self.color = SHAPE_COLORS[SHAPES.index(shape)]
#         self.rotation = 0

# # --- HELPER FUNCTIONS ---
# def create_grid(locked_positions={}):
#     grid = [[COLOR_GRID_BG for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
#     for (x, y), color in locked_positions.items():
#         if y >= 0:
#             grid[y][x] = color
#     return grid

# def convert_shape_format(piece):
#     positions = []
#     shape = piece.shape

#     for i, row in enumerate(shape):
#         for j, column in enumerate(row):
#             if column == 1:
#                 positions.append((piece.x + j, piece.y + i))
#     return positions

# def valid_space(piece, grid):
#     accepted_positions = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == COLOR_GRID_BG] for i in range(GRID_HEIGHT)]
#     accepted_positions = [j for sub in accepted_positions for j in sub]

#     formatted = convert_shape_format(piece)

#     for pos in formatted:
#         if pos not in accepted_positions:
#             if pos[1] >= 0:  # Allow piece to spawn above screen
#                 return False
#     return True

# def check_lost(positions):
#     for pos in positions:
#         x, y = pos
#         if y < 1:
#             return True
#     return False

# def clear_rows(grid, locked):
#     inc = 0
#     for i in range(GRID_HEIGHT - 1, -1, -1):
#         row = grid[i]
#         if COLOR_GRID_BG not in row:
#             inc += 1
#             # Delete row elements in locked
#             for j in range(GRID_WIDTH):
#                 try:
#                     del locked[(j, i)]
#                 except:
#                     continue

#     if inc > 0:
#         # Shift rows down
#         for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
#             x, y = key
#             if y < i:
#                 new_key = (x, y + inc)
#                 locked[new_key] = locked.pop(key)

#     return inc

# def rotate_shape(shape):
#     return [list(row) for row in zip(*shape[::-1])]

# def get_shape():
#     return Piece(3, 0, random.choice(SHAPES))

# # --- DRAW FUNCTIONS ---
# def draw_block(x, y, color):
#     """Draws a block with modern glossy/neon effect"""
#     rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
#     pygame.draw.rect(screen, color, rect, border_radius=4)
#     # Highlight effect at top-left corner
#     pygame.draw.rect(screen, (255, 255, 255, 80), (x + 2, y + 2, GRID_SIZE - 4, 4), border_radius=2)

# def draw_grid(grid):
#     for i in range(GRID_HEIGHT):
#         for j in range(GRID_WIDTH):
#             x = GRID_OFFSET_X + j * GRID_SIZE
#             y = GRID_OFFSET_Y + i * GRID_SIZE
            
#             if grid[i][j] != COLOR_GRID_BG:
#                 draw_block(x, y, grid[i][j])
#             else:
#                 pygame.draw.rect(screen, COLOR_GRID_BG, (x, y, GRID_SIZE, GRID_SIZE), border_radius=2)
#                 pygame.draw.rect(screen, COLOR_GRID_LINE, (x, y, GRID_SIZE, GRID_SIZE), 1, border_radius=2)

# def draw_side_panel(score, next_piece):
#     panel_x = 370
#     panel_y = 30

#     # Score Panel
#     pygame.draw.rect(screen, COLOR_PANEL, (panel_x, panel_y, 110, 100), border_radius=8)
#     font = pygame.font.SysFont("Arial", 18, bold=True)
#     score_label = font.render("SCORE", True, COLOR_WHITE)
#     score_val = font.render(str(score), True, (0, 240, 240))
#     screen.blit(score_label, (panel_x + 25, panel_y + 15))
#     screen.blit(score_val, (panel_x + 25, panel_y + 45))

#     # Next Piece Panel
#     pygame.draw.rect(screen, COLOR_PANEL, (panel_x, panel_y + 120, 110, 150), border_radius=8)
#     next_label = font.render("NEXT", True, COLOR_WHITE)
#     screen.blit(next_label, (panel_x + 30, panel_y + 135))

#     if next_piece:
#         shape = next_piece.shape
#         for i, row in enumerate(shape):
#             for j, column in enumerate(row):
#                 if column == 1:
#                     px = panel_x + 20 + j * 20
#                     py = panel_y + 170 + i * 20
#                     pygame.draw.rect(screen, next_piece.color, (px, py, 18, 18), border_radius=3)

# # --- MAIN GAME LOOP ---
# def main():
#     locked_positions = {}
#     grid = create_grid(locked_positions)

#     change_piece = False
#     run = True
#     current_piece = get_shape()
#     next_piece = get_shape()
    
#     fall_time = 0
#     fall_speed = 0.35  # Speed of piece falling
#     score = 0

#     while run:
#         grid = create_grid(locked_positions)
#         fall_time += clock.get_rawtime()
#         clock.tick()

#         # Automatic falling logic
#         if fall_time / 1000 >= fall_speed:
#             fall_time = 0
#             current_piece.y += 1
#             if not valid_space(current_piece, grid) and current_piece.y > 0:
#                 current_piece.y -= 1
#                 change_piece = True

#         # Keyboard Controls
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.display.quit()
#                 sys.exit()

#             if event.type == pygame.KEYDOWN:
#                 # Left Arrow -> Move Left
#                 if event.key == pygame.K_LEFT:
#                     current_piece.x -= 1
#                     if not valid_space(current_piece, grid):
#                         current_piece.x += 1

#                 # Right Arrow -> Move Right
#                 elif event.key == pygame.K_RIGHT:
#                     current_piece.x += 1
#                     if not valid_space(current_piece, grid):
#                         current_piece.x -= 1

#                 # Down Arrow -> Fast Fall
#                 elif event.key == pygame.K_DOWN:
#                     current_piece.y += 1
#                     if not valid_space(current_piece, grid):
#                         current_piece.y -= 1

#                 # Up Arrow -> Rotate Shape
#                 elif event.key == pygame.K_UP:
#                     rotated = rotate_shape(current_piece.shape)
#                     old_shape = current_piece.shape
#                     current_piece.shape = rotated
#                     if not valid_space(current_piece, grid):
#                         current_piece.shape = old_shape

#         shape_pos = convert_shape_format(current_piece)

#         # Draw falling piece on grid
#         for i in range(len(shape_pos)):
#             x, y = shape_pos[i]
#             if y >= 0:
#                 grid[y][x] = current_piece.color

#         # When piece touches bottom or another block
#         if change_piece:
#             for pos in shape_pos:
#                 p = (pos[0], pos[1])
#                 locked_positions[p] = current_piece.color
            
#             current_piece = next_piece
#             next_piece = get_shape()
#             change_piece = False

#             # Check for completed lines
#             cleared = clear_rows(grid, locked_positions)
#             score += cleared * 100

#         # Screen Rendering
#         screen.fill(COLOR_BG)
#         draw_grid(grid)
#         draw_side_panel(score, next_piece)
        
#         # Check Game Over
#         if check_lost(locked_positions):
#             font = pygame.font.SysFont("Arial", 40, bold=True)
#             game_over_txt = font.render("GAME OVER", True, (255, 50, 50))
#             screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 20))
#             pygame.display.update()
#             pygame.time.delay(2000)
#             run = False

#         pygame.display.update()

# # Run Game
# main()
# Second code
import pygame
import random
import sys

# ============================================================
# TETRIS JEWEL / FALLING BLOCK GAME
# ============================================================

pygame.init()

# ------------------------------------------------------------
# SCREEN
# ------------------------------------------------------------

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("Jewel Block Game")

clock = pygame.time.Clock()

# ------------------------------------------------------------
# BOARD
# ------------------------------------------------------------

COLS = 10
ROWS = 20

CELL = 30

BOARD_WIDTH = COLS * CELL
BOARD_HEIGHT = ROWS * CELL

BOARD_X = 40
BOARD_Y = 40

# ------------------------------------------------------------
# COLORS
# ------------------------------------------------------------

BLACK = (10, 10, 18)
DARK = (25, 25, 40)
GRID = (45, 45, 65)
WHITE = (245, 245, 245)
GRAY = (160, 160, 170)

RED = (235, 65, 75)
GREEN = (60, 210, 110)
BLUE = (60, 130, 240)
YELLOW = (245, 205, 60)
PURPLE = (170, 80, 230)
ORANGE = (245, 135, 45)
CYAN = (50, 210, 220)

COLORS = [
    CYAN,
    YELLOW,
    PURPLE,
    GREEN,
    RED,
    BLUE,
    ORANGE
]

# ------------------------------------------------------------
# FONTS
# ------------------------------------------------------------

font_title = pygame.font.Font(None, 45)
font_score = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 25)
font_gameover = pygame.font.Font(None, 55)


# ============================================================
# TETROMINO SHAPES
# ============================================================

SHAPES = {

    "I": [
        [
            [1, 1, 1, 1]
        ]
    ],

    "O": [
        [
            [1, 1],
            [1, 1]
        ]
    ],

    "T": [
        [
            [0, 1, 0],
            [1, 1, 1]
        ]
    ],

    "L": [
        [
            [1, 0],
            [1, 0],
            [1, 1]
        ]
    ],

    "J": [
        [
            [0, 1],
            [0, 1],
            [1, 1]
        ]
    ],

    "S": [
        [
            [0, 1, 1],
            [1, 1, 0]
        ]
    ],

    "Z": [
        [
            [1, 1, 0],
            [0, 1, 1]
        ]
    ]
}


# ============================================================
# ROTATE MATRIX
# ============================================================

def rotate_shape(shape):

    # Clockwise rotation
    return [
        list(row)
        for row in zip(*shape[::-1])
    ]


# ============================================================
# PIECE CLASS
# ============================================================

class Piece:

    def __init__(self):

        self.name = random.choice(
            list(SHAPES.keys())
        )

        self.shape = [
            row[:] for row in SHAPES[self.name][0]
        ]

        self.color = random.choice(COLORS)

        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):

        new_shape = rotate_shape(
            self.shape
        )

        old_shape = self.shape

        self.shape = new_shape

        # If rotation is impossible,
        # return old shape.
        if not valid_position(
            self,
            self.x,
            self.y
        ):

            self.shape = old_shape


# ============================================================
# BOARD
# ============================================================

board = [
    [None for _ in range(COLS)]
    for _ in range(ROWS)
]


# ============================================================
# VALID POSITION
# ============================================================

def valid_position(piece, x, y):

    for row_index, row in enumerate(
        piece.shape
    ):

        for col_index, value in enumerate(
            row
        ):

            if value == 0:
                continue

            board_x = x + col_index
            board_y = y + row_index

            # Left/right wall
            if board_x < 0:
                return False

            if board_x >= COLS:
                return False

            # Bottom
            if board_y >= ROWS:
                return False

            # Top
            if board_y < 0:
                continue

            # Existing block
            if board[board_y][board_x] is not None:
                return False

    return True


# ============================================================
# LOCK PIECE
# ============================================================

def lock_piece(piece):

    for row_index, row in enumerate(
        piece.shape
    ):

        for col_index, value in enumerate(
            row
        ):

            if value == 0:
                continue

            board_x = piece.x + col_index
            board_y = piece.y + row_index

            if (
                0 <= board_y < ROWS
                and 0 <= board_x < COLS
            ):

                board[board_y][board_x] = (
                    piece.color
                )


# ============================================================
# CLEAR COMPLETED LINES
# ============================================================

def clear_lines():

    global score
    global lines_cleared

    new_board = []

    removed = 0

    for row in board:

        # Complete row
        if all(
            cell is not None
            for cell in row
        ):

            removed += 1

        else:

            new_board.append(row)

    # Add empty rows at top
    while len(new_board) < ROWS:

        new_board.insert(
            0,
            [None for _ in range(COLS)]
        )

    # Update board
    for r in range(ROWS):

        board[r] = new_board[r]

    # Scoring
    if removed == 1:
        score += 100

    elif removed == 2:
        score += 300

    elif removed == 3:
        score += 500

    elif removed >= 4:
        score += 800

    lines_cleared += removed


# ============================================================
# DRAW BLOCK
# ============================================================

def draw_block(x, y, color):

    rect = pygame.Rect(
        x,
        y,
        CELL - 2,
        CELL - 2
    )

    # Shadow
    shadow = rect.move(2, 3)

    pygame.draw.rect(
        screen,
        (5, 5, 10),
        shadow,
        border_radius=5
    )

    # Main block
    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=5
    )

    # Bright top
    bright_color = tuple(
        min(255, c + 45)
        for c in color
    )

    highlight = pygame.Rect(
        x + 4,
        y + 4,
        CELL - 10,
        5
    )

    pygame.draw.rect(
        screen,
        bright_color,
        highlight,
        border_radius=3
    )


# ============================================================
# DRAW BOARD
# ============================================================

def draw_board():

    # Board background
    pygame.draw.rect(
        screen,
        DARK,
        (
            BOARD_X - 5,
            BOARD_Y - 5,
            BOARD_WIDTH + 10,
            BOARD_HEIGHT + 10
        ),
        border_radius=8
    )

    for row in range(ROWS):

        for col in range(COLS):

            x = BOARD_X + col * CELL
            y = BOARD_Y + row * CELL

            # Empty cell
            pygame.draw.rect(
                screen,
                GRID,
                (
                    x,
                    y,
                    CELL - 2,
                    CELL - 2
                ),
                border_radius=3
            )

            # Existing block
            if board[row][col] is not None:

                draw_block(
                    x,
                    y,
                    board[row][col]
                )


# ============================================================
# DRAW CURRENT FALLING PIECE
# ============================================================

def draw_piece(piece):

    for row_index, row in enumerate(
        piece.shape
    ):

        for col_index, value in enumerate(
            row
        ):

            if value == 0:
                continue

            x = (
                BOARD_X
                + (piece.x + col_index) * CELL
            )

            y = (
                BOARD_Y
                + (piece.y + row_index) * CELL
            )

            if piece.y + row_index >= 0:

                draw_block(
                    x,
                    y,
                    piece.color
                )


# ============================================================
# GHOST PIECE
# ============================================================

def get_drop_distance(piece):

    distance = 0

    while valid_position(
        piece,
        piece.x,
        piece.y + distance + 1
    ):

        distance += 1

    return distance


def draw_ghost(piece):

    distance = get_drop_distance(
        piece
    )

    ghost_color = (
        piece.color[0] // 3,
        piece.color[1] // 3,
        piece.color[2] // 3
    )

    for row_index, row in enumerate(
        piece.shape
    ):

        for col_index, value in enumerate(
            row
        ):

            if value == 0:
                continue

            x = (
                BOARD_X
                + (
                    piece.x
                    + col_index
                ) * CELL
            )

            y = (
                BOARD_Y
                + (
                    piece.y
                    + row_index
                    + distance
                ) * CELL
            )

            rect = pygame.Rect(
                x,
                y,
                CELL - 2,
                CELL - 2
            )

            pygame.draw.rect(
                screen,
                ghost_color,
                rect,
                2,
                border_radius=4
            )


# ============================================================
# NEXT PIECE
# ============================================================

next_piece = Piece()


def draw_next_piece():

    text = font_small.render(
        "NEXT",
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            BOARD_X
            + BOARD_WIDTH
            + 25,
            170
        )
    )

    preview_x = (
        BOARD_X
        + BOARD_WIDTH
        + 20
    )

    preview_y = 210

    preview_cell = 20

    for row_index, row in enumerate(
        next_piece.shape
    ):

        for col_index, value in enumerate(
            row
        ):

            if value == 0:
                continue

            rect = pygame.Rect(
                preview_x
                + col_index * preview_cell,

                preview_y
                + row_index * preview_cell,

                preview_cell - 2,
                preview_cell - 2
            )

            pygame.draw.rect(
                screen,
                next_piece.color,
                rect,
                border_radius=4
            )


# ============================================================
# SCORE DISPLAY
# ============================================================

def draw_information():

    title = font_title.render(
        "JEWEL BLOCK",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            BOARD_X,
            8
        )
    )

    score_text = font_score.render(
        f"Score: {score}",
        True,
        YELLOW
    )

    screen.blit(
        score_text,
        (
            BOARD_X
            + BOARD_WIDTH
            + 15,
            80
        )
    )

    lines_text = font_small.render(
        f"Lines: {lines_cleared}",
        True,
        WHITE
    )

    screen.blit(
        lines_text,
        (
            BOARD_X
            + BOARD_WIDTH
            + 15,
            115
        )
    )

    controls = [
        "CONTROLS",
        "",
        "LEFT  = Move Left",
        "RIGHT = Move Right",
        "UP    = Rotate",
        "DOWN  = Fast Down",
        "",
        "SPACE = Drop",
        "",
        "P = Pause",
        "R = Restart"
    ]

    y = 300

    for text in controls:

        rendered = font_small.render(
            text,
            True,
            GRAY
        )

        screen.blit(
            rendered,
            (
                BOARD_X
                + BOARD_WIDTH
                + 15,
                y
            )
        )

        y += 27


# ============================================================
# GAME OVER SCREEN
# ============================================================

def draw_game_over():

    overlay = pygame.Surface(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 190)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    text = font_gameover.render(
        "GAME OVER",
        True,
        RED
    )

    rect = text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50
        )
    )

    screen.blit(
        text,
        rect
    )

    score_text = font_score.render(
        f"Score: {score}",
        True,
        WHITE
    )

    rect2 = score_text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 10
        )
    )

    screen.blit(
        score_text,
        rect2
    )

    restart = font_score.render(
        "Press R to Restart",
        True,
        GREEN
    )

    rect3 = restart.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 65
        )
    )

    screen.blit(
        restart,
        rect3
    )


# ============================================================
# PAUSE SCREEN
# ============================================================

def draw_pause():

    overlay = pygame.Surface(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 150)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    text = font_gameover.render(
        "PAUSED",
        True,
        WHITE
    )

    rect = text.get_rect(
        center=(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
    )

    screen.blit(
        text,
        rect
    )


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global board
    global current_piece
    global next_piece
    global score
    global lines_cleared
    global game_over
    global paused
    global fall_timer

    board = [
        [None for _ in range(COLS)]
        for _ in range(ROWS)
    ]

    score = 0
    lines_cleared = 0

    game_over = False
    paused = False

    fall_timer = 0

    current_piece = Piece()
    next_piece = Piece()


# ============================================================
# GAME VARIABLES
# ============================================================

score = 0
lines_cleared = 0

fall_timer = 0

fall_speed = 500

game_over = False
paused = False

current_piece = Piece()


# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:

    dt = clock.tick(60)

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # Quit
            if event.key == pygame.K_ESCAPE:

                running = False

            # Restart
            if event.key == pygame.K_r:

                reset_game()

            if game_over:
                continue

            # Pause
            if event.key == pygame.K_p:

                paused = not paused

            if paused:
                continue

            # ------------------------------------------------
            # LEFT
            # ------------------------------------------------

            if event.key == pygame.K_LEFT:

                if valid_position(
                    current_piece,
                    current_piece.x - 1,
                    current_piece.y
                ):

                    current_piece.x -= 1

            # ------------------------------------------------
            # RIGHT
            # ------------------------------------------------

            elif event.key == pygame.K_RIGHT:

                if valid_position(
                    current_piece,
                    current_piece.x + 1,
                    current_piece.y
                ):

                    current_piece.x += 1

            # ------------------------------------------------
            # DOWN
            # ------------------------------------------------

            elif event.key == pygame.K_DOWN:

                if valid_position(
                    current_piece,
                    current_piece.x,
                    current_piece.y + 1
                ):

                    current_piece.y += 1

                    score += 1

            # ------------------------------------------------
            # ROTATE
            # ------------------------------------------------

            elif event.key == pygame.K_UP:

                current_piece.rotate()

            # ------------------------------------------------
            # HARD DROP
            # ------------------------------------------------

            elif event.key == pygame.K_SPACE:

                distance = get_drop_distance(
                    current_piece
                )

                current_piece.y += distance

                score += distance * 2

                lock_piece(
                    current_piece
                )

                clear_lines()

                current_piece = next_piece
                next_piece = Piece()

                # Check game over
                if not valid_position(
                    current_piece,
                    current_piece.x,
                    current_piece.y
                ):

                    game_over = True

    # --------------------------------------------------------
    # GAME UPDATE
    # --------------------------------------------------------

    if not game_over and not paused:

        fall_timer += dt

        # Automatic falling
        if fall_timer >= fall_speed:

            fall_timer = 0

            if valid_position(
                current_piece,
                current_piece.x,
                current_piece.y + 1
            ):

                current_piece.y += 1

            else:

                # Piece reaches bottom
                lock_piece(
                    current_piece
                )

                clear_lines()

                # New piece
                current_piece = next_piece
                next_piece = Piece()

                # Game over check
                if not valid_position(
                    current_piece,
                    current_piece.x,
                    current_piece.y
                ):

                    game_over = True

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    screen.fill(BLACK)

    draw_board()

    if not game_over:

        draw_ghost(
            current_piece
        )

        draw_piece(
            current_piece
        )

    draw_information()

    draw_next_piece()

    if paused and not game_over:

        draw_pause()

    if game_over:

        draw_game_over()

    pygame.display.flip()


pygame.quit()
sys.exit()