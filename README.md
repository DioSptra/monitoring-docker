# 🚀 Monitoring Tools dengan Docker - 3 Aplikasi Demo dengan Animasi

## 📋 Deskripsi

Proyek ini adalah materi praktik untuk mempelajari monitoring tools berbasis container menggunakan **Prometheus**, **Grafana**, dan **Node Exporter**. Proyek ini dilengkapi dengan **3 aplikasi demo yang menarik** dengan animasi CSS yang keren untuk memberikan pengalaman monitoring yang lebih interaktif dan visual.

## 🎯 Aplikasi Demo yang Tersedia

### 1. 🛒 **E-Commerce Dashboard** (Port 8001)
Dashboard monitoring untuk toko online dengan fitur:
- **Real-time sales tracking** dengan animasi counter
- **User engagement metrics** dengan efek hover yang smooth
- **Product analytics** dengan visualisasi yang menarik
- **Activity feed** dengan animasi slide-in
- **Auto-refresh** setiap 5 detik

**Metrics yang dimonitor:**
- Active Users
- Total Sales (USD)
- Total Orders
- Average Cart Items
- Conversion Rate
- Product Views

### 2. 🌤️ **Weather Monitoring** (Port 8002)
Dashboard cuaca real-time dengan animasi yang menawan:
- **Animated weather icons** dengan efek bounce
- **Floating clouds** yang bergerak di background
- **Rain animation** ketika curah hujan tinggi
- **Gradient backgrounds** yang berubah sesuai kondisi
- **Weather forecast** dengan slide animations

**Metrics yang dimonitor:**
- Temperature (°C)
- Humidity (%)
- Atmospheric Pressure (hPa)
- Wind Speed (km/h)
- Rainfall (mm)
- Air Quality Index

### 3. 📱 **Social Media Analytics** (Port 8003)
Dashboard analytics media sosial dengan animasi yang dinamis:
- **Floating social icons** yang bergerak di background
- **Platform cards** dengan efek shine dan hover
- **Engagement bars** dengan animasi fill
- **Trending hashtags** dengan real-time updates
- **Multi-platform monitoring** (Facebook, Instagram, Twitter, TikTok)

**Metrics yang dimonitor:**
- Followers count per platform
- Posts/content count
- Likes, shares, comments
- Engagement rate
- Trending hashtags

## 🔧 Komponen Monitoring

### 1. **Prometheus**
Sistem monitoring dan alerting open-source yang mengumpulkan metrics dari ketiga aplikasi demo melalui HTTP endpoints.

**Fitur utama:**
- Mengumpulkan metrics dari 3 aplikasi demo + Node Exporter
- Menyimpan data dalam time-series database
- Query language (PromQL) untuk analisis data
- Web UI untuk query dan visualisasi

### 2. **Grafana**
Platform visualisasi yang terhubung ke Prometheus untuk membuat dashboard interaktif.

**Fitur utama:**
- Dashboard yang dapat dikustomisasi untuk setiap aplikasi
- Berbagai jenis visualisasi (graph, table, heatmap, gauge)
- Alerting dan notification
- Multi-datasource support

### 3. **Node Exporter**
Exporter untuk hardware dan OS metrics dari host system.

**Metrics yang dikumpulkan:**
- CPU usage dan load average
- Memory dan swap usage
- Disk space dan I/O statistics
- Network interface statistics
- System uptime

## 🚀 Instruksi Deployment di EC2 Ubuntu

### Langkah 1: Login ke EC2 Ubuntu via SSH

```bash
ssh -i your-key.pem ubuntu@<EC2-Public-IP>
```

### Langkah 2: Install Docker & Docker Compose

```bash
# Update package index
sudo apt update

# Install dependencies
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again
sudo apt update

# Install Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again to apply group changes
exit
```

Login kembali ke EC2:
```bash
ssh -i your-key.pem ubuntu@<EC2-Public-IP>
```

### Langkah 3: Clone atau Upload Project

```bash
# Jika menggunakan git
git clone <repository-url>

# Atau upload folder Monitoring-Docker ke EC2
# Gunakan scp atau tools lainnya untuk upload
```

