from spidev import SpiDev
import threading

class MCP3008:

    def __init__(self, bus=0, device=0):
        self.lock = threading.Lock
        self._bus = bus
        self._device = device
        self._spi = SpiDev()
        self.open()
        self._spi.max_speed_hz = 1000000  # 1MHz

    def __del__(self):
        self.close()

    def open(self):
        self._spi.open(self._bus, self._device)
        self._spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel=0):
        """Short description.

        Long description.

        Args:
            channel: <was auch immer>

        Returns:
            A full sentence.
        """
        with self.lock:
            adc = self._spi.xfer2([1, (8 + channel) << 4, 0])
            data = ((adc[1] & 3) << 8) + adc[2]
            return data

    def close(self):
        self._spi.close()


