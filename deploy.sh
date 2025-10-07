#!/bin/bash
set -e

# Target directory untuk cloning/pulling code
APP_DIR=/home/ubuntu/myapp  

GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

echo -e "${BLUE}🚀 [1/4] Update & install Docker CE (Official) ...${RESET}"

echo -e "${RED}▶ MENJALANKAN : sudo apt-get update...${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo apt-get update -y
echo -e "${GREEN}✅ UPDATE SELESAI ! ! ! ${RESET}\n"

echo -e "${RED}▶ INSTALL DEPENDENCIES UNTUK DOCKER CE...${RESET}"
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common git
echo -e "${GREEN}✅ DEPENDENCIES TERINSTALL ! ! !${RESET}\n"

echo -e "${RED}▶ MENAMBAHKAN GPG KEY DOCKER & REPOSITORY RESMI...${RESET}"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
echo -e "${GREEN}✅ REPOSITORY DOCKER DITAMBAHKAN ! ! !${RESET}\n"

echo -e "${RED}▶ INSTALL DOCKER CE (COMMUNITY EDITION) ...${RESET}"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
echo -e "${GREEN}✅ DOCKER CE & PLUGIN COMPOSE TERINSTALL ! ! !${RESET}\n"

echo -e "${RED}▶ ENABLE & START DOCKER SERVICE ...${RESET}"
sudo systemctl enable docker
sudo systemctl start docker
echo -e "${GREEN}✅ DOCKER SERVICE AKTIF ! ! !${RESET}\n"

echo -e "${BLUE}🔄 [2/4] Clone or pull latest code...${RESET}"

echo -e "${RED}▶ JIKA REPO SUDAH ADA MAKA RESET & PULL . . .${RESET}"
if [ -d "$APP_DIR" ]; then
  echo -e "${YELLOW}🔄 CHECKING REPO AND UPDATE . . . ${RESET}"
  cd $APP_DIR
  git reset --hard
  git pull origin master
  echo -e "${GREEN}✅ REPO SUDAH TERUPDATE ! ! !${RESET}\n"
else
  echo -e "${RED}▶ JIKA REPO BELUM ADA MAKA CLONE UNTUK PERTAMA KALI . . .${RESET}"
  echo -e "${YELLOW}🔄 JALANKAN PERINTAH : GIT CLONE . . . ${RESET}"
  git clone https://github.com/DioSptra/monitoring-docker.git $APP_DIR
  cd $APP_DIR
  echo -e "${GREEN}✅ CLONE SELESAI ! ! !${RESET}\n"
fi

echo -e "${BLUE}⚙️ [3/4] Build & start containers...${RESET}"

echo -e "${RED}▶ HENTIKAN CONTAINER LAMA . . .${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo docker compose down || true
echo -e "${GREEN}✅ CONTAINER LAMA DIHENTIKAN ! ! !${RESET}\n"

echo -e "${RED}▶ BUILD ULANG IMAGE TANPA CACHE . . .${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo docker compose build --no-cache
echo -e "${GREEN}✅ BUILD SELESAI ! ! !${RESET}\n"

echo -e "${RED}▶ MENJALANKAN CONTAINER BARU . . .${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo docker compose up -d
echo -e "${GREEN}✅ CONTAINER BERHASIL DIJALANKAN ! ! !${RESET}\n"

echo -e "${BLUE}🎉 [4/4] DEPLOYMENT COMPLETED ! ! !${RESET}"
sudo docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
