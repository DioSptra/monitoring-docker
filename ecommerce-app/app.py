#!/usr/bin/env python3

import time
import random
import json
from flask import Flask, Response, render_template_string
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Inisialisasi Flask app
app = Flask(__name__)

# Prometheus metrics untuk E-commerce
REQUEST_COUNT = Counter('ecommerce_requests_total', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('ecommerce_request_duration_seconds', 'Request latency')
ACTIVE_USERS = Gauge('ecommerce_active_users', 'Number of active users')
TOTAL_SALES = Gauge('ecommerce_total_sales_usd', 'Total sales in USD')
ORDERS_COUNT = Counter('ecommerce_orders_total', 'Total number of orders', ['status'])
PRODUCT_VIEWS = Counter('ecommerce_product_views_total', 'Total product views', ['category'])
CART_ITEMS = Gauge('ecommerce_cart_items_average', 'Average items in cart')
CONVERSION_RATE = Gauge('ecommerce_conversion_rate_percent', 'Conversion rate percentage')

# HTML template dengan animasi CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛒 E-Commerce Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            animation: fadeInDown 1s ease-out;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideInUp 0.8s ease-out;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            animation: bounce 2s infinite;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
            animation: countUp 2s ease-out;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .actions {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 40px;
        }
        
        .btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            animation: pulse 2s infinite;
        }
        
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .activity-feed {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .activity-item {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            animation: slideInLeft 0.5s ease-out;
        }
        
        .activity-item:last-child {
            border-bottom: none;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }
        
        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(255, 107, 107, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(255, 107, 107, 0);
            }
        }
        
        @keyframes countUp {
            from {
                opacity: 0;
                transform: scale(0.5);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 E-Commerce Dashboard</h1>
            <p>Real-time monitoring untuk toko online Anda</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-value">{{ active_users }}</div>
                <div class="stat-label">Active Users</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-value">${{ "%.2f"|format(total_sales) }}</div>
                <div class="stat-label">Total Sales</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">📦</div>
                <div class="stat-value">{{ total_orders }}</div>
                <div class="stat-label">Total Orders</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🛍️</div>
                <div class="stat-value">{{ "%.1f"|format(cart_items) }}</div>
                <div class="stat-label">Avg Cart Items</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-value">{{ "%.1f"|format(conversion_rate) }}%</div>
                <div class="stat-label">Conversion Rate</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">👀</div>
                <div class="stat-value">{{ product_views }}</div>
                <div class="stat-label">Product Views</div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/simulate-sales" class="btn">🚀 Simulate Sales</a>
            <a href="/metrics" class="btn">📊 View Metrics</a>
            <a href="/health" class="btn">❤️ Health Check</a>
        </div>
        
        <div class="activity-feed">
            <h3 style="margin-bottom: 20px;">📈 Recent Activity</h3>
            {% for activity in recent_activities %}
            <div class="activity-item">
                <strong>{{ activity.time }}</strong> - {{ activity.message }}
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        // Auto refresh setiap 5 detik
        setTimeout(() => {
            location.reload();
        }, 5000);
        
        // Animasi counter
        document.querySelectorAll('.stat-value').forEach(el => {
            const finalValue = parseFloat(el.textContent.replace(/[^0-9.-]/g, ''));
            if (!isNaN(finalValue)) {
                let currentValue = 0;
                const increment = finalValue / 50;
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        currentValue = finalValue;
                        clearInterval(timer);
                    }
                    if (el.textContent.includes('$')) {
                        el.textContent = '$' + currentValue.toFixed(2);
                    } else if (el.textContent.includes('%')) {
                        el.textContent = currentValue.toFixed(1) + '%';
                    } else {
                        el.textContent = Math.round(currentValue);
                    }
                }, 50);
            }
        });
    </script>
</body>
</html>
'''

# Data untuk simulasi
recent_activities = []

def add_activity(message):
    global recent_activities
    current_time = time.strftime("%H:%M:%S")
    recent_activities.insert(0, {"time": current_time, "message": message})
    recent_activities = recent_activities[:10]  # Keep only last 10 activities

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_LATENCY.time():
        # Simulasi data real-time
        active_users = random.randint(50, 200)
        total_sales = random.uniform(10000, 50000)
        total_orders = random.randint(100, 500)
        cart_items = random.uniform(2.0, 8.0)
        conversion_rate = random.uniform(2.0, 8.0)
        product_views = random.randint(1000, 5000)
        
        # Update metrics
        ACTIVE_USERS.set(active_users)
        TOTAL_SALES.set(total_sales)
        CART_ITEMS.set(cart_items)
        CONVERSION_RATE.set(conversion_rate)
        
        return render_template_string(HTML_TEMPLATE,
                                    active_users=active_users,
                                    total_sales=total_sales,
                                    total_orders=total_orders,
                                    cart_items=cart_items,
                                    conversion_rate=conversion_rate,
                                    product_views=product_views,
                                    recent_activities=recent_activities)

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    add_activity("Health check performed")
    return {'status': 'healthy', 'timestamp': time.time(), 'service': 'ecommerce-dashboard'}

@app.route('/simulate-sales')
def simulate_sales():
    REQUEST_COUNT.labels(method='GET', endpoint='/simulate-sales').inc()
    with REQUEST_LATENCY.time():
        # Simulasi penjualan
        sales_amount = random.uniform(100, 1000)
        orders = random.randint(5, 20)
        
        # Update metrics
        ORDERS_COUNT.labels(status='completed').inc(orders)
        PRODUCT_VIEWS.labels(category='electronics').inc(random.randint(10, 50))
        PRODUCT_VIEWS.labels(category='clothing').inc(random.randint(5, 30))
        PRODUCT_VIEWS.labels(category='books').inc(random.randint(3, 15))
        
        add_activity(f"Generated ${sales_amount:.2f} in sales with {orders} orders")
        
        time.sleep(random.uniform(0.5, 1.5))
        return f'✅ Sales simulation completed! Generated ${sales_amount:.2f} with {orders} orders'

@app.route('/simulate-load')
def simulate_load():
    REQUEST_COUNT.labels(method='GET', endpoint='/simulate-load').inc()
    with REQUEST_LATENCY.time():
        # Simulasi beban kerja
        duration = random.uniform(0.5, 2.0)
        time.sleep(duration)
        
        # Update metrics
        ACTIVE_USERS.set(random.randint(10, 100))
        
        add_activity(f"Load simulation completed in {duration:.2f} seconds")
        
        return f'Load simulation completed in {duration:.2f} seconds'

@app.route('/metrics')
def metrics():
    # Update metrics sebelum serving
    ACTIVE_USERS.set(random.randint(30, 150))
    TOTAL_SALES.set(random.uniform(5000, 30000))
    CART_ITEMS.set(random.uniform(1.5, 6.0))
    CONVERSION_RATE.set(random.uniform(1.5, 7.0))
    
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    print("🛒 Starting E-Commerce Dashboard...")
    print("📊 Metrics available at: http://localhost:8000/metrics")
    print("🌐 Dashboard available at: http://localhost:8000")
    add_activity("E-Commerce Dashboard started")
    app.run(host='0.0.0.0', port=8000, debug=False)