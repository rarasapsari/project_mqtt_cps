"""
============================================================
TUGAS PRAKTIKUM: KOMUNIKASI MQTT - SMART ROOM MONITORING
Skenario 3: Penggunaan Beberapa Topik
------------------------------------------------------------
Studi Kasus : Smart Room Monitoring
File        : skenario3_publisher_topics.py
Deskripsi   : Publisher mengirim berbagai jenis data sensor
              ke topik yang berbeda-beda sesuai jenisnya.

Struktur Topik:
  smartroom/{ruangan}/{jenis_sensor}

Contoh:
  smartroom/ruangA/temperature
  smartroom/ruangA/humidity
  smartroom/ruangA/light
  smartroom/ruangB/temperature
  smartroom/ruangB/motion
============================================================
"""

import paho.mqtt.client as mqtt
import json
import time
import random

# ─── Konfigurasi Broker ───────────────────────────────────
BROKER_HOST = "localhost"
BROKER_PORT = 1883

# ─── Definisi topik dan data sensor ──────────────────────
sensor_messages = [
    {
        "topic"  : "smartroom/ruangA/temperature",
        "payload": {
            "sensor_id": "temp-A01",
            "nilai"    : round(random.uniform(24.0, 28.0), 2),
            "satuan"   : "Celsius",
            "lokasi"   : "Ruang Kelas A",
        }
    },
    {
        "topic"  : "smartroom/ruangA/humidity",
        "payload": {
            "sensor_id": "hum-A01",
            "nilai"    : round(random.uniform(55.0, 70.0), 2),
            "satuan"   : "%",
            "lokasi"   : "Ruang Kelas A",
        }
    },
    {
        "topic"  : "smartroom/ruangA/light",
        "payload": {
            "sensor_id": "lux-A01",
            "nilai"    : random.randint(300, 700),
            "satuan"   : "lux",
            "lokasi"   : "Ruang Kelas A",
        }
    },
    {
        "topic"  : "smartroom/ruangB/temperature",
        "payload": {
            "sensor_id": "temp-B01",
            "nilai"    : round(random.uniform(22.0, 26.0), 2),
            "satuan"   : "Celsius",
            "lokasi"   : "Ruang Kelas B",
        }
    },
    {
        "topic"  : "smartroom/ruangB/motion",
        "payload": {
            "sensor_id": "pir-B01",
            "nilai"    : random.choice([True, False]),
            "satuan"   : "boolean",
            "lokasi"   : "Ruang Kelas B",
        }
    },
]

# ─── Callback ─────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[PUBLISHER] Terhubung ke broker {BROKER_HOST}:{BROKER_PORT}\n")

def on_publish(client, userdata, mid):
    pass  # dikonfirmasi di loop utama

# ─── Setup Client ─────────────────────────────────────────
client = mqtt.Client(client_id="publisher-multitopic-01")
client.on_connect = on_connect
client.on_publish  = on_publish

print("=" * 55)
print("  SKENARIO 3: Penggunaan Beberapa Topik")
print("  Studi Kasus: Smart Room Monitoring")
print("=" * 55)
print("\n  Struktur topik: smartroom/{ruangan}/{sensor}")
print("  Topik yang digunakan:")
for m in sensor_messages:
    print(f"    • {m['topic']}")
print()

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_start()
time.sleep(1)

# ─── Publish ke masing-masing topik ───────────────────────
for i, msg in enumerate(sensor_messages, 1):
    payload = json.dumps({**msg["payload"], "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")})

    print(f"[{i}/{len(sensor_messages)}] Mengirim ke: {msg['topic']}")
    print(f"     Payload: {payload}")

    client.publish(msg["topic"], payload, qos=1)
    time.sleep(1.5)

client.loop_stop()
client.disconnect()
print("\n[PUBLISHER] Semua data terkirim. Koneksi ditutup.")
