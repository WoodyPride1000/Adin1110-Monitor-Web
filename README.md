# ADIN1110 Monitor System

ADIN1110 10BASE-T1L PHY の状態を SPI 経由で取得し、10秒ごとにログを保存し、Web UIでグラフ表示します。

## 構成

- `adin1110.py`: SPI通信ドライバ
- `logger.py`: 10秒ごとにログ保存
- `app.py`: Flask Web サーバー
- `templates/index.html`: Web UI（Chart.js）
- `log.csv`: ログファイル

## 使い方

1. 必要なパッケージをインストール：

```bash
sudo apt install python3-pip
pip3 install flask spidev
```

2. ログ記録を開始：

```bash
python3 logger.py
```

3. 別ターミナルでWebサーバを起動：

```bash
python3 app.py
```

4. Webブラウザで表示：

```
http://<ラズパイのIP>:5000
```

## 注意

- SPIは有効にしておいてください（`raspi-config` → インターフェース → SPI）。
- `logger.py` と `app.py` は並行して実行する必要があります。