# Mini-Tastatur

[![donate](https://img.shields.io/badge/donate-PayPal-blue.svg)](https://www.paypal.me/Sinclair81)

<!-- markdownlint-disable MD033 -->
<img src="https://github.com/Sinclair81/Mini-Tastatur/blob/main/Images/3D_Front.jpg" align="right" alt="3D_Front" height="516" width="350">
<!-- markdownlint-enable MD033 -->

A smal clone of the [Adafruit MacroPad RP2040](https://learn.adafruit.com/adafruit-macropad-rp2040).  

- Raspberry Pi Pico
- I2C Display
- 9 Buttons

[CircuitPython for Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico)

[MacroPad CircuitPython Library](https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-circuitpython-library)

Extract the zip and navigate to the lib folder found within. Drag the necessary libraries from the zip lib folder to the lib folder on your CIRCUITPY drive.

At a minimum, the following libraries are required to use the MacroPad CircuitPython library. Drag the following files and folders to the lib folder on your CIRCUITPY drive:

adafruit_macropad.mpy - A helper library for using the features of the Adafruit MacroPad.
adafruit_debouncer.mpy - A helper library for debouncing pins. Used to provide a debounced instance of the rotary encoder switch.
adafruit_simple_text_display.mpy - A helper library for easily displaying lines of text on a display.
neopixel.mpy - A CircuitPython driver for NeoPixel LEDs.
adafruit_display_text/ - A library to display text using displayio. Used for the text display functionality of the MacroPad library that allows you easily display lines of text on the built-in display.
adafruit_hid/ - CircuitPython USB HID drivers.
adafruit_midi/ - A CircuitPython helper for encoding/decoding MIDI packets over a MIDI or UART connection
adafruit_ticks.mpy - A helper to work with intervals and deadlines in milliseconds

There is an example included that uses a library that is not required for the MacroPad library to work, but provides a convenient way to layout text in grid. The following library is recommended as well:

adafruit_displayio_layout - A library that includes a grid layout helper.

[MacroPad Basics](https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-basics)  

[MacroPad Display Text](https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-display-text)  

[MacroPad Keyboard and Mouse](https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-keyboard-and-mouse)  

[Arduino IDE Setup](https://learn.adafruit.com/adafruit-macropad-rp2040/arduino-ide-setup)  

[MacroPad Arduino Example](https://learn.adafruit.com/adafruit-macropad-rp2040/arduino)  

Name                  | Pin
--------------------- | ---------------------
Button / Boot select  | GPIO0 / TP6  
Button 1              | GPIO1  
Button 2              | GPIO2  
Button 3              | GPIO3  
Button 4              | GPIO4  
Button 5              | GPIO5  
Button 6              | GPIO6  
Button 7              | GPIO7  
Button 8              | GPIO8  
Button 9              | GPIO9  
Rotary Encoder A      | GPIO17  
Rotary Encoder B      | GPIO18  
Neopixel (9)          | GPIO19  
Display SDA           | GPIO20  
Display SCL           | GPIO21  
Reset                 | RUN  
