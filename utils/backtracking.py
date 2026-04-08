import numpy as np
import matplotlib.pyplot as plt
import os

def get_unvisited_neighbors(current_row:int, current_col:int, visited_cells:np.ndarray):
    """
    Gets unvisited neighboring cells in the four cardinal directions.
    
    Checks the North, South, West, and East neighbors of the current cell
    and returns only those that have not been visited yet.
    
    Args:
        current_row: The row index of the current cell.
        current_col: The column index of the current cell.
        visited_cells: A 2D numpy array tracking which cells have been visited.
        
    Returns:
        A list of tuples containing (row, col) coordinates of unvisited neighbors.
    """
    neighbours = []
    # North
    if (current_row-1 >= 0) and (not visited_cells[current_row-1][current_col]):
        neighbours.append((current_row - 1, current_col))
    # South
    if (current_row+1 < visited_cells.shape[0]) and (not visited_cells[current_row+1][current_col]):
        neighbours.append((current_row + 1, current_col))
    # Weast:
    if (current_col-1 >= 0) and (not visited_cells[current_row][current_col-1]):
        neighbours.append((current_row, current_col - 1))
    # East
    if (current_col+ 1 < visited_cells.shape[1]) and (not visited_cells[current_row][current_col+1]):
        neighbours.append((current_row, current_col +1))

    return neighbours
  
def backtracking(rows:int, cols:int, save_maze:bool=True):
    """
    Generates a maze using the depth-first search algorithm.
    
    Creates a perfect maze using the randomized depth-first search (DFS) algorithm,
    which expands the grid to a (2n+1)x(2m+1) format where even indices represent
    walls and odd indices represent passages. Optionally saves the maze as an image.
    
    Args:
        rows: The number of rows in the maze grid.
        cols: The number of columns in the maze grid.
        save_maze: Whether to save the generated maze as a PNG image. Defaults to True.
        
    Returns:
        A 2D numpy array representing the maze, where True indicates walls and
        False indicates passages.
    """

    # Expand the maze to a (2n+1)×(2m+1) grid where even indices 
    # are walls (True) and odd indices are passages/cells (False)
    maze = np.full((2*rows +1, 2*cols +1), True) 
    maze[1::2, 1::2] = False

    # Initialize the visited cells matrix to False.
    visited_cells = np.full((rows, cols), False)

    # Start at (0,0) and stack the position:
    visited_cells[0][0] = True
    stack = [(0,0)]# Loop while remains unvisited cells
    
    # Open exists --> Upper and lower corners
    maze[0][1] = False
    maze[2*rows][2*cols-1] = False

    # Loop until all cells have been visited.
    while stack:
        # Get current position:
        current_row, current_col = stack[-1]

        # Get its neighbours:
        neighbours = get_unvisited_neighbors(current_row, current_col, visited_cells)

        # Move through the maze logic:
        if neighbours:
            # Get next cell
            next_cell = neighbours[np.random.randint(len(neighbours))]

            # Save position
            visited_cells[next_cell[0]][next_cell[1]] = True
            stack.append(next_cell)

            # Remove the wall between cells:
            wall_row = 2 * current_row + 1 + (next_cell[0] - current_row)
            wall_col = 2 * current_col + 1 + (next_cell[1] - current_col)
            maze[wall_row][wall_col] = False
        else:
            stack.pop()

    # Plot:
    if save_maze:
        # Make directory
        os.makedirs('./Mazes', exist_ok=True)

        # Check whether the file exits already
        base = f'./Mazes/maze_{rows}x{cols}'
        path = f'{base}.png'
        i = 1
        while os.path.exists(path):
            path = f'{base}_{i}.png'
            i += 1
        # Plot
        fig, ax = plt.subplots()
        ax.imshow(maze, cmap='Grays')
        ax.axis('off')
        fig.savefig(path, bbox_inches='tight')

    return maze
    