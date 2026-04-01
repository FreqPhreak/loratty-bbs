import time
import serial.tools.list_ports
from meshtastic.serial_interface import StreamInterface
from meshtastic.util import EventReceiver
from rich.console import Console

console = Console()


class LoRaTTYTransport(EventReceiver):
    """
    Meshtastic 2.7.x compatible transport layer for LoRaTTY.
    Uses StreamInterface instead of the deprecated SerialInterface.
    """

    def __init__(self):
        super().__init__()
        self.client = None
        self.interface = None

    def list_serial_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        console.log("[bold green]Available serial ports:[/]")
        for p in ports:
            console.log(f" - {p}")
        return ports

    def connect(self, port: str):
        console.log(f"[cyan]Connecting to Meshtastic device on {port}...[/]")

        # StreamInterface is the correct transport for 2.7.x firmware
        self.interface = StreamInterface(devPath=port, noProto=False)

        # Register this class as the event receiver
        self.interface.addEventReceiver(self)

        console.log("[bold green]Connected to Meshtastic radio (2.7.x transport active).[/]")

    # Meshtastic 2.7.x event callback
    def onReceive(self, packet, interface):
        console.log(f"[yellow]RX Packet:[/] {packet}")

    def send_text(self, text: str):
        if not self.interface:
            console.log("[red]Cannot send — no interface connected.[/]")
            return

        console.log(f"[cyan]Sending text:[/] {text}")
        self.interface.sendText(text)

    def loop_forever(self):
        console.log("[magenta]Starting Meshtastic event loop...[/]")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            console.log("[red]Stopping LoRaTTY transport...[/]")
            if self.interface:
                self.interface.close()