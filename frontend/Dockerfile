FROM php:8.1-apache
# Disable mpm_event at build time (mod_php requires prefork only)
RUN a2dismod mpm_event mpm_worker 2>/dev/null || true && \
    a2enmod mpm_prefork 2>/dev/null || true
COPY . /var/www/html/
RUN chown -R www-data:www-data /var/www/html
EXPOSE 80
# Also fix at runtime in case platform re-enables event module
CMD ["bash", "-c", "a2dismod mpm_event 2>/dev/null || true && apache2-foreground"]
