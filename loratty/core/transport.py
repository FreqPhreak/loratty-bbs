import time
import asyncio
import serial.tools.list_ports
from meshtastic.serial_interface import SerialInterface
from rich.console import Console

console = Console()


class Transport:
    """
    Meshtastic 2.7.x+ compatible transport layer.
    Uses SerialInterface (StreamInterface is now abstract).
    """

    def __init__(self, config=None, event_bus=None):
        self.config = config
        self.event_bus = event_bus
        self.interface = None
        self._loop_task = None

    # ---------------------------------------------------------
    # Serial Port Discovery
    # ---------------------------------------------------------
    def list_serial_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        console.log("[bold green]Available serial ports:[/]")
        for p in ports:
            console.log(f" - {p}")
        return ports

    # ---------------------------------------------------------
    # Async Start (called by main.py)
    # ---------------------------------------------------------
    async def start(self):
        console.log("[cyan]Transport.start() called[/]")

        ports = self.list_serial_ports()
        if not ports:
            console.log("[red]No serial ports found![/]")
            return

        port = ports[0]
        console.log(f"[cyan]Auto-selecting port:[/] {port}")

        self.connect(port)

        loop = asyncio.get_running_loop()
        self._loop_task = loop.run_in_executor(None, self.loop_forever)

    # ---------------------------------------------------------
    # Connect to Meshtastic Radio
    # ---------------------------------------------------------
    def connect(self, port: str):
        console.log(f"[cyan]Connecting to Meshtastic device on {port}...[/]")

        # Correct class for your installed Meshtastic version
        self.interface = SerialInterface(port)

        # Register callbacks
        self.interface.onReceive = self._on_receive
        self.interface.onConnection = self._on_connection
        self.interface.onDisconnect = self._on_disconnect

        console.log("[bold green]Connected to Meshtastic radio (SerialInterface active).[/]")

    # ---------------------------------------------------------
    # Meshtastic Callback Handlers
    # ---------------------------------------------------------
    def _on_receive(self, packet, interface):
        console.log(f"[yellow]RX Packet:[/] {packet}")
        if self.event_bus:
            self.event_bus.emit("packet_received", packet)

    def _on_connection(self, interface):
        console.log("[green]Meshtastic connection established.[/]")
        if self.event_bus:
            self.event_bus.emit("connected")

    def _on_disconnect(self, interface):
        console.log("[red]Meshtastic disconnected.[/]")
        if self.event_bus:
            self.event_bus.emit("disconnected")

    # ---------------------------------------------------------
    # Sending Text
    # ---------------------------------------------------------
    def send_text(self, text: str):
        if not self.interface:
            console.log("[red]Cannot send — no interface connected.[/]")
            return

        console.log(f"[cyan]Sending text:[/] {text}")
        self.interface.sendText(text)

    # ---------------------------------------------------------
    # Event Loop
    # ---------------------------------------------------------
    def loop_forever(self):
        console.log("[magenta]Starting Meshtastic event loop...[/]")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            console.log("[red]Stopping LoRaTTY transport...[/]")
            if self.interface:
                self.interface.close()