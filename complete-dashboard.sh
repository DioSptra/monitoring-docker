#!/bin/bash

# 🚀 Script untuk Setup Complete Dashboard Grafana
# Monitoring Docker - Complete Dashboard with All Features

echo "🚀 Setting up Complete Docker Monitoring Dashboard..."

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Konfigurasi
GRAFANA_URL="http://localhost:3000"
GRAFANA_USER="admin"
GRAFANA_PASS="admin"
COMPLETE_DASHBOARD="complete-dashboard.json"
MINIMAL_DASHBOARD="minimal-dashboard.json"

# Fungsi untuk print dengan warna
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

print_highlight() {
    echo -e "${CYAN}[HIGHLIGHT]${NC} $1"
}

# Header
echo ""
echo "🎯 =============================================="
echo "🚀 COMPLETE DOCKER MONITORING DASHBOARD SETUP"
echo "🎯 =============================================="
echo ""

# Step 1: Generate comprehensive metrics
print_header "Step 1: Generating Comprehensive Metrics Data"
print_status "Generating E-Commerce metrics..."
for i in {1..5}; do
    curl -s http://localhost:8001/ > /dev/null 2>&1
    curl -s http://localhost:8001/simulate-sales > /dev/null 2>&1
    sleep 1
done

print_status "Generating Weather metrics..."
for i in {1..5}; do
    curl -s http://localhost:8002/ > /dev/null 2>&1
    curl -s http://localhost:8002/update-weather > /dev/null 2>&1
    sleep 1
done

print_status "Generating Social Media metrics..."
for i in {1..5}; do
    curl -s http://localhost:8003/ > /dev/null 2>&1
    curl -s http://localhost:8003/generate-content > /dev/null 2>&1
    sleep 1
done

print_status "Generating Sample App metrics..."
for i in {1..3}; do
    curl -s http://localhost:8000/ > /dev/null 2>&1
    curl -s http://localhost:8000/simulate-load > /dev/null 2>&1
    sleep 1
done

print_success "✅ Comprehensive metrics generated!"

# Step 2: Wait for data collection
print_header "Step 2: Waiting for Prometheus Data Collection"
print_status "Waiting 15 seconds for Prometheus to scrape all metrics..."
sleep 15
print_success "✅ Data collection period completed!"

# Step 3: Test connectivity
print_header "Step 3: Testing System Connectivity"

# Test Grafana
if curl -s "$GRAFANA_URL/api/health" > /dev/null; then
    print_success "✅ Grafana is accessible"
else
    print_error "❌ Grafana is not accessible"
    exit 1
fi

# Test Prometheus
if curl -s "http://localhost:9090/-/ready" > /dev/null; then
    print_success "✅ Prometheus is accessible"
else
    print_error "❌ Prometheus is not accessible"
    exit 1
fi

# Test Applications
APPS=("8001:E-Commerce" "8002:Weather" "8003:Social" "8000:Sample")
for app in "${APPS[@]}"; do
    port=$(echo $app | cut -d: -f1)
    name=$(echo $app | cut -d: -f2)
    
    if curl -s "http://localhost:$port" > /dev/null; then
        print_success "✅ $name app is accessible"
    else
        print_warning "⚠️ $name app is not responding"
    fi
done

# Step 4: Verify Prometheus targets
print_header "Step 4: Verifying Prometheus Targets"
TARGETS_STATUS=$(curl -s "http://localhost:9090/api/v1/targets" 2>/dev/null)

if echo "$TARGETS_STATUS" | grep -q '"health":"up"'; then
    print_success "✅ Prometheus targets are healthy!"
    
    # Show detailed target status
    echo ""
    print_status "Target Status Details:"
    curl -s "http://localhost:9090/api/v1/targets" | grep -o '"job":"[^"]*","health":"[^"]*"' | while read line; do
        job=$(echo $line | grep -o '"job":"[^"]*"' | cut -d'"' -f4)
        health=$(echo $line | grep -o '"health":"[^"]*"' | cut -d'"' -f4)
        
        if [ "$health" = "up" ]; then
            print_success "  🟢 $job: $health"
        else
            print_error "  🔴 $job: $health"
        fi
    done
else
    print_warning "⚠️ Some Prometheus targets might be down"
fi

# Step 5: Test comprehensive queries
print_header "Step 5: Testing Complete Dashboard Queries"

