from spidev import SpiDev
import threading


class MCP3008:
    """Handled the MCP3008.

    Args:
        bus: Number from used SPI-bus on the raspberry pi.
        device: Number of the SPI-device at the chosen bus
    """
    def __init__(self, bus=0, device=0):
        self.lock = threading.Lock
        self._bus = bus
        self._device = device
        self._spi = SpiDev()
        self._open()
        self._spi.max_speed_hz = 1000000  # 1MHz

    def __del__(self):
        self._spi.close()

    def _open(self):
        self._spi.open(self._bus, self._device)
        self._spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel=0):
        """Reads a chosen analog channel.

        Reads a channel from the MCP3008 wich is initialized.
        Reads a value between 0 and 1023.

        Args:
            channel: Number of channel to read value.

        Returns:
            Returns the read channel int-value between 0 and 1023.
        """
        adc = self._spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
