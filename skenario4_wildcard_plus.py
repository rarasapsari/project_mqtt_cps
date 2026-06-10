"""
============================================================
TUGAS PRAKTIKUM: KOMUNIKASI MQTT - SMART ROOM MONITORING
Skenario 4: Penggunaan Wildcard '+'
------------------------------------------------------------
Studi Kasus : Smart Room Monitoring
File        : skenario4_wildcard_plus.py
Deskripsi   : Mendemonstrasikan wildcard '+' yang menggantikan
              TEPAT SATU level topik.

Wildcard '+':
  • Menggantikan satu segmen level topik
  • Contoh: smartroom/+/temperature
    → COCOK dengan: smartroom/ruangA/temperature
    → COCOK dengan: smartroom/ruangB/temperature
    → TIDAK cocok : smartroom/ruangA/sensor/temperature (2 level)

Program ini menjalankan publisher dan subscriber
dalam satu file menggunakan dua client terpisah.
============================================================
"""

import paho.mqtt.client as mqtt
import json
import time
import threading
import random

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# ══════════════════════════════════════════════════════════
# SUBSCRIBER – berlangganan dengan wildcard '+'
# ══════════════════════════════════════════════════════════

def jalankan_subscriber():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            # Wildcard '+' = hanya satu level
            wildcard = "smartroom/+/temperature"
            client.subscribe(wildcard, qos=1)
            print(f"[SUB] Berlangganan dengan wildcard: '{wildcard}'")
            print(f"[SUB] Akan menerima dari SEMUA ruangan, hanya topik 'temperature'\n")

    def on_message(client, userdata, msg):
        parts   = msg.topic.split("/")
        ruangan = parts[1] if len(parts) > 1 else "?"
        print(f"[SUB ✔] Diterima dari: {msg.topic}")
        try:
            d = json.loads(msg.payload.decode())
            print(f"        Ruangan : {ruangan.upper()}")
            print(f"        Suhu    : {d.get('nilai', '-')} {d.get('satuan', '')}")
            print(f"        Waktu   : {d.get('timestamp', '-')}\n")
        except:
            print(f"        Payload : {msg.payload.decode()}\n")

    sub = mqtt.Client(client_id="sub-wildcard-plus")
    sub.on_connect = on_connect
    sub.on_message  = on_message
    sub.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    sub.loop_forever()

# ══════════════════════════════════════════════════════════
# PUBLISHER – kirim ke berbagai topik untuk uji wildcard
# ══════════════════════════════════════════════════════════

def jalankan_publisher():
    time.sleep(2)  # Beri waktu subscriber terhubung

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[PUB] Publisher terhubung ke broker\n")

    pub = mqtt.Client(client_id="pub-wildcard-plus")
    pub.on_connect = on_connect
    pub.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    pub.loop_start()
    time.sleep(1)

    test_cases = [
        # (topik, deskripsi, apakah cocok?)
        ("smartroom/ruangA/temperature", "Ruang A – Suhu",       "✔ COCOK"),
        ("smartroom/ruangB/temperature", "Ruang B – Suhu",       "✔ COCOK"),
        ("smartroom/ruangC/temperature", "Ruang C – Suhu",       "✔ COCOK"),
        ("smartroom/ruangA/humidity",    "Ruang A – Kelembaban", "✘ TIDAK COCOK"),
        ("smartroom/ruangA/light",       "Ruang A – Cahaya",     "✘ TIDAK COCOK"),
    ]

    print("[PUB] Mengirim ke berbagai topik untuk menguji wildcard '+':")
    print(f"      Pola subscriber: smartroom/+/temperature\n")

    for topic, desc, match in test_cases:
        payload = json.dumps({
            "nilai"    : round(random.uniform(23.0, 30.0), 2),
            "satuan"   : "Celsius",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"[PUB] Kirim → {topic:<40} [{match}]")
        pub.publish(topic, payload, qos=1)
        time.sleep(1.5)

    pub.loop_stop()
    pub.disconnect()

# ─── Jalankan keduanya ────────────────────────────────────
print("=" * 60)
print("  SKENARIO 4: Wildcard '+' (Single-Level)")
print("  Studi Kasus: Smart Room Monitoring")
print("=" * 60 + "\n")

t_sub = threading.Thread(target=jalankan_subscriber, daemon=True)
t_pub = threading.Thread(target=jalankan_publisher)

t_sub.start()
t_pub.start()
t_pub.join()

print("\n[INFO] Publisher selesai. Tekan Ctrl+C untuk menutup subscriber.")
try:
    t_sub.join()
except KeyboardInterrupt:
    print("\nProgram dihentikan.")
