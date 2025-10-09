#!/bin/bash
set -Eeuo pipefail

APP_DIR="/home/ubuntu/myapp"

log()   { echo -e "\033[34m$*\033[0m"; }
ok()    { echo -e "\033[32m$*\033[0m"; }
warn()  { echo -e "\033[33m$*\033[0m"; }
err()   { echo -e "\033[31m$*\033[0m" >&2; }

dump_logs() {
  $COMPOSE ps -a || true
  echo -e "\n--- prometheus ---"; $COMPOSE logs --tail=150 prometheus || true
  echo -e "\n--- grafana    ---"; $COMPOSE logs --tail=150 grafana || true
  echo -e "\n--- others     ---"; $COMPOSE logs --tail=80  node-exporter sample-app ecommerce-app weather-app social-app || true
}

log "🚀 Ensure Docker"
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common git
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | sudo gpg --dearmor --yes --batch -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
fi
sudo systemctl enable docker
sudo systemctl start docker

log "🔄 Sync repo"
if [ -d "$APP_DIR/.git" ]; then
  cd "$APP_DIR"
  git fetch origin
  git reset --hard origin/master
else
  sudo rm -rf "$APP_DIR"
  git clone https://github.com/DioSptra/monitoring-docker.git "$APP_DIR"
  cd "$APP_DIR"
fi
ok "Repo: $(pwd)"

# pilih compose file
if     [ -f docker-compose.yml ];  then CF=docker-compose.yml
elif   [ -f docker-compose.yaml ]; then CF=docker-compose.yaml
elif   [ -f compose.yml ];         then CF=compose.yml
elif   [ -f compose.yaml ];        then CF=compose.yaml
else err "❌ Tidak ada docker-compose.* di $(pwd)"; ls -la; exit 1; fi
COMPOSE="sudo docker compose -f $CF"

log "🧪 Validate compose"
$COMPOSE config --quiet || { err "❌ Compose invalid"; $COMPOSE config; exit 1; }

log "🧹 Down old stack"
$COMPOSE down || true

log "🛠️ Build (lihat error jelas bila gagal)"
$COMPOSE build --no-cache --progress=plain || { err "❌ Build gagal"; exit 1; }

log "🚀 Up stack"
$COMPOSE up -d --remove-orphans || { err "❌ Up gagal"; dump_logs; exit 1; }

log "📋 Status"
$COMPOSE ps -a || true

RUNNING=$($COMPOSE ps --status running --services | wc -l || echo 0)
if [ "$RUNNING" -eq 0 ]; then
  err "❌ Tidak ada container yang running setelah up"
  dump_logs
  exit 1
fi
ok "✅ Running services: $RUNNING"

# (opsional) health quick check
if curl -sSf http://localhost:9090/-/ready >/dev/null 2>&1; then ok "Prometheus ready"; else warn "Prometheus belum ready"; fi
HTTP_GRAFANA=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/login || true)
[ "$HTTP_GRAFANA" = "200" ] && ok "Grafana login OK" || warn "Grafana belum accessible (HTTP $HTTP_GRAFANA)"

ok "🎉 Deployment completed"
sudo docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
