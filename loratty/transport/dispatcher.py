from loratty.transport.framing import deframe, frame_packet


class Dispatcher:
    def __init__(self, transport):
        self.transport = transport
        self.buffer = bytearray()
        self.handlers = []

        transport.register_callback(self._ingest)

    def register(self, handler):
        self.handlers.append(handler)

    def send(self, text: str):
        payload = text.encode("utf-8")
        framed = frame_packet(payload)
        print("DISPATCH SEND:", framed)  # DEBUG
        self.transport.write(framed)

    def _ingest(self, chunk: bytes):
        print("DISPATCH INGEST:", chunk)  # DEBUG
        self.buffer.extend(chunk)

        for payload in deframe(self.buffer):
            print("DEFRAMED PAYLOAD:", payload)  # DEBUG

            try:
                text = payload.decode("utf-8", errors="replace")
            except Exception:
                text = "<decode error>"

            print("DISPATCH TEXT:", text)  # DEBUG

            for handler in self.handlers:
                handler(text)