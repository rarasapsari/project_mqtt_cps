"""
============================================================
TUGAS PRAKTIKUM: KOMUNIKASI MQTT - SMART ROOM MONITORING
Skenario 2: Pengiriman Data dengan QoS Berbeda (0, 1, 2)
------------------------------------------------------------
Studi Kasus : Smart Room Monitoring
File        : skenario2_subscriber_qos.py
Deskripsi   : Subscriber berlangganan ke tiga topik QoS
              berbeda sekaligus dan menampilkan perbedaannya
============================================================
"""

import paho.mqtt.client as mqtt
import json
import time

# ─── Konfigurasi Broker ───────────────────────────────────
BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Daftar topik beserta QoS subscribe-nya
SUBSCRIPTIONS = [
    ("smartroom/qos0/temperature", 0),
    ("smartroom/qos1/temperature", 1),
    ("smartroom/qos2/temperature", 2),
]

QOS_LABEL = {
    0: "QoS 0 – At most once",
    1: "QoS 1 – At least once",
    2: "QoS 2 – Exactly once ",
}

msg_count = {0: 0, 1: 0, 2: 0}  # Hitung berapa kali tiap QoS diterima

# ─── Callback saat koneksi berhasil ───────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[SUBSCRIBER] Terhubung ke broker {BROKER_HOST}:{BROKER_PORT}")
        for topic, qos in SUBSCRIPTIONS:
            client.subscribe(topic, qos=qos)
            print(f"  Berlangganan: '{topic}' dengan {QOS_LABEL[qos]}")
        print("\n[SUBSCRIBER] Menunggu pesan...\n")

# ─── Callback saat pesan diterima ────────────────────────
def on_message(client, userdata, msg):
    # Tentukan QoS level dari topik
    qos = msg.qos
    msg_count[qos] += 1

    print(f"{'═'*50}")
    print(f"  [TERIMA] {QOS_LABEL[qos]}")
    print(f"  Topik       : {msg.topic}")
    print(f"  QoS Level   : {qos}")
    print(f"  Diterima ke : {msg_count[qos]} kali")

    try:
        data = json.loads(msg.payload.decode())
        print(f"  Sensor ID   : {data['sensor_id']}")
        print(f"  Suhu        : {data['suhu_celsius']} °C")
        print(f"  Lokasi      : {data['lokasi']}")
        print(f"  Waktu       : {data['timestamp']}")
    except:
        print(f"  Raw payload : {msg.payload.decode()}")

# ─── Setup Client ─────────────────────────────────────────
client = mqtt.Client(client_id="subscriber-qos-demo")
client.on_connect = on_connect
client.on_message  = on_message

print("=" * 55)
print("  SKENARIO 2: Subscriber Multi-QoS")
print("  Studi Kasus: Smart Room Monitoring")
print("=" * 55)

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_forever()
