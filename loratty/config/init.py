from loratty.proto import meshtastic_pb2
from loratty.transport.framing import frame_packet

def initial_config(transport):
    # Adjust these values if you want different defaults
    msg = meshtastic_pb2.ToRadio()
    msg.set_radio.serial_enabled = True
    msg.set_radio.debug_log_enabled = False

    payload = msg.SerializeToString()
    framed = frame_packet(payload)
    transport.write(framed)