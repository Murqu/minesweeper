import pyautogui, keyboard, os, mouse
import time, random, threading, multiprocessing
import json, tkinter as tk
from PIL import Image, ImageTk
from pynput.mouse import Controller, Button


def click_positions(positions):
    """"""
    for pos in positions:
        mouse.move(pos[0], pos[1])
        mouse.click()

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
            
def click_position(x, y):
    mouse = Controller()
    mouse.position = (x, y)
    mouse.click(Button.left, 1)

# Function to simulate simultaneous mouse clicks at multiple positions using multiprocessing
def multi_click(positions):
    with multiprocessing.Pool() as pool:
        pool.starmap(click_position, positions)

def get_image(screen_region=(0, 0, 1920, 1080)):
    """Takes a screenshot and returns an image"""
    
    
    number = len(os.listdir("screenshots")) + 1
    
    # screenshot = pyautogui.screenshot(f"screenshots/{number}.png", region=screen_region)
    screenshot = pyautogui.screenshot(region=screen_region)
    
    
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
        self.has_failed = False


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
            x, y = pos

            square_color = all_squares[pos]

            offsets = self.number_offsets


            # if square_color in [1, 2, 3, 4, 5, 6, 7, 8] or square_color == "empty":
            #     continue

            try:
                if color_map[get_hex(image, pos)] == "concealed":
                    continue
            except:
                self.has_failed = True
                return
            
            
            if square_color == "concealed" and color_map[get_hex(image, pos)] != "concealed":
                self.all_squares[pos] = "pending"



            for values in offsets:

                i, j, offset_color = values
                # position realtive to chosen square top corner
                temp_pos = (x+i, y+j)

                # checking if the color matches
                color = get_hex(image, temp_pos)
                if color == offset_color:
                    all_squares[pos] = offsets[values]
                    
                    break

            else:
                # if none of the offsets match we check if its an empty square
                
                colors, square_pos = self.surround_squares(pos)
                
                if colors.count("concealed") == 0 and colors.count("bomb") == 0:
                    square_color = get_hex(image, pos)
                    color_map[square_color] = "empty"
                    self.all_squares[pos] = "empty"
                    continue
                
                
                

                # Cheking if it can get new information to the colormap 
                # Runs through the possible values on the squares and checks if the current number has the two different permutations saved
                # If they have been saved then it continues
                # If they haven't been saved it breaks the loop and checks if the square is eligible for the number

                

                for value in [1, 2, 3, 4, 5, 6, 7, 8]:
                    
                    counter = 0

                    

                    for color in offsets:

                        if offsets[color] != value:
                            continue
                        
                        counter += 1

                    if counter < 2:
                        current_number = value

                    else:
                        continue

                    if current_number != 1 and colors.count("bomb") == 0:
                        continue 

                    if colors.count("concealed") == current_number - colors.count("bomb"):
                        size = self.square_size
                        all_squares[pos] = current_number
                        for i in range(size):
                            for j in range(size):
                                temp_color = get_hex(image, (x+i, y+j))

                                try:
                                    color_map[temp_color]
                                except KeyError:
                                    self.number_offsets[(i, j, temp_color)] = current_number
                                    break
                            else:
                                continue
                            break
                    
                    break
             
    def first_press(self):
        """function for the first press of the game
        (only meant to be activated once)"""


        # Clicks a random square on the grid and updates the grid
        all_squares = self.all_squares

        first_square = random.choice(list(all_squares.items()))
        pyautogui.click(first_square[0])
        pyautogui.moveTo(25, 25)
        time.sleep(1)

        
        # Checks for the transition color that appears between the numbered squares and the concealed squares
        # since it always appears in the corner we can check all corners on a numbered square to find it since no numbers reach the corner of the square
        # This color gets named "irrelevant" in the program
        image = get_image()

        for pos in all_squares:
            
            # updating the squares that changed after the game started
            try:
                color_map[get_hex(image, pos)]

            except KeyError:

                all_squares[pos] = "pending"

        for pos in all_squares:
            
            if all_squares[pos] == "concealed":
                continue

            # updating the squares that changed after the game started

            # finding the empty squares and updating the memory
            x, y = pos
            s = self.square_size
            colors, square_pos = self.surround_squares(pos)
            if colors.count("concealed") == 0:
                
                self.all_squares[pos] = "empty"
                color_map[get_hex(image, pos)] = "empty"
                continue


            # Check to make sure both variations on the empty square have been found
            temp_value = 0
            all_squares = self.all_squares
            for color in color_map:
                
                if color_map[color] != "empty":
                    continue
                temp_value += 1

            if temp_value < 2:
                continue

            # Checking all four corners of the square
            # Checking if the color is registered in the colormap
            # if it is it's the normal background color
            # if it isn't it's the transition color 
            four_corners = [(x, y),
                            (x+s, y),
                            (x, y+s),
                            (x+s, y+s)]
            
            if all_squares[pos] == "empty":
                continue
            
            for test_pos in four_corners:

                color = get_hex(image, test_pos)

                try:                
                    color_map[color]
                except KeyError:
                    color_map[color] = "irrelevant"
                    return
            
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

        #https://www.minesweeper.info/wiki/Strategy for further explanation of the strategies

        #finding bombs
        for pos in all_squares:

            square_color = all_squares[pos]

            if square_color not in [1, 2, 3, 4, 5, 6, 7, 8]:
                continue
            # the corresponding colors and position of the surrounding squares
            colors, square_pos = self.surround_squares(pos)


            #basic pattern
            if colors.count("concealed") == square_color - colors.count("bomb"):
                for i, color in enumerate(colors):

                    if color != "concealed":
                        continue
                    
                    all_squares[square_pos[i]] = "bomb"
                    # pyautogui.rightClick(square_pos[i])



            #1-1 and 1-2 pattern
            if square_color == 2:
                
                if colors.count("concealed") > 3:
                    continue
                
                temp_list = []
                
                for i, color in enumerate(colors):
                    
                    if color != 1:
                        continue
                    
                    temp_list.append(square_pos[i])
                
                for temp_pos in temp_list:
                    pass
                
                
                
                    

            


            #1-2-1 pattern
            """ if square_color == 2 or square_color - colors.count("bomb") == 2:
                
                if colors.count("concealed") > 3:
                    continue
                
                temp_list = []

                for i, color in enumerate(colors):

                    if color != "concealed":
                        continue
                    
                    temp_list.append(square_pos[i])


                val_1, val_2, val_3 = temp_list

                #checking if the concealed squares are have the same x or y value
                if val_1[0] == val_2[0] == val_3[0]:
                    x_or_y = "x"

                if val_1[1] == val_2[1] == val_3[1]:
                    x_or_y = "ý"


                if True:
                    pass

 """




            #1-2-2-1 pattern

                
        

            




        #Getting the actions
        for pos in all_squares:

            square_color = all_squares[pos]
            if square_color not in [1, 2, 3, 4, 5, 6, 7, 8]:
                continue

            colors, square_pos = self.surround_squares(pos)

            if colors.count("bomb") != square_color:
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

    def display_test(self, window=None):
        while True:
            # Calculate the total number of squares
            colors = []
            for x in self.positions:
                colors.append(self.all_squares[x])
            size = 20
            rows = self.length
            columns = self.height

    
            if window is None:

                # Create a new window
                window = tk.Tk()
                window.title("minesweeper brain")
                window.attributes("-topmost", True)
            
            else:
                # Remove the existing squares from the window
                for widget in window.winfo_children():
                    widget.destroy()
            

            # Create a grid of squares
            for i in range(rows):
                for j in range(columns):
                    index = i * columns + j
                    img_path = f"images_2/{colors[index]}.png"
                    img = Image.open(img_path)
                    img = img.resize((size, size))
                    photo = ImageTk.PhotoImage(img)
                    canvas = tk.Canvas(window, width=size, height=size, highlightthickness=0, highlightbackground="black")
                    canvas.grid(row=j, column=i)
                    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                    canvas.photo = photo
                    window.geometry(f"{size*rows}x{size*columns}+30+30")
            

            window.update()

            # Run the window
            # window.mainloop()

        

