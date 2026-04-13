import pandas as pd
from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import threading

app = Flask(__name__)

# --- 1. VERİTABANI MİMARİSİ ---
def init_db():
    """Veritabanını ve gerekli tabloları hazırlar."""
    conn = sqlite3.connect('iot_warehouse.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temp REAL,
            hum REAL,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# --- 2. VERİ ANALİZİ (İleri Seviye) ---
def perform_analysis():
    """Pandas kullanarak son veriler üzerinden trend tahmini yapar."""
    try:
        conn = sqlite3.connect('iot_warehouse.db')
        df = pd.read_sql_query("SELECT temp FROM sensor_logs ORDER BY id DESC LIMIT 10", conn)
        conn.close()

        if len(df) < 5:
            return "Collecting Data..."

        # Basit Hareketli Ortalama (SMA) ile trend kontrolü
        avg_temp = df['temp'].mean()
        last_temp = df['temp'].iloc[0]
        
        status = "Rising" if last_temp > avg_temp else "Stable/Falling"
        return {"avg": round(avg_temp, 2), "trend": status}
    except Exception as e:
        return str(e)

# --- 3. API ENDPOINT'LERİ ---

@app.route('/api/telemetry', methods=['POST'])
def receive_data():
    """ESP32'den gelen verileri karşılar."""
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    temp = data.get('temp')
    hum = data.get('hum')

    # Veritabanına Kayıt
    conn = sqlite3.connect('iot_warehouse.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_logs (temp, hum, timestamp) VALUES (?, ?, ?)",
                   (temp, hum, datetime.now()))
    conn.commit()
    conn.close()

    print(f"[*] Veri Kaydedildi: {temp}°C - {hum}%")
    return jsonify({"status": "success", "analysis": perform_analysis()}), 201

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Flutter uygulamasının verileri çekeceği yer."""
    analysis = perform_analysis()
    return jsonify({
        "system_time": datetime.now().strftime("%H:%M:%S"),
        "metrics": analysis
    })

if __name__ == '__main__':
    init_db()
    # Host 0.0.0.0, ağdaki diğer cihazların (ESP32/Telefon) erişmesini sağlar.
    app.run(host='0.0.0.0', port=5000, debug=True)
