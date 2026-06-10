"""
============================================================
TUGAS PRAKTIKUM: KOMUNIKASI MQTT - SMART ROOM MONITORING
Skenario 3: Penggunaan Beberapa Topik
------------------------------------------------------------
Studi Kasus : Smart Room Monitoring
File        : skenario3_subscriber_topics.py
Deskripsi   : Subscriber berlangganan ke beberapa topik
              spesifik sekaligus (tanpa wildcard).
              Menampilkan data dari tiap ruangan & sensor.
============================================================
"""

import paho.mqtt.client as mqtt
import json

# ─── Konfigurasi Broker ───────────────────────────────────
BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Daftar topik yang ingin dipantau
TOPICS = [
    "smartroom/ruangA/temperature",
    "smartroom/ruangA/humidity",
    "smartroom/ruangA/light",
    "smartroom/ruangB/temperature",
    "smartroom/ruangB/motion",
]

# ─── Callback saat koneksi ────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[SUBSCRIBER] Terhubung ke broker {BROKER_HOST}:{BROKER_PORT}")
        for topic in TOPICS:
            client.subscribe(topic, qos=1)
            print(f"  + Berlangganan: {topic}")
        print("\n[SUBSCRIBER] Memantau semua sensor...\n")

# ─── Callback saat pesan diterima ────────────────────────
def on_message(client, userdata, msg):
    topic_parts = msg.topic.split("/")
    ruangan     = topic_parts[1] if len(topic_parts) > 1 else "?"
    jenis       = topic_parts[2] if len(topic_parts) > 2 else "?"

    print(f"┌─ Topik: {msg.topic}")
    try:
        data = json.loads(msg.payload.decode())
        print(f"│  Ruangan   : {ruangan.upper()}")
        print(f"│  Sensor    : {jenis}")
        print(f"│  ID Sensor : {data.get('sensor_id', '-')}")
        print(f"│  Nilai     : {data.get('nilai', '-')} {data.get('satuan', '')}")
        print(f"│  Waktu     : {data.get('timestamp', '-')}")
    except:
        print(f"│  Payload   : {msg.payload.decode()}")
    print(f"└{'─'*40}")

# ─── Setup Client ─────────────────────────────────────────
client = mqtt.Client(client_id="subscriber-multitopic-01")
client.on_connect = on_connect
client.on_message  = on_message

print("=" * 55)
print("  SKENARIO 3: Subscriber Beberapa Topik")
print("  Studi Kasus: Smart Room Monitoring")
print("=" * 55)

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_forever()
