# Ultra-optimized multi-stage build for xsstrange project
# Stage 1: Build stage - install build dependencies and prepare application
FROM python:3.9-alpine AS builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    && rm -rf /var/cache/apk/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    # Aggressively remove unnecessary files
    find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type f -name "*.pyc" -delete && \
    find /opt/venv -type f -name "*.pyo" -delete && \
    find /opt/venv -type f -name "*.pyd" ! -name "_ssl.pyd" -delete && \
    find /opt/venv -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type d -name "test" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type f -name "*.txt" ! -name "requirements.txt" -delete && \
    find /opt/venv -type f -name "*.md" -delete && \
    find /opt/venv -type f -name "*.rst" -delete

# Stage 2: Production stage - create ultra-minimal runtime image
FROM python:3.9-alpine AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Install only essential runtime dependencies including PHP
RUN apk add --no-cache \
    libstdc++ \
    php \
    php-cli \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1000 appuser && \
    adduser -D -s /bin/sh -u 1000 -G appuser appuser

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Verify Python and pip are available
RUN /opt/venv/bin/python --version && \
    /opt/venv/bin/pip list

# Set working directory
WORKDIR /app

# Copy only necessary application files
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser utils/ ./utils/
COPY --chown=appuser:appuser templates/ ./templates/
COPY --chown=appuser:appuser cases/ ./cases/
COPY --chown=appuser:appuser src/ ./src/

# Create necessary directories and set permissions
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD /opt/venv/bin/python -c "import requests; requests.get('http://localhost:5000/')" || exit 1

# Command to run the application
CMD ["/opt/venv/bin/python", "app.py"]
