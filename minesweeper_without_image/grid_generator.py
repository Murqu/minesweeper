import mine_functions as mf


width = int(input("width: "))
height = int(input("height: "))
grids = int(input("grids: "))
mine_count = (width*height) * 0.2


grid_mine_positions = [mf.create_minesweeper_grid(height, width, mine_count, True) for i in range(grids)]

# grid_mine_positions = mf.create_minesweeper_grid(height, width, mine_count, True)

mf.file_handling(grid_mine_positions, type="w")