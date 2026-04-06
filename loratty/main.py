from loratty.transport.serial import SerialTransport
from loratty.transport.dispatcher import Dispatcher
from loratty.tui.dashboard import Dashboard


def main():
    transport = SerialTransport(port="/dev/ttyUSB0", baud=115200)
    dispatcher = Dispatcher(transport)
    dashboard = Dashboard()

    dispatcher.register(dashboard.handle_incoming)
    dashboard.set_send_callback(dispatcher.send)

    dashboard.run()


if __name__ == "__main__":
    main()