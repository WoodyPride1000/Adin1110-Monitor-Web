import time
import csv
from datetime import datetime
from adin1110 import ADIN1110

LOG_FILE = "log.csv"

def log_status():
    adin = ADIN1110()
    try:
        while True:
            status = adin.get_status()
            now = datetime.now().isoformat()
            row = [
                now,
                status["link"],
                status["mode"],
                status["snr"],
                status["distance"],
                status["tx"],
                status["rx"],
                status["drop"]
            ]
            with open(LOG_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row)
            time.sleep(10)
    finally:
        adin.close()

if __name__ == "__main__":
    log_status()