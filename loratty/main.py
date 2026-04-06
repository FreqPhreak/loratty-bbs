from loratty.transport.serial import SerialTransport
from loratty.transport.dispatcher import Dispatcher
from loratty.config.init import initial_config
from loratty.tui.dashboard import Dashboard

def main():
    transport = SerialTransport("/dev/ttyUSB0", 115200)
    dispatcher = Dispatcher(transport)

    initial_config(transport)

    ui = Dashboard(dispatcher)
    ui.run()

if __name__ == "__main__":
    main()