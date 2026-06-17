#!/bin/bash
set -e
# Fix MPM at runtime
a2dismod mpm_event 2>/dev/null || true

# Configure Apache to listen on Railway's $PORT
PORT=${PORT:-80}
sed -i "s/Listen 80/Listen $PORT/" /etc/apache2/ports.conf
sed -i "s/<VirtualHost \*:80>/<VirtualHost *:$PORT>/" /etc/apache2/sites-enabled/000-default.conf

apache2-foreground
