from transport.framing import deframe
from proto import meshtastic_pb2

class Dispatcher:
    def __init__(self, transport):
        self.transport = transport
        self.buffer = bytearray()
        self.handlers = {}

        transport.register_callback(self._ingest)

    def register(self, msg_type, handler):
        self.handlers[msg_type] = handler

    def send(self, msg):
        payload = msg.SerializeToString()
        framed = b"\x94" + payload + b"\xc3"
        self.transport.write(framed)

    def _ingest(self, chunk):
        self.buffer.extend(chunk)

        for payload in deframe(self.buffer):
            msg = meshtastic_pb2.FromRadio()
            msg.ParseFromString(payload)

            key = msg.WhichOneof("payload")
            handler = self.handlers.get(key)

            if handler:
                handler(msg)