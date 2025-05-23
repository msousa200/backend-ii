# Session 16: Building CI/CD Pipelines for Python Projects with GitHub Actions

This repository contains a sample Python project demonstrating continuous integration and continuous deployment (CI/CD) pipelines using GitHub Actions.

## Project Structure

- **calculator/**: A simple Python package with basic arithmetic functions
- **.github/workflows/**: GitHub Actions workflow definition files
  - **ci.yml**: Basic CI pipeline running tests on a single Python version
  - **exercise.yml**: Advanced CI pipeline using matrix strategy for multiple Python versions
  - **challenge.yml**: Complete CI/CD pipeline with testing, building, and deployment stages

## Calculator Package

The calculator package provides basic arithmetic operations:
- Addition (`add`)
- Subtraction (`subtract`)
- Multiplication (`multiply`)
- Division (`divide`)
- Power (`power`)
- Square (`square`)
- Cube (`cube`)

## CI/CD Workflows

### Basic CI Pipeline (ci.yml)

This workflow demonstrates the fundamental concepts of GitHub Actions:
- Triggers on push to main/develop branches or pull requests to main
- Runs on the latest Ubuntu environment
- Sets up Python 3.9
- Installs dependencies and the package in development mode
- Runs tests with pytest

### Multi-Python CI Pipeline (exercise.yml)

An enhanced version of the basic CI pipeline:
- Uses a matrix strategy to test on multiple Python versions (3.7, 3.8, 3.9, 3.10)
- Adds test coverage reporting
- Uploads coverage artifacts for later analysis

### Complete CI/CD Pipeline (challenge.yml)

A fully-featured CI/CD pipeline that:
1. **Tests**: Runs tests on multiple Python versions with coverage reporting
2. **Builds**: Creates Python distribution packages (.whl and .tar.gz)
3. **Deploys**: Publishes the package to Test PyPI (simulated)

The deployment stage only runs when changes are pushed to the main branch, implementing a conditional deployment strategy.

## Running the Examples

### Local Development

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the package in development mode:
   ```bash
   pip install -e .
   ```
4. Run the tests:
   ```bash
   pytest calculator/tests/
   ```

### GitHub Actions

The CI/CD workflows will automatically run when:
- You push code to the main or develop branches
- You create a pull request targeting the main branch

To see the workflows in action:
1. Fork this repository to your GitHub account
2. Make a change to any file
3. Commit and push the change
4. Go to the "Actions" tab in your GitHub repository to see the workflows running

## Learning Points

This session demonstrates:
- Setting up basic GitHub Actions workflows for Python projects
- Using matrix strategies to test on multiple Python versions
- Adding code quality checks with coverage reports
- Building Python packages for distribution
- Implementing conditional deployment based on branch/event
- Securely handling credentials with GitHub Secrets

## Next Steps

To extend this project, consider:
- Adding more code quality tools (black, isort, mypy)
- Implementing semantic versioning and automated releases
- Setting up deployment to multiple environments (staging, production)
- Adding status badges to your README.md
- Integrating with code scanning tools for security analysis
