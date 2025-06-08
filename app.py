from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)
LOG_FILE = "logs/adin_log_latest.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    try:
        if not os.path.exists(LOG_FILE):
            return jsonify({"error": "ログファイルが見つかりません"}), 404
        df = pd.read_csv(LOG_FILE)
        return jsonify(df.tail(360).to_dict(orient='records'))
    except Exception as e:
        print(f"APIエラー: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
