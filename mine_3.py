from PIL import Image
import pyautogui, time
import pynput, keyboard
#import Among_Us as amogus




def get_total_grid(start_square):
    #skapar en grid för alla fyrkanter som går att klicka på
    all_positions = []
    x, y = start_square
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

def get_pixel_colors(positions, outer):
    
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
            print(f"unknown color: {hex_color}, position: {pos}")
            
            quit()
        
        
        if color_map[hex_color] in ["flag", "empty", "unknown"]:
            pixel_colors[pos] = name
        else:
            pixel_colors[pos] = name
    
    # Return the dictionary of pixel colors
    return pixel_colors

def check_surrounding_pixels(position, all_squares):
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
        
        for i, color in enumerate(surrounding_colors):
            
            if color == "unknown":
                unknown_list.append(surrounding_pixels[i])
            
            elif color == "flag":
                flag_list.append(surrounding_pixels[i])
        
        if len(flag_list) == square_value and len(unknown_list) > 0:
            pyautogui.moveTo(position)
            mouse = pynput.mouse.Controller()

            # Click both left and right mouse buttons simultaneously
            mouse.press(pynput.mouse.Button.left)
            mouse.press(pynput.mouse.Button.right)
            mouse.release(pynput.mouse.Button.left)
            mouse.release(pynput.mouse.Button.right)
            pyautogui.moveTo((300, 400))
            #time.sleep(1)
            return True

        elif len(unknown_list) != 0:
            
            if square_value - len(flag_list) - len(unknown_list) == 0:
                # print(surrounding_colors)
                # print(square_value - len(flag_list) - len(unknown_list))
                # pyautogui.moveTo(position)
                # quit()
                
                for pos in unknown_list:
                    pyautogui.rightClick(pos)
                    pyautogui.moveTo((300, 400))
                    #time.sleep(1)
                    
                return True
        
        
        # 1-2-1 pattern check
        elif square_value == 2 and len(unknown_list) == 3 and len(flag_list) == 0:
            counter = 0
            ones_list = []
            # check for if unknown squares are in a row
            if unknown_list[0][0] == unknown_list[1][0] == unknown_list[2][0] or unknown_list[0][0] == unknown_list[1][0] == unknown_list[2][0]:
                
                #chek for similar value for 
            
                for i, color in enumerate(surrounding_colors):
                    if color == 1:
                        counter += 1
                        ones_list.append(surrounding_pixels[i])
                if counter >= 2:
                    pass
                    for i in range(len(ones_list) - 1):
                        if ones_list[i][0] == ones_list[i+1][0] or ones_list[i][1] == ones_list[i+1][1]:
                            return True
                    
                else:
                    pass
            
            print("1-2-1")
        
            
        
time.sleep(2)
""" time.sleep(2)

positions = get_total_grid((672, 347))

print(get_pixel_colors(positions))
 """
 
while True:
    if keyboard.is_pressed("q"):
        quit()
    grid, outer_grid = get_total_grid((672, 347))
    
    """ for x in outer_grid:
        pyautogui.moveTo(x)
        
    quit() """
    
    
    items_to_remove = []
    
    color_grid = get_pixel_colors(grid, outer_grid)
    #print(color_grid)
    for pos in color_grid:
        if keyboard.is_pressed("q"):
            quit()
        if check_surrounding_pixels(pos, color_grid):
            items_to_remove.append(pos)
            break
    for items in items_to_remove:
        color_grid.pop(items)
        
    time.sleep(1)
    #print(color_grid)
    #coolgang
    