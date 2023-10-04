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



