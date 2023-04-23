import pyautogui, time
import keyboard, random
import ctypes, json, webbrowser
from PIL import Image


def file_handling(file, action, data=None):
    if action == "read":
        
        with open(file, "r") as file:
            return json.load(file)

            
    if action == "write":   
        with open(file, "w") as file:
            json.dump(data, file)

def get_image():
    screenshot = pyautogui.screenshot()
    image = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())
    return image

def get_hex(image, pos):
    return "{:02x}{:02x}{:02x}".format(*image.getpixel(pos)).upper()

def wait_for_input(start_key):
    """väntar tills startknappen är tryckt och läser sedan av färgen där musen var
    !Viktigt: håll msuen över rutan högst up i vänstar hörnet"""
    while True:
        if keyboard.is_pressed(start_key.lower()):
            pos = pyautogui.position()
            pyautogui.moveTo(25, 25)
            time.sleep(2)
            return get_hex(get_image(), pos)




color_map = {}

#hittar storleken på totala griden
#hittar storleken på varje ruta
def map_out_grid(start_color):
    
    # Tar bild, omvandlar bild till rgb värden.

    image = get_image()
    size = image.size
    # tittar på alla pixlar tills någon matchar 
    for i in range(size[0]):
        for j in range(size[1]):
            color = get_hex(image, (i, j))
            
            if color == start_color:
                                   
                left_corner = (i, j)
                
                break
        else:       
            continue
        break

    #räkna ut storleken på rutan
    square_size = None
    for i in range(200):

        pos = left_corner[0] + i, left_corner[1]
        color = get_hex(image, (pos))


        if color != start_color:
            square_size = i
            second_color = color
            break
    
    for i in [start_color, second_color]:
        color_map[i] = "concealed"


    #räkna ut antalet rutor 

    #längd
    for i in range(100):
        pos = left_corner[0] + i*square_size, left_corner[1]
        color = get_hex(image, (pos))

        try:
            color_map[color]
        except:
            total_square_size = i
            break
    
    #höjd
    for i in range(100):
        pos = left_corner[0], left_corner[1] + i*square_size
        color = get_hex(image, (pos))

        try:
            color_map[color]
        except:
            total_square_height = i
            break

    
    all_squares = {}
    #ta positione av alla rutors vänstra hörn
    #gör detta tille en lista som sedan kan användas för att undersöka dem.
    for i in range(total_square_size):
        
        for j in range(total_square_height):
            pos = left_corner[0] + i*square_size, left_corner[1] + j*square_size


            all_squares[pos] = "concealed"
    


    #extra för att starta spelet

    start_postiton = random.choice(list(all_squares))
    pyautogui.click(start_postiton)
    pyautogui.moveTo(25, 25)
    time.sleep(1)
    image = get_image()

    # hittar de rutor som inte är gröna längre och ger dem taggen pending
    for pos in all_squares:
        color = get_hex(image, pos)
        try:
            all_squares[pos] = color_map[color]
        except:
            all_squares[pos] = "pending"


    for pos in all_squares:
        color = get_hex(image, pos)
        try:
            color_map[color]
        except:

            if all_squares[pos] == "pending":

                for i in range(square_size):
                    for j in range(square_size):
                        sqaure_pos = pos[0] + i, pos[1] + j
                        temp_color = get_hex(image, sqaure_pos)

                        if temp_color != color:
                            break
                    else:
                        continue
                    break
                else:
                    color_map[color] = "empty"
                    all_squares[pos] = "empty"

    print(color_map)

    return all_squares





def get_actions(all_squares, image):
    """finds all possible actions from any given state"""
    global square_size

        

    for pos in all_squares:
        pass
        #looking at all the pixels




if __name__ == "__main__":

    start_color = wait_for_input("q")

    image = get_image()
    
    all_squares = map_out_grid(start_color)
    #print(all_squares)
    while True:
        get_actions(all_squares, image)
        break
        screenshot = pyautogui.screenshot()
        image = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())