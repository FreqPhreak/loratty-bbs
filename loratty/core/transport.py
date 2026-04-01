import time
import asyncio
import serial.tools.list_ports
from meshtastic.serial_interface import SerialInterface
from rich.console import Console

console = Console()


class Transport:
    """
    Transport layer for Meshtastic 2.7.x+ using SerialInterface.
    Handles connection, callbacks, and background event loop.
    """

    def __init__(self, config=None, event_bus=None):
        self.config = config
        self.event_bus = event_bus
        self.interface = None
        self._loop_task = None

    def list_serial_ports(self):
        """Return available serial ports."""
        ports = [p.device for p in serial.tools.list_ports.comports()]
        console.log("[bold green]Available serial ports:[/]")
        for p in ports:
            console.log(f" - {p}")
        return ports

    async def start(self):
        """Async entry point called by main.py."""
        console.log("[cyan]Transport.start() called[/]")

        ports = self.list_serial_ports()
        if not ports:
            console.log("[red]No serial ports found![/]")
            return

        port = ports[0]
        console.log(f"[cyan]Auto-selecting port:[/] {port}")

        self.connect(port)

        # Run the blocking event loop in a background thread
        loop = asyncio.get_running_loop()
        self._loop_task = loop.run_in_executor(None, self.loop_forever)

    def connect(self, port: str):
        """Connect to the Meshtastic radio and register callbacks."""
        console.log(f"[cyan]Connecting to Meshtastic device on {port}...[/]")

        # SerialInterface is the correct class for Meshtastic 2.7.x+
        self.interface = SerialInterface(port)

        # Register callbacks (new API)
        self.interface.addReceiveCallback(self._on_receive)
        self.interface.addConnectionCallback(self._on_connection)
        self.interface.addDisconnectCallback(self._on_disconnect)

        console.log("[bold green]Connected to Meshtastic radio.[/]")

    # --- Callback handlers ----------------------------------------------------

    def _on_receive(self, packet):
        """Called when a packet is received."""
        console.log(f"[yellow]RX Packet:[/] {packet}")
        if self.event_bus:
            self.event_bus.emit("packet_received", packet)

    def _on_connection(self):
        """Called when the radio connects."""
        console.log("[green]Meshtastic connection established.[/]")
        if self.event_bus:
            self.event_bus.emit("connected")

    def _on_disconnect(self):
        """Called when the radio disconnects."""
        console.log("[red]Meshtastic disconnected.[/]")
        if self.event_bus:
            self.event_bus.emit("disconnected")

    # --- Sending --------------------------------------------------------------

    def send_text(self, text: str):
        """Send a text message over Meshtastic."""
        if not self.interface:
            console.log("[red]Cannot send — no interface connected.[/]")
            return

        console.log(f"[cyan]Sending text:[/] {text}")
        self.interface.sendText(text)

    # --- Background event loop ------------------------------------------------

    def loop_forever(self):
        """Blocking loop required by the Meshtastic client."""
        console.log("[magenta]Starting Meshtastic event loop...[/]")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            console.log("[red]Stopping LoRaTTY transport...[/]")
            if self.interface:
                self.interface.close()