import mine_functions as mf
import tkinter as tk
from tkinter import PhotoImage

width = int(input("width: "))
height = int(input("height: "))
mine_count = (width*height) * 0.2


grid_mine_positions = [mf.create_minesweeper_grid(height, width, mine_count, True) for x in range(100)]

mf.display_minesweeper_game_sequence(grid_mine_positions)
