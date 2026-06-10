# Tugas Praktikum MQTT - Smart Room Monitoring

Dokumen ini berisi panduan lengkap mengenai prasyarat, instalasi, dan cara menjalankan tiap skenario praktikum simulasi pemantauan ruangan pintar menggunakan protokol MQTT.

---

## Prasyarat dan Instalasi

### 1. Install Mosquitto Broker

#### Ubuntu / Debian
Jalankan perintah berikut di terminal untuk memperbarui package list dan menginstal Mosquitto beserta client tools-nya:
```bash
sudo apt update && sudo apt install -y mosquitto mosquitto-clients

```

#### Menjalankan Broker

Jalankan broker secara langsung di foreground untuk melihat log:

```bash
mosquitto -v

```

Atau jalankan sebagai background service:

```bash
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

```

### 2. Install Python Library

Pastikan Python dan pip sudah terinstal, lalu instal library Paho MQTT dengan perintah:

```bash
pip install paho-mqtt

```

---

## Cara Menjalankan Tiap Skenario

Untuk skenario yang menggunakan file publisher dan subscriber terpisah, buka 2 terminal berbeda. Selalu jalankan file subscriber terlebih dahulu agar dapat menerima pesan yang dikirim oleh publisher.

### Skenario 1 - Komunikasi Dasar

* **Terminal 1 (Subscriber):**
```bash
python skenario1_subscriber.py

```


* **Terminal 2 (Publisher):**
```bash
python skenario1_publisher.py

```



### Skenario 2 - Variasi QoS (Quality of Service)

* **Terminal 1 (Subscriber):**
```bash
python skenario2_subscriber_qos.py

```


* **Terminal 2 (Publisher):**
```bash
python skenario2_publisher_qos.py

```



### Skenario 3 - Beberapa Topik

* **Terminal 1 (Subscriber):**
```bash
python skenario3_subscriber_topics.py

```


* **Terminal 2 (Publisher):**
```bash
python skenario3_publisher_topics.py

```



### Skenario 4 - Wildcard '+'

Skenario ini menggabungkan fungsi publisher dan subscriber di dalam satu file tunggal. Untuk menjalankan skenario ini hanya diperlukan satu terminal.

* **Terminal 1:**
```bash
python skenario4_wildcard_plus.py

```



### Skenario 5 - Wildcard '#'

Skenario ini juga menggabungkan semua client di dalam satu file tunggal.

* **Terminal 1:**
```bash
python skenario5_wildcard_hash.py

```



---

## Pengujian Manual dengan Mosquitto CLI

Pengujian broker juga bisa dilakukan secara manual tanpa menggunakan script Python dengan memanfaatkan perintah bawaan dari Mosquitto CLI.

### 1. Subscribe Manual

Buka satu terminal khusus untuk memantau semua topik di bawah struktur `smartroom/`:

```bash
mosquitto_sub -h localhost -t "smartroom/#" -v

```

### 2. Publish Manual

Buka terminal lain untuk mengirimkan data payload sampel:

```bash
mosquitto_pub -h localhost -t "smartroom/ruangA/temperature" -m '{"nilai":27.5}'

```
