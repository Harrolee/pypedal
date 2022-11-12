import os
from machine import I2C, I2S, Pin, SPI  # type: ignore
from sgtl5000 import CODEC

print('running passthrough')
# ======= I2S INPUT CONFIGURATION =======
SCK_PIN = 21
WS_PIN = 20
LI_SD_PIN = 8
MCK_PIN = 23
I2S_ID = 1
BUFFER_LENGTH_IN_BYTES = 100000

# ======= I2S OUTPUT CONFIGURATION =======
OUT_SCK_PIN = 4 # try 16 if bclk2(4) does not work
OUT_WS_PIN = 3 
OUT_SD_PIN = 7
OUT_MCK_PIN = 23 # 33 shouldn't work
OUT_I2S_ID = 2
OUT_BUFFER_LENGTH_IN_BYTES = 100000

# ======= AUDIO CONFIGURATION =======
RECORD_TIME_IN_SECONDS = 10
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO
SAMPLE_RATE_IN_HZ = 44100


format_to_channels = {I2S.MONO: 1, I2S.STEREO: 2}
NUM_CHANNELS = format_to_channels[FORMAT]
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
RECORDING_SIZE_IN_BYTES = (
    RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
)

# audio_in = I2S(
#     I2S_ID,
#     sck=Pin(SCK_PIN),
#     ws=Pin(WS_PIN),
#     sd=Pin(LI_SD_PIN),
#     mck=Pin(MCK_PIN),
#     mode=I2S.RX,
#     bits=WAV_SAMPLE_SIZE_IN_BITS,
#     format=FORMAT,
#     rate=SAMPLE_RATE_IN_HZ,
#     ibuf=BUFFER_LENGTH_IN_BYTES,
# )

audio_out = I2S(
    OUT_I2S_ID,
    sck=Pin(OUT_SCK_PIN),
    ws=Pin(OUT_WS_PIN),
    sd=Pin(OUT_SD_PIN),
    mck=Pin(OUT_MCK_PIN),
    mode=I2S.TX,
    bits=WAV_SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)

# ======= SGTL5000 CONFIGURATION =======
i2c = I2C(0, freq=400000)
codec = CODEC(0x0A, i2c)
# input 
# codec.vag_ramp(slow=True)  # Minimize Pop
codec.headphone_select(codec.AUDIO_HEADPHONE_LINEIN)  # Line In to headphones
codec.input_select(codec.AUDIO_INPUT_LINEIN)  # Recording input to Line In
codec.linein_level(15, 15)  # Maximum Line In levels
codec.mute_headphone(False)  # Enable headphone monitoring while recording
codec.volume(0.8, 0.8)  # Set headphone volume
# output
# codec.mute_dac(False)# codec.mute_dac(True) # what function does this provide?
# codec.dac_volume(1, 1)
# codec.headphone_select(codec.AUDIO_HEADPHONE_DAC) # do we need this?
# codec.mute_lineout(False)
# codec.lineout_level(4, 4)
# ======= SGTL5000 CONFIGURATION =======


# allocate sample arrays
# memoryview used to reduce heap allocation in while loop
mic_samples = bytearray(10000)
mic_samples_mv = memoryview(mic_samples)

num_sample_bytes_written_to_wav = 0


try:
    print('passing through')
    while True:#num_sample_bytes_written_to_wav < RECORDING_SIZE_IN_BYTES:
        print('in loop')
        # read a block of samples from the SGTL5000 I2S output
        # num_bytes_read_from_mic = 
        # num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
        # audio_out.write(mic_samples_mv)
        # if num_bytes_read_from_mic > 0:
        #     num_bytes_to_write = min(
        #         num_bytes_read_from_mic, RECORDING_SIZE_IN_BYTES - num_sample_bytes_written_to_wav
        #     )
        #     # write samples to WAV file
        #     num_bytes_written = wav.write(mic_samples_mv[:num_bytes_to_write])
        #     num_sample_bytes_written_to_wav += num_bytes_written
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))



codec.deinit()
audio_in.deinit()
audio_out.deinit()
print("Done")