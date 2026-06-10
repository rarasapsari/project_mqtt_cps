"""
============================================================
TUGAS PRAKTIKUM: KOMUNIKASI MQTT - SMART ROOM MONITORING
Skenario 1: Komunikasi Dasar Publisher–Subscriber
------------------------------------------------------------
Studi Kasus : Smart Room Monitoring
File        : skenario1_publisher.py
Deskripsi   : Publisher mengirimkan data sensor ruangan
              (suhu, kelembaban, cahaya) ke Mosquitto Broker
============================================================
"""

import paho.mqtt.client as mqtt
import json
import time
import random

# ─── Konfigurasi Broker ───────────────────────────────────
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC       = "smartroom/sensor"

# ─── Callback saat koneksi berhasil ───────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[PUBLISHER] Terhubung ke broker {BROKER_HOST}:{BROKER_PORT}")
    else:
        print(f"[PUBLISHER] Gagal terhubung, kode: {rc}")

# ─── Callback setelah pesan berhasil dipublish ────────────
def on_publish(client, userdata, mid):
    print(f"[PUBLISHER] Pesan berhasil dikirim (mid={mid})")

# ─── Setup Client ─────────────────────────────────────────
client = mqtt.Client(client_id="publisher-smartroom-01")
client.on_connect = on_connect
client.on_publish  = on_publish

print("=" * 55)
print("  SKENARIO 1: Komunikasi Dasar Publisher–Subscriber")
print("  Studi Kasus: Smart Room Monitoring")
print("=" * 55)

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_start()

time.sleep(1)  # tunggu koneksi stabil

# ─── Kirim 5 data sensor secara periodik ──────────────────
for i in range(1, 6):
    payload = {
        "id"          : f"sensor-room-A{i}",
        "suhu_celsius": round(random.uniform(24.0, 30.0), 2),
        "kelembaban"  : round(random.uniform(55.0, 75.0), 2),
        "cahaya_lux"  : random.randint(200, 800),
        "timestamp"   : time.strftime("%Y-%m-%d %H:%M:%S")
    }

    message = json.dumps(payload)
    result  = client.publish(TOPIC, message)

    print(f"\n[PUBLISHER] Mengirim data ke-{i}:")
    print(f"  Topik   : {TOPIC}")
    print(f"  Payload : {message}")
    time.sleep(2)

client.loop_stop()
client.disconnect()
print("\n[PUBLISHER] Koneksi ditutup.")
