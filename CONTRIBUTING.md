# Contributing to XSStrange

Thank you for your interest in contributing to XSStrange! This document provides detailed guidelines for contributing to the project, with a special focus on creating web security vulnerability test cases.

## Table of Contents

- [Contributing to XSStrange](#contributing-to-xsstrange)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Fork and Clone](#fork-and-clone)
    - [Development Environment](#development-environment)
  - [Creating Vulnerability Test Cases](#creating-vulnerability-test-cases)
    - [Test Case Structure](#test-case-structure)
    - [Using the Template](#using-the-template)
    - [Testing Your Changes](#testing-your-changes)
  - [Contribution Workflow](#contribution-workflow)
    - [Branch Creation](#branch-creation)
    - [Making Changes](#making-changes)
    - [Submitting Changes](#submitting-changes)
  - [Review Process](#review-process)
  - [Questions and Support](#questions-and-support)

## Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/xsstrange.git
   cd xsstrange
   ```

### Development Environment

You can use either:
- The project's Docker environment
- A local Python setup with Flask

For Docker setup:
```bash
docker-compose up -d --build
```

For local setup:
```bash
pip install -r requirements.txt
python app.py
```

## Creating Vulnerability Test Cases

### Test Case Structure

XSStrange focuses on the following types of vulnerabilities:

1. Reflected XSS Variants:
   - Basic Reflected XSS
   - Angular-based XSS
   - URL-based XSS
   - Tag-based XSS
   - Escaped XSS

2. DOM-based Vulnerabilities:
   - DOM XSS
   - URL-based DOM XSS
   - JavaScript Import Issues
   - DOM Event Handler XSS

3. Client-side Security Issues:
   - Mixed Content Issues
   - HSTS Issues
   - Remote Inclusion XSS
   - Insecure Third-Party Script Embedding

Each test case should:
- Demonstrate a single vulnerability concept
- Be easily reproducible
- Not require server-side storage
- Include proper documentation and risk assessment
- Focus on detection capabilities
- Present edge cases when applicable

### Using the Template

1. Locate the base template:
   ```
   xsstrange/templates/case_form.html
   ```

2. Copy the template to the appropriate category folder:
   ```
   cases/<category>/<your_test_case>.html
   ```
   Categories include: 
   - reflected_xss
   - dom_xss
   - angular_xss
   - clickjacking
   - cors
   - mixed_content
   - remote_inclusion

3. When editing the template, you can modify:

   a. Content within square brackets [...]:
      - Remove the brackets and replace with your content
      - Example: Change `[VULNERABILITY TITLE]` to `Angular-based XSS in Template Binding`
      - Never include the square brackets in your final case file

   b. Content within HTML comments:
      ```html
      <!-- Add your vulnerability description here -->
      <!-- Modify the form structure as needed -->
      ```
      - You can modify or replace these commented sections
      - Add your own implementation and descriptions
      - Keep the HTML structure intact

4. Required sections to replace:
   - Title and short description
   - Vulnerability type and target
   - Difficulty level (beginner/intermediate/advanced)
   - Category (based on vulnerability type)
   - Risk level (low/medium/high)
   - Detailed description
   - Test case implementation
   - Expected behavior
   - Detection hints for scanners

5. Keep all HTML structure intact - only modify the placeholder content

### Testing Your Changes

Before submitting your test case:

1. Test with a local server:
   - Use VS Code Live Server extension, or
   - XAMPP/WAMP/MAMP

2. Verify the vulnerability works as expected
3. Ensure proper error handling
4. Check for unintended side effects

## Contribution Workflow

### Branch Creation

Create a new branch for your changes:
```bash
git checkout -b feature/new_xss_case
```

### Making Changes

1. Create your test case following the template
2. Add necessary documentation
3. Test thoroughly
4. Commit your changes:
   ```bash
   git add cases/<category>/<your_test_case>.html
   git commit -m "Add new XSS case: Brief description"
   ```

### Submitting Changes

1. Push to your fork:
   ```bash
   git push origin feature/new_xss_case
   ```

2. Create a Pull Request:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Provide a clear description of your test case

## Review Process

After submitting your Pull Request:
1. Maintainers will review your test case
2. They may request changes or clarification
3. Once approved, your contribution will be merged

## Questions and Support

If you have questions or need help:
- Open an issue for general questions
- Contact the maintainers for specific concerns

Thank you for contributing to XSStrange! 🚀
