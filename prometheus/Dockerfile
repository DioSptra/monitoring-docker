FROM prom/prometheus:latest

USER root
# Copy konfigurasi prometheus
COPY --chown=65534:65534 --chmod=0644 prometheus.yml /etc/prometheus/prometheus.yml

USER 65534
# Expose port 9090
EXPOSE 9090

# Jalankan Prometheus pakai default user
CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.console.libraries=/etc/prometheus/console_libraries", \
     "--web.console.templates=/etc/prometheus/consoles", \
     "--storage.tsdb.retention.time=200h", \
     "--web.enable-lifecycle"]
