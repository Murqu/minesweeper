import mine_functions as mf
import time, json, random


def get_neighbors(grid, position):
    neighbors = []
    neighbors_position =[]
    row, col = position

    # Define the possible offsets for neighboring squares
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Iterate over the offsets to get neighboring positions
    for offset_row, offset_col in offsets:
        neighbor_row = row + offset_row
        neighbor_col = col + offset_col

        # Check if the neighboring position is within the grid bounds
        if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):
            neighbors.append(grid[neighbor_row][neighbor_col])
            neighbors_position.append((neighbor_row, neighbor_col))

    return neighbors, neighbors_position



def click_square(position, current_game_state, current_game_solved):
    
    # value and position of neighboring squares
    values, pos = get_neighbors(current_game_solved, position)
    
    # If there's an empty square check the surrounding squares until all empty connecting squares and the numbered squares on the edges are opened
    for i, value in enumerate(values):
        row, column = pos[i]
        
        if value == -1:
            raise RuntimeError("something went wrong, bomb is not suppupsed to be here!")
            
        if value != 0:
            current_game_state[row][column] = current_game_solved[row][column]
            continue
        
        if current_game_state[row][column] == current_game_solved[row][column]:
            print("work")
            continue
        # print("0")
        current_game_state = click_square(pos[i], current_game_state, current_game_solved)
        
            
    
    
    return current_game_state

    





width = int(input("width: "))
height = int(input("height: "))
mine_count = (width*height) * 0.1
start = time.time()

grid_mine_positions = mf.create_minesweeper_grid(height, width, mine_count, True)


grid_cover = mf.replace_all(grid_mine_positions, "c")


game_sequence = []






# for i in range(len(grid_mine_positions)):
    
#     for j in range(len(grid_mine_positions[0])):
#         grid_cover[i][j] = grid_mine_positions[i][j]

#         game_sequence.append(copy.deepcopy(grid_cover))
        
# with open("game_grids.json", "w") as json_file:
#     json.dump(game_sequence, json_file)



# with open("game_grids.json", "r") as json_file:
#     game_sequence = json.load(json_file)



# mf.display_minesweeper_game_sequence(game_sequence)



# first_game = game_sequence[0]





first_game = grid_cover

grid_mine_positions

# print(grid_mine_positions)

start_position = (random.randint(0, len(first_game)-1), random.randint(0, len(first_game[0])-1))




first_game = click_square(start_position, first_game, grid_mine_positions)



# mf.display_minesweeper_game_sequence([first_game, first_game, first_game, first_game, first_game, first_game, first_game])
mf.display_minesweeper_game_sequence([grid_mine_positions])












# end = time.time()
# time_elapsed = end - start


# if time_elapsed < 60:
#     print(f"{round(time_elapsed, 2)} s")

# if time_elapsed > 60:
#     seconds = round(time_elapsed % 60, 2)
#     minutes = (time_elapsed - seconds)/60
#     print(f"{minutes} m {seconds} s")
   