### Langkah 4: Masuk ke Folder Project

```bash
cd Monitoring-Docker/
```

### Langkah 5: Build Docker Images

```bash
docker-compose build
```

### Langkah 6: Jalankan Stack Monitoring

```bash
docker-compose up -d
```

### Langkah 7: Verifikasi Services

```bash
# Cek status containers
docker-compose ps

# Cek logs jika ada masalah
docker-compose logs

# Cek logs aplikasi tertentu
docker-compose logs ecommerce-app
docker-compose logs weather-app
docker-compose logs social-app
```

## 🌐 Akses Aplikasi

Setelah semua services berjalan, Anda dapat mengakses aplikasi melalui Public IP EC2:

### 📊 Monitoring Tools
- **Prometheus**: `http://<EC2-Public-IP>:9090`
- **Grafana**: `http://<EC2-Public-IP>:3000`
- **Node Exporter**: `http://<EC2-Public-IP>:9100/metrics`

### 🎨 Demo Applications (dengan Animasi!)
- **📊 Sample App (Basic)**: `http://<EC2-Public-IP>:8000`
- **🛒 E-Commerce Dashboard**: `http://<EC2-Public-IP>:8001`
- **🌤️ Weather Monitoring**: `http://<EC2-Public-IP>:8002`
- **📱 Social Media Analytics**: `http://<EC2-Public-IP>:8003`

### Login Grafana
- **Username**: `admin`
- **Password**: `admin`

## 📊 Konfigurasi Grafana

### 1. Menambahkan Prometheus sebagai Data Source

Prometheus sudah dikonfigurasi secara otomatis sebagai data source melalui file `datasources.yml`.

### 2. Membuat Dashboard untuk E-Commerce App

**Panel 1: Active Users**
```promql
ecommerce_active_users
```

**Panel 2: Total Sales**
```promql
ecommerce_total_sales_usd
```

**Panel 3: Orders Rate**
```promql
rate(ecommerce_orders_total[5m])
```

**Panel 4: Conversion Rate**
```promql
ecommerce_conversion_rate_percent
```

**Panel 5: Product Views by Category**
```promql
rate(ecommerce_product_views_total[5m])
```

### 3. Membuat Dashboard untuk Weather App

**Panel 1: Temperature**
```promql
weather_temperature_celsius
```

**Panel 2: Humidity**
```promql
weather_humidity_percent
```

**Panel 3: Wind Speed**
```promql
weather_wind_speed_kmh
```

**Panel 4: Air Quality**
```promql
weather_air_quality_index
```

**Panel 5: Rainfall**
```promql
weather_rainfall_mm
```

### 4. Membuat Dashboard untuk Social Media App

**Panel 1: Followers by Platform**
```promql
social_followers_count
```

**Panel 2: Engagement Rate**
```promql
social_engagement_rate_percent
```

**Panel 3: Posts Rate**
```promql
rate(social_posts_total[5m])
```

**Panel 4: Likes Rate**
```promql
rate(social_likes_total[5m])
```

**Panel 5: Active Users**
```promql
social_active_users_count
```

### 5. Dashboard untuk Node Exporter

