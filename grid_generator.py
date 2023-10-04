import random

def generate_minesweeper_grid(width, height, mine_count):
    grid = [[0] * width for _ in range(height)]

    def dfs(x, y):
        if grid[y][x] != 0:
            return
        
        grid[y][x] = -1  # Place a mine in the current cell

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if grid[ny][nx] != -1:
                        grid[ny][nx] += 1

        directions = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                dfs(nx, ny)

    # Randomly select a starting point
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    dfs(start_x, start_y)

    # Place remaining mines randomly
    placed_mines = 1
    while placed_mines < mine_count:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if grid[y][x] == 0:
            grid[y][x] = -1
            placed_mines += 1

    return grid


def create_minesweeper_grid(rows, cols, num_mines):
    # Initialize an empty grid filled with zeros
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Randomly place a portion of mines to ensure solvability
    initial_mines = int(0.1 * rows * cols)  # 10% of the total cells
    for _ in range(initial_mines):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        grid[row][col] = -1  # Place a mine

    # Calculate the number of remaining mines to place
    remaining_mines = num_mines - initial_mines

    # Randomly place the remaining mines while avoiding marked safe cells
    while remaining_mines > 0:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        # Check if the cell is already a mine or a marked safe cell
        if grid[row][col] == -1 or grid[row][col] > 0:
            continue

        grid[row][col] = -1  # Place a mine
        remaining_mines -= 1

    return grid
