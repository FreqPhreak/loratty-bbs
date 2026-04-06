import curses
from loratty.tui.messages import MessagesView


class Dashboard:
    def __init__(self):
        self.messages = MessagesView()
        self.send_callback = None

    def set_send_callback(self, fn):
        self.send_callback = fn

    def handle_incoming(self, text: str):
        self.messages.add(text)
        self._refresh()

    def run(self):
        curses.wrapper(self._main)

    def _main(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(1)

        self._refresh()

        while True:
            user_input = self._input_line()
            if user_input.strip():
                if self.send_callback:
                    self.send_callback(user_input)

    def _refresh(self):
        if not hasattr(self, "stdscr"):
            return

        self.stdscr.clear()

        # Render last 10 messages
        msg_text = self.messages.render()
        self.stdscr.addstr(0, 0, msg_text)

        # Input prompt
        self.stdscr.addstr(12, 0, "> ")
        self.stdscr.refresh()

    def _input_line(self):
        curses.echo()
        self.stdscr.move(12, 2)
        line = self.stdscr.getstr().decode("utf-8", errors="replace")
        curses.noecho()
        return line