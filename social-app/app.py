#!/usr/bin/env python3

import time
import random
import json
from flask import Flask, Response, render_template_string
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Inisialisasi Flask app
app = Flask(__name__)

# Prometheus metrics untuk Social Media Analytics
REQUEST_COUNT = Counter('social_requests_total', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('social_request_duration_seconds', 'Request latency')
ACTIVE_USERS = Gauge('social_active_users_count', 'Number of active users')
TOTAL_POSTS = Counter('social_posts_total', 'Total number of posts', ['platform'])
LIKES_COUNT = Counter('social_likes_total', 'Total number of likes', ['platform'])
SHARES_COUNT = Counter('social_shares_total', 'Total number of shares', ['platform'])
COMMENTS_COUNT = Counter('social_comments_total', 'Total number of comments', ['platform'])
ENGAGEMENT_RATE = Gauge('social_engagement_rate_percent', 'Engagement rate percentage', ['platform'])
FOLLOWERS_COUNT = Gauge('social_followers_count', 'Number of followers', ['platform'])

# HTML template dengan animasi CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 Social Media Analytics</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }
        
        .floating-icons {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .floating-icon {
            position: absolute;
            font-size: 2rem;
            opacity: 0.1;
            animation: float-up 8s infinite linear;
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
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient-shift 3s ease-in-out infinite;
        }
        
        .platforms-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .platform-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideInUp 0.8s ease-out;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .platform-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .platform-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: slide-shine 3s infinite;
        }
        
        .platform-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .platform-icon {
            font-size: 2.5rem;
            margin-right: 15px;
            animation: bounce 2s infinite;
        }
        
        .platform-name {
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .stats-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            animation: fadeInLeft 1s ease-out;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .stat-value {
            font-weight: bold;
            font-size: 1.1rem;
            animation: countUp 2s ease-out;
        }
        
        .engagement-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .engagement-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
            border-radius: 4px;
            animation: fillBar 2s ease-out;
        }
        
        .actions {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 40px;
        }
        
        .btn {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            animation: pulse-glow 2s infinite;
        }
        
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(255, 107, 107, 0.4);
        }
        
        .trending {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .trending-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            animation: slideInRight 0.5s ease-out;
        }
        
        .trending-item:last-child {
            border-bottom: none;
        }
        
        .trending-hashtag {
            font-weight: bold;
            color: #4ecdc4;
        }
        
        .trending-count {
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
        }
        
        @keyframes float-up {
            from {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0.1;
            }
            to {
                transform: translateY(-100px) rotate(360deg);
                opacity: 0;
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
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translateX(-20px);
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
        
        @keyframes pulse-glow {
            0% {
                box-shadow: 0 0 5px rgba(255, 107, 107, 0.5);
            }
            50% {
                box-shadow: 0 0 20px rgba(255, 107, 107, 0.8);
            }
            100% {
                box-shadow: 0 0 5px rgba(255, 107, 107, 0.5);
            }
        }
        
        @keyframes gradient-shift {
            0%, 100% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
        }
        
        @keyframes slide-shine {
            0% {
                left: -100%;
            }
            100% {
                left: 100%;
            }
        }
        
        @keyframes fillBar {
            from {
                width: 0%;
            }
            to {
                width: var(--fill-width);
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
    <div class="floating-icons" id="floating-icons"></div>
    
    <div class="container">
        <div class="header">
            <h1>📱 Social Media Analytics</h1>
            <p>Real-time monitoring untuk semua platform social media</p>
        </div>
        
        <div class="platforms-grid">
            <div class="platform-card">
                <div class="platform-header">
                    <div class="platform-icon">📘</div>
                    <div class="platform-name">Facebook</div>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Followers</span>
                    <span class="stat-value">{{ "{:,}".format(facebook_followers) }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Posts Today</span>
                    <span class="stat-value">{{ facebook_posts }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Likes</span>
                    <span class="stat-value">{{ "{:,}".format(facebook_likes) }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Shares</span>
                    <span class="stat-value">{{ "{:,}".format(facebook_shares) }}</span>
                </div>
                <div class="engagement-bar">
                    <div class="engagement-fill" style="--fill-width: {{ facebook_engagement }}%; width: {{ facebook_engagement }}%;"></div>
                </div>
                <small>Engagement: {{ "%.1f"|format(facebook_engagement) }}%</small>
            </div>
            
            <div class="platform-card">
                <div class="platform-header">
                    <div class="platform-icon">📷</div>
                    <div class="platform-name">Instagram</div>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Followers</span>
                    <span class="stat-value">{{ "{:,}".format(instagram_followers) }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Posts Today</span>
                    <span class="stat-value">{{ instagram_posts }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Likes</span>
                    <span class="stat-value">{{ "{:,}".format(instagram_likes) }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Comments</span>
                    <span class="stat-value">{{ "{:,}".format(instagram_comments) }}</span>
                </div>
                <div class="engagement-bar">
                    <div class="engagement-fill" style="--fill-width: {{ instagram_engagement }}%; width: {{ instagram_engagement }}%;"></div>
                </div>
                <small>Engagement: {{ "%.1f"|format(instagram_engagement) }}%</small>
            </div>
            
            <div class="platform-card">
                <div class="platform-header">
                    <div class="platform-icon">🐦</div>
                    <div class="platform-name">Twitter</div>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Followers</span>
                    <span class="stat-value">{{ "{:,}".format(twitter_followers) }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Tweets Today</span>
                    <span class="stat-value">{{ twitter_posts }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Retweets</span>
                    <span class="stat-value">{{ "{:,}".format(twitter_shares) }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Likes</span>
                    <span class="stat-value">{{ "{:,}".format(twitter_likes) }}</span>
                </div>
                <div class="engagement-bar">
                    <div class="engagement-fill" style="--fill-width: {{ twitter_engagement }}%; width: {{ twitter_engagement }}%;"></div>
                </div>
                <small>Engagement: {{ "%.1f"|format(twitter_engagement) }}%</small>
            </div>
            
            <div class="platform-card">
                <div class="platform-header">
                    <div class="platform-icon">🎵</div>
                    <div class="platform-name">TikTok</div>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Followers</span>
                    <span class="stat-value">{{ "{:,}".format(tiktok_followers) }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Videos Today</span>
                    <span class="stat-value">{{ tiktok_posts }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Likes</span>
                    <span class="stat-value">{{ "{:,}".format(tiktok_likes) }}</span>
                </div>
                <div class="stats-row">
                    <span class="stat-label">Shares</span>
                    <span class="stat-value">{{ "{:,}".format(tiktok_shares) }}</span>
                </div>
                <div class="engagement-bar">
                    <div class="engagement-fill" style="--fill-width: {{ tiktok_engagement }}%; width: {{ tiktok_engagement }}%;"></div>
                </div>
                <small>Engagement: {{ "%.1f"|format(tiktok_engagement) }}%</small>
            </div>
        </div>
        
        <div class="actions">
            <a href="/generate-content" class="btn">🚀 Generate Content</a>
            <a href="/metrics" class="btn">📊 View Metrics</a>
            <a href="/health" class="btn">❤️ Health Check</a>
        </div>
        
        <div class="trending">
            <h3 style="margin-bottom: 20px;">🔥 Trending Hashtags</h3>
            {% for hashtag in trending_hashtags %}
            <div class="trending-item">
                <span class="trending-hashtag">#{{ hashtag.tag }}</span>
                <span class="trending-count">{{ "{:,}".format(hashtag.count) }} posts</span>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        // Auto refresh setiap 8 detik
        setTimeout(() => {
            location.reload();
        }, 8000);
        
        // Floating social media icons
        const icons = ['👍', '❤️', '💬', '🔄', '📱', '📸', '🎥', '✨'];
        const floatingContainer = document.getElementById('floating-icons');
        
        function createFloatingIcon() {
            const icon = document.createElement('div');
            icon.className = 'floating-icon';
            icon.textContent = icons[Math.floor(Math.random() * icons.length)];
            icon.style.left = Math.random() * 100 + '%';
            icon.style.animationDuration = (Math.random() * 3 + 5) + 's';
            icon.style.animationDelay = Math.random() * 2 + 's';
            floatingContainer.appendChild(icon);
            
            setTimeout(() => {
                icon.remove();
            }, 8000);
        }
        
        // Create floating icons every 2 seconds
        setInterval(createFloatingIcon, 2000);
        
        // Initial floating icons
        for (let i = 0; i < 5; i++) {
            setTimeout(createFloatingIcon, i * 400);
        }
        
        // Animasi counter untuk nilai stats
        document.querySelectorAll('.stat-value').forEach(el => {
            const text = el.textContent.replace(/,/g, '');
            const finalValue = parseInt(text);
            if (!isNaN(finalValue) && finalValue > 0) {
                let currentValue = 0;
                const increment = finalValue / 50;
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        currentValue = finalValue;
                        clearInterval(timer);
                    }
                    el.textContent = Math.round(currentValue).toLocaleString();
                }, 30);
            }
        });
    </script>
</body>
</html>
'''

# Data untuk simulasi trending hashtags
trending_hashtags = []

def generate_trending():
    global trending_hashtags
    hashtags = ["TechNews", "AI", "WebDev", "Docker", "Monitoring", "DevOps", "CloudComputing", "DataScience", "MachineLearning", "Kubernetes"]
    trending_hashtags = []
    for i in range(5):
        trending_hashtags.append({
            "tag": random.choice(hashtags),
            "count": random.randint(1000, 50000)
        })

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_LATENCY.time():
        # Simulasi data social media real-time
        facebook_followers = random.randint(10000, 100000)
        facebook_posts = random.randint(5, 25)
        facebook_likes = random.randint(500, 5000)
        facebook_shares = random.randint(50, 500)
        facebook_engagement = random.uniform(2.0, 8.0)
        
        instagram_followers = random.randint(15000, 150000)
        instagram_posts = random.randint(3, 15)
        instagram_likes = random.randint(800, 8000)
        instagram_comments = random.randint(100, 1000)
        instagram_engagement = random.uniform(3.0, 12.0)
        
        twitter_followers = random.randint(8000, 80000)
        twitter_posts = random.randint(10, 50)
        twitter_likes = random.randint(200, 2000)
        twitter_shares = random.randint(50, 800)
        twitter_engagement = random.uniform(1.5, 6.0)
        
        tiktok_followers = random.randint(20000, 200000)
        tiktok_posts = random.randint(2, 10)
        tiktok_likes = random.randint(1000, 20000)
        tiktok_shares = random.randint(100, 2000)
        tiktok_engagement = random.uniform(5.0, 15.0)
        
        # Update metrics
        ACTIVE_USERS.set(random.randint(100, 1000))
        FOLLOWERS_COUNT.labels(platform='facebook').set(facebook_followers)
        FOLLOWERS_COUNT.labels(platform='instagram').set(instagram_followers)
        FOLLOWERS_COUNT.labels(platform='twitter').set(twitter_followers)
        FOLLOWERS_COUNT.labels(platform='tiktok').set(tiktok_followers)
        
        ENGAGEMENT_RATE.labels(platform='facebook').set(facebook_engagement)
        ENGAGEMENT_RATE.labels(platform='instagram').set(instagram_engagement)
        ENGAGEMENT_RATE.labels(platform='twitter').set(twitter_engagement)
        ENGAGEMENT_RATE.labels(platform='tiktok').set(tiktok_engagement)
        
        generate_trending()
        
        return render_template_string(HTML_TEMPLATE,
                                    facebook_followers=facebook_followers,
                                    facebook_posts=facebook_posts,
                                    facebook_likes=facebook_likes,
                                    facebook_shares=facebook_shares,
                                    facebook_engagement=facebook_engagement,
                                    instagram_followers=instagram_followers,
                                    instagram_posts=instagram_posts,
                                    instagram_likes=instagram_likes,
                                    instagram_comments=instagram_comments,
                                    instagram_engagement=instagram_engagement,
                                    twitter_followers=twitter_followers,
                                    twitter_posts=twitter_posts,
                                    twitter_likes=twitter_likes,
                                    twitter_shares=twitter_shares,
                                    twitter_engagement=twitter_engagement,
                                    tiktok_followers=tiktok_followers,
                                    tiktok_posts=tiktok_posts,
                                    tiktok_likes=tiktok_likes,
                                    tiktok_shares=tiktok_shares,
                                    tiktok_engagement=tiktok_engagement,
                                    trending_hashtags=trending_hashtags)

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return {'status': 'healthy', 'timestamp': time.time(), 'service': 'social-media-analytics'}

@app.route('/generate-content')
def generate_content():
    REQUEST_COUNT.labels(method='GET', endpoint='/generate-content').inc()
    with REQUEST_LATENCY.time():
        # Simulasi generate content untuk semua platform
        platforms = ['facebook', 'instagram', 'twitter', 'tiktok']
        
        for platform in platforms:
            posts = random.randint(1, 5)
            likes = random.randint(50, 1000)
            shares = random.randint(10, 200)
            comments = random.randint(5, 100)
            
            TOTAL_POSTS.labels(platform=platform).inc(posts)
            LIKES_COUNT.labels(platform=platform).inc(likes)
            SHARES_COUNT.labels(platform=platform).inc(shares)
            COMMENTS_COUNT.labels(platform=platform).inc(comments)
        
        time.sleep(random.uniform(0.5, 1.5))
        return '✅ Content generated for all social media platforms!'

@app.route('/metrics')
def metrics():
    # Update metrics sebelum serving
    platforms = ['facebook', 'instagram', 'twitter', 'tiktok']
    for platform in platforms:
        FOLLOWERS_COUNT.labels(platform=platform).set(random.randint(5000, 100000))
        ENGAGEMENT_RATE.labels(platform=platform).set(random.uniform(1.0, 10.0))
    
    ACTIVE_USERS.set(random.randint(50, 500))
    
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    print("📱 Starting Social Media Analytics Dashboard...")
    print("📊 Metrics available at: http://localhost:8002/metrics")
    print("🌐 Dashboard available at: http://localhost:8002")
    app.run(host='0.0.0.0', port=8002, debug=False)