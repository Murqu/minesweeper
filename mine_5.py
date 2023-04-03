from PIL import Image
import pyautogui, time, random
import pynput, keyboard






def get_total_grid(start_square):
    all_positions = []
    x, y = start_square
    for height in range(20):
        
        x = start_square[0]
        if height > 0:
            y += 25
        for width in range(24):
            if width > 0:
                x += 25
            all_positions.append((x,y))
    
    outer_grid = []

    x, y = start_square
    
    for squares in range(24):
        outer_grid.append((x+squares*25,y-25))
        outer_grid.append((x+squares*25,y+25*20))
        
    
    y -= 25
    for squares in range(22):
        outer_grid.append((x-25, y+squares*25))
        
        outer_grid.append((x+25*24, y+squares*25))

    return all_positions, outer_grid


def get_pixel_colors(color_map, positions, outer):
        
    
    global running
    screenshot = pyautogui.screenshot()
    
    img = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())
    
    pixel_colors = {}
    
    for pos in outer:
        
        color = img.getpixel(pos)
        
        hex_color = "{:02x}{:02x}{:02x}".format(*color).upper()
        
        color_map[hex_color] = "outside"
        
    for pos in outer:
        positions.append(pos)
        
    for pos in positions:

        color = img.getpixel(pos)

        
        
        hex_color = "{:02x}{:02x}{:02x}".format(*color).upper()
        
        try:
            name = color_map[hex_color]
        except:
            
            running = False
            return pixel_colors

        
        
        if color_map[hex_color] in ["flag", "empty", "unknown"]:
            
            pixel_colors[pos] = name
        else:
            pixel_colors[pos] = name
    
    for pos in pixel_colors:
        
        x, y = pos
        
        spacing = 25
        
        if pixel_colors[pos] in [1, 2, 3, 4, 5, 6, 7, 8]:
            
            
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
                pixel_colors[(x-spacing, y-spacing)], # top left
                pixel_colors[(x, y-spacing)], # top
                pixel_colors[(x+spacing, y-spacing)], # top right
                pixel_colors[(x-spacing, y)], # left
                pixel_colors[(x+spacing, y)], # right
                pixel_colors[(x-spacing, y+spacing)], # bottom left
                pixel_colors[(x, y+spacing)], # bottom
                pixel_colors[(x+spacing, y+spacing)] # bottom right
            ]
            
            unknown_list = []
            
            for i, color in enumerate(surrounding_colors):
            
                if color == "unknown":
                    unknown_list.append(surrounding_pixels[i])
                    
            
            if pixel_colors[pos] - len(unknown_list) == 0:

                for pos in unknown_list:

                    pixel_colors[pos] = "flag"
    
    
    return pixel_colors

def check_surrounding_pixels(position, all_squares):
    left_list = []

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
        
        for i, pos in enumerate(flag_list):
            print(len(unknown_list))
            for j, position in enumerate(unknown_list):
                if position == pos:
                    print("j")
                    unknown_list.pop(j)

        
        
        
        if len(flag_list) == square_value:

            left_list = unknown_list
            
        
    #print(left_list)
    return left_list


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
                    
                for pos in check_surrounding_pixels(pos, color_grid):

                    if color_grid[pos] != "flag":
                        

                        done_action = True
                        pyautogui.moveTo(pos)
                        mouse = pynput.mouse.Controller()

                        mouse.press(pynput.mouse.Button.left)

                        mouse.release(pynput.mouse.Button.left)


            if not done_action:
                unknown_list = []

                for pos in color_grid:

                    if color_grid[pos] == "unknown":
                        unknown_list.append(pos)
                
                pyautogui.click(random.choice(unknown_list))
                counter = 0
            
      
        pyautogui.moveTo((300, 400))
        time.sleep(0.5)

    pyautogui.moveTo((300, 400))
    rgb = pyautogui.pixel(847,671)
    hex_color = "%02X%02X%02X"%rgb

    if hex_color == "4A752C":

        pyautogui.click(847,671)
        pyautogui.moveTo(300, 400)
        time.sleep(1)

    running = True


