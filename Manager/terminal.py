import curses
import threading


class History:
    def __init__(self):
        self.history = []
        self.current = None
        self.index = 0

    def add(self, command):
        self.history.append(command)

    def __update_current(self, value):
        if self.current is None:
            self.current = list(filter(lambda cmd: cmd.startswith(value), self.history))
            self.current.append(value)
            self.current = self.current[::-1]
            self.index = 0
        return len(self.current) > 0

    def reset(self):
        self.current = None

    def next(self, value):
        if self.__update_current(value):
            self.index += 0 if self.index >= len(self.current) - 1 else 1
            val = self.current[self.index]
            return val, len(val) + 2

    def previous(self, value):
        if self.__update_current(value):
            self.index -= 0 if self.index <= 0 else 1
            val = self.current[self.index]
            return val, len(val) + 2


CTRL_D = 0
RESIZE = 1


class Result:
    def __init__(self, value=None, special=None):
        self.value = value
        self.special = special

    def get_line(self):
        return self.value

    def equals(self, other):
        return self.value == other if self.special is None else self.special == other


class Terminal:
    def __init__(self):
        self.lock = threading.Lock()
        self.history = History()
        self.value = ""
        self.next_cursor = 0

    def write(self, window, string, clear=True):
        self.lock.acquire()
        if clear:
            window.erase()
        window.addstr(string)
        window.refresh()
        self.lock.release()

    def __print_input_line(self, input_window):
        if self.next_cursor == 0:
            self.write(input_window, "> " + self.value)
        else:
            self.write(input_window, "")

    def read(self, input_window):
        self.__print_input_line(input_window)

        while True:
            c, (y, x) = input_window.getch(), input_window.getyx()

            if c == curses.KEY_RESIZE:
                return Result(special=RESIZE)
            elif c == curses.KEY_LEFT:
                x = max(2, x - 1)
            elif c == curses.KEY_RIGHT:
                x = min(len(self.value) + 2, x + 1)
            elif c == ord('\n'):
                if self.next_cursor != 0:
                    return Result(value="")

                self.history.add(self.value)
                temp, self.value = self.value, ""
                return Result(value=temp)
            elif c == 4:
                return Result(special=CTRL_D)
            elif c == curses.KEY_UP or c == curses.KEY_DOWN:
                if self.next_cursor != 0:
                    continue

                self.value, x = self.history.next(self.value) if c == curses.KEY_UP else self.history.previous(
                    self.value)
            else:
                if c == curses.KEY_BACKSPACE:
                    x = max(2, x - 1)
                if c == curses.KEY_BACKSPACE or c == curses.KEY_DC:
                    self.value = self.value[:(x - 2)] + self.value[(x - 1):]
                else:
                    if self.next_cursor != 0:
                        continue

                    self.value = self.value[:(x - 2)] + chr(c) + self.value[(x - 2):]
                    x += 1

                self.history.reset()

            self.__print_input_line(input_window)
            input_window.move(y, x)

    def toggle_cursor(self):
        self.next_cursor = curses.curs_set(self.next_cursor)
