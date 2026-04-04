import asyncio
import serial
import serial.tools.list_ports


class SerialTransport:
    START_BYTE = ord("!")

    def __init__(self, port: str | None = None, baud: int = 115200):
        self.port = port
        self.baud = baud
        self._ser = None
        self._running = False
        self._read_task = None
        self._callbacks = []

    def subscribe(self, callback):
        self._callbacks.append(callback)

    async def connect(self):
        if self.port is None:
            self.port = self._auto_detect_port()
        if self.port is None:
            raise RuntimeError("No serial device found")

        self._ser = serial.Serial(self.port, self.baud, timeout=0.05)
        self._running = True

        loop = asyncio.get_running_loop()
        self._read_task = loop.create_task(self._read_loop())

    async def disconnect(self):
        self._running = False
        if self._read_task:
            await self._read_task
        if self._ser and self._ser.is_open:
            self._ser.close()

    async def send_raw_hex(self, payload_hex: str):
        if not self._ser or not self._ser.is_open:
            raise RuntimeError("Serial not connected")

        payload = bytes.fromhex(payload_hex)
        length = len(payload)

        # Meshtastic serial framing: ! <len_lo> <len_hi> <payload>
        frame = bytearray()
        frame.append(self.START_BYTE)
        frame.append(length & 0xFF)
        frame.append((length >> 8) & 0xFF)
        frame.extend(payload)

        self._ser.write(frame)

    def _auto_detect_port(self) -> str | None:
        # Looks for CP210x or common USB/ACM serial device names
        for p in serial.tools.list_ports.comports():
            name = p.device.lower()
            desc = (p.description or "").lower()

            if "cp210" in desc:
                return p.device
            if "usb" in name or "acm" in name:
                return p.device

        return None

    async def _read_loop(self):
        buf = bytearray()

        while self._running:
            try:
                data = self._ser.read(256)
            except serial.SerialException:
                break

            if data:
                buf.extend(data)
                await self._process_buffer(buf)
            else:
                await asyncio.sleep(0.01)

    async def _process_buffer(self, buf: bytearray):
        while True:
            if len(buf) < 3:
                return

            # Sync to start byte
            if buf[0] != self.START_BYTE:
                try:
                    idx = buf.index(self.START_BYTE)
                    del buf[:idx]
                except ValueError:
                    buf.clear()
                    return

            if len(buf) < 3:
                return

            length = buf[1] | (buf[2] << 8)
            if len(buf) < 3 + length:
                return

            payload = bytes(buf[3:3 + length])
            del buf[:3 + length]

            packet = {
                "type": "raw",
                "payload_hex": payload.hex(),
            }

            for cb in self._callbacks:
                cb(packet)