START = b"\x94"
END = b"\xc3"


def frame_packet(payload: bytes) -> bytes:
    return START + payload + END


def deframe(buffer: bytearray):
    packets = []
    while True:
        try:
            start = buffer.index(START)
            end = buffer.index(END, start + 1)
        except ValueError:
            break

        packets.append(bytes(buffer[start+1:end]))
        del buffer[:end+1]

    return packets