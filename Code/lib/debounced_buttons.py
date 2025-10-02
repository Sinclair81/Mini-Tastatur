import board
import digitalio
import time

class DebouncedButtons:
    def __init__(self, button_map, debounce_time=0.02, hold_time=1.0):
        self._buttons = {}
        self._states = {}
        self._last_times = {}
        self._debounce_time = debounce_time
        self._hold_time = hold_time

        self._pressed_flags = {}
        self._short_flags = {}
        self._held_flags = {}
        self._released_flags = {}
        self._press_start_times = {}
        self._pressed_flags_return_true = {}
        self._held_flags_return_true = {}

        for name, pin in button_map.items():
            btn = digitalio.DigitalInOut(pin)
            btn.direction = digitalio.Direction.INPUT
            btn.pull = digitalio.Pull.UP
            self._buttons[name] = btn
            self._states[name] = btn.value
            self._last_times[name] = time.monotonic()
            self._pressed_flags[name] = False
            self._short_flags[name] = False
            self._held_flags[name] = False
            self._released_flags[name] = False
            self._press_start_times[name] = None
            self._pressed_flags_return_true[name] = True
            self._held_flags_return_true[name] = True

    def update(self):
        now = time.monotonic()
        for name, btn in self._buttons.items():
            current = btn.value
            if current != self._states[name]:
                self._last_times[name] = now
                self._states[name] = current

            # Taste gedrückt (LOW)
            if not current:
                if (now - self._last_times[name]) > self._debounce_time:
                    if not self._pressed_flags[name]:
                        self._pressed_flags[name] = True
                        self._short_flags[name] = True
                        self._press_start_times[name] = now
                    elif self._press_start_times[name] and (now - self._press_start_times[name]) > self._hold_time:
                        self._held_flags[name] = True
                        self._short_flags[name] = False
                self._released_flags[name] = False

            # Taste losgelassen (HIGH)
            else:
                if self._pressed_flags[name]:
                    self._released_flags[name] = True
                else:
                    self._released_flags[name] = False
                self._pressed_flags[name] = False
                self._held_flags[name] = False
                self._press_start_times[name] = None

    def pressed(self, name):
        if self._pressed_flags.get(name, False) and self._pressed_flags_return_true.get(name, False):
            self._pressed_flags_return_true[name] = False
            return True
        else:
            return False
        
    def short_press(self, name):
        if self._short_flags.get(name, False) and self._released_flags.get(name, False):
            self._short_flags[name] = False
            return True
        else:
            return False

    def held(self, name):
        if self._held_flags.get(name, False) and self._held_flags_return_true.get(name, False):
            self._held_flags_return_true[name] = False
            return True
        else:
            return False

    def released(self, name):
        if self._released_flags.get(name, False):
            self._released_flags[name] = False  # Nur einmal zurückgeben
            self._pressed_flags_return_true[name] = True
            self._held_flags_return_true[name] = True
            return True
        return False

