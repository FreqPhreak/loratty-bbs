import serial
import threading


class SerialTransport:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout=0.1)

        self.callbacks = []
        self.running = True

        threading.Thread(target=self._reader, daemon=True).start()

    def write(self, data: bytes):
        self.ser.write(data)

    def register_callback(self, fn):
        self.callbacks.append(fn)

    def _reader(self):
        while self.running:
            chunk = self.ser.read(256)
            if chunk:
                for cb in self.callbacks:
                    cb(chunk)