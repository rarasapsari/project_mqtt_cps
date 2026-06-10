# ============================================================
# TUGAS PRAKTIKUM MQTT - SMART ROOM MONITORING
# README & Panduan Menjalankan
# ============================================================

## Prasyarat

### 1. Install Mosquitto Broker
# Ubuntu/Debian:
sudo apt update && sudo apt install -y mosquitto mosquitto-clients

# Jalankan broker:
mosquitto -v
# atau sebagai service:
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

### 2. Install Python Library
pip install paho-mqtt

# ============================================================
# CARA MENJALANKAN TIAP SKENARIO
# (Buka 2 terminal berbeda untuk publisher & subscriber)
# ============================================================

## SKENARIO 1 – Komunikasi Dasar
# Terminal 1 (jalankan subscriber dulu):
python skenario1_subscriber.py

# Terminal 2 (jalankan publisher):
python skenario1_publisher.py

# ─────────────────────────────────────────────────────────
## SKENARIO 2 – Variasi QoS
# Terminal 1:
python skenario2_subscriber_qos.py

# Terminal 2:
python skenario2_publisher_qos.py

# ─────────────────────────────────────────────────────────
## SKENARIO 3 – Beberapa Topik
# Terminal 1:
python skenario3_subscriber_topics.py

# Terminal 2:
python skenario3_publisher_topics.py

# ─────────────────────────────────────────────────────────
## SKENARIO 4 – Wildcard '+'
# (Cukup satu terminal, publisher & subscriber di satu file)
python skenario4_wildcard_plus.py

# ─────────────────────────────────────────────────────────
## SKENARIO 5 – Wildcard '#'
# (Cukup satu terminal, semua client di satu file)
python skenario5_wildcard_hash.py

# ============================================================
# PENGUJIAN MANUAL DENGAN MOSQUITTO CLI
# ============================================================

# Subscribe manual (terminal tersendiri):
mosquitto_sub -h localhost -t "smartroom/#" -v

# Publish manual untuk uji:
mosquitto_pub -h localhost -t "smartroom/ruangA/temperature" -m '{"nilai":27.5}'
