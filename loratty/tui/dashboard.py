import curses
from loratty.tui.messages import MessagesView


class Dashboard:
    def __init__(self):
        self.messages = MessagesView()
        self.send_callback = None
        self.stdscr = None

    def set_send_callback(self, fn):
        self.send_callback = fn

    def handle_incoming(self, text: str):
        print("TUI RECEIVED:", text)  # DEBUG
        self.messages.add(text)
        self._refresh()

    def run(self):
        curses.wrapper(self._main)

    def _main(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(1)
        curses.start_color()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)   # status bar
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # messages
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # input label

        self._refresh()

        while True:
            try:
                user_input = self._input_line()
            except KeyboardInterrupt:
                return

            if user_input.strip():
                print("TUI SEND:", user_input)  # DEBUG
                if self.send_callback:
                    self.send_callback(user_input)

    def _refresh(self):
        if not self.stdscr:
            return

        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()

        # Status bar
        status = " LoRaTTY BBS — TC2 style "
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(0, 0, status.ljust(max_x))
        self.stdscr.attroff(curses.color_pair(1))

        # Message area
        msg_height = max_y - 3
        msgs = self.messages.render(msg_height)

        self.stdscr.attron(curses.color_pair(2))
        for i, line in enumerate(msgs):
            if i >= msg_height:
                break
            self.stdscr.addstr(1 + i, 0, line[:max_x])
        self.stdscr.attroff(curses.color_pair(2))

        # Input label
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(max_y - 2, 0, " > ")
        self.stdscr.attroff(curses.color_pair(3))

        # Input line
        self.stdscr.move(max_y - 1, 0)
        self.stdscr.clrtoeol()

        self.stdscr.refresh()

    def _input_line(self):
        max_y, _ = self.stdscr.getmaxyx()
        curses.echo()
        self.stdscr.move(max_y - 1, 0)
        self.stdscr.clrtoeol()
        line = self.stdscr.getstr().decode("utf-8", errors="replace")
        curses.noecho()
        self._refresh()
        return line