import platform
from serial.tools import list_ports

KNOWN_USB_VIDS = {0x10C4, 0x1A86, 0x0403}
KNOWN_USB_PIDS = {0xEA60, 0x7523, 0x6001}

DEFAULT_PORTS = {
    "Windows": ["COM3", "COM4", "COM5", "COM6"],
    "Linux": ["/dev/ttyUSB0", "/dev/ttyACM0", "/dev/ttyAMA0"],
    "Darwin": ["/dev/cu.usbserial-0001", "/dev/cu.SLAB_USBtoUART", "/dev/cu.usbmodem14101"],
}


def find_serial_port(preferred_port=None):
    if preferred_port:
        return preferred_port

    ports = list_ports.comports()
    for port in ports:
        if port.vid in KNOWN_USB_VIDS or port.pid in KNOWN_USB_PIDS:
            return port.device

    system = platform.system()
    for candidate in DEFAULT_PORTS.get(system, []):
        try:
            with open(candidate):
                return candidate
        except Exception:
            continue

    return None
