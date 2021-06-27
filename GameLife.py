import pygame
import random
import sys

# ----Game Settings---- #
CELL_SIZE = 10
BOARD_SIZE = (600, 600)
GRID_SIZE = BOARD_SIZE[0] // CELL_SIZE
FPS = 20

# ----Color Constants----#
WHITE = (255, 255, 255)
CYAN = (0, 150, 150)
COLOR_DICT = {1: CYAN, 0: WHITE}


def count_alive_neighbors(game_matrix, cell_row_index, cell_col_index):
    """Calculates the number of alive neighbors of a given cell (life_matrix[i][j]

    returns the amount of alive neighbors.
    """

    def cell_in_bounds(bound_row, bound_col):
        """Inner function for bounds checking,  Checks if (r,c) indexes are in bounds of grid_size.

        returns 1 if the cell is in bounds and alive (life_matrix[r][c] = 1)
        """
        inside_bounds = 0 <= bound_row < len(game_matrix) and 0 <= bound_col < len(game_matrix[bound_row])

        return inside_bounds and game_matrix[bound_row][bound_col]

    living_neighbors = 0
    # Permutes all neighbors indexes
    permutation = range(-1, 2)

    for row in permutation:
        for col in permutation:
            if not (row == 0 and col == 0):
                living_neighbors += cell_in_bounds(cell_row_index + row, cell_col_index + col)

    return living_neighbors


def determine_next_status(game_matrix, cell_row_index, cell_col_index):
    """Determines a cell (life_matrix[i][j] status (alive/dead) in the next generation.

    Function logic is based on Game of life rules specified in the doc i made.

    returns its next generation value.
    """
    alive_neighbors = count_alive_neighbors(game_matrix, cell_row_index, cell_col_index)

    neighbors_count_to_stay_alive = range(2, 4)
    neighbors_count_to_revive = 3

    if game_matrix[cell_row_index][cell_col_index]:
        return int(alive_neighbors in neighbors_count_to_stay_alive)

    return int(alive_neighbors == neighbors_count_to_revive)


def calc_next_gen(game_matrix):
    """Calculates next gen and sets new gen in life_matrix

    returns next gen matrix
    """
    next_gen = game_matrix.copy()
    for row in range(len(game_matrix)):
        for col in range(len(game_matrix)):
            next_gen[row][col] = determine_next_status(game_matrix, row, col)

    return next_gen


# ---- Pygame initials  & Game 2D list initialization ---- #
pygame.init()
pygame.display.set_caption("Game of life")
screen = pygame.display.set_mode(BOARD_SIZE)
life_matrix = [[random.randint(0, 1) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
clock = pygame.time.Clock()


def run(game_matrix):
    """"Runs the game loop until user exists via exit button.
    Draws the screen by draw function, and sets game_matrix to next_gen

    """
    paused = False
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pausing/Unpausing
                    paused = not paused
        if not paused:
            draw()
            game_matrix = calc_next_gen(game_matrix)


def draw():
    """"Fills the screen with a white background, Live cells are represented as Cyan colored cells
        Dead cells stay blank (white).

    """

    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = COLOR_DICT[life_matrix[row][col]]
            pygame.draw.rect(screen, color, pygame.Rect(row * CELL_SIZE, col * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.update()


if __name__ == '__main__':
    run(life_matrix)
