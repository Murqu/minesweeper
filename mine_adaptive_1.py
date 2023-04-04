from PIL import Image
import pyautogui, time, random
import pynput, keyboard, os
import ctypes, json, webbrowser



webbrowser.open("https://www.google.com/search?q=röj")
time.sleep(1)
keyboard.press("f11")
time.sleep(2)
for i in range(23):
    time.sleep(0.1)
    keyboard.press("tab")

keyboard.press("space")
time.sleep(0.5)
keyboard.press("tab")
keyboard.press("space")
time.sleep(0.1)
keyboard.press("down arrow")
keyboard.press("down arrow")
keyboard.press("space")


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

#finding the top corner square




color_map = {
        "1976D2": 1,
        "1B77D1": 1,
        "182633": 1,
        "A7A8A6": 1,
        "4284C5": 1,
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
        "A2D049": "unknown",
        "A4D34B": "unknown",
        "A6D44D": "unknown",
        "A8D54F": "unknown",
        }

# color_map = pickle.load(open("color_map.p", "rb"))
def file_handling(file, action, data=None):
    if action == "read":
        
        with open(file, "r") as file:
            return json.load(file)

            
    if action == "write":   
        with open(file, "w") as file:
            json.dump(data, file)



def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Function to check if a pixel is within the green range


def get_color(pos, image):
    
    """pos should be either a single tuple or a list of two tuples 
    where the first one is the top left corner and the second one is the bottom right corner
    image should be the image you want to get colors from
    """
    #print(type(pos))
    if type(pos) == tuple:
        return "{:02x}{:02x}{:02x}".format(*image.getpixel(pos)).upper()
    else:
        colors = []
        (x1, y1), (x2, y2) = pos
        for y_coord in range(y1, y2 + 1):

            for x_coord in range(x1, x2 + 1):
                colors.append("{:02x}{:02x}{:02x}".format(*image.getpixel(pos)).upper())
        
        return list(set(colors))


time.sleep(2)
screenshot = pyautogui.screenshot()
    
# Convert the screenshot to an image object
img = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())




#find top corner tile 

for x in range(screensize[0]):

    for y in range(screensize[1]):
        try:
            if color_map[get_color((x,y), img)] == "unknown":
                first_pixel = (x,y)
                top_square_color = get_color((x,y), img)

                break
        except:
            pass
    else:
        # Continue if the inner loop wasn't broken.
        continue
    # Inner loop was broken, break the outer.
    break


print(set(get_color([(0, 0), (150, 0)], img)))

quit()
colorus = []

for x in range(first_pixel[0], 1240):

    for y in range(first_pixel[1], 820):

        
        colorus.append(get_color((x,y), img))


color = list(set(colorus))


# find middle of top corner tile
x, y = first_pixel
for i in range(100):
    # print(get_color((x+i,y), img))
    #print(i)
    if get_color((x+i,y), img) != top_square_color:
        
        square_size = i
        # print(get_color((x+i,y), img))
        break
    # pyautogui.moveTo(x+i, y)
    # pyautogui.moveTo(300, 400)
    # time.sleep(0.2)

print(square_size)

length = 0
height = 0


x, y = first_pixel




#get length
for i in range(30):
    print(get_color((x+i*square_size,y), img))
    pyautogui.moveTo((x+i*square_size,y))
    pyautogui.moveTo(300, 400)
    time.sleep(0.2)
    try:

        #color_map[get_color((x+i*square_size,y), img)]
        print(color_map[get_color((x+i*square_size,y), img)])
        pass
    except:
        print(i)
        length = i
        pyautogui.moveTo(10, 10)
        break 
    
        
#get height     
for i in range(30):
    
    try:
        color_map[get_color((x,y+i*square_size), img)]
    except:
        height = i
        break
    

        
print(height, length)

pyautogui.moveTo(300, 400)