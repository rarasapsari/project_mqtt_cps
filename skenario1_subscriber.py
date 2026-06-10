"""
============================================================
TUGAS PRAKTIKUM: KOMUNIKASI MQTT - SMART ROOM MONITORING
Skenario 1: Komunikasi Dasar Publisher–Subscriber
------------------------------------------------------------
Studi Kasus : Smart Room Monitoring
File        : skenario1_subscriber.py
Deskripsi   : Subscriber menerima dan menampilkan data sensor
              dari topik smartroom/sensor
============================================================
"""

import paho.mqtt.client as mqtt
import json

# ─── Konfigurasi Broker ───────────────────────────────────
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC       = "smartroom/sensor"

# ─── Callback saat koneksi berhasil ───────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[SUBSCRIBER] Terhubung ke broker {BROKER_HOST}:{BROKER_PORT}")
        client.subscribe(TOPIC)
        print(f"[SUBSCRIBER] Berlangganan topik: '{TOPIC}'")
        print(f"[SUBSCRIBER] Menunggu pesan...\n")
    else:
        print(f"[SUBSCRIBER] Gagal terhubung, kode: {rc}")

# ─── Callback saat pesan diterima ────────────────────────
def on_message(client, userdata, msg):
    print("-" * 45)
    print(f"[SUBSCRIBER] Pesan diterima!")
    print(f"  Topik   : {msg.topic}")
    try:
        data = json.loads(msg.payload.decode())
        print(f"  Sensor ID   : {data['id']}")
        print(f"  Suhu        : {data['suhu_celsius']} °C")
        print(f"  Kelembaban  : {data['kelembaban']} %")
        print(f"  Cahaya      : {data['cahaya_lux']} lux")
        print(f"  Waktu       : {data['timestamp']}")
    except Exception as e:
        print(f"  Raw payload : {msg.payload.decode()}")
        print(f"  Error parse : {e}")

# ─── Setup Client ─────────────────────────────────────────
client = mqtt.Client(client_id="subscriber-smartroom-01")
client.on_connect = on_connect
client.on_message  = on_message

print("=" * 55)
print("  SKENARIO 1: Komunikasi Dasar Publisher–Subscriber")
print("  Studi Kasus: Smart Room Monitoring")
print("=" * 55)

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

# loop_forever() membuat subscriber terus berjalan
client.loop_forever()
