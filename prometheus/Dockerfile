FROM prom/prometheus:latest

# Copy konfigurasi prometheus
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Expose port 9090
EXPOSE 9090

# Set user prometheus
USER prometheus

# Command untuk menjalankan prometheus
CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.console.libraries=/etc/prometheus/console_libraries", \
     "--web.console.templates=/etc/prometheus/consoles", \
     "--storage.tsdb.retention.time=200h", \
     "--web.enable-lifecycle"]