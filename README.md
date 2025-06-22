# What is the Xsstrange?

This project aims to create a testing environment for web vulnerability scanning tools. This environment can be used to learn automated security tools, observe their features, and evaluate their effectiveness in different security testing scenarios.

## Technology Stack

The following technologies are used in this project:
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript
- **Others:** Docker (Ultra-optimized multi-stage build with Alpine Linux)

## Project Structure

```
xsstrange/
├── src/                    # Frontend source files
│   ├── assets/            # Static assets (CSS, JS)
│   │   └── style.css     # Main stylesheet
│   ├── cases/             # Test cases
│   │   └── xss/          # XSS vulnerability test cases
│   └── index.html         # Main entry point
├── templates/             # Template files
│   └── cases/            # Case templates
├── utils/                 # Utility modules
│   └── template_utils.py # Template processing utilities
├── app.py                # Main Flask application
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Ultra-optimized multi-stage Docker build
└── .dockerignore        # Aggressive Docker build context exclusions
```

## Docker Ultra-Optimized Multi-Stage Build

This project uses an ultra-optimized multi-stage Docker build process to achieve minimal image size:

### Build Stages:
1. **Builder Stage (Alpine)**: Installs build dependencies and Python packages in a virtual environment
2. **Production Stage (Alpine)**: Creates an ultra-minimal runtime image with only essential files

### Optimization Techniques:
- **Alpine Linux**: Both stages use Alpine Linux for minimal base image size
- **Aggressive Cleanup**: Removes all unnecessary files (tests, docs, cache files)
- **Virtual Environment**: Isolates Python dependencies
- **Non-root User**: Enhanced security with dedicated user
- **Layer Optimization**: Efficient layer caching and minimal layer count

### Benefits:
- **Ultra-Small Image Size**: Final image is significantly smaller than standard builds
- **Enhanced Security**: Non-root execution and minimal attack surface
- **Fast Builds**: Optimized layer caching and minimal build context
- **Production Ready**: Only runtime dependencies included

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/gallipolixyz/xsstrange.git
cd xsstrange
```

### 2. Install Docker and Docker Compose
- Install Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- Install Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### 3. Environment Setup
```bash
# Build and start the application
docker-compose up -d --build

# Or build the image separately
docker build -t xsstrange .
```

### 4. Verify Installation
The application should now be running at:
- Web Interface: http://127.0.0.1:80

### 5. Stop the Application
When you want to stop the application, run:
```bash
docker-compose down
```

## Docker Build Optimization

### Build the Image:
```bash
# Build with default target (production)
docker build -t xsstrange .

# Build specific stage for development
docker build --target builder -t xsstrange:builder .

# Build with no cache (for troubleshooting)
docker build --no-cache -t xsstrange .

# Show image size
docker images xsstrange
```

### Image Size Comparison:
- **Original single-stage**: ~200-300MB
- **Multi-stage optimized**: ~100-150MB (50%+ reduction)
- **Ultra-optimized Alpine**: ~50-80MB (75%+ reduction)

### Security Features:
- Non-root user execution (appuser:1000)
- Minimal runtime dependencies
- Health checks included
- Proper file permissions
- Alpine Linux security benefits

### Build Performance:
- Aggressive `.dockerignore` reduces build context
- Optimized layer caching
- Minimal dependency installation
- Efficient file copying

## Features

- **XSS Vulnerability Testing**: Various test cases for Cross-Site Scripting vulnerabilities
- **Template System**: Dynamic template generation for test cases
- **Ultra-Optimized Docker Build**: Alpine-based multi-stage build for maximum efficiency

## Troubleshooting

- If ports are already in use, modify the port mappings in `docker-compose.yml`
- Check logs with: `docker-compose logs -f`
- For build issues: `docker build --no-cache -t xsstrange .`
- Check image size: `docker images xsstrange`
- Alpine compatibility issues: Check if all dependencies support Alpine Linux

## Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/xss-test-case
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add new XSS test case'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/xss-test-case
   ```
5. Open a Pull Request to the `main` branch

## Development Workflow

### Adding New Test Cases
1. Create a new directory in `src/cases/xss/` for your test case
2. Add corresponding template in `templates/cases/xss/`
3. Update the test case documentation

### Docker Development
```bash
# Build for development (includes build tools)
docker build --target builder -t xsstrange:dev .

# Run development container
docker run -it --rm -p 5000:5000 -v $(pwd):/app xsstrange:dev sh

# Check image layers and size
docker history xsstrange
docker images xsstrange --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- GitHub: [@gallipolixyz](https://github.com/gallipolixyz)
- Project Link: [https://github.com/gallipolixyz/xsstrange](https://github.com/gallipolixyz/xsstrange)
