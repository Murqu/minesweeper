from PIL import Image
import pyautogui, time, random
import pynput, keyboard
#import Among_Us as amogus
import ctypes, tempfile
ctypes.windll.user32.SetProcessDPIAware()



def get_total_grid(start_square):
    
    

    
    
    #skapar en grid för alla fyrkanter som går att klicka på
    all_positions = []
    x, y = start_square
    spacing = 25
    for height in range(20):
        
        x = start_square[0]
        if height > 0:
            #pixellängd av en fyrkant
            y += 25
        for width in range(24):
            if width > 0:
                x += 25
            all_positions.append((x,y))
    
    outer_grid = []
    #top and bottom row

    x, y = start_square
    
    for squares in range(24):
        #top row
        outer_grid.append((x+squares*25,y-25))
        #bottom row
        outer_grid.append((x+squares*25,y+25*20))
        
    
    #both down rows without top square and bottom square
    y -= 25
    for squares in range(22):
        outer_grid.append((x-25, y+squares*25))
        
        outer_grid.append((x+25*24, y+squares*25))

    return all_positions, outer_grid


def get_pixel_colors(color_map, positions, outer):
        
    #global because I'm lazy
    
    global running
    # Take a screenshot of the current screen
    screenshot = pyautogui.screenshot()
    
    # Convert the screenshot to an image object
    img = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
    
    # Create an empty dictionary to store the pixel colors
    pixel_colors = {}
    
    for pos in outer:
        
        color = img.getpixel(pos)
        
        # Convert the color value to a hex string and add it to the dictionary
        hex_color = '{:02x}{:02x}{:02x}'.format(*color).upper()
        
        color_map[hex_color] = "outside"
        
    for pos in outer:
        positions.append(pos)
        
    # Loop through each pixel position and get the color value
    for pos in positions:
        # Get the color value at the current position

        color = img.getpixel(pos)

        
        
        # Convert the color value to a hex string and add it to the dictionary
        hex_color = '{:02x}{:02x}{:02x}'.format(*color).upper()
        
        try:
            name = color_map[hex_color]
        except:
            #print(f"unknown color: {hex_color}, position: {pos}")
            running = False
            return pixel_colors
            #quit()
        
        
        if color_map[hex_color] in ["flag", "empty", "unknown"]:
            pixel_colors[pos] = name
        else:
            pixel_colors[pos] = name
    
    # Return the dictionary of pixel colors
    return pixel_colors


def check_surrounding_pixels(position, all_squares):
    left_list = []
    right_list = []
    if all_squares[position] in [1, 2, 3, 4, 5, 6, 7, 8]:
        x, y = position
        
        square_value = all_squares[position]
        
        spacing = 25
        
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
        
        surrounding_colors = [
            all_squares[(x-spacing, y-spacing)], # top left
            all_squares[(x, y-spacing)], # top
            all_squares[(x+spacing, y-spacing)], # top right
            all_squares[(x-spacing, y)], # left
            all_squares[(x+spacing, y)], # right
            all_squares[(x-spacing, y+spacing)], # bottom left
            all_squares[(x, y+spacing)], # bottom
            all_squares[(x+spacing, y+spacing)] # bottom right
        ]
        #print(surrounding_colors)
        
        unknown_list = []
        flag_list = []
        
        #list for left and right clicks
        
        
        for i, color in enumerate(surrounding_colors):
            
            if color == "unknown":
                unknown_list.append(surrounding_pixels[i])
            
            elif color == "flag":
                flag_list.append(surrounding_pixels[i])
        
        if len(flag_list) == square_value and len(unknown_list) > 0:
            #pyautogui.moveTo(position)
            left_list.append(position)
            #mouse = pynput.mouse.Controller()

            # Click both left and right mouse buttons simultaneously
            #mouse.press(pynput.mouse.Button.left)
            #mouse.press(pynput.mouse.Button.right)
            #mouse.release(pynput.mouse.Button.left)
            #mouse.release(pynput.mouse.Button.right)
            #pyautogui.moveTo((300, 400))
            #time.sleep(1)
            #return True

        elif len(unknown_list) != 0:
            
            if square_value - len(flag_list) - len(unknown_list) == 0:

                
                for pos in unknown_list:
                    right_list.append(pos)
                    #pyautogui.rightClick(pos)
                    #pyautogui.moveTo((300, 400))
                    #time.sleep(1)
                    
                #return True
        
        if square_value == 2:
            x, y = position
            square_value = all_squares[position]
            
            spacing = 25

            
            top_row_color = [all_squares[(x-spacing, y-spacing)], # top left
                all_squares[(x, y-spacing)], # top
                all_squares[(x+spacing, y-spacing)], # top right
                ]
            
            middle_row_color = [
                all_squares[(x-spacing, y)], # left
                all_squares[(x+spacing, y)], # right
            ]
            
            bottom_row_color = [
                all_squares[(x-spacing, y+spacing)], # bottom left
                all_squares[(x, y+spacing)], # bottom
                all_squares[(x+spacing, y+spacing)] # bottom right
            ]
            
            flags = False
            
            top = 0
            
            middle = 0
            
            bottom = 1
            
            for color in top_row_color:
                if color == "unknown":
                    top += 1
                
                if color == "flag":
                    flags = True
            
            for color in bottom_row_color:
                if color == "unknown":
                    bottom += 1
                
                if color == "flag":
                    flags = True
            
            for color in middle_row_color:
                if color == 1:
                    middle += 1
                
                if color == "flag":
                    flags = True
            
            if not flags:
                
                if middle == 2:
                    
                    if top == 3 and bottom == 0:
                        pyautogui.click((x,y-spacing))
                        print("1_2_1")

                    if bottom == 3 and top == 0:
                        pyautogui.click((x,y+spacing))
                        print("1_2_1")
        
        
        if square_value == 1:
            
            
            """ top_row_pos = [
                (x-spacing, y-spacing), # top left
                (x, y-spacing), # top
                (x+spacing, y-spacing), # top right
            ]
            
            middle_row_pos = [
                (x-spacing, y), # left
                (x+spacing, y), # right
            ]
            
            bottom_row_color = [
                (x-spacing, y+spacing), # bottom left
                (x, y+spacing), # bottom
                (x+spacing, y+spacing) # bottom right
            ]
            
            top_row_color = [all_squares[(x-spacing, y-spacing)], # top left
                all_squares[(x, y-spacing)], # top
                all_squares[(x+spacing, y-spacing)], # top right
                ]
            
            middle_row_color = [
                all_squares[(x-spacing, y)], # left
                all_squares[(x+spacing, y)], # right
            ]
            
            bottom_row_color = [
                all_squares[(x-spacing, y+spacing)], # bottom left
                all_squares[(x, y+spacing)], # bottom
                all_squares[(x+spacing, y+spacing)] # bottom right
            ]

            for color in top_row_color:
                if color == "outside":
                    top += 1
                
                if color == "flag":
                    flags = True
            
            for color in bottom_row_color:
                if color == "outside":
                    bottom += 1
                
                if color == "flag":
                    flags = True
            
            for color in middle_row_color:
                if color == 1:
                    middle += 1
                
                if color == "flag":
                    flags = True     """
        
        
        
    return left_list, right_list

