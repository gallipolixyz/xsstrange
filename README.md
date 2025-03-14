# What is the Xsstrange?

This project aims to create a testing environment for web vulnerability scanning tools. This environment can be used to learn automated security tools, observe their features, and evaluate their effectiveness in different security testing scenarios.

## Technology Stack

The following technologies are used in this project:
- **Backend:** PHP
- **Frontend:** HTML, CSS, JavaScript
- **Others:** Docker, Apache server

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/gallipolixyz/xsstrange.git
cd xsstrange
```

### 2. Install Docker and Docker Compose
- Install Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)


### 3. Environment Setup
```bash
docker-compose up -d --build
```

### 4. Verify Installation
The application should now be running at:
- Web Interface: http://localhost:80

### 5. Stop the Application
When you want to stop the application, run:
```bash
docker-compose down
```

### Troubleshooting
- If ports are already in use, modify the port mappings in `docker-compose.yml`
- Check logs with: `docker-compose logs -f`


