import pyautogui, keyboard
import time, random
import json
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
    """Takes a screenshot of the image"""
    screenshot = pyautogui.screenshot()
    image = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())
    return image

def get_hex(image, pos):
    """Returns a hexcode for a pixel in a given image"""
    return "{:02x}{:02x}{:02x}".format(*image.getpixel(pos)).upper()


class grid_info():
    def __init__(self) -> None:
        # Don't know why
        self.offset = {}

    def map_out_grid(self, startcolor):
        """start color is the color of the leftmost square in the grid
        
        Gets the amount of squares heightwise and lengthwise. Gets the lenght f the individual squares.
        Get the inbetween color between squares.
        """
        
    def surround_squares(self, pos):
        """Gets the 8 surrounding squares and their colors
        pos: the position of the sqaure you want to look at"""
        
    def get_actions(self):
        """Get the possible actions from the given grid state"""
        
    def display(self):
        """Displays the current state of the grid the computer sees"""
    

if __name__ == "__main__":
    
    running = True
    
    color_map = {}
    
    grid = grid_info()
    
    # Define first color here
    first_color = None
    
    grid.map_out_grid(first_color)
    
    image = get_image()
    
    while running:
        
        
        for pos in actions:
            pyautogui.click(pos)
            # slight delay to minimize chance of animations obstructing the game
            time.sleep(0.4)
            # Square changes when clicked so gets assigned as "pending"
            grid.all_squares[pos] = "pending"
        
        actions = grid.get_actions()
        
        if len(actions) == 0:
            image = get_image()
        
        
        grid.display()