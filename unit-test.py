import os
import sys
import time
from bs4 import BeautifulSoup

# ==============================
# 🔍 REQUIRED FILES / STRUCTURE
# ==============================
REQUIRED_FILES = [
    "docker-compose.yml",
    "complete-dashboard.sh",
    "complete-dashboard.json",
    "README.md",

    # Main app folders & files
    "ecommerce-app/app.py",
    "ecommerce-app/Dockerfile",
    "ecommerce-app/requirements.txt",

    "sample-app/app.py",
    "sample-app/Dockerfile",
    "sample-app/requirements.txt",

    "social-app/app.py",
    "social-app/Dockerfile",
    "social-app/requirements.txt",

    # Monitoring
    "grafana/Dockerfile",
    "grafana/datasources.yml",

    "prometheus/Dockerfile",
    "prometheus/prometheus.yml",
]

# 🎨 Warna ANSI
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

LOADING_CHARS = ['|', '/', '-', '\\']

def spinner_print(msg, duration=0.1):
    """Animasi loading dengan warna sesuai status"""
    sys.stdout.write(f"\r{RED}{msg} [START]{RESET}\n")
    sys.stdout.flush()
    time.sleep(0.3)

    for _ in range(2):  # Loop pendek biar cepat
        for char in LOADING_CHARS:
            sys.stdout.write(f"\r{YELLOW}{msg} please wait... {char}{RESET}")
            sys.stdout.flush()
            time.sleep(duration)

    sys.stdout.write(f"\r{GREEN}{msg} ✅ Selesai!{RESET}\n")

def check_file(path):
    spinner_print(f"[CHECK] Mengecek file: {path}")
    if not os.path.isfile(path):
        print(f"{RED}[ERROR] File hilang: {path}{RESET}")
        raise FileNotFoundError(path)

def check_app_structure():
    """Pastikan setiap folder app punya 3 file penting"""
    spinner_print("[CHECK] Mengecek struktur folder aplikasi")

    app_folders = ["ecommerce-app", "sample-app", "social-app"]
    for folder in app_folders:
        files = ["app.py", "Dockerfile", "requirements.txt"]
        for f in files:
            full_path = os.path.join(folder, f)
            if not os.path.isfile(full_path):
                print(f"{RED}[ERROR] File hilang di {folder}: {f}{RESET}")
                raise FileNotFoundError(full_path)
    print(f"{GREEN}✅ Semua aplikasi punya struktur lengkap!{RESET}")

def check_docker_compose_services(path="docker-compose.yml"):
    """Pastikan docker-compose berisi service utama"""
    spinner_print(f"[CHECK] Mengecek service di {path}")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    expected_services = ["grafana", "prometheus", "ecommerce", "sample", "social"]
    for svc in expected_services:
        if svc not in content:
            print(f"{RED}[ERROR] Service '{svc}' tidak ditemukan di docker-compose.yml!{RESET}")
            raise AssertionError(f"Service '{svc}' missing")
    print(f"{GREEN}✅ Semua service ditemukan di docker-compose.yml!{RESET}")

def main():
    print(f"{RED}=== START UNIT TEST FOR MONITORING-DOCKER PROJECT ==={RESET}\n")

    # 1️⃣ Cek semua file wajib
    for f in REQUIRED_FILES:
        check_file(f)

    # 2️⃣ Cek struktur folder app
    check_app_structure()

    # 3️⃣ Cek service di docker-compose.yaml
    check_docker_compose_services()

    print(f"\n{GREEN}🎉 SEMUA FILE, STRUKTUR, DAN KONFIGURASI TERVALIDASI DENGAN AMAN!{RESET}\n")

if __name__ == "__main__":
    main()
