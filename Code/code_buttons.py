import board
import time
from debounced_buttons import DebouncedButtons

button_map = {
    "Encoder": board.GP0,
    "Button_A": board.GP1,
    "Button_B": board.GP2,
    "Button_C": board.GP3,
    "Button_D": board.GP4,
    "Button_E": board.GP5,
    "Button_F": board.GP6,
    "Button_G": board.GP7,
    "Button_H": board.GP8,
    "Button_I": board.GP9,
}

buttons = DebouncedButtons(button_map, debounce_time=0.02, hold_time=1.5)

while True:
    buttons.update()
    for name in button_map:
        if buttons.held(name):
            print(f"Taste {name} wird gehalten!")
        if buttons.pressed(name):
            print(f"Taste {name} wurde gedrückt!")
        if buttons.short_press(name):
            print(f"Taste {name} wurde kurz gedrückt!")
        if buttons.released(name):
            print(f"Taste {name} wurde losgelassen!")
    time.sleep(0.01)
