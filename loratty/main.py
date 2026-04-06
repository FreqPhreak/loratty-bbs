from loratty.transport.serial import SerialTransport
from loratty.transport.dispatcher import Dispatcher
from loratty.tui.dashboard import Dashboard


def main():
    # Adjust port/baud as needed for your hardware
    transport = SerialTransport(port="/dev/ttyUSB0", baud=115200)

    dispatcher = Dispatcher(transport)

    dashboard = Dashboard()

    # Incoming messages → TUI
    dispatcher.register(dashboard.handle_incoming)

    # Outgoing messages ← TUI
    dashboard.set_send_callback(dispatcher.send)

    # Start the TUI loop
    dashboard.run()


if __name__ == "__main__":
    main()