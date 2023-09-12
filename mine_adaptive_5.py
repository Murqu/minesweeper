import mouse


def click_positions(positions):
    for pos in positions:
        mouse.move(pos[0], pos[1])
        mouse.click()


if __name__ == "__main__":
    pass
    
    
    
    
    