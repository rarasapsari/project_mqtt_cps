"""
============================================================
TUGAS PRAKTIKUM: KOMUNIKASI MQTT - SMART ROOM MONITORING
Skenario 2: Pengiriman Data dengan QoS Berbeda (0, 1, 2)
------------------------------------------------------------
Studi Kasus : Smart Room Monitoring
File        : skenario2_publisher_qos.py
Deskripsi   : Publisher mengirim data sensor yang sama dengan
              tiga level QoS berbeda untuk membandingkan
              perilaku pengiriman pesan.

QoS 0 – At most once  : Pesan dikirim sekali, tanpa konfirmasi
QoS 1 – At least once : Pesan dijamin sampai, bisa duplikat
QoS 2 – Exactly once  : Pesan dijamin sampai tepat satu kali
============================================================
"""

import paho.mqtt.client as mqtt
import json
import time

# ─── Konfigurasi Broker ───────────────────────────────────
BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPICS = {
    0: "smartroom/qos0/temperature",
    1: "smartroom/qos1/temperature",
    2: "smartroom/qos2/temperature",
}

QOS_DESC = {
    0: "At most once  (tidak ada konfirmasi)",
    1: "At least once (konfirmasi PUBACK)",
    2: "Exactly once  (handshake 4 langkah)",
}

# ─── Callback ─────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[PUBLISHER] Terhubung ke broker {BROKER_HOST}:{BROKER_PORT}\n")

def on_publish(client, userdata, mid):
    print(f"  ✔ Konfirmasi diterima (mid={mid})")

# ─── Setup Client ─────────────────────────────────────────
client = mqtt.Client(client_id="publisher-qos-demo")
client.on_connect = on_connect
client.on_publish  = on_publish

print("=" * 55)
print("  SKENARIO 2: Pengiriman Data dengan QoS Berbeda")
print("  Studi Kasus: Smart Room Monitoring")
print("=" * 55)

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_start()
time.sleep(1)

# ─── Data sensor contoh ───────────────────────────────────
sensor_data = {
    "sensor_id"   : "sensor-suhu-01",
    "suhu_celsius": 27.5,
    "lokasi"      : "Ruang Kelas A",
    "timestamp"   : time.strftime("%Y-%m-%d %H:%M:%S")
}

# ─── Kirim dengan masing-masing QoS ──────────────────────
for qos_level in [0, 1, 2]:
    topic   = TOPICS[qos_level]
    payload = json.dumps(sensor_data)

    print(f"\n{'─'*50}")
    print(f"  Mengirim dengan QoS {qos_level}: {QOS_DESC[qos_level]}")
    print(f"  Topik   : {topic}")
    print(f"  Payload : {payload}")

    result = client.publish(topic, payload, qos=qos_level)
    result.wait_for_publish()   # tunggu hingga broker konfirmasi

    print(f"  Status  : {'Berhasil' if result.rc == 0 else 'Gagal'} (rc={result.rc})")
    time.sleep(2)

print(f"\n{'─'*50}")
print("\n[INFO] Perbandingan QoS:")
print("  QoS 0 → Cepat, efisien, tapi bisa hilang jika jaringan buruk")
print("  QoS 1 → Terjamin sampai, tapi bisa diterima lebih dari sekali")
print("  QoS 2 → Paling andal, tapi paling lambat (4-way handshake)")

client.loop_stop()
client.disconnect()
print("\n[PUBLISHER] Koneksi ditutup.")
