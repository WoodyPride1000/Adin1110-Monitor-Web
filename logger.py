import csv
import time
from datetime import datetime
from adin1110 import ADIN1110
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "adin_log_latest.csv")

def log_loop():
    # ログディレクトリの作成
    os.makedirs(LOG_DIR, exist_ok=True)

    with ADIN1110() as adin:
        adin.init_device()  # デバイス初期化
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "link", "mode", "snr", "distance", "tx_packets", "rx_packets", "drop_packets"])
            try:
                while True:
                    status = adin.get_status()
                    if status:
                        row = [
                            datetime.now().isoformat(),
                            status["link"],
                            status["mode"],
                            status["snr"],
                            status["distance"],
                            status["tx_packets"],
                            status["rx_packets"],
                            status["drop_packets"]
                        ]
                        writer.writerow(row)
                        f.flush()
                        print(f"ログ記録: {row}")
                    else:
                        print("ステータス取得に失敗しました")
                    time.sleep(10)
            except KeyboardInterrupt:
                print("ログ記録を終了しました")
            except Exception as e:
                print(f"ログ記録エラー: {e}")

if __name__ == "__main__":
    log_loop()
