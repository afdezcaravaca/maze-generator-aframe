from utils.backtracking import backtracking
from utils.maze_to_html import maze_to_html

# ============== CONFIGURATION ==============
# Modify these values to change the maze dimensions
ROWS = 30  # Number of rows in the maze
COLS = 30  # Number of columns in the maze
SAVE_MAZE = True # Whether to save the generated maze or not.

# ============== MAZE GENERATION ==============
# Do not modify the code below - it generates and exports the maze
maze = backtracking(ROWS, COLS)
maze_to_html(maze, ROWS, COLS)