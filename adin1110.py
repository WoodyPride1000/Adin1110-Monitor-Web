import spidev
import time

class ADIN1110:
    def __init__(self, bus=0, device=0, speed_hz=1000000, mode=0):
        self.spi = spidev.SpiDev()
        try:
            self.spi.open(bus, device)
            self.spi.max_speed_hz = speed_hz
            self.spi.mode = mode
        except Exception as e:
            print(f"SPI初期化エラー: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        try:
            self.spi.close()
            print("SPI接続を閉じました")
        except Exception as e:
            print(f"SPIクローズエラー: {e}")

    def read_register(self, addr):
        try:
            control_word = (0 << 15) | (addr & 0x3FF)
            a_hi = (control_word >> 8) & 0xFF
            a_lo = control_word & 0xFF
            tx = [a_hi, a_lo, 0x00, 0x00]
            rx = self.spi.xfer2(tx)
            value = (rx[2] << 8) | rx[3]
            print(f"レジスタ読み取り (アドレス {hex(addr)}): {hex(value)}")
            return value
        except Exception as e:
            print(f"レジスタ読み取りエラー (アドレス {hex(addr)}): {e}")
            return None

    def write_register(self, addr, value):
        try:
            control_word = (1 << 15) | (addr & 0x3FF)
            a_hi = (control_word >> 8) & 0xFF
            a_lo = control_word & 0xFF
            v_hi = (value >> 8) & 0xFF
            v_lo = value & 0xFF
            tx = [a_hi, a_lo, v_hi, v_lo]
            self.spi.xfer2(tx)
            print(f"レジスタ書き込み (アドレス {hex(addr)}, 値 {hex(value)})")
        except Exception as e:
            print(f"レジスタ書き込みエラー (アドレス {hex(addr)}): {e}")

    def read_32bit(self, addr):
        try:
            hi_hi = self.read_register(addr)
            hi_lo = self.read_register(addr + 1)
            lo_hi = self.read_register(addr + 2)
            lo_lo = self.read_register(addr + 3)
            if None in [hi_hi, hi_lo, lo_hi, lo_lo]:
                return None
            return (hi_hi << 24) | (hi_lo << 16) | (lo_hi << 8) | lo_lo
        except Exception as e:
            print(f"32ビット読み取りエラー (アドレス {hex(addr)}): {e}")
            return None

    def init_device(self):
        try:
            # ソフトリセット（レジスタ0x0000に0x8000）
            self.write_register(0x0000, 0x8000)
            time.sleep(0.1)  # リセット後の安定化待ち
            # 伝送レベルを2.4Vに設定（CONFIG0のビット6=1）
            self.write_register(0x0010, 0x0040)
            print("ADIN1110の初期化が完了しました")
        except Exception as e:
            print(f"デバイス初期化エラー: {e}")
            raise

    def get_status(self):
        REG_PHYSTS = 0x0011
        REG_CONFIG0 = 0x0010
        REG_MSE_VAL = 0x0036
        REG_CABLE_LEN = 0x0037
        REG_RX_PKT = 0x0200
        REG_TX_PKT = 0x0204
        REG_DROP_PKT = 0x0208

        try:
            status = self.read_register(REG_PHYSTS)
            link = "Up" if (status & 0x0004) else "Down" if status is not None else "Error"

            config = self.read_register(REG_CONFIG0)
            mode = "2.4V" if (config & (1 << 6)) else "1V" if config is not None else "Error"

            mse = self.read_register(REG_MSE_VAL)
            snr = round(10 * (mse / 1000.0), 1) if mse is not None else 0.0

            cable_len = self.read_register(REG_CABLE_LEN)
            distance = round(cable_len * 0.1, 1) if cable_len is not None else 0.0

            rx = self.read_32bit(REG_RX_PKT)
            tx = self.read_32bit(REG_TX_PKT)
            drop = self.read_32bit(REG_DROP_PKT)

            return {
                "link": link,
                "mode": mode,
                "snr": snr,
                "distance": distance,
                "rx_packets": rx if rx is not None else 0,
                "tx_packets": tx if tx is not None else 0,
                "drop_packets": drop if drop is not None else 0
            }
        except Exception as e:
            print(f"ステータス取得エラー: {e}")
            return None
