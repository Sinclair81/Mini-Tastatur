import board
import busio
import displayio
from i2cdisplaybus import I2CDisplayBus
from adafruit_displayio_ssd1306 import SSD1306
from adafruit_display_text import label
import terminalio

# Displayio freigeben
displayio.release_displays()

# I2C initialisieren (GPIO21 = SCL, GPIO20 = SDA)
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

# Display-Bus erzeugen
display_bus = I2CDisplayBus(i2c, device_address=0x3C)

# Display erzeugen
display = SSD1306(display_bus, width=128, height=64)

# Textgruppe erstellen
splash = displayio.Group()
text = label.Label(terminalio.FONT, text="Hello World!!", x=10, y=10)
splash.append(text)

# Anzeige setzen
display.root_group = splash