if __name__ == "__main__":
    
    
    running = True
    
    color_map = {}
    
    grid = grid_info()
    
    gui_thread = threading.Thread(target=grid.display_test)



    
    # Define first color herec
    first_color = wait_for_input("q")

    
    gui_started = False
    has_failed = False
    while running:
        
        
        updates_wo_clicks = 0
        
        


        if has_failed == True:
            color_found = False
            all_squares = grid.all_squares
            time.sleep(0.5)
            pyautogui.leftClick(list(all_squares.keys())[0])
            while not color_found:
                image = get_image()
                temp_list = []
                for pos in all_squares:
                    if get_hex(image, pos) == "4A752C":
                        #  pyautogui.click(pos)
                        temp_list.append(pos) 
                    multi_click(temp_list)
                    
                    grid.has_failed = False
                    color_found = True
                    has_failed = False
                    pyautogui.moveTo(25, 25)
                    time.sleep(0.25)
                        
                    break
                


        grid.map_out_grid(first_color)
        
        grid.first_press()


        if not gui_started:
            # gui_thread.start()
            gui_started = True
        

        updates_wo_clicks = 0


        while not has_failed:
            
            # print(grid.all_squares)
            
            
            has_failed = grid.has_failed
            if has_failed:
                break

            # actions = grid.get_actions()
            
            actions = grid.get_actions()

            

            for pos in actions:
                
                pyautogui.click(pos)
                # slight delay to minimize chance of animations obstructing the game
                
                # Square changes when clicked so gets assigned as "pending"
                grid.all_squares[pos] = "pending"

            pyautogui.moveTo(25, 25)

            if len(actions) == 0:
                time.sleep(0.7)
                grid.update_grid()
                # grid.update_grid()
                # print(grid.number_offsets)
                updates_wo_clicks += 1

            else:
                updates_wo_clicks = 0
                
                        
            if updates_wo_clicks > 3:

                click_list = []
                
                for pos in grid.all_squares:

                    if grid.all_squares[pos] == "concealed":
                        click_list.append(pos)
                
                pyautogui.click(random.choice(click_list))
                updates_wo_clicks = 0

            