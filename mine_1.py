#from PIL import Image, ImageGrab
import keyboard
import pyautogui
import time, ctypes, random


def getHex(rgb):
    return "%02X%02X%02X"%rgb

def check_color(pos):

    x,y = pos
    # bbox = (x,y,x+1,y+1)
    # im = ImageGrab.grab(bbox=bbox)
    # rgbim = im.convert("RGB")
    # r,g,b = rgbim.getpixel((0,0))
    r, g, b = pyautogui.pixel(x, y)
    return getHex((r,g,b))



def get_total_grid(start_square):
    #skapar en grid för alla fyrkanter som går att klicka på
    all_positions = []
    x, y = start_square
    for width in range(20):
        
        x = start_square[0]
        if width > 0:
            #pixellängd av en fyrkant
            y += 25
        for length in range(24):
            if length > 0:
                x += 25
            all_positions.append((x,y))
    
    return all_positions      
            
def get_surrounding_grid(center_square):
    positions = []
    x, y = center_square
    
    #ändrar position till vänstra hörnet
    y -= 25
    
    for width in range(3):
        #ändrar position till vänstra hörnet
        x = center_square[0] - 25
        if width > 0:
            y += 25
        for length in range(3):
            if length > 0:
                x += 25
            positions.append((x,y))
    #tar bort mitten rutan ur listan
    positions.pop(4)

    return positions
       
            
def check_bombs(grid, number):
    bombs = 0
    
    posistions = []
    for i in grid:
        color = check_color(i)
        
        #oklickade fyrkanter
        if color == "AAD751" or color == "A2D149":
            bombs += 1
            posistions.append(i)
        
        #flaggor
        if color == "E74E12" or color == "E64D11":
            number -= 1
        
        

    print(posistions, bombs, number)
      
    if number == 0:
        return posistions, "left"
    elif number >= bombs:
        #positioner och klick commando
        return posistions, "right"
    else:
        return [], "right"


if __name__ == "__main__":
    #pyautogui.moveTo(first_square)
    
    flags_placed = 0
    
    first_square = (672, 347)
    time.sleep(3)
    counter = 0

    grid_positions = get_total_grid(first_square)
    
    pyautogui.moveTo(random.choice(grid_positions))
    pyautogui.click()
    pyautogui.moveTo(300, 400)
    running = True
    while running:
        random.shuffle(grid_positions)
        for index, i in enumerate(grid_positions):
            if keyboard.is_pressed('q'):
                running = False
                break
            color = check_color(i)
            
            if flags_placed == 99:
                for i in grid_positions:
                    pyautogui.moveTo(i)
                    pyautogui.click()

            #etta
            if color == "1976D2":
                print("one")

                surround_grid = get_surrounding_grid(i)
                pos, click_command = check_bombs(surround_grid, 1)
                
                
                    
                for pos in pos:
                    pyautogui.moveTo(pos)
                    if click_command == "right":
                    
                        pyautogui.rightClick()
                        flags_placed += 1
                    if click_command == "left":
                    
                        pyautogui.click()
                       
                    pyautogui.moveTo(300, 400)
                
                if click_command == "left":
                    grid_positions.pop(index)
                    time.sleep(0.5)
                    pass
                
            if (color == "C9B491" or color == "D6BD96") or (color == "D6B898" or color == "E4C29E"):
                print("two")
                
                surround_grid = get_surrounding_grid(i)
                pos, click_command = check_bombs(surround_grid, 2)
                
                
                for pos in pos:
                    pyautogui.moveTo(pos)
                    if click_command == "right":
                    
                        pyautogui.rightClick()
                        flags_placed += 1
                    if click_command == "left":
                    
                        pyautogui.click()
                      
                    pyautogui.moveTo(300, 400)
                    
                if click_command == "left":
                    grid_positions.pop(index)
                    time.sleep(0.5)
                    pass
                
            if (color == "D75149" or color == "D44F47") or (color == "D32F2F"):
                print("three")
                
                surround_grid = get_surrounding_grid(i)
                pos, click_command = check_bombs(surround_grid, 3)
                
                    
                
                for pos in pos:
                    pyautogui.moveTo(pos)
                    if click_command == "right":
                    
                        pyautogui.rightClick()
                        flags_placed += 1
                    if click_command == "left":
                    
                        pyautogui.click()
                    
                    pyautogui.moveTo(300, 400)
                
                if click_command == "left":
                    grid_positions.pop(index)
                    time.sleep(0.5)
                    pass
                
            if (color == "D3A7A0" or color == "C89F9B") or (color == "E3BFA0" or color == "D6B59A"):
                print("four")
                
                surround_grid = get_surrounding_grid(i)
                pos, click_command = check_bombs(surround_grid, 4)
                
                    
                for pos in pos:
                    pyautogui.moveTo(pos)
                    if click_command == "right":
                    
                        pyautogui.rightClick()
                        flags_placed += 1
                    if click_command == "left":
                    
                        pyautogui.click()
                        
                    pyautogui.moveTo(300, 400)
                
                if click_command == "left":
                    grid_positions.pop(index)
                    time.sleep(0.5)
                    pass
                    
            if color == "FF8F00":
                print("five")
                
                surround_grid = get_surrounding_grid(i)
                pos, click_command = check_bombs(surround_grid, 5)
                
                for pos in pos:
                    pyautogui.moveTo(pos)
                    if click_command == "right":
                    
                        pyautogui.rightClick()
                        flags_placed += 1
                    if click_command == "left":
                    
                        pyautogui.click()
                        
                    pyautogui.moveTo(300, 400)
                if click_command == "left":
                    grid_positions.pop(index)
                    time.sleep(0.5)
                    pass
            
            if color == "119AA7" or color == "0097A7":
                print("six")
                
                surround_grid = get_surrounding_grid(i)
                pos, click_command = check_bombs(surround_grid, 6)
                
                for pos in pos:
                    pyautogui.moveTo(pos)
                    if click_command == "right":
                    
                        pyautogui.rightClick()
                        flags_placed += 1
                    if click_command == "left":
                    
                        pyautogui.click()
                        
                    pyautogui.moveTo(300, 400)
                if click_command == "left":
                    grid_positions.pop(index)
                    time.sleep(0.5)
                    pass
                    
            if color == "E74E12" or color == "E64D11":
                print("flag")
                grid_positions.pop(index)
                        
            if color == "E5C29F" or color == "D7B899":
                print("empty")
                grid_positions.pop(index)
            
            if color == "AAD751" or color == "A2D149":
                print("green")
                counter += 1
                
                if counter > 35:
                    counter = 0
                    break
            else:
                counter = 0
            
            
            pyautogui.moveTo(i)
            # time.sleep(1)
        