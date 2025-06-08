from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def data():
    rows = []
    try:
        with open("log.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append({
                    "time": row[0],
                    "link": row[1],
                    "mode": row[2],
                    "snr": float(row[3]),
                    "distance": float(row[4]),
                    "tx": int(row[5]),
                    "rx": int(row[6]),
                    "drop": int(row[7])
                })
    except:
        pass
    return jsonify(rows[-100:])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)