import time
import board
import keypad
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# -----------------------------
# Belegung deiner 9 Tasten
# Reihenfolge: Taste 0..8
# -----------------------------
COMBOS = [
    "^!+A",      # Taste 0: Ctrl+Alt+Shift+A # Mac ok
    "^#+A",      # Taste 1: Ctrl+Win+Shift+A
    "$C",        # Taste 2: Command+C
    "$V",        # Taste 3: Command+V
    "^C",        # Taste 4: Ctrl+C
    "^V",        # Taste 5: Ctrl+V
    "#+[ESC]",   # Taste 6: Win+Shift+Esc
    "!^T",       # Taste 7: Alt+Ctrl+T
    "^[TAB]",    # Taste 8: Ctrl+Tab
    "^+[TAB]",   # Taste .: Ctrl+Shift+Tab
    "#D",        # Taste .: Win+D
    "[F5]",      # Taste .: F5
]

# -----------------------------
# Pins der 9 Tasten (anpassen!)
# value_when_pressed=False + Pull-Up => Taster nach GND
# -----------------------------
KEY_PINS = (board.GP1, board.GP2, board.GP3,
            board.GP4, board.GP5, board.GP6, 
            board.GP7, board.GP8, board.GP9)

# -----------------------------
# Mapping für Modifikatoren
# -----------------------------
MOD_MAP = {
    '^': Keycode.LEFT_CONTROL,
    '+': Keycode.LEFT_SHIFT,
    '!': Keycode.LEFT_ALT,
    '#': Keycode.LEFT_GUI,   # Windows/GUI-Taste
    '$': Keycode.COMMAND,    # Mac Command Taste
}

# -----------------------------
# Mapping für Ziffern
# -----------------------------
DIGIT_MAP = {
    '0': Keycode.ZERO,
    '1': Keycode.ONE,
    '2': Keycode.TWO,
    '3': Keycode.THREE,
    '4': Keycode.FOUR,
    '5': Keycode.FIVE,
    '6': Keycode.SIX,
    '7': Keycode.SEVEN,
    '8': Keycode.EIGHT,
    '9': Keycode.NINE,
}

# -----------------------------
# Mapping für Sondertasten in [KLAMMERN]
# Du kannst hier beliebig erweitern.
# -----------------------------
NAME_MAP = {
    "ESC": Keycode.ESCAPE,
    "ESCAPE": Keycode.ESCAPE,
    "TAB": Keycode.TAB,
    "ENTER": Keycode.ENTER,
    "RETURN": Keycode.ENTER,
    "SPACE": Keycode.SPACEBAR,
    "SPACEBAR": Keycode.SPACEBAR,
    "BACKSPACE": Keycode.BACKSPACE,
    "DELETE": Keycode.DELETE,
    "HOME": Keycode.HOME,
    "END": Keycode.END,
    "PAGEUP": Keycode.PAGE_UP,
    "PAGEDOWN": Keycode.PAGE_DOWN,
    "UP": Keycode.UP_ARROW,
    "DOWN": Keycode.DOWN_ARROW,
    "LEFT": Keycode.LEFT_ARROW,
    "RIGHT": Keycode.RIGHT_ARROW,
    # Funktionstasten:
    "F1": Keycode.F1,  "F2": Keycode.F2,  "F3": Keycode.F3,  "F4": Keycode.F4,
    "F5": Keycode.F5,  "F6": Keycode.F6,  "F7": Keycode.F7,  "F8": Keycode.F8,
    "F9": Keycode.F9,  "F10": Keycode.F10, "F11": Keycode.F11, "F12": Keycode.F12,
}

def parse_combo(combo: str):
    """
    Parsen deiner Syntax in eine Liste Keycodes für Keyboard.send().
    - Modifikatoren: ^ (Ctrl), + (Shift), ! (Alt), # (GUI/Win), $ (Command)
    - Buchstaben/Ziffern direkt (A-Z, 0-9)
    - Sondertasten in eckigen Klammern, z.B. [ESC], [F4], [ENTER]
    """
    codes = []

    i = 0
    n = len(combo)
    while i < n:
        ch = combo[i]

        # Modifikatoren
        if ch in MOD_MAP:
            codes.append(MOD_MAP[ch])
            i += 1
            continue

        # Sondertasten [NAME]
        if ch == '[':
            j = combo.find(']', i + 1)
            if j == -1:
                raise ValueError("Fehlende schließende Klammer in Sondertaste: " + combo)
            name = combo[i+1:j].strip().upper()
            if name not in NAME_MAP:
                raise ValueError(f"Unbekannte Sondertaste [{name}]")
            codes.append(NAME_MAP[name])
            i = j + 1
            continue

        # Buchstaben A-Z
        if 'A' <= ch.upper() <= 'Z' and len(ch) == 1:
            codes.append(getattr(Keycode, ch.upper()))
            i += 1
            continue

        # Ziffern 0-9
        if ch in DIGIT_MAP:
            codes.append(DIGIT_MAP[ch])
            i += 1
            continue

        # Leerzeichen ignorieren (optional)
        if ch in (' ', '\t'):
            i += 1
            continue

        # Falls etwas nicht gemappt ist:
        raise ValueError(f"Nicht unterstütztes Zeichen in Combo: {ch!r}")

    # Duplikate entfernen (z. B. doppelt gesetzte Modifikatoren), Reihenfolge beibehalten
    seen = set()
    deduped = []
    for c in codes:
        if c not in seen:
            deduped.append(c)
            seen.add(c)
    return tuple(deduped)

# ---------- HID & Keypad initialisieren ----------
kbd = Keyboard(usb_hid.devices)
time.sleep(0.8)  # kurze Wartezeit, bis Host das HID-Device erkennt

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

print("Bereit. 9 Tasten -> sendet definierte Tastenkombinationen.")

# ---------- Event-Loop ----------
while True:
    event = keys.events.get()
    if event:
        if event.pressed:
            key_no = event.key_number
            try:
                combo = COMBOS[key_no]
                codes = parse_combo(combo)
                # EINMALIGER "Tap" der gesamten Akkord-Kombination:
                kbd.send(*codes)
                # Falls du Modifikatoren HALTEN willst, statt send(): siehe unten.
                # kbd.press(*modifier_codes); kbd.send(non_modifier); kbd.release_all()
                # (hier nicht nötig – send() macht Tap für alle auf einmal)
                # Debug:
                # print(f"Taste {key_no} -> {combo} -> {codes}")
                #
                # Der Stern * in kbd.send(*codes) bedeutet in Python Argument‑Unpacking (Auspacken von Argumenten).
            except Exception as e:
                # Fehler sichtbar machen, blockiert aber die Schleife nicht
                print("Fehler bei Taste", key_no, "Combo:", COMBOS[key_no], "->", e)
        # released ignorieren (kein Auto-Repeat)
    # kleines sleep optional, um CPU zu sparen
    time.sleep(0.001)
