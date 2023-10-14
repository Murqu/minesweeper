import mine_functions as mf
import tkinter as tk
from tkinter import PhotoImage

width = int(input("width: "))
height = int(input("height: "))
mine_count = (width*height) * 0.2




grid_mine_positions = mf.create_minesweeper_grid(height, width, mine_count, True)

print(grid_mine_positions)


grid_copy = grid_mine_positions



grid_cover = mf.replace_all(grid_copy, "c")

print(grid_mine_positions)

game_sequence = []

temp_list = grid_cover
print(temp_list)
for i in range(len(game_sequence)):
    
    for j in range(len(game_sequence[0])):
        
        temp_list[i][j] = grid_mine_positions[i][j]
        game_sequence.append(temp_list)


print(game_sequence)

mf.display_minesweeper_game_sequence(game_sequence)