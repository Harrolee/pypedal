PEDAL_MANIFEST=/Users/lee/pedal/micropython/manifest.py
MICROPYTHON_MAKEFILE=/Users/lee/projects/micropython/ports/mimxrt

make --directory=$MICROPYTHON_MAKEFILE BOARD=TEENSY41 FROZEN_MANIFEST=$PEDAL_MANIFEST
mv $MICROPYTHON_MAKEFILE/build-TEENSY41/firmware.hex micropython/build/pedal_firmware_teensy41.hex

# this will reliably fail the first time.
./teensy_loader_cli/teensy_loader_cli --mcu=TEENSY41 -w micropython/build/pedal_firmware_teensy41.hex
./teensy_loader_cli/teensy_loader_cli --mcu=TEENSY41 -w micropython/build/pedal_firmware_teensy41.hex
