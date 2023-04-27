import pyautogui, time
import keyboard, random
import ctypes, json, webbrowser
from PIL import Image
import tkinter as tk



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


class grid_info():
    def __init__(self) -> None:
        self.offset = {}
    

    def map_out_grid(self, start_color):
    
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
            #pyautogui.moveTo(pos)
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
            #pyautogui.moveTo(pos)
            #time.sleep(1)
            try:
                color_map[color]
            except:
                total_square_lenght = i
                break
        
        #höjd
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
        #ta positione av alla rutors vänstra hörn
        #gör detta tille en lista som sedan kan användas för att undersöka dem.
        for i in range(total_square_lenght):
            
            for j in range(total_square_height):
                pos = left_corner[0] + i*square_size, left_corner[1] + j*square_size

                positions_list.append(pos)
                
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
            # try:
            #     color_map[color]
            # except:

            if all_squares[pos] == "pending":

                for i in range(square_size):
                    for j in range(square_size):
                        square_pos = pos[0] + i, pos[1] + j
                        temp_color = get_hex(image, square_pos)

                        if temp_color != color:
                            break
                    else:
                        continue
                    break
                else:
                    color_map[color] = "empty"
                    all_squares[pos] = "empty"


        self.height = total_square_height
        self.length = total_square_lenght
        self.positions = positions_list
        self.square_size = square_size
        self.all_squares = all_squares
        
        #hitta övergångsfärgen mellan gröna rutor och de meedd siffror

        for i, pos in enumerate(positions_list):
            if all_squares[positions_list[i]] == "pending" and all_squares[positions_list[i + 1]] == "concealed":

                irrelevant_color = get_hex(image, (positions_list[i+1][0], positions_list[i+1][1]-1))

                color_map[irrelevant_color] = "irrelevant"
                print(irrelevant_color, "h")
                break
                
        #print(irrelevant_color)

        return self
    



    def get_surround_squares(self, pos):

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
            except:
                surrounding_colors.append("outside")


        return surrounding_colors, surrounding_pixels

    def display(self, window=None): 
        # Calculate the total number of squares
        colors = []
        for x in self.positions:
            colors.append(self.all_squares[x])
        size = 20
        rows = self.length
        columns = self.height
        
        for i,x in enumerate(colors):

            if x == "concealed":
                colors[i] = "green"
            if x == "empty":
                colors[i] = "white"
            
            if colors[i] == "pending":
                colors[i] = "gray"
            
            if colors[i] == "bomb":
                colors[i] = "black"
            
            if colors[i] == 1:
                colors[i] = "blue"


        
        if window is None:

            # Create a new window
            window = tk.Tk()
            window.title("Grid")
            window.attributes("-topmost", True)
        
        else:
            # Remove the existing squares from the window
            for widget in window.winfo_children():
                widget.destroy()
        
        # Create a grid of squares
        for i in range(rows):
            for j in range(columns):
                index = i * columns + j
                color = colors[index]
                canvas = tk.Canvas(window, width=size, height=size, bg=color, highlightthickness=1, highlightcolor="black")
                canvas.grid(row=j, column=i)
        

        window.update()

        # Run the window
        window.mainloop()

    def get_colors(self, image):
        
        color_pos = self.all_squares
        
        




        for pos in color_pos:

            if color_pos[pos] == "concealed":
                if color_map[get_hex(image, pos)] != "concealed":
                    self.all_squares[pos] = "pending"


            try:
                #print("yes")
                x1, y1 = pos
                x2, y2 = self.offset[1]
                pos_check = x1 + x2, y1 + y2
                #print(get_hex(image, pos_check))
                if color_map[get_hex(image, pos_check)] == 1:
                    self.all_squares[pos] = 1
                    #print(get_hex(image, pos_check))
            except:
                pass



            if color_pos[pos] == "pending":
                surround_colors, surround_pixels = self.get_surround_squares(pos)

                if (surround_colors.count("concealed") == 1 and surround_colors.count("bomb") == 0) or (surround_colors.count("concealed") == 0 and surround_colors.count("bomb") == 1):
                    try:
                        self.offset[1]
                        
                        x, y = pos
                        i, j = self.offset[1]
                        position = (x + i, y + j)
                        
                        color_map[get_hex(image, position)]



                        self.all_squares[pos] = 1

                        
                    except:
                        color = get_hex(image, pos)
                        x, y = pos
                        for i in range(self.square_size):
                            for j in range(self.square_size):
                                
                                position = (x + i, y + j)
                                color_temp = get_hex(image, position)
                                self.offset[1] = i, j

                                try:
                                    color_map[color_temp]

                                except:
                                    print(color_temp)
                                    self.all_squares[pos] = 1
                                    color_map[color_temp] = 1
                                    break


                            else:
                                continue
                            break


            if color_pos[pos] in [1, 2, 3, 4, 5, 6, 7, 8]:

                surround_colors, surround_pixels = self.get_surround_squares(pos)



                if surround_colors.count("concealed") - surround_colors.count("bomb") == color_pos[pos] and surround_colors.count("bomb") < color_pos[pos]:
                    
                    for i, color in enumerate(surround_colors):
                        if color == "concealed":
                            pos = surround_pixels[i]
                            self.all_squares[pos] = "bomb"

        return self 
                        
    


    def get_actions(self):
        
        
        press_list = [] 
        color_pos = self.all_squares

        for pos in color_pos:

            if color_pos[pos] in [1, 2, 3, 4, 5, 6, 7, 8]:
                
                surround_colors, surround_pixels = self.get_surround_squares(pos)

                #covered_count = surround_colors.count("concealed")
                bomb_count = surround_colors.count("bomb")
    
                           
                if color_pos[pos] - bomb_count == 0:
                    for i, color in enumerate(surround_colors):
                        if color == "concealed":

                            press_list.append(surround_pixels[i])

        
        return press_list



if __name__ == "__main__":

    running = True

    color_map = {}

    grid = grid_info()

    first_color = wait_for_input("q")

    grid.map_out_grid(first_color)

    
    image = get_image()

    for x in range(8):
        

        grid.get_colors(image)
        grid.get_colors(image)
        press_positions = grid.get_actions()

        for pos in press_positions:
            pyautogui.click(pos)
            grid.all_squares[pos] = "pending"
        pyautogui.moveTo(25, 25)

        print(len(press_positions))
        if len(press_positions) == 0:
            time.sleep(0.5)
            image = get_image()

        #break
    grid.display()
