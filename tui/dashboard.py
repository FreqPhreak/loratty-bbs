import curses
from tui.messages import MessagesView

class Dashboard:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.messages = MessagesView()

    def run(self):
        curses.wrapper(self._loop)

    def _loop(self, stdscr):
        stdscr.nodelay(True)

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "LoRaTTY — Dashboard")
            stdscr.addstr(2, 0, self.messages.render())
            stdscr.refresh()