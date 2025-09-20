import board
import rotaryio
import digitalio
import time

# The divisor of the quadrature signal.
# Use 1 for encoders without detents, or encoders with 4 detents per cycle.
# Use 2 for encoders with 2 detents per cycle.
# Use 4 for encoders with 1 detent per cycle.
# class rotaryio.IncrementalEncoder(pin_a: microcontroller.Pin, pin_b: microcontroller.Pin, divisor: int = 4)

# Rotary Encoder an Pin GP17 (A) und GP18 (B) anschließen
encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP18, 2)

# Optional: Taster am Encoder (z.B. an GP0)
button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

last_position = None

while True:
    position = encoder.position
    if position != last_position:
        print("Position:", position)
        last_position = position

    if not button.value:
        print("Button gedrückt!")
    time.sleep(0.01)
