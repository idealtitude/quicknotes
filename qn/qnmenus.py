# -*- coding: utf-8 -*-

from typing import Any

import curses

COLORS = {
    "black"    : curses.COLOR_BLACK,
    "red"      : curses.COLOR_RED,
    "green"    : curses.COLOR_GREEN,
    "yellow"   : curses.COLOR_YELLOW,
    "blue"     : curses.COLOR_BLUE,
    "magenta"  : curses.COLOR_MAGENTA,
    "cyan"     : curses.COLOR_CYAN,
    "white"    : curses.COLOR_WHITE
}

ATTRS = {
    "normal"    : curses.A_NORMAL,
    "blink"     : curses.A_BLINK,
    "bold"      : curses.A_BOLD,
    "dim"       : curses.A_DIM,
    "reverse"   : curses.A_REVERSE,
    "standout"  : curses.A_STANDOUT,
    "underline" : curses.A_UNDERLINE
}

class TUIBase:
    """
    This class create a basic ncurses window, for use by other classes.
    """
    def __init__(self, colors: dict[str, str], show_cursor: int = 0)->None:
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(show_cursor)

        self.screen.keypad(True)
        #self.colors = colors
        self.dims: tuple[int, int] = self.screen.getmaxyx()

        fore = colors["foreground"]
        back = colors["background"]

        self.colors_pairs = [("null", "null"), (colors["foreground"], colors["background"])]
        curses.init_pair(1, COLORS[fore], COLORS[back])
        self.hilite_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL

    def set_colors(self, fore: str = "white", back: str = "black")->None:
        pair = (fore, back)
        idx = 0

        if pair not in self.colors_pairs:
            self.colors_pairs.append(pair)
            curses.init_pair(len(pair), COLORS[fore], COLORS[back])

        idx = self.colors_pairs.index(pair)

        self.hilite_color = curses.color_pair(idx)

    def mkwin(self, rows: int = 0, cols: int = 0, pos_y: int = 0, pos_x: int = 0)->Any:
        """Create a ncurses window."""
        return curses.newwin(rows, cols, pos_y, pos_x)

    def center_text(self, text: Any)->None:
        pos_x = self.dims[1] // 2 - len(text) // 2
        pos_y = self.dims[0] // 2
        self.screen.addstr(pos_y, pos_x, text)

    def clear(self)->None:
        self.screen.clear()

    def fresh(self)->None:
        self.screen.refresh()

    def exit(self)->None:
        curses.endwin()

    def __del__(self)->Any:
        """Destructor, restoring terminal to its normal state."""
        curses.endwin()

class MainMenu(TUIBase):
    """
    This is main menu for the app.

    Attributes
    ----------

    Methods
    -------
    """

    def __init__(self, colors: dict[str, str], show_cursor: int = 0)->None:
        super().__init__(colors, show_cursor)
        menu: Any = {
            "title": "QuickNotes",
            "type" : "menu",
            "subtitle": "Notes management"
        }

        option_new_note = {
            "title": "New note",
            "type" : "command",
            "command": "create new note"
        }

        menu["options"] = [option_new_note]

        self.menu_options = menu
        self.selected_option = 0
        self._previously_selected_option = None
        self.running = True

