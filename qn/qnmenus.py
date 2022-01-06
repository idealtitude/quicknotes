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
    def __init__(self, version: str, colors: dict[str, str], show_cursor: int = 0)->None:
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
        self.screen.attron(curses.color_pair(1))
        #self.screen.addstr(1, 1, f"QuickNotes {version}", curses.A_BOLD)
        self.screen.attroff(curses.color_pair(1))
        self.fresh()
        # self.hilite_color = curses.color_pair(1)
        # self.normal_color = curses.A_NORMAL

    def set_colors(self, fore: str = "white", back: str = "black")->int:
        pair = (fore, back)
        idx = 0

        if pair not in self.colors_pairs:
            self.colors_pairs.append(pair)
            curses.init_pair(len(pair), COLORS[fore], COLORS[back])

        idx = self.colors_pairs.index(pair)
        #self.screen.attron(curses.color_pair(idx))

        # self.hilite_color = curses.color_pair(idx)
        #self.fresh()
        return idx

    def unset_colors(self, pair: int)->None:
        self.screen.attroff(curses.color_pair(pair))
        self.fresh()

    def set_attr(self, attr: str = "normal")->None:
        # self.normal_color = ATTRS["attr"]
        # self.fresh()
        pass

    def mkwin(self, rows: int = 0, cols: int = 0, pos_y: int = 0, pos_x: int = 0)->Any:
        """Create a ncurses window."""
        return curses.newwin(rows, cols, pos_y, pos_x)

    def center_text(self, text: Any)->None:
        pos_x = self.dims[1] // 2 - len(text) // 2
        pos_y = self.dims[0] // 2
        self.screen.addstr(pos_y, pos_x, text)
        self.fresh()

    def get_key(self)->int:
        return self.screen.getch()

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

    def __init__(self, version: str, colors: dict[str, str], show_cursor: int = 0)->None:
        super().__init__(version, colors, show_cursor)
        self.version = version
        self.menu_items: list[str] = ["New", "Read", "Search", "Edit", "Settings", "Help", "Exit"]
        self.selected_item = 0
        self.selected_item_colors = self.set_colors(fore = "black", back = "white")
        self.selected_action: Any
        self.height: int = self.dims[0]
        self.width: int = self.dims[1]

        self.screen.addstr(self.dims[0] - 2, 1, "Add note(s)")
        self.screen.addstr(self.dims[0] - 2, self.dims[1] - 16, "Enter to select")

        self.set_menu()
        self.main_loop()
        # self.screen.getch()

    def set_menu(self)->None:
        self.screen.addstr(1, 1, f"QuickNotes {self.version}", curses.A_BOLD)
        for idx, row in enumerate(self.menu_items):
            pos_x: int = self.width // 2 - len(row) // 2
            pos_y: int = self.height // 2 - len(self.menu_items) // 2 + idx

            if idx == self.selected_item:
                self.screen.attron(curses.color_pair(self.selected_item_colors))
                self.screen.addstr(pos_y, pos_x, row)
                self.screen.attroff(curses.color_pair(self.selected_item_colors))
            else:
                self.screen.addstr(pos_y, pos_x, row)

        self.fresh()

    def get_item_info(self, item_name: str)->str:
        help_string: str

        if item_name == "New":
            help_string = "Add notes"
        elif item_name == "Read":
            help_string = "Read notes"
        elif item_name == "Search":
            help_string = "Search notes"
        elif item_name == "Edit":
            help_string = "Edit notes"
        elif item_name == "Settings":
            help_string = "Configure QuickNotes"
        elif item_name == "Help":
            help_string = "Documentation of QuickNotes"
        elif item_name == "Exit":
            help_string = "Close and exit QuickNotes"

        return help_string

    # def items_actions(self, item_name: str)->None:
    #     self.clear()
    #     res = True

    #     if item_name == "New":
    #         pass
    #     elif item_name == "Read":
    #         pass
    #     elif item_name == "Search":
    #         pass
    #     elif item_name == "Edit":
    #         pass
    #     elif item_name == "Settings":
    #         pass
    #     elif item_name == "Help":
    #         pass
    #     elif item_name == "Exit":
    #         res = False

    #     if res:
    #         self.screen.addstr(1, 1, "Returning to main loop")
    #         self.screen.getch()
    #         self.set_menu()
    #         self.main_loop()

    def main_loop(self)->None:
        while True:
            key = self.get_key()

            if key == curses.KEY_UP and self.selected_item > 0:
                self.selected_item -= 1
                self.clear()
                self.screen.addstr(self.dims[0] - 2, 1, self.get_item_info(self.menu_items[self.selected_item]))
                self.screen.addstr(self.dims[0] - 2, self.dims[1] - 16, "Enter to select")
                self.fresh()
            elif key == curses.KEY_DOWN and self.selected_item < len(self.menu_items) - 1:
                self.selected_item += 1
                self.clear()
                self.screen.addstr(self.dims[0] - 2, 1, self.get_item_info(self.menu_items[self.selected_item]))
                self.screen.addstr(self.dims[0] - 2, self.dims[1] - 16, "Enter to select")
                self.fresh()
            # elif key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
            #     self.clear()
            #     self.screen.addstr(self.dims[0] - 2, 1, self.get_item_info(self.menu_items[self.selected_item]))
            #     self.fresh()
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.selected_action = action = self.menu_items[self.selected_item]
                break

            # TODO: on key left or right, display imenu tem info

            self.set_menu()
            self.fresh()

        #self.items_actions(self.menu_items[self.selected_item])

