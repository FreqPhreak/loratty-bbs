import asyncio
from .transport import SerialTransport

async def main():
    print("LoRaTTY starting...")

    transport = SerialTransport()

    def on_packet(pkt):
        print("RX:", pkt["payload_hex"])

    transport.subscribe(on_packet)

    print("Connecting to radio...")
    await transport.connect()
    print(f"Connected on {transport.port}")

    # Main loop placeholder
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())