import mouse, pyautogui
import PIL, keyboard, time



def click_positions(positions):
    """"""
    for pos in positions:
        mouse.move(pos[0], pos[1])
        mouse.click()

def get_hex(image, pos):
    """Returns a hexcode for a pixel in a given image"""
    return "{:02x}{:02x}{:02x}".format(*image.getpixel(pos)).upper()

def get_image(screen_region=(0, 0, 1920, 1080)):
    """Takes a screenshot and returns an image"""
    
    
    # number = len(os.listdir("screenshots")) + 1
    
    # screenshot = pyautogui.screenshot(f"screenshots/{number}.png", region=screen_region)
    screenshot = pyautogui.screenshot(region=screen_region)
    
    
    image = PIL.Image.frombytes("RGB", screenshot.size, screenshot.tobytes())
    return image


class grid_info():
    def __init__(self) -> None:
        
        self.number_offsets = {}
        self.screen_region = []
        
        
    def start(self):
        
        
        """waits until q is pressed and takes the color that it was over
        !put the mouse in the top leftmost corner of the grid"""
        while True:
            if keyboard.is_pressed("q"):
                pos = pyautogui.position()
                pyautogui.moveTo(25, 25)
                image = get_image()
                first_color = get_hex(image, pos)
                break
            
            
        #*Mapping out grid
        
        
        #Finding the leftmost pixel of the grid
        
        for x in range(1920):
            for y in range(1080):
                color = get_hex(image, (x, y))
                if color == first_color:
                    #adding the corner position to the screen region variable
                    #to reduce screenshot size later in the program
                    self.screen_region.extend((x, y))
        
        #Calculating the side lenght of the squares
        
        #Using the leftmost corner of the grid to claculate the lenght of the square
        #Since they are squares the lenght is accurate for both sides
        for width in range(100):
            x, y = self.screen_region
            
            color = get_hex(image, (x+width, y))
            
            if color != first_color:
                square_lenght = width
                break
                
                
        
        
        
        #Calculating amount of squares and the total size of the grid
        
        
        
        
        
        
        
                
                
                
                
    def map_out_grid(self):
        pass