import grid_generator as gg
import tkinter as tk
from tkinter import PhotoImage
import os

image_files = {-1:"-1.png",
          0:"0.png",
          1:"1.png",
          2:"2.png",
          3:"3.png",
          4:"4.png",
          5:"5.png",
          6:"6.png",
          7:"7.png",
          8:"8.png"}



width = int(input("width: "))
height = int(input("height: "))
mine_count = (width*height) * 0.2


CELL_SIZE = 24



def display_minesweeper_grid_window(height, width, grid):
    # Create a tkinter window
    root = tk.Tk()
    root.title("Minesweeper")

    # Load images into PhotoImage objects
    images = {key: PhotoImage(file=f"images/{image_files[key]}") for key in image_files}

    # Create a canvas to display the Minesweeper grid
    canvas = tk.Canvas(root, width=CELL_SIZE * width, height=CELL_SIZE * height)

    canvas.pack()

    # Function to close the window
    def close_window():
        root.destroy()

    # Bind the window close event to the close_window function
    root.protocol("WM_DELETE_WINDOW", close_window)

    for row in range(height):
        for col in range(width):
            cell_value = grid[row][col]
            image = images.get(cell_value)

            if image:
                canvas.create_image(col * CELL_SIZE, row * CELL_SIZE, anchor=tk.NW, image=image)
    # Run the tkinter main loop
    root.mainloop()

grid_mine_positions = gg.create_minesweeper_grid(height, width, mine_count)

# writing to txt file
with open("grid.txt", "a" ) as file:
    for temp_list in grid_mine_positions:
        temp_string = ""
        for value in temp_list:
            temp_string = f"{temp_string} {value}"

        file.writelines(temp_string)
    


for temp_list in grid_mine_positions:
    
    for i, x in enumerate(temp_list):
        
        if x == -1:
            temp_list[i] = 1


# print(len(grid_mine_positions))


visual_list = []

for x in range(len(grid_mine_positions)):
    temp_list = []
    for pos, value in enumerate(grid_mine_positions[x]):
        
        surround_value = 0
        
        if value == 1:
            temp_list.append(-1)
            continue
            
        
            # General case
        for i in range(x-1,x+2):
            
            for j in range(pos-1, pos+2):
                
                if i == -1 or j == -1:
                    continue
                
                try:
                    surround_value += grid_mine_positions[i][j]
                except IndexError:
                    pass

        

        temp_list.append(surround_value)
        
        
        
        
    
    visual_list.append(temp_list)


# print(visual_list)

def display_minesweeper_grid(grid):
    for row in grid:
        for cell in row:
            if cell == -1:
                print("!", end=" ")  # -1 represents a mine
            elif cell == 0:
                print("#", end=" ")
            else:
                print(cell, end=" ")  # Display the number of neighboring mines
        print()  # Move to the next row



display_minesweeper_grid(grid_mine_positions)
print()
display_minesweeper_grid(visual_list)
display_minesweeper_grid_window(height, width, visual_list)




