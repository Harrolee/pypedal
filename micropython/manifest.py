# variables available here that resolve to absolute paths
# $(MPY_DIR) – path to the micropython repo.
# $(MPY_LIB_DIR) – path to the micropython-lib submodule. Prefer to use require().
# $(PORT_DIR) – path to the current port (e.g. ports/stm32)
# $(BOARD_DIR) – path to the current board (e.g. ports/stm32/boards/PYBV11)

MIMXR_MANIFEST = '/Users/lee/projects/micropython/ports/mimxrt/boards/manifest.py'

# will this manifest find the mimxr port if I pass $(PORT_DIR) ?
# give it a try
include(MIMXR_MANIFEST)
module('sgtl5000.py', base_path="packages/pedal_core")
module('demo_li.py', base_path="packages/pedal_core")
module('passthrough.py', base_path="packages/pedal_core")
module('test.py', base_path="packages")
