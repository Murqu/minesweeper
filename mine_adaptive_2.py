import pyautogui, time
import keyboard, PIL
import ctypes, json, webbrowser


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


def file_handling(file, action, data=None):
    if action == "read":
        
        with open(file, "r") as file:
            return json.load(file)

            
    if action == "write":   
        with open(file, "w") as file:
            json.dump(data, file)



def color_grid():
    pass


while True:
    pass