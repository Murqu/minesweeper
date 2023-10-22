import mine_functions as mf
import time, copy

width = int(input("width: "))
height = int(input("height: "))
mine_count = (width*height) * 0.2
start = time.time()

grid_mine_positions = mf.create_minesweeper_grid(height, width, mine_count, True)


grid_cover = mf.replace_all(grid_mine_positions, "c")


# game_sequence = []


# for i in range(len(grid_mine_positions)):
    
#     for j in range(len(grid_mine_positions[0])):
#         grid_cover[i][j] = grid_mine_positions[i][j]

#         game_sequence.append(copy.deepcopy(grid_cover))
        

# mf.display_minesweeper_game_sequence(game_sequence)





end = time.time()
time_elapsed = end - start


if time_elapsed < 60:
    print(f"{round(time_elapsed, 2)} s")

if time_elapsed > 60:
    seconds = round(time_elapsed % 60, 2)
    minutes = (time_elapsed - seconds)/60
    print(f"{minutes} m {seconds} s")
   


