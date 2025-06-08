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





## コンソール（logger.py）
```bash

ADIN1110の初期化が完了しました
レジスタ書き込み (アドレス 0x0, 値 0x8000)
レジスタ書き込み (アドレス 0x10, 値 0x40)
レジスタ読み取り (アドレス 0x11): 0x0004
...
ログ記録: ['2025-06-09T12:33:00.123456', 'Up', '2.4V', 4.0, 10.0, 100, 200, 0]
```


## Webブラウザ
SNRグラフ：青い線でSNR（dB）が時系列で表示。

パケットグラフ：TX（緑）、RX（オレンジ）、DROP（赤）の3本の線。

エラー発生時：赤いエラーメッセージが表示。


