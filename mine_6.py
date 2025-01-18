from PIL import Image
import pyautogui
import PIL
# import mss kan  vara sanabbare
# Makes it faster i guess
pyautogui.PAUSE = 0.0
pyautogui.MINIMUM_DURATION = 0.0

# <div jsname="LOtDEe" class="Uobaif">{time}</div>

# top left corner x: 980, y: 524
# top right corner x: 1579, y: 524
# bottom left corner x: 980, y: 1023
# bottom right corner x: 1579, y: 1023
# region=(980, 524, 599, 499)





def get_image():
    """Takes a screenshot and returns an image"""
    

    screenshot = pyautogui.screenshot()
    
    
    image = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())
    return image

image = get_image()

def get_hex(image, pos):
    """Returns a hexcode for a pixel in a given image"""
    return "{:02x}{:02x}{:02x}".format(*image.getpixel(pos)).upper()


COLORS = {
    "light_closed" : "AAD751",
    "dark_closed" : "A2D149",
    "light_open" : "E5C29F",
    "dark_open" : "D7B899",
    }




# {num}:((x,y), {color})
NUMBERS = {

    1: ((12, 23), -1)
}



# -1: Unknwon
# 0-8: Number on square

SQUARES = {

}


for x in range(100):
    for y in range(100):
        color = get_hex(image, (x, y))
        if color == COLORS["light_square"]:
            top_left = (x,y)









# if __name__ == "__main__":
    
    
#     running = True
    
#     while running:
        
#         pass        

    
    
    
