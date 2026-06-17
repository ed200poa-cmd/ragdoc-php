FROM php:8.1-apache
# Disable mpm_event at build time (mod_php requires prefork only)
RUN a2dismod mpm_event mpm_worker 2>/dev/null || true && \
    a2enmod mpm_prefork 2>/dev/null || true
COPY . /var/www/html/
RUN chown -R www-data:www-data /var/www/html
COPY start.sh /start.sh
RUN chmod +x /start.sh
EXPOSE 80
CMD ["/start.sh"]
