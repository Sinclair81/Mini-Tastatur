import json

# --- Decoder: Windows-1252 robust dekodieren ---
_CP1252_MAP = {
    0x80: "\u20AC", 0x82: "\u201A", 0x83: "\u0192", 0x84: "\u201E",
    0x85: "\u2026", 0x86: "\u2020", 0x87: "\u2021", 0x88: "\u02C6",
    0x89: "\u2030", 0x8A: "\u0160", 0x8B: "\u2039", 0x8C: "\u0152",
    0x91: "\u2018", 0x92: "\u2019", 0x93: "\u201C", 0x94: "\u201D",
    0x95: "\u2022", 0x96: "\u2013", 0x97: "\u2014", 0x98: "\u02DC",
    0x99: "\u2122", 0x9A: "\u0161", 0x9B: "\u203A", 0x9C: "\u0153",
    0x9E: "\u017E", 0x9F: "\u0178",
    }
    # 0x81, 0x8D, 0x8F, 0x90, 0x9D bleiben unverändert.

def decode_win1252_best_effort(b: bytes) -> str:
    # 1) UTF-8 versuchen
    try:
        return b.decode("utf-8")
    except Exception:
        pass
    # 2) cp1252 versuchen (falls die Firmware das kann)
    try:
        return b.decode("cp1252")
    except Exception:
        pass
    # 3) Fallback: Byte-für-Byte wie Windows-1252 mappen
    return "".join(_CP1252_MAP.get(x, chr(x)) for x in b)

class Parser:
    def parse_user_json(path):
        # JSON-Datei öffnen und laden
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data["username"], data["short"], data["buttons"], data["menu"], data["encoder"], data["btn_inactive"], data["btn_active"]

    def parse_user_lines(path, max_lines=None):
        lastname, name_abbreviation = "", ""

        with open(path, "rb") as f:
            for i, raw in enumerate(f):
                if max_lines is not None and i >= max_lines:
                    break

                raw = raw.strip()   # Bytes: entfernt \r\n und Außen-Spaces
                if not raw or raw[:1] in (b";", b"/", b"*", b"#"):
                    continue

                if raw.count(b";") < 2:
                    continue

                parts_b = [p.strip() for p in raw.split(b";")]
                parts = [decode_win1252_best_effort(p) for p in parts_b]

                if parts[0] == "user":
                    lastname          = parts[1]
                    name_abbreviation = parts[2]

        # EOF erreicht → mehrere Variablen zurückgeben
        return lastname, name_abbreviation
    
    def parse_favorits_lines(path, lastname, name_abbreviation, max_lines=None):
        base_hotkey_long, base_hotkey_short, first_hotkey = "", "", ""
        name, hotkey, num = [], [], []
        abbreviation_index = 0
        hotkey_index = 0

        with open(path, "rb") as f:
            for i, raw in enumerate(f):
                if max_lines is not None and i >= max_lines:
                    break

                raw = raw.strip() # Bytes: entfernt \r\n und Außen-Spaces
                if not raw or raw[:1] in (b";", b"/", b"*", b"#"):
                    continue

                if raw.count(b";") < 4:
                    continue

                parts_b = [p.strip() for p in raw.split(b";", 4)]
                parts = [decode_win1252_best_effort(p) for p in parts_b]

                if parts[0] == "sys":
                    base_hotkey_long  = parts[1]
                    base_hotkey_short = parts[2]
                    first_hotkey      = parts[3]
                    # 5. Feld in Optionen zerlegen:
                    # Falls deine Datei Pipe trennt (z. B. "07 | 07"), werden beide unterstützt.
                    fifth = parts[4].replace("|", "\n")
                    y = [z.strip() for z in fifth.split("\n") if z.strip()]
                    for idx, a in enumerate(y):
                        if a == name_abbreviation:
                            abbreviation_index = idx
                            break
                else:
                    if parts[0] == lastname or parts[0] == "all":
                        name.append(parts[1])

                        # Hotkey berechnen (ein Zeichen + Offset)
                        if len(first_hotkey) != 1:
                            # Absichern, damit ord() nicht crasht, falls first_hotkey mal leer/zu lang ist
                            raise ValueError("first_hotkey muss genau 1 Zeichen sein (z. B. 'A').")
                        hotkey.append(chr(ord(first_hotkey) + hotkey_index))

                        # Wert aus dem 5. Feld entsprechend abbreviation_index ziehen
                        fifth = parts[4].replace("|", "\n")
                        y = [z.strip() for z in fifth.split("\n") if z.strip()]
                        num.append(y[abbreviation_index] if abbreviation_index < len(y) else "")

                        hotkey_index += 1

        # Sortieren: an num (numerisch) ausrichten
        triple_sorted = sorted(zip(num, name, hotkey), key=lambda t: int(t[0]))  # t[0] ist der num-String
        num_sorted, name_sorted, hotkey_sorted = map(list, zip(*triple_sorted))

        return base_hotkey_long, base_hotkey_short, name_sorted, hotkey_sorted, num_sorted

    def parse_ini_lines(path):
        """
        Generator, der (section, key, value) für jede gefundene Einstellung liefert.
        Kommentare (beginnend mit ';' oder '#') und leere Zeilen werden ignoriert.
        """
        section = None
        with open(path, "r") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith(";") or line.startswith("#"):
                    continue

                # Sektionen: [network], [wifi], ...
                if line.startswith("[") and line.endswith("]"):
                    section = line[1:-1].strip()
                    continue

                # key = value  (oder key: value)
                sep_pos = line.find("=")
                if sep_pos < 0:
                    sep_pos = line.find(":")
                if sep_pos > 0:
                    key = line[:sep_pos].strip()
                    value = line[sep_pos+1:].strip()

                    # Inline-Kommentare entfernen:  value ; Kommentar  oder  value # Kommentar
                    for marker in (" ;", "\t;", " #", "\t#"):
                        cut = value.find(marker)
                        if cut != -1:
                            value = value[:cut].strip()

                    # Einfache Anführungszeichen entfernen
                    if (len(value) >= 2) and (
                        (value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")
                    ):
                        value = value[1:-1]

                    yield (section, key, value)
                # Alles andere wird ignoriert (z. B. Zeilen ohne Trennzeichen)
