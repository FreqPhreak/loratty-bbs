from loratty.transport.framing import deframe, frame_packet


class Dispatcher:
    def __init__(self, transport):
        self.transport = transport
        self.buffer = bytearray()
        self.handlers = []

        # Transport pushes raw bytes into _ingest()
        transport.register_callback(self._ingest)

    def register(self, handler):
        """Register a callback that receives decoded text messages."""
        self.handlers.append(handler)

    def send(self, text: str):
        """Send a raw text message through the transport."""
        payload = text.encode("utf-8")
        framed = frame_packet(payload)
        self.transport.write(framed)

    def _ingest(self, chunk: bytes):
        """Receive raw bytes, deframe them, decode to text, and dispatch."""
        self.buffer.extend(chunk)

        for payload in deframe(self.buffer):
            try:
                text = payload.decode("utf-8", errors="replace")
            except Exception:
                text = "<decode error>"

            for handler in self.handlers:
                handler(text)