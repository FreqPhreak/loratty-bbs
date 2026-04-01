import asyncio
from loratty.core.config import Config
from loratty.core.logging import setup_logging
from loratty.core.events import EventBus
from loratty.core.transport import Transport

async def main():
    config = Config()
    log = setup_logging(config.get("server.log_level"))

    log.info("Starting LoRaTTY BBS...")

    event_bus = EventBus()
    transport = Transport(config, event_bus)

    # Example listener
    async def on_radio_message(packet):
        log.info(f"RX: {packet}")

    event_bus.on("radio.message", on_radio_message)

    await transport.start()

if __name__ == "__main__":
    asyncio.run(main())