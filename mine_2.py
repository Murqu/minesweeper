import keyboard
import pyautogui
import time, random



def checkColor(pos):

    x, y = pos

    rgb = pyautogui.pixel(x, y)
    return "%02X%02X%02X"%rgb

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
        color = checkColor(i)
        
        #oklickade fyrkanter
        if color == "AAD751" or color == "A2D149":
            bombs += 1
            posistions.append(i)
        
        #flaggor
        if color == "E74E12" or color == "E64D11":
            number -= 1
    print(posistions, bombs, number)
      
    if number == 0:
        #return posistions, "left"
        for pos in posistions:
            pyautogui.moveTo(pos)
            pyautogui.click()
            pyautogui.moveTo(300, 400)
        return True, True
    elif number >= bombs:
        #positioner och klick commando
        #return posistions, "right"
        for pos in posistions:
            pyautogui.moveTo(pos)
            pyautogui.rightClick()
            pyautogui.moveTo(300, 400)
        return False, True
    else:
        return False, False
  
def check_1_2_1(grid, pos):

    green_squares = []
    one_squares = []
    #print("hello")
    for pos in grid:
        color = checkColor(pos)
        if color == "AAD751" or color == "A2D149":
            green_squares.append(pos)
            
        if color == "E74E12" or color == "E64D11":
              return None
        
        if color == "1976D2":
            one_squares.append(pos)
    
    print(len(one_squares))
    print(len(green_squares))
    
    if len(one_squares) == 2:
      
        if len(green_squares) == 3:

            # green square row
            if (green_squares[0][0] == green_squares[1][0] == green_squares[2][0]) or (green_squares[0][1] == green_squares[1][1] == green_squares[2][1]):
                print("one")
                if one_squares[0][0] == one_squares[1][0] == pos[0]:
                    print("two")
                    difference = green_squares[0][0] - one_squares[0][0]
                    print(difference)
                    pyautogui.moveTo(one_squares[0][0] + difference, one_squares[0][1])
                    pyautogui.rightClick()
                    pyautogui.moveTo(one_squares[1][0] + difference, one_squares[1][1])
                    pyautogui.rightClick()
                
                elif one_squares[0][1] == one_squares[1][1] == pos[1]:
                    print("two")
                    difference = green_squares[0][1] - one_squares[0][1]
                    print(difference)
                    pyautogui.moveTo(one_squares[0][0], one_squares[0][1] + difference)
                    pyautogui.rightClick() 
                    pyautogui.moveTo(one_squares[1][0], one_squares[1][1] + difference)
                    pyautogui.rightClick()
                
        
  
        
      
    
    

if __name__ == "__main__":
  
    first_square = (672, 347)
    
    grid_positions = get_total_grid(first_square)
    
    pyautogui.moveTo(random.choice(grid_positions))
    #pyautogui.click()
    pyautogui.moveTo(300, 400)
    
    running = True
  
    while running:
        random.shuffle(grid_positions)
        clicked = False
      
      #basic check
        for i, position in enumerate(grid_positions):
      
            if keyboard.is_pressed('q'):
                running = False
                break
            
            color = checkColor(position)
        
            if color == "1976D2":
                print("one")
                
                surround_grid = get_surrounding_grid(position)
                cleared, clicked = check_bombs(surround_grid, 1)
                if cleared:
                    grid_positions.pop(i)
                    
            if (color == "C9B491" or color == "D6BD96") or (color == "D6B898" or color == "E4C29E"):
                print("two")
                    
                surround_grid = get_surrounding_grid(position)
                cleared, clicked = check_bombs(surround_grid, 2)
                if cleared:
                    grid_positions.pop(i)
            
            if (color == "D75149" or color == "D44F47") or (color == "D32F2F"):
                print("three")
                
                surround_grid = get_surrounding_grid(position)
                cleared, clicked = check_bombs(surround_grid, 3)
                if cleared:
                    grid_positions.pop(i)
            
            if (color == "D3A7A0" or color == "C89F9B") or (color == "E3BFA0" or color == "D6B59A"):
                print("four")
                
                surround_grid = get_surrounding_grid(position)
                
                cleared, clicked = check_bombs(surround_grid, 4)
                if cleared:
                    grid_positions.pop(i)
            
            if color == "FF8F00":
                print("five")
                
                surround_grid = get_surrounding_grid(position)
                
                cleared, clicked = check_bombs(surround_grid, 5)
                if cleared:
                    grid_positions.pop(i)
            
            if color == "119AA7" or color == "0097A7":
                print("six")
                
                surround_grid = get_surrounding_grid(position)
                
                cleared, clicked = check_bombs(surround_grid, 6)
                if cleared:
                    grid_positions.pop(i)
                    
            if color == "E74E12" or color == "E64D11":
                print("flag")
                grid_positions.pop(i)
                        
            if color == "E5C29F" or color == "D7B899":
                print("empty")
                grid_positions.pop(i)
            
            if color == "AAD751" or color == "A2D149":
                print("green")

            pyautogui.moveTo()
      
      #more advanced check
        if not True:
          print("advanced check")
          for i, position in enumerate(grid_positions):
            
              if keyboard.is_pressed('q'):
                  running = False
                  break
              
              color = checkColor(position)
              
              if (color == "C9B491" or color == "D6BD96") or (color == "D6B898" or color == "E4C29E"):
                  grid = get_surrounding_grid(position)
                  check_1_2_1(grid, position)
                  pyautogui.moveTo(position)
              
              
