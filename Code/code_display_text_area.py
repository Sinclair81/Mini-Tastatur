# SPDX-FileCopyrightText: 2024 foamyguy for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
import displayio
from i2cdisplaybus import I2CDisplayBus
from adafruit_displayio_ssd1306 import SSD1306
import terminalio

from adafruit_display_text.text_box import TextBox

displayio.release_displays()
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = SSD1306(display_bus, width=128, height=64)

main_group = displayio.Group()

left_text = ("left").rstrip()
left_text_area = TextBox(
    terminalio.FONT,
    190,
    TextBox.DYNAMIC_HEIGHT,
    align=TextBox.ALIGN_LEFT,
    text=left_text,
    background_color=0xFFFFFF,
    color=0x000000,
    scale=1,
)

left_text_area.anchor_point = (0, 0)
left_text_area.anchored_position = (0, 0)
main_group.append(left_text_area)


center_text = ("center").rstrip()
center_text_area = TextBox(
    terminalio.FONT,
    90,
    TextBox.DYNAMIC_HEIGHT,
    align=TextBox.ALIGN_CENTER,
    text="test", #center_text,
    background_color=0xFFFFFF,
    color=0x000000,
    scale=1,
)

center_text_area.anchor_point = (0.5, 0.5)
center_text_area.anchored_position = (display.width // 2, display.height // 2)
main_group.append(center_text_area)


right_text = ("right").rstrip()
right_text_area = TextBox(
    terminalio.FONT,
    190,
    TextBox.DYNAMIC_HEIGHT,
    align=TextBox.ALIGN_RIGHT,
    text=right_text,
    background_color=0xFFFFFF,
    color=0x000000,
    scale=1,
)

right_text_area.anchor_point = (1.0, 1.0)
right_text_area.anchored_position = (display.width, display.height)
main_group.append(right_text_area)

display.root_group = main_group
while True:
    pass