# Kombiniertes Display + Rotary Encoder Script (Raspberry Pi Pico + CircuitPython)
# - SSD1306/SSD1315 I2C-Display @ 0x3C an GP21 (SCL) / GP20 (SDA)
# - Rotary Encoder an GP17 (A) / GP18 (B), divisor=2 (2 Detents pro Zyklus)
# - Optionaler Taster am GP0 (auf GND, interner Pull-Up aktiv)

import time
import board
import busio
import displayio
from i2cdisplaybus import I2CDisplayBus
from adafruit_displayio_ssd1306 import SSD1306
from adafruit_display_text import label
import terminalio

import rotaryio
import digitalio

# --- Display einrichten ---
displayio.release_displays()

# I2C initialisieren (GP21=SCL, GP20=SDA)
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

# Display-Bus + Display
display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = SSD1306(display_bus, width=128, height=64)

# Root-Gruppe und Text-Label
splash = displayio.Group()
# Größere Schrift durch scale; Position leicht eingerückt
value_label = label.Label(
    terminalio.FONT,
    text="Encoder: 0",
    color=0xFFFFFF,
    scale=1,
    x=4,    # linke Einrückung
    y=36,   # ungefähr mittig (Baseline)
)
splash.append(value_label)
display.root_group = splash

# --- Encoder + Taster einrichten ---
# divisor=2 wie in deinem Encoder-Snippet (für 2 Detents pro Zyklus)
encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP18, 2)

# Optionaler Button am Encoder (Pull-Up aktiv -> gedrückt == False)
button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
last_position = None
last_btn_state = True  # True = nicht gedrückt (wegen Pull-Up)

# --- Hauptloop ---
while True:
    # Encoder-Wert lesen
    position = encoder.position

    # Nur bei Änderung das Display-Label aktualisieren (schont I2C und CPU)
    if position != last_position:
        value_label.text = f"Encoder: {position}"
        last_position = position

    # Button-Edge-Detection (optional)
    btn_state = button.value
    if btn_state != last_btn_state:
        if not btn_state:
            # Kurz sichtbar machen, dass Button gedrückt wurde
            value_label.text = f"Encoder: {position} *"
        else:
            # Stern wieder entfernen
            value_label.text = f"Encoder: {position}"
        last_btn_state = btn_state

    time.sleep(0.01)  # kleines Delay zur Entlastung
