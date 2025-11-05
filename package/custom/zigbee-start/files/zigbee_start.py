#!/usr/bin/env python3
import sys
sys.path.insert(0, '/')
import asyncio
import zigpy
from bellows.ezsp.app import EZSPApplication  # Direct import for EFR32MG24 NCP v0x12 (bypasses entry points)

async def main():
    config = {
        "device": {
            "path": "/dev/ttyUSB0",  # Confirmed present
            "speed": 115200,  # Matches NCP v0x12; try 1000000 if timeouts occur
        },
        "network": {
            "pan_id": 0x1234,  # Short PAN ID
            "extended_pan_id": 0x1234567890ABCDEF,  # 64-bit extended ID (required for EZSP stability)
            "channel": 15,  # Zigbee channel (11-26)
            "key": b"one" * 16,  # 16-byte network key (use random hex for production: e.g., bytes.fromhex('1a2b3c...'))
        },
    }
    try:
        app = await EZSPApplication.new(config=config)
        print("Zigbee app started. Listening...")
        await asyncio.sleep(60)  # 60s for discovery (power on devices during this)
        print("Discovered devices:")
        for device in app.devices.values():
            ieee = getattr(device, 'ieee', 'Unknown')
            print(f"  - NWK: {device.nwk:04x} | IEEE: {ieee} | Manufacturer: {getattr(device, 'manufacturer', 'Unknown')} | Model: {getattr(device, 'model', 'Unknown')}")
        await app.shutdown()
        print("App shutdown.")
    except Exception as startup_exc:
        print(f"Startup failed: {startup_exc}")
        import traceback
        traceback.print_exc()  # Full stack for debugging

if __name__ == '__main__':
    asyncio.run(main())
