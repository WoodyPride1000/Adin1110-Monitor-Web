import spidev
import time

# ADIN1110のSPI設定
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED_HZ = 1000000
SPI_MODE = 0

REG_CONFIG0 = 0x0010
REG_PHYSTS = 0x0011
REG_MSE_VAL = 0x0036
REG_CABLE_LEN = 0x0037
REG_RX_PKT_CNT = 0x0038
REG_TX_PKT_CNT = 0x0039
REG_PKT_DROP_CNT = 0x003A

class ADIN1110:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_SPEED_HZ
        self.spi.mode = SPI_MODE

    def close(self):
        self.spi.close()

    def read_register(self, addr):
        control_word = (0 << 15) | (addr & 0x3FF)
        a_hi = (control_word >> 8) & 0xFF
        a_lo = control_word & 0xFF
        tx = [a_hi, a_lo, 0x00, 0x00]
        rx = self.spi.xfer2(tx)
        return (rx[2] << 8) | rx[3]

    def get_status(self):
        status = self.read_register(REG_PHYSTS)
        link = "Up" if (status & 0x0004) else "Down"
        config = self.read_register(REG_CONFIG0)
        mode = "2.4V" if (config & (1 << 6)) else "1V"
        mse = self.read_register(REG_MSE_VAL)
        snr = round(10 * (mse / 1000.0), 1)
        cable_len = self.read_register(REG_CABLE_LEN)
        distance = round(cable_len * 0.1, 1)
        tx_pkts = self.read_register(REG_TX_PKT_CNT)
        rx_pkts = self.read_register(REG_RX_PKT_CNT)
        drop_pkts = self.read_register(REG_PKT_DROP_CNT)

        return {
            "link": link,
            "mode": mode,
            "snr": snr,
            "distance": distance,
            "tx": tx_pkts,
            "rx": rx_pkts,
            "drop": drop_pkts
        }