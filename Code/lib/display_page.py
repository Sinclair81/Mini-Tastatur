# /lib/display_page.py
# Robuste Page/Manager-Implementierung ohne next(), mit tolerantem show/hide

class Page:
    __slots__ = ("name", "group", "refs")

    def __init__(self, name, group, refs):
        """
        name  : str                   - Logischer Name (z. B. "A" oder "B")
        group : displayio.Group       - Anzeige-Gruppe der Page
        refs  : dict                  - Referenzen auf Labels/Elemente, z. B.
                                        {"z2": labelObj, "z3": (lblL, lblM, lblR)}
        """
        self.name = name
        self.group = group
        self.refs = refs

    # Sichtbarkeit steuern – tolerant gegenüber versehentlichen Zusatzargumenten
    def show(self, *_args, **_kwargs):
        self.group.hidden = False

    def hide(self, *_args, **_kwargs):
        self.group.hidden = True

    # Bequemes Update einzelner Labels
    def set_text(self, key, value):
        """
        key: "z2" oder Tuple ("z3", idx) für link/mid/right in Zeile 3
        """
        if isinstance(key, tuple):
            k, idx = key
            self.refs[k][idx].text = str(value)
        else:
            self.refs[key].text = str(value)

    # Mehrere Updates auf einmal
    def update_many(self, mapping):
        for key, val in mapping.items():
            self.set_text(key, val)


class PageManager:
    __slots__ = ("container", "pages", "current_index", "on_show", "_name_to_index")

    def __init__(self, container, on_show=None):
        """
        container : displayio.Group  - Hier werden alle Page-Gruppen eingefügt.
        on_show   : callable(name, index, page) oder None
        """
        self.container = container
        self.pages = []
        self.current_index = -1
        self.on_show = on_show
        self._name_to_index = {}

    def add(self, page: Page, visible=False):
        # ins Display einhängen
        self.container.append(page.group)
        page.group.hidden = not visible

        # registrieren
        self._name_to_index[page.name] = len(self.pages)
        self.pages.append(page)

        if visible:
            self.current_index = len(self.pages) - 1
            if self.on_show:
                self.on_show(page.name, self.current_index, page)

    def _resolve_index(self, which):
        # which: int (Index) oder str (Name)
        if isinstance(which, int):
            return which
        # String-Name → Nachschlagen, ohne next()
        return self._name_to_index.get(which, -1)

    def show(self, which):
        """
        which: int (Index) oder str (Name)
        Blendet die gewünschte Page ein.
        """
        idx = self._resolve_index(which)
        if idx < 0 or idx >= len(self.pages):
            raise ValueError("Page '{}' nicht gefunden".format(which))

        if idx == self.current_index:
            return  # schon sichtbar

        # aktuelle ausblenden
        if 0 <= self.current_index < len(self.pages):
            self.pages[self.current_index].hide()

        # neue einblenden (ohne Argument!)
        self.pages[idx].show()
        self.current_index = idx

        if self.on_show:
            self.on_show(self.pages[idx].name, idx, self.pages[idx])
