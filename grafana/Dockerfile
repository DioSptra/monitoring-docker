FROM grafana/grafana:latest

USER root

COPY --chown=472:0 ./provisioning/datasources/datasources.yml \
     /etc/grafana/provisioning/datasources/datasources.yml

# Set environment variables
ENV GF_SECURITY_ADMIN_PASSWORD=admin
ENV GF_USERS_ALLOW_SIGN_UP=false

# Expose port 3000
EXPOSE 3000

# Set user grafana
USER grafana