#!/usr/bin/env python3

import time
import random
import json
from flask import Flask, Response, render_template_string
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Inisialisasi Flask app
app = Flask(__name__)

# Prometheus metrics untuk Weather Monitoring
REQUEST_COUNT = Counter('weather_requests_total', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('weather_request_duration_seconds', 'Request latency')
TEMPERATURE = Gauge('weather_temperature_celsius', 'Temperature in Celsius', ['location'])
HUMIDITY = Gauge('weather_humidity_percent', 'Humidity percentage', ['location'])
PRESSURE = Gauge('weather_pressure_hpa', 'Atmospheric pressure in hPa', ['location'])
WIND_SPEED = Gauge('weather_wind_speed_kmh', 'Wind speed in km/h', ['location'])
RAINFALL = Gauge('weather_rainfall_mm', 'Rainfall in mm', ['location'])
AIR_QUALITY = Gauge('weather_air_quality_index', 'Air Quality Index', ['location'])

# HTML template dengan animasi CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌤️ Weather Monitoring Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 50%, #6c5ce7 100%);
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }
        
        .clouds {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .cloud {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50px;
            animation: float 20s infinite linear;
        }
        
        .cloud:before {
            content: '';
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50px;
        }
        
        .cloud1 {
            width: 100px;
            height: 40px;
            top: 20%;
            animation-duration: 25s;
        }
        
        .cloud1:before {
            width: 50px;
            height: 50px;
            top: -25px;
            left: 10px;
        }
        
        .cloud2 {
            width: 80px;
            height: 30px;
            top: 40%;
            animation-duration: 30s;
            animation-delay: -10s;
        }
        
        .cloud2:before {
            width: 40px;
            height: 40px;
            top: -20px;
            left: 15px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 2;
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
        
        .weather-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .weather-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideInUp 0.8s ease-out;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .weather-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        
        .weather-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }
        
        .weather-icon {
            font-size: 3rem;
            margin-bottom: 15px;
            animation: bounce 2s infinite;
        }
        
        .weather-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            animation: pulse 2s infinite;
        }
        
        .weather-label {
            font-size: 1rem;
            opacity: 0.9;
            margin-bottom: 5px;
        }
        
        .weather-location {
            font-size: 0.8rem;
            opacity: 0.7;
        }
        
        .actions {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 40px;
        }
        
        .btn {
            background: linear-gradient(45deg, #00b894, #00cec9);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            animation: glow 2s infinite alternate;
        }
        
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0,184,148,0.4);
        }
        
        .forecast {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .forecast-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            animation: slideInLeft 0.5s ease-out;
        }
        
        .forecast-item:last-child {
            border-bottom: none;
        }
        
        @keyframes float {
            from {
                transform: translateX(-100px);
            }
            to {
                transform: translateX(calc(100vw + 100px));
            }
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
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
            }
        }
        
        @keyframes glow {
            from {
                box-shadow: 0 0 5px rgba(0,184,148,0.5);
            }
            to {
                box-shadow: 0 0 20px rgba(0,184,148,0.8);
            }
        }
        
        @keyframes shine {
            0% {
                transform: translateX(-100%) translateY(-100%) rotate(45deg);
            }
            100% {
                transform: translateX(100%) translateY(100%) rotate(45deg);
            }
        }
        
        .rain {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .raindrop {
            position: absolute;
            width: 2px;
            height: 20px;
            background: rgba(255, 255, 255, 0.3);
            animation: fall linear infinite;
        }
        
        @keyframes fall {
            from {
                transform: translateY(-100vh);
            }
            to {
                transform: translateY(100vh);
            }
        }
    </style>
</head>
<body>
    <div class="clouds">
        <div class="cloud cloud1"></div>
        <div class="cloud cloud2"></div>
    </div>
    
    {% if rainfall > 5 %}
    <div class="rain" id="rain"></div>
    {% endif %}
    
    <div class="container">
        <div class="header">
            <h1>🌤️ Weather Monitoring</h1>
            <p>Real-time weather data dari berbagai lokasi</p>
        </div>
        
        <div class="weather-grid">
            <div class="weather-card">
                <div class="weather-icon">🌡️</div>
                <div class="weather-value">{{ "%.1f"|format(temperature) }}°C</div>
                <div class="weather-label">Temperature</div>
                <div class="weather-location">Jakarta</div>
            </div>
            
            <div class="weather-card">
                <div class="weather-icon">💧</div>
                <div class="weather-value">{{ "%.0f"|format(humidity) }}%</div>
                <div class="weather-label">Humidity</div>
                <div class="weather-location">Jakarta</div>
            </div>
            
            <div class="weather-card">
                <div class="weather-icon">🌪️</div>
                <div class="weather-value">{{ "%.1f"|format(pressure) }}</div>
                <div class="weather-label">Pressure (hPa)</div>
                <div class="weather-location">Jakarta</div>
            </div>
            
            <div class="weather-card">
                <div class="weather-icon">💨</div>
                <div class="weather-value">{{ "%.1f"|format(wind_speed) }}</div>
                <div class="weather-label">Wind Speed (km/h)</div>
                <div class="weather-location">Jakarta</div>
            </div>
            
            <div class="weather-card">
                <div class="weather-icon">🌧️</div>
                <div class="weather-value">{{ "%.1f"|format(rainfall) }}</div>
                <div class="weather-label">Rainfall (mm)</div>
                <div class="weather-location">Jakarta</div>
            </div>
            
            <div class="weather-card">
                <div class="weather-icon">🏭</div>
                <div class="weather-value">{{ "%.0f"|format(air_quality) }}</div>
                <div class="weather-label">Air Quality Index</div>
                <div class="weather-location">Jakarta</div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/update-weather" class="btn">🔄 Update Weather</a>
            <a href="/metrics" class="btn">📊 View Metrics</a>
            <a href="/health" class="btn">❤️ Health Check</a>
        </div>
        
        <div class="forecast">
            <h3 style="margin-bottom: 20px;">📅 Weather Forecast</h3>
            {% for forecast in weather_forecast %}
            <div class="forecast-item">
                <span><strong>{{ forecast.time }}</strong></span>
                <span>{{ forecast.condition }} {{ forecast.temp }}°C</span>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        // Auto refresh setiap 10 detik
        setTimeout(() => {
            location.reload();
        }, 10000);
        
        // Animasi hujan jika rainfall > 5mm
        if ({{ rainfall }} > 5) {
            const rainContainer = document.getElementById('rain');
            if (rainContainer) {
                for (let i = 0; i < 50; i++) {
                    const raindrop = document.createElement('div');
                    raindrop.className = 'raindrop';
                    raindrop.style.left = Math.random() * 100 + '%';
                    raindrop.style.animationDuration = (Math.random() * 0.5 + 0.5) + 's';
                    raindrop.style.animationDelay = Math.random() * 2 + 's';
                    rainContainer.appendChild(raindrop);
                }
            }
        }
        
        // Animasi counter untuk nilai weather
        document.querySelectorAll('.weather-value').forEach(el => {
            const text = el.textContent;
            const finalValue = parseFloat(text.replace(/[^0-9.-]/g, ''));
            if (!isNaN(finalValue)) {
                let currentValue = 0;
                const increment = finalValue / 30;
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        currentValue = finalValue;
                        clearInterval(timer);
                    }
                    if (text.includes('°C')) {
                        el.textContent = currentValue.toFixed(1) + '°C';
                    } else if (text.includes('%')) {
                        el.textContent = Math.round(currentValue) + '%';
                    } else if (text.includes('.')) {
                        el.textContent = currentValue.toFixed(1);
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

# Data untuk simulasi cuaca
weather_forecast = []

def generate_forecast():
    global weather_forecast
    conditions = ["☀️ Sunny", "⛅ Partly Cloudy", "☁️ Cloudy", "🌧️ Rainy", "⛈️ Stormy"]
    weather_forecast = []
    for i in range(5):
        hour = (int(time.strftime("%H")) + i + 1) % 24
        weather_forecast.append({
            "time": f"{hour:02d}:00",
            "condition": random.choice(conditions),
            "temp": random.randint(20, 35)
        })

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_LATENCY.time():
        # Simulasi data cuaca real-time
        temperature = random.uniform(20.0, 35.0)
        humidity = random.uniform(40.0, 90.0)
        pressure = random.uniform(1000.0, 1020.0)
        wind_speed = random.uniform(0.0, 25.0)
        rainfall = random.uniform(0.0, 15.0)
        air_quality = random.uniform(50.0, 200.0)
        
        # Update metrics
        TEMPERATURE.labels(location='jakarta').set(temperature)
        HUMIDITY.labels(location='jakarta').set(humidity)
        PRESSURE.labels(location='jakarta').set(pressure)
        WIND_SPEED.labels(location='jakarta').set(wind_speed)
        RAINFALL.labels(location='jakarta').set(rainfall)
        AIR_QUALITY.labels(location='jakarta').set(air_quality)
        
        generate_forecast()
        
        return render_template_string(HTML_TEMPLATE,
                                    temperature=temperature,
                                    humidity=humidity,
                                    pressure=pressure,
                                    wind_speed=wind_speed,
                                    rainfall=rainfall,
                                    air_quality=air_quality,
                                    weather_forecast=weather_forecast)

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return {'status': 'healthy', 'timestamp': time.time(), 'service': 'weather-monitoring'}

@app.route('/update-weather')
def update_weather():
    REQUEST_COUNT.labels(method='GET', endpoint='/update-weather').inc()
    with REQUEST_LATENCY.time():
        # Simulasi update data cuaca
        locations = ['jakarta', 'bandung', 'surabaya', 'medan']
        
        for location in locations:
            TEMPERATURE.labels(location=location).set(random.uniform(18.0, 38.0))
            HUMIDITY.labels(location=location).set(random.uniform(30.0, 95.0))
            PRESSURE.labels(location=location).set(random.uniform(995.0, 1025.0))
            WIND_SPEED.labels(location=location).set(random.uniform(0.0, 30.0))
            RAINFALL.labels(location=location).set(random.uniform(0.0, 20.0))
            AIR_QUALITY.labels(location=location).set(random.uniform(40.0, 250.0))
        
        time.sleep(random.uniform(0.5, 1.5))
        return '✅ Weather data updated for all locations!'

@app.route('/metrics')
def metrics():
    # Update metrics sebelum serving
    locations = ['jakarta', 'bandung', 'surabaya']
    for location in locations:
        TEMPERATURE.labels(location=location).set(random.uniform(20.0, 35.0))
        HUMIDITY.labels(location=location).set(random.uniform(40.0, 85.0))
        PRESSURE.labels(location=location).set(random.uniform(1000.0, 1020.0))
        WIND_SPEED.labels(location=location).set(random.uniform(0.0, 20.0))
        RAINFALL.labels(location=location).set(random.uniform(0.0, 10.0))
        AIR_QUALITY.labels(location=location).set(random.uniform(50.0, 180.0))
    
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    print("🌤️ Starting Weather Monitoring Dashboard...")
    print("📊 Metrics available at: http://localhost:8001/metrics")
    print("🌐 Dashboard available at: http://localhost:8001")
    app.run(host='0.0.0.0', port=8001, debug=False)