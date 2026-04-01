import time
import serial.tools.list_ports
from meshtastic.serial_interface import StreamInterface
from rich.console import Console

console = Console()


class Transport:
    """
    Meshtastic 2.7.x compatible transport layer.
    Uses StreamInterface and the new callback API.
    """

    def __init__(self):
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

        # Register callbacks
        self.interface.onReceive = self._on_receive
        self.interface.onConnection = self._on_connection
        self.interface.onDisconnect = self._on_disconnect

        console.log("[bold green]Connected to Meshtastic radio (2.7.x transport active).[/]")

    # --- Meshtastic 2.7.x callback handlers ---

    def _on_receive(self, packet, interface):
        console.log(f"[yellow]RX Packet:[/] {packet}")

    def _on_connection(self, interface):
        console.log("[green]Meshtastic connection established.[/]")

    def _on_disconnect(self, interface):
        console.log("[red]Meshtastic disconnected.[/]")

    # --- Sending text ---

    def send_text(self, text: str):
        if not self.interface:
            console.log("[red]Cannot send — no interface connected.[/]")
            return

        console.log(f"[cyan]Sending text:[/] {text}")
        self.interface.sendText(text)

    # --- Event loop ---

    def loop_forever(self):
        console.log("[magenta]Starting Meshtastic event loop...[/]")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            console.log("[red]Stopping LoRaTTY transport...[/]")
            if self.interface:
                self.interface.close()