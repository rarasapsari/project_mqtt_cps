"""
============================================================
TUGAS PRAKTIKUM: KOMUNIKASI MQTT - SMART ROOM MONITORING
Skenario 5: Penggunaan Wildcard '#'
------------------------------------------------------------
Studi Kasus : Smart Room Monitoring
File        : skenario5_wildcard_hash.py
Deskripsi   : Mendemonstrasikan wildcard '#' yang menggantikan
              SEMUA level topik di bawahnya (multi-level).

Wildcard '#':
  • Harus berada di AKHIR pola topik
  • Menangkap satu atau lebih level topik
  • Contoh: smartroom/#
    → COCOK: smartroom/ruangA/temperature
    → COCOK: smartroom/ruangB/humidity
    → COCOK: smartroom/ruangA/sensor/temp/detail
    → COCOK: smartroom/status (hanya 1 level di bawah)

Program ini menjalankan beberapa subscriber sekaligus
dengan cakupan wildcard berbeda untuk perbandingan.
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
# HELPER: Buat subscriber dengan wildcard tertentu
# ══════════════════════════════════════════════════════════

def buat_subscriber(client_id, wildcard, label):
    """Factory function untuk membuat subscriber."""

    counter = {"n": 0}

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(wildcard, qos=1)
            print(f"[{label}] Berlangganan: '{wildcard}'")

    def on_message(client, userdata, msg):
        counter["n"] += 1
        print(f"[{label}] #{counter['n']:02d} | Topik: {msg.topic}")

    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.on_message  = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    return client

# ══════════════════════════════════════════════════════════
# PUBLISHER – kirim ke berbagai topik hierarkis
# ══════════════════════════════════════════════════════════

def jalankan_publisher():
    time.sleep(3)  # Beri waktu semua subscriber terhubung

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("\n[PUB] Publisher siap mengirim\n")

    pub = mqtt.Client(client_id="pub-wildcard-hash")
    pub.on_connect = on_connect
    pub.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    pub.loop_start()
    time.sleep(1)

    # Topik dengan kedalaman hierarki berbeda
    topik_list = [
        "smartroom/ruangA/temperature",
        "smartroom/ruangA/humidity",
        "smartroom/ruangA/light",
        "smartroom/ruangB/temperature",
        "smartroom/ruangB/motion",
        "smartroom/ruangA/sensor/co2/detail",   # 5 level
        "smartroom/status",                      # 2 level
        "gedung/lantai1/smartroom/temperature",  # beda awalan
    ]

    print("[PUB] Topik yang akan dikirim:")
    for t in topik_list:
        print(f"       • {t}")
    print()

    for topic in topik_list:
        payload = json.dumps({
            "nilai"    : round(random.uniform(20.0, 35.0), 2),
            "timestamp": time.strftime("%H:%M:%S")
        })
        print(f"[PUB] Kirim → {topic}")
        pub.publish(topic, payload, qos=1)
        time.sleep(1.2)

    pub.loop_stop()
    pub.disconnect()

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════

print("=" * 60)
print("  SKENARIO 5: Wildcard '#' (Multi-Level)")
print("  Studi Kasus: Smart Room Monitoring")
print("=" * 60)
print("\n  Tiga subscriber dengan cakupan berbeda:")
print("  [A] smartroom/#          → semua di bawah smartroom")
print("  [B] smartroom/ruangA/#   → hanya Ruang A")
print("  [C] #                    → SEMUA topik di broker")
print()

# Buat subscriber dengan wildcard berbeda
sub_a = buat_subscriber("sub-hash-all",    "smartroom/#",        "SUB-A smartroom/#       ")
sub_b = buat_subscriber("sub-hash-ruanga", "smartroom/ruangA/#", "SUB-B smartroom/ruangA/#")
sub_c = buat_subscriber("sub-hash-global", "#",                  "SUB-C #                 ")

# Jalankan semua subscriber di thread terpisah
for sub in [sub_a, sub_b, sub_c]:
    t = threading.Thread(target=sub.loop_forever, daemon=True)
    t.start()

# Jalankan publisher
t_pub = threading.Thread(target=jalankan_publisher)
t_pub.start()
t_pub.join()

print("\n[INFO] Analisis Wildcard '#':")
print("  SUB-A (smartroom/#)        → menerima semua topik yang dimulai 'smartroom/'")
print("  SUB-B (smartroom/ruangA/#) → hanya topik Ruang A")
print("  SUB-C (#)                  → menerima SEMUA topik termasuk 'gedung/...'")
print("\nTekan Ctrl+C untuk berhenti.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram dihentikan.")
