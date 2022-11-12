"""Demo record WAV from line in."""
import os
from machine import I2C, I2S, Pin, SPI  # type: ignore
# from machine import SDCard  # Teensy 4.1 Built-in SD Card
from sgtl5000 import CODEC

spisd = SPI(0, baudrate=40000000)

""" SD Card baudrate should be set on SD Card class (Teensy 4.0 only):
Class 10 = 10 MHz
Class 6  =  6 MHz
Class 4  =  4 MHz
Class 2  =  2 MHz
Probably need a minimum of Class 6 depending on recording setttings"""
# sd = SDCard(1)  # Teensy 4.1: sck=45, mosi=43, miso=42, cs=44

# ======= I2S CONFIGURATION =======
SCK_PIN = 21
WS_PIN = 20
SD_PIN = 8
MCK_PIN = 23
I2S_ID = 1
BUFFER_LENGTH_IN_BYTES = 100000

# ======= AUDIO CONFIGURATION =======
WAV_FILE = "linein.wav"
RECORD_TIME_IN_SECONDS = 10
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.STEREO
SAMPLE_RATE_IN_HZ = 44100

format_to_channels = {I2S.MONO: 1, I2S.STEREO: 2}
NUM_CHANNELS = format_to_channels[FORMAT]
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
RECORDING_SIZE_IN_BYTES = (
    RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
)



audio_in = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mck=Pin(MCK_PIN),
    mode=I2S.RX,
    bits=WAV_SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)

# configure the SGTL5000 codec
i2c = I2C(0, freq=400000)
codec = CODEC(0x0A, i2c)
# codec.vag_ramp(slow=True)  # Minimize Pop
codec.mute_dac(True)
codec.headphone_select(codec.AUDIO_HEADPHONE_LINEIN)  # Line In to headphones
codec.input_select(codec.AUDIO_INPUT_LINEIN)  # Recording input to Line In
codec.linein_level(15, 15)  # Maximum Line In levels
codec.mute_headphone(False)  # Enable headphone monitoring while recording
codec.volume(0.8, 0.8)  # Set headphone volume

# allocate sample arrays
# memoryview used to reduce heap allocation in while loop
mic_samples = bytearray(10000)
mic_samples_mv = memoryview(mic_samples)

num_sample_bytes_written_to_wav = 0

print("Recording size: {} bytes".format(RECORDING_SIZE_IN_BYTES))
print("==========  START RECORDING ==========")

try:
    while True:#num_sample_bytes_written_to_wav < RECORDING_SIZE_IN_BYTES:
        print('in loop')
        # read a block of samples from the SGTL5000 I2S output
        # num_bytes_read_from_mic = 
        num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
    # while num_sample_bytes_written_to_wav < RECORDING_SIZE_IN_BYTES:
    #     # read a block of samples from the SGTL5000 I2S output
    #     num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
    #     print(mic_samples_mv)
    #     print(f'bytes read: {num_bytes_read_from_mic}')
    #     if num_bytes_read_from_mic > 0:
    #         num_bytes_to_write = min(
    #             num_bytes_read_from_mic, RECORDING_SIZE_IN_BYTES - num_sample_bytes_written_to_wav
    #         )
    #         num_sample_bytes_written_to_wav += num_bytes_to_write

    print("==========  DONE RECORDING ==========")
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

# cleanup

codec.deinit()
audio_in.deinit()
print("Done")
