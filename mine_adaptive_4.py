import pyautogui, keyboard
import time, random, threading
import json, tkinter as tk
from PIL import Image, ImageTk

def file_handling(file, action, data=None):
    """Opens a json file and either reads it or writes new data to it
    
    file: The name the file want to handle
    action: What you want to do either read or write
    data: the data to write to the file if you want to write over a file"""
    if action == "read":
        
        with open(file, "r") as file:
            return json.load(file)

            
    if action == "write":   
        with open(file, "w") as file:
            json.dump(data, file)

def get_image():
    """Takes a screenshot and returns an image"""
    screenshot = pyautogui.screenshot()
    image = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())
    return image

def get_hex(image, pos):
    """Returns a hexcode for a pixel in a given image"""
    return "{:02x}{:02x}{:02x}".format(*image.getpixel(pos)).upper()

def wait_for_input(start_key):
    """waits until q is pressed and takes the color that it was over
    !put the mouse in the top leftmost corner of the grid"""
    while True:
        if keyboard.is_pressed(start_key.lower()):
            pos = pyautogui.position()
            pyautogui.moveTo(25, 25)
            time.sleep(0.1)
            return get_hex(get_image(), pos)

class grid_info():
    def __init__(self) -> None:
        # special offset for each number as a special identifier
        
        # formatted as: (offset_x, offset_y, hexcolor):corresponding value

        self.number_offsets = {} 


    def map_out_grid(self, start_color):
        """start color is the color of the leftmost square in the grid
        
        Gets the amount of squares heightwise and lengthwise. Gets the lenght f the individual squares.
        Get the inbetween color between squares.
        """
        image = get_image()
        size = image.size
        # checks pixles staring from (0, 0) until they match the starting color
        for i in range(size[0]):
            for j in range(size[1]):
                color = get_hex(image, (i, j))
                
                if color == start_color:
                                    
                    left_corner = (i, j)
                    
                    break
            else:       
                continue
            break
        
        # calculates the size of the square
        for i in range(200):

            pos = left_corner[0] + i, left_corner[1]
            color = get_hex(image, (pos))
            #pyautogui.moveTo(pos)
            if color != start_color:
                square_size = i
                second_color = color
                break
        
        # sets every squares starting value as concealed.
        for i in [start_color, second_color]:
            color_map[i] = "concealed"
        
        
        # calcualtes the amount of squares in heght and width

        # lenght
        for i in range(100):
            pos = left_corner[0] + i*square_size, left_corner[1]
            color = get_hex(image, (pos))
            #pyautogui.moveTo(pos)
            #time.sleep(1)
            try:
                color_map[color]
            except:
                total_square_lenght = i
                break
        
        # height
        for i in range(100):
            pos = left_corner[0], left_corner[1] + i*square_size
            color = get_hex(image, (pos))
            #pyautogui.moveTo(pos)
            try:
                color_map[color]
            except:
                total_square_height = i
                break
        
        all_squares = {}
        positions_list = []
        
        # makes a list of every squares position so they can be pressed later

        for i in range(total_square_lenght):
            
            for j in range(total_square_height):
                pos = left_corner[0] + i*square_size, left_corner[1] + j*square_size

                positions_list.append(pos)
                
                all_squares[pos] = "concealed"

        self.all_squares = all_squares
        self.height = total_square_height
        self.length = total_square_lenght
        self.positions = positions_list
        self.square_size = square_size

    def update_grid(self):
        """updates the grid using by taking a screenshot and checking what has changed since the last update"""

        image = get_image()

        all_squares = self.all_squares


        for pos in all_squares:
            # checking if the sqaure should be updated
            if all_squares[pos] != "concealed" and all_squares[pos] != "pending":
                continue
            offsets = self.number_offsets

            for values in offsets:
                
                # position realtive to chosen square top corner
                temp_pos = (pos[0]+values[0], pos[1]+values[1])

                # checking if the color matches
                color = get_hex(image, temp_pos)

                if color == values[2]:
                    all_squares[pos] = offsets[values]
                    break

            else:
                # if none of the offsets match we check if its an empty square
                
                colors, square_pos = self.surround_squares(pos)

                if colors.count("concealed") != 0:
                    continue

                all_squares[pos] == "empty"
                square_color = get_hex(image, pos)
                color_map[square_color] = "empty"

    def first_press(self):
        """function for the first press of the game
        (only meant to be activated once)"""


        # Clicks a random square on the grid and updates the grid
        all_squares = self.all_squares
        first_square = random.choice(all_squares)
        pyautogui.click(first_square)
        time.sleep(0.5)

        
        # Checks for the transition color that appears between the numbered squares and the concealed squares
        # since it always appears in the corner we can check all corners on a numbered square to find it since no numbers reach the corner of the square
        # This color gets named "irrelevant" in the program
        image = get_image()
        for pos in all_squares:

            if all_squares[pos] != color_map[get_hex(image, pos)]:
                all_squares[pos] = "pending"
            else:
                continue

            x, y = pos
            s = self.square_size


            colors, square_pos = self.surround_squares(pos)

            if colors.count("concealed") == 0:
                all_squares[pos] = "empty"
                color_map[get_hex(image, pos)] = "empty"



            # Check to make sure both variations on the empty square have been found
            temp_value = 0
            for color in color_map:
                
                if color_map[color] != "empty":
                    continue
                temp_value += 1

            if temp_value < 2:
                continue
            # Checking all four corners of the square
            # Checking if the color is registered in the colormap
            # if it is it's teh normal background color
            # if it isn't it's the transition color 
            four_corners = [(x, y)
                            (x+s, y)
                            (x, y+s)
                            (x+s, y+s)]
            
            for test_pos in four_corners:

                color = get_hex(image, test_pos)

                try:                
                    color_map[color]
                except KeyError:
                    color_map[color] = "irrelevant"

            




    def surround_squares(self, pos):
        """Gets the 8 surrounding squares and their colors
        pos: the position of the sqaure you want to look at"""

        x, y = pos
        spacing = self.square_size
        colors = self.all_squares

        surrounding_pixels = [
            (x-spacing, y-spacing), # top left
            (x, y-spacing), # top
            (x+spacing, y-spacing), # top right
            (x-spacing, y), # left
            (x+spacing, y), # right
            (x-spacing, y+spacing), # bottom left
            (x, y+spacing), # bottom
            (x+spacing, y+spacing) # bottom right
        ]
        surrounding_colors = []
        for pos in surrounding_pixels:
            try:
                surrounding_colors.append(colors[pos])
            except KeyError:
                surrounding_colors.append("outside")


        return surrounding_colors, surrounding_pixels
    
    def get_actions(self):
        """Get the possible actions from the given grid state"""

        all_squares = self.all_squares

        actions = []

        for pos in all_squares:

            if all_squares[pos] == "concealed" or all_squares[pos] == "empty":
                continue

            # the corresponding colors and position of the surrounding squares
            colors, square_pos = self.surround_squares(pos)

            if colors.count("concealed") != all_squares[pos]:
                continue

            for i, color in enumerate(colors):

                if color != "concealed":
                    continue
                    
                actions.append(square_pos[i])
        
        return actions


        
    def display(self):
        """Displays the current state of the grid the computer sees"""
        # Create the main window

        height = 20
        lenght = 24

        window = tk.Tk()
        window.title("minesweeper brain")
        window.attributes("-topmost", True)
        window.geometry("550x500+0+0")

        # Create a grid frame inside the window
        grid_frame = tk.Frame(window)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights to make cells expand
        for i in range(height):
            grid_frame.rowconfigure(i, weight=1)
        for j in range(lenght):
            grid_frame.columnconfigure(j, weight=1)

        # Create a grid of colored squares inside the grid frame
        for row in range(height):
            for col in range(lenght):
                square = tk.Canvas(grid_frame, width=20, height=20, bg="blue")
                square.grid(row=row, column=col, sticky="nsew")

        # Run the main event loop
        window.mainloop()
    

if __name__ == "__main__":
    
    
    running = True
    
    color_map = {}
    
    grid = grid_info()
    
    gui_thread = threading.Thread(target=grid.display)

    # Define first color here
    first_color = wait_for_input("q")

    grid.map_out_grid(first_color)
    

    while running:

        # gui_thread.start()

        # actions = grid.get_actions()
        
        actions = grid.get_actions()

        

        for pos in actions:
            
            pyautogui.click(pos)
            # slight delay to minimize chance of animations obstructing the game
            time.sleep(0.4)
            # Square changes when clicked so gets assigned as "pending"
            grid.all_squares[pos] = "pending"
            

        if len(actions) == 0:
            grid.update_grid()

        
        # grid.display()