import grid_generator as gg


width = int(input("width: "))
height = int(input("height: "))
mine_count = int(input("mine_count: "))


grid_mine_positions = gg.generate_minesweeper_grid(width, height, mine_count)

for temp_list in grid_mine_positions:
    
    for i, x in enumerate(temp_list):
        
        if x == -1:
            temp_list[i] = 1





visual_list = []

for x in range(len(grid_mine_positions)):
    temp_list = []
    for pos, value in enumerate(grid_mine_positions[x]):
        
        surround_value = 0
        
        if value == "mine":
            temp_list.append(-1)
            continue
        
        # Is top row
        elif x == 0:
            pass
    
        # Is Bottom row
        elif x == len(grid_mine_positions) - 1:
            pass
        
        # Is left egde
        elif pos == 0:
            pass
        
        # Is right edge
        elif pos == len(grid_mine_positions[x]) - 1:
            pass
            
        else:
            # General case
            for x in range(x-1,x+2):
                
                surround_value + grid_mine_positions[x][pos-1]
                surround_value + value
                surround_value + grid_mine_positions[x][pos+1]

        
        
        
        
        print(surround_value)
        
        
        
    
    visual_list.append(temp_list)
    


# for temp_list in grid_mine_positions:
#     print(temp_list)




