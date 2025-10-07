FROM grafana/grafana:latest

# Set environment variables
ENV GF_SECURITY_ADMIN_PASSWORD=admin
ENV GF_USERS_ALLOW_SIGN_UP=false

# Copy datasource configuration
COPY datasources.yml /etc/grafana/provisioning/datasources/datasources.yml

# Expose port 3000
EXPOSE 3000

# Set user grafana
USER grafana