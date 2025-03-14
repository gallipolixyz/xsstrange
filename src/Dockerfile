FROM httpd:2.4

# Create log directory
RUN mkdir -p /usr/local/apache2/logs \
    && chmod -R 755 /usr/local/apache2/logs \
    && chmod -R 755 /usr/local/apache2/htdocs

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the custom httpd.conf
COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf

# Copy website files
COPY . /usr/local/apache2/htdocs/

# Expose port 80
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:80/ || exit 1
