import mine_adaptive_4 as mfunc





if __name__ == "__main__":
    
    grid = mfunc.grid_info()
    
    
    running = True
    
    grid.start()
    while running:
        
        positions = grid.get_actions()
        
        mfunc.click_positions(positions)

    
    
    
