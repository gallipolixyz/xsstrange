# Contributing to XSStrange

Thank you for your interest in contributing to XSStrange! This document provides detailed guidelines for contributing to the project, with a special focus on creating XSS vulnerability test cases.

## Table of Contents

- [Contributing to XSStrange](#contributing-to-xsstrange)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Fork and Clone](#fork-and-clone)
    - [Development Environment](#development-environment)
  - [Creating XSS Test Cases](#creating-xss-test-cases)
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

## Creating XSS Test Cases

### Test Case Structure

XSStrange focuses on two main types of XSS vulnerabilities:
- Reflected XSS
- DOM-based XSS

Each test case should:
- Demonstrate a single XSS vulnerability concept
- Be clear and educational
- Include proper documentation and risk assessment

### Using the Template

1. Locate the base template:
   ```
   xsstrange/templates/case_form.html
   ```

2. Copy the template to the appropriate category folder:
   ```
   cases/<category>/<your_test_case>.html
   ```
   Categories include: reflected_xss, dom_xss, etc.

3. When editing the template, you can modify:

   a. Content within square brackets [...]:
      - Remove the brackets and replace with your content
      - Example: Change `[ZAFİYET BAŞLIĞI]` to `Reflected XSS in Search Field`
      - Never include the square brackets in your final case file

   b. Content within HTML comments:
      ```html
      <!-- Bu kısımda açıklama yazabilirsiniz -->
      <!-- Burada form yapısını değiştirebilirsiniz -->
      ```
      - You can modify or replace these commented sections
      - Add your own implementation and descriptions
      - Keep the HTML structure intact

4. Required sections to replace:
   - Title and short description (in head section)
   - Vulnerability type and target
   - Difficulty level (beginner/intermediate/advanced)
   - Category (Input Handling/Authentication/File Operations/Data Handling)
   - Risk level (low/medium/high)
   - Detailed description
   - Form elements and content
   - JavaScript functions and event handlers
   - Database initialization scripts (if needed)

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
