import serial
import threading


class SerialTransport:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout=0.1)

        self.callbacks = []
        self.running = True

        threading.Thread(target=self._reader, daemon=True).start()

    def write(self, data: bytes):
        print("SERIAL WRITE:", data)  # DEBUG
        self.ser.write(data)

    def register_callback(self, fn):
        self.callbacks.append(fn)

    def _reader(self):
        while self.running:
            chunk = self.ser.read(256)
            if chunk:
                print("SERIAL RAW:", chunk)  # DEBUG
                for cb in self.callbacks:
                    cb(chunk)