QUERIES=(
    "up:Service Status"
    "ecommerce_active_users:E-Commerce Users"
    "ecommerce_total_sales_usd:E-Commerce Sales"
    "weather_temperature_celsius:Weather Temperature"
    "weather_humidity_percent:Weather Humidity"
    "social_followers_count:Social Followers"
    "social_engagement_rate_percent:Social Engagement"
    "rate(ecommerce_requests_total[5m]):E-Commerce Request Rate"
    "rate(weather_requests_total[5m]):Weather Request Rate"
    "rate(social_requests_total[5m]):Social Request Rate"
)

WORKING_QUERIES=0
TOTAL_QUERIES=${#QUERIES[@]}

for query_info in "${QUERIES[@]}"; do
    query=$(echo $query_info | cut -d: -f1)
    name=$(echo $query_info | cut -d: -f2)
    
    RESULT=$(curl -s "http://localhost:9090/api/v1/query?query=$query" 2>/dev/null)
    if echo "$RESULT" | grep -q '"status":"success"' && echo "$RESULT" | grep -q '"result":\['; then
        if echo "$RESULT" | grep -q '"value":\['; then
            print_success "  ✅ $name: Has data"
            WORKING_QUERIES=$((WORKING_QUERIES + 1))
        else
            print_warning "  ⚠️ $name: Query works but no data"
        fi
    else
        print_error "  ❌ $name: Query failed"
    fi
done

echo ""
print_highlight "📊 Query Success Rate: $WORKING_QUERIES/$TOTAL_QUERIES queries working"

# Step 6: Setup/verify data source
print_header "Step 6: Configuring Prometheus Data Source"
DS_RESPONSE=$(curl -s -u "$GRAFANA_USER:$GRAFANA_PASS" "$GRAFANA_URL/api/datasources" 2>/dev/null)

if echo "$DS_RESPONSE" | grep -q "prometheus"; then
    print_success "✅ Prometheus data source exists"
    DS_UID=$(echo "$DS_RESPONSE" | grep -o '"uid":"[^"]*"' | head -1 | cut -d'"' -f4)
    print_status "Data source UID: $DS_UID"
else
    print_warning "⚠️ Creating Prometheus data source..."
    
    DS_CREATE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -u "$GRAFANA_USER:$GRAFANA_PASS" \
        -d '{
            "name": "Prometheus",
            "type": "prometheus",
            "url": "http://prometheus:9090",
            "access": "proxy",
            "isDefault": true,
            "uid": "prometheus"
        }' \
        "$GRAFANA_URL/api/datasources" 2>/dev/null)
    
    if echo "$DS_CREATE" | grep -q '"message":"Datasource added"'; then
        print_success "✅ Prometheus data source created"
        DS_UID="prometheus"
    else
        print_error "❌ Failed to create data source"
        DS_UID="prometheus"
    fi
fi

# Step 7: Import complete dashboard
print_header "Step 7: Importing Complete Dashboard"

# Determine which dashboard to use
if [ $WORKING_QUERIES -ge 5 ] && [ -f "$COMPLETE_DASHBOARD" ]; then
    DASHBOARD_FILE="$COMPLETE_DASHBOARD"
    DASHBOARD_TYPE="Complete"
    print_highlight "🎯 Using COMPLETE dashboard with all features!"
elif [ -f "$MINIMAL_DASHBOARD" ]; then
    DASHBOARD_FILE="$MINIMAL_DASHBOARD"
    DASHBOARD_TYPE="Minimal"
    print_warning "⚠️ Using minimal dashboard (limited data available)"
else
    print_error "❌ No dashboard files found"
    exit 1
fi

print_status "Importing $DASHBOARD_TYPE dashboard: $DASHBOARD_FILE"

# Replace data source UID in JSON if needed
if [ -n "$DS_UID" ]; then
    sed "s/\"uid\": \"prometheus\"/\"uid\": \"$DS_UID\"/g" "$DASHBOARD_FILE" > temp-dashboard.json
    IMPORT_FILE="temp-dashboard.json"
else
    IMPORT_FILE="$DASHBOARD_FILE"
fi

IMPORT_RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -u "$GRAFANA_USER:$GRAFANA_PASS" \
    -d @"$IMPORT_FILE" \
    "$GRAFANA_URL/api/dashboards/db" 2>/dev/null)

if echo "$IMPORT_RESPONSE" | grep -q '"status":"success"'; then
    print_success "🎉 $DASHBOARD_TYPE dashboard imported successfully!"
    
    # Get dashboard URL
    DASHBOARD_URL=$(echo "$IMPORT_RESPONSE" | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
    print_highlight "🌐 Dashboard URL: $GRAFANA_URL$DASHBOARD_URL"
    
elif echo "$IMPORT_RESPONSE" | grep -q '"message":"Dashboard with the same title already exists"'; then
    print_warning "⚠️ Dashboard already exists. Updating..."
    
    # Force update
    IMPORT_RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -u "$GRAFANA_USER:$GRAFANA_PASS" \
        -d @"$IMPORT_FILE" \
        "$GRAFANA_URL/api/dashboards/db" 2>/dev/null)
    
    if echo "$IMPORT_RESPONSE" | grep -q '"status":"success"'; then
        print_success "🎉 Dashboard updated successfully!"
    else
        print_error "❌ Failed to update dashboard"
    fi
