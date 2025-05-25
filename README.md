# What is the Xsstrange?

This project aims to create a testing environment for web vulnerability scanning tools. This environment can be used to learn automated security tools, observe their features, and evaluate their effectiveness in different security testing scenarios.

## Technology Stack

The following technologies are used in this project:
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript
- **Others:** Docker

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
└── Dockerfile           # Docker build instructions
```

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
docker-compose up -d --build
```

### 4. Verify Installation
The application should now be running at:
- Web Interface: http://127.0.0.1:80

### 5. Stop the Application
When you want to stop the application, run:
```bash
docker-compose down
```

## Features

- **XSS Vulnerability Testing**: Various test cases for Cross-Site Scripting vulnerabilities
- **Template System**: Dynamic template generation for test cases

## Troubleshooting

- If ports are already in use, modify the port mappings in `docker-compose.yml`
- Check logs with: `docker-compose logs -f`

## Contributing

We welcome contributions to the XSStrange project! We're especially looking for:

- New XSS vulnerability test cases (reflected and DOM-based)
- Documentation improvements
- Bug fixes and feature enhancements

### How to Contribute

Please check our [CONTRIBUTING.md](CONTRIBUTING.md) guide for detailed instructions on:

- Setting up your development environment
- Creating new XSS test cases
- Following the project template structure
- Submitting your contributions

### Quick Start for Contributors

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/xss-test-case
   ```
3. Copy the base template from `templates/case_form.html`
4. Create your test case following the guidelines
5. Test your changes locally
6. Submit a Pull Request

For detailed guidelines on creating XSS test cases, please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) document.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- GitHub: [@gallipolixyz](https://github.com/gallipolixyz)
- Project Link: [https://github.com/gallipolixyz/xsstrange](https://github.com/gallipolixyz/xsstrange)