**Panel 1: CPU Usage**
```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Panel 2: Memory Usage**
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

**Panel 3: Disk Usage**
```promql
100 - ((node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100)
```

## 🎯 Ekspektasi Hasil

Setelah menyelesaikan praktik ini, peserta diharapkan dapat:

1. ✅ **Mengakses Prometheus** di `http://<EC2-Public-IP>:9090` dan melihat 5 targets yang ter-scrape
2. ✅ **Mengakses Grafana** di `http://<EC2-Public-IP>:3000` dengan login admin/admin
3. ✅ **Melihat 3 aplikasi demo** dengan animasi yang menarik:
   - E-Commerce Dashboard dengan animasi sales metrics
   - Weather Monitoring dengan animasi cuaca
   - Social Media Analytics dengan animasi engagement
4. ✅ **Membuat dashboard Grafana** untuk setiap aplikasi
5. ✅ **Mengambil screenshot** yang menampilkan:
   - Ketiga aplikasi demo dengan animasi berjalan
   - Dashboard Grafana dengan metrics dari semua aplikasi
   - URL browser menunjukkan `<EC2-Public-IP>` sebagai bukti akses

## 🎨 Fitur Animasi yang Tersedia

### E-Commerce Dashboard
- ✨ **Counter animations** untuk sales metrics
- 🎯 **Hover effects** pada cards
- 📈 **Pulse animations** untuk buttons
- 🔄 **Auto-refresh** dengan smooth transitions

### Weather Monitoring
- ☁️ **Floating clouds** animation
- 🌧️ **Rain drops** ketika curah hujan tinggi
- 💫 **Bounce effects** untuk weather icons
- 🌈 **Gradient backgrounds** yang dinamis

### Social Media Analytics
- 📱 **Floating social icons** di background
- ✨ **Shine effects** pada platform cards
- 📊 **Animated progress bars** untuk engagement
- 🔥 **Trending hashtags** dengan real-time updates

## 🔍 Tips Troubleshooting

### Jika containers tidak bisa diakses dari internet:
1. Pastikan Security Group EC2 membuka port:
   - 3000 (Grafana)
   - 9090 (Prometheus)
   - 9100 (Node Exporter)
   - 8000 (Sample App)
   - 8001 (E-Commerce App)
   - 8002 (Weather App)
   - 8003 (Social App)

### Jika ada error saat build:
```bash
# Cek logs detail
docker-compose logs [service-name]

# Rebuild tanpa cache
docker-compose build --no-cache

# Restart service tertentu
docker-compose restart [service-name]
```

### Jika aplikasi tidak menampilkan animasi:
1. Pastikan browser mendukung CSS3 animations
2. Coba refresh halaman (Ctrl+F5)
3. Cek console browser untuk error JavaScript

## 📝 Struktur Project

```
Monitoring-Docker/
├── docker-compose.yml          # Orchestration untuk 6 services
├── README.md                   # Dokumentasi lengkap
├── prometheus/
│   ├── Dockerfile
│   └── prometheus.yml          # Config untuk scrape 3 apps
├── grafana/
│   ├── Dockerfile
│   └── datasources.yml
├── sample-app/                 # 📊 Basic Monitoring App
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py                  # Simple Flask monitoring app
├── ecommerce-app/              # 🛒 E-Commerce Dashboard
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py                  # Flask app dengan animasi CSS
├── weather-app/                # 🌤️ Weather Monitoring
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py                  # Flask app dengan weather animations
└── social-app/                 # 📱 Social Media Analytics
    ├── Dockerfile
    ├── requirements.txt
    └── app.py                  # Flask app dengan social media animations
```

## 🎓 Pembelajaran Selanjutnya

Setelah menguasai dasar-dasar ini, Anda dapat melanjutkan dengan:
- Membuat alerting rules di Prometheus untuk setiap aplikasi
- Menggunakan Grafana alerting dengan notification channels
- Menambahkan aplikasi demo baru dengan animasi yang berbeda
- Implementasi service discovery untuk auto-discovery targets
- Menggunakan Prometheus Operator di Kubernetes
- Membuat custom metrics untuk business logic yang spesifik

## 🌟 Keunggulan Project Ini

1. **3 Aplikasi Demo Berbeda** - E-commerce, Weather, Social Media
2. **Animasi CSS yang Menarik** - Membuat monitoring lebih visual dan engaging
3. **Real-time Updates** - Data berubah secara dinamis dengan auto-refresh
4. **Responsive Design** - Tampil baik di desktop dan mobile
5. **Comprehensive Metrics** - Berbagai jenis metrics untuk pembelajaran
6. **Easy Deployment** - Satu command untuk menjalankan semua services

---

**Selamat belajar dan berkreasi dengan monitoring tools! 🚀✨**

*Jangan lupa untuk mengambil screenshot aplikasi dengan animasi yang berjalan sebagai bukti pembelajaran!* 📸