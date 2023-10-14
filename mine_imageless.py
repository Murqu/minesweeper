import mine_functions as mf
import tkinter as tk
from tkinter import PhotoImage

width = int(input("width: "))
height = int(input("height: "))
mine_count = (width*height) * 0.2




grid_mine_positions = mf.create_minesweeper_grid(height, width, mine_count, True)




grid_cover = mf.replace_all(grid_mine_positions, "c")


game_sequence = []

for i in range(len(grid_mine_positions)):
    
    for j in range(len(grid_mine_positions[0])):
        grid_cover[i][j] = grid_mine_positions[i][j]
        print(grid_cover)

        game_sequence.append(grid_cover)
        


print(game_sequence)

mf.display_minesweeper_game_sequence(game_sequence)