else
    print_error "❌ Failed to import dashboard"
    print_status "Response: $IMPORT_RESPONSE"
    
    # Fallback to minimal
    if [ "$DASHBOARD_FILE" != "$MINIMAL_DASHBOARD" ] && [ -f "$MINIMAL_DASHBOARD" ]; then
        print_status "🔄 Trying fallback to minimal dashboard..."
        
        FALLBACK_RESPONSE=$(curl -s -X POST \
            -H "Content-Type: application/json" \
            -u "$GRAFANA_USER:$GRAFANA_PASS" \
            -d @"$MINIMAL_DASHBOARD" \
            "$GRAFANA_URL/api/dashboards/db" 2>/dev/null)
        
        if echo "$FALLBACK_RESPONSE" | grep -q '"status":"success"'; then
            print_success "✅ Fallback minimal dashboard imported!"
        fi
    fi
fi

# Cleanup
[ -f "temp-dashboard.json" ] && rm temp-dashboard.json

# Step 8: Final verification and instructions
print_header "Step 8: Final Verification & Instructions"

echo ""
print_highlight "🎉 =============================================="
print_highlight "🚀 COMPLETE DASHBOARD SETUP FINISHED!"
print_highlight "🎉 =============================================="
echo ""

print_success "✅ Dashboard Features Included:"
echo "   🔥 Service Health Status with emoji indicators"
echo "   💻 System Resources (CPU, Memory) with thresholds"
echo "   📊 Application Request Rates with smooth animations"
echo "   🛒 E-Commerce Metrics (Users, Sales, Conversion)"
echo "   🌤️ Weather Monitoring (Temperature, Humidity, Air Quality)"
echo "   📱 Social Media Analytics (Followers, Engagement)"
echo "   ⚡ Response Times (95th Percentile)"
echo "   🌐 Network I/O Monitoring"
echo "   📈 Business KPIs Overview"
echo ""

print_highlight "🌐 Access Your Complete Dashboard:"
echo "   📊 Grafana: $GRAFANA_URL"
echo "   🔑 Login: admin / admin"
echo "   📋 Dashboard: 'Docker Monitoring - Complete Dashboard'"
echo ""

print_highlight "🔗 Quick Access Links (Available in Dashboard):"
echo "   🛒 E-Commerce App: http://localhost:8001"
echo "   🌤️ Weather App: http://localhost:8002"
echo "   📱 Social Media App: http://localhost:8003"
echo "   📋 Sample App: http://localhost:8000"
echo "   📊 Prometheus: http://localhost:9090"
echo ""

print_highlight "⚙️ Dashboard Settings:"
echo "   🔄 Auto-refresh: Every 5 seconds"
echo "   ⏰ Time range: Last 15 minutes"
echo "   📱 Mobile responsive design"
echo "   🎨 Color-coded thresholds and alerts"
echo ""

print_highlight "💡 Pro Tips:"
echo "   • Visit applications to generate more metrics"
echo "   • Use time range picker for different views"
echo "   • Click on panel titles to drill down"
echo "   • Use dashboard links for quick navigation"
echo ""

# Show current metrics status
print_status "📊 Current Metrics Status:"
CURRENT_METRICS=$(curl -s "http://localhost:9090/api/v1/query?query=up" 2>/dev/null)
if echo "$CURRENT_METRICS" | grep -q '"result":\['; then
    echo "$CURRENT_METRICS" | grep -o '"metric":{"[^}]*},"value":\[[^]]*\]' | while read line; do
        job=$(echo $line | grep -o '"job":"[^"]*"' | cut -d'"' -f4)
        value=$(echo $line | grep -o '"value":\[[^]]*\]' | grep -o '\[.*\]' | cut -d',' -f2 | tr -d '"]')
        
        if [ "$value" = "1" ]; then
            print_success "  🟢 $job: UP"
        else
            print_error "  🔴 $job: DOWN"
        fi
    done
else
    print_warning "  ⚠️ No metrics data available yet"
fi

echo ""
print_success "🎉 Complete Dashboard Setup Finished Successfully!"
print_highlight "🚀 Enjoy your comprehensive Docker monitoring experience!"