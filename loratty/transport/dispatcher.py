from loratty.transport.framing import deframe, frame_packet


class Dispatcher:
    def __init__(self, transport):
        self.transport = transport
        self.buffer = bytearray()
        self.line_buffer = bytearray()
        self.handlers = []

        transport.register_callback(self._ingest)

    def register(self, handler):
        self.handlers.append(handler)

    def send(self, text: str):
        payload = text.encode("utf-8")
        framed = frame_packet(payload)
        print("DISPATCH SEND:", framed)
        self.transport.write(framed)

    def _dispatch_text(self, text: str):
        print("DISPATCH TEXT:", text)
        for handler in self.handlers:
            handler(text)

    def _ingest(self, chunk: bytes):
        print("DISPATCH INGEST:", chunk)
        self.buffer.extend(chunk)

        # 1. Try framed packets first
        for payload in deframe(self.buffer):
            try:
                text = payload.decode("utf-8", errors="replace")
            except Exception:
                text = "<decode error>"
            self._dispatch_text(text)

        # 2. Raw newline-based fallback
        for b in chunk:
            if b == 10:  # '\n'
                try:
                    text = self.line_buffer.decode("utf-8", errors="replace")
                except Exception:
                    text = "<decode error>"
                self.line_buffer.clear()
                self._dispatch_text(text)
            else:
                self.line_buffer.append(b)