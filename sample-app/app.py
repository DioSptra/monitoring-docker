#!/usr/bin/env python3

import time
import random
from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Inisialisasi Flask app
app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('sample_app_requests_total', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('sample_app_request_duration_seconds', 'Request latency')
ACTIVE_USERS = Gauge('sample_app_active_users', 'Number of active users')
CPU_USAGE = Gauge('sample_app_cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('sample_app_memory_usage_bytes', 'Memory usage in bytes')

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_LATENCY.time():
        # Simulasi processing time
        time.sleep(random.uniform(0.1, 0.5))
        return '''
        <h1>Sample Monitoring Application</h1>
        <p>Aplikasi sederhana untuk demonstrasi monitoring dengan Prometheus dan Grafana</p>
        <ul>
            <li><a href="/metrics">Metrics endpoint</a></li>
            <li><a href="/health">Health check</a></li>
            <li><a href="/simulate-load">Simulate load</a></li>
        </ul>
        '''

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return {'status': 'healthy', 'timestamp': time.time()}

@app.route('/simulate-load')
def simulate_load():
    REQUEST_COUNT.labels(method='GET', endpoint='/simulate-load').inc()
    with REQUEST_LATENCY.time():
        # Simulasi beban kerja
        duration = random.uniform(0.5, 2.0)
        time.sleep(duration)
        
        # Update metrics
        ACTIVE_USERS.set(random.randint(10, 100))
        CPU_USAGE.set(random.uniform(20, 80))
        MEMORY_USAGE.set(random.randint(100000000, 500000000))  # 100MB - 500MB
        
        return f'Load simulation completed in {duration:.2f} seconds'

@app.route('/metrics')
def metrics():
    # Update some metrics before serving
    ACTIVE_USERS.set(random.randint(5, 50))
    CPU_USAGE.set(random.uniform(10, 70))
    MEMORY_USAGE.set(random.randint(50000000, 300000000))
    
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    print("Starting Sample Monitoring Application...")
    print("Metrics available at: http://localhost:8000/metrics")
    app.run(host='0.0.0.0', port=8000, debug=False)