counter = 0
running = True

while True:

    while running:
        
        
        color_map = {
        "1976D2": 1,
        "1B77D1": 1,
        "182633": 1,
        "C9B491": 2,
        "D6BD96": 2,
        "D6B898": 2,
        "E4C29E": 2,
        "D75149": 3,
        "D44F47": 3,
        "D32F2F": 3,
        "D3A7A0": 4,
        "C89F9B": 4,
        "E3BFA0": 4,
        "D6B59A": 4,
        "FF8F00": 5,
        "119AA7": 6,
        "0097A7": 6,
        "AB957F": 7,
        "B59C83": 7,
        "E74E12": "flag",
        "E64D11": "flag",
        "EA5019": "flag",
        "E74A0F": "flag",
        "E5C29F": "empty",
        "D7B899": "empty",
        "AAD751": "unknown",
        "A2D149": "unknown",
        "AAD651": "unknown",
        "A6CF4E": "unknown",
        "A2D049": "unknown"
        }
        
        done_action = False
        
        left_click = []
        right_click = []
        if keyboard.is_pressed("q"):
            quit()
            
        grid, outer_grid = get_total_grid((672, 347))
        
        
        color_grid = get_pixel_colors(color_map, grid, outer_grid)
        if running:
            for pos in color_grid:
                if keyboard.is_pressed("q"):
                    quit()
                left, right = check_surrounding_pixels(pos, color_grid)
                
                for pos in left:
                    left_click.append(pos)
                    
                for pos in right:
                    
                    right_click.append(pos)
            
            right_click = list(set(right_click))
            random.shuffle(left_click)
            
            for pos in left_click:
                #print("yes")
                done_action = True
                pyautogui.moveTo(pos)
                mouse = pynput.mouse.Controller()

                # Click both left and right mouse buttons simultaneously
                mouse.press(pynput.mouse.Button.left)
                mouse.press(pynput.mouse.Button.right)
                mouse.release(pynput.mouse.Button.left)
                mouse.release(pynput.mouse.Button.right)
            
            for pos in right_click:
                
                done_action = True
                pyautogui.moveTo(pos)
                mouse = pynput.mouse.Controller()
                mouse.press(pynput.mouse.Button.right)
                mouse.release(pynput.mouse.Button.right)
            
            if not done_action:
                counter += 1
            
            if counter == 1:
                unknown_list = []
                #print("yes")
                #print(color_grid)
                for pos in color_grid:
                    #print(color_grid[pos])
                    if color_grid[pos] == "unknown":
                        unknown_list.append(pos)
                
                pyautogui.click(random.choice(unknown_list))
                counter = 0
            
      
        pyautogui.moveTo((300, 400))
        time.sleep(0.5)

    pyautogui.moveTo((300, 400))
    rgb = pyautogui.pixel(847,671)
    hex_color = "%02X%02X%02X"%rgb
    #print(hex_color)    
    if hex_color == "4A752C":
        #print("Hello")
        pyautogui.click(847,671)
        pyautogui.moveTo(300, 400)
        time.sleep(1)
    #keyboard.press("space")
    running = True
    

