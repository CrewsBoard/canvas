# Contributing to Canvas

Thank you for your interest in contributing to Canvas! This document provides guidelines and instructions for contributing to the project.

## 🎯 Before You Start

- Make sure you have Python 3.11 installed
- Install Docker and Docker Compose
- Install Make (for development workflow)
- Familiarize yourself with the project structure
- Read the README.md file
- Check the existing issues and pull requests

## 🛠️ Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/canvas.git
   cd canvas
   ```

3. Set up the development environment:
   ```bash
   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   uv pip install -e .

   # Create DB named `canvas` in postgres
   ```

4. For Docker development:
   ```bash
   make up
   ```

## 🏃 Running the Application

### Local Development

```bash
export PYTHONPATH="$PYTHONPATH:$(pwd)" && gunicorn -w 4 -k uvicorn.workers.UvicornWorker core.main:create_app # or python -m core.main
```

### Docker Development

The services will be available at:
- API Documentation: http://localhost:8001/docs
- ReDoc Documentation: http://localhost:8001/redoc
- UI: http://localhost:3000

## 🧪 Development Workflow

The project uses a Makefile for common development tasks:

```bash
make dev      # Start development environment
make up       # Start services
make down     # Stop services
make build    # Build services
make rebuild  # Rebuild services from scratch
make logs     # View logs
make clean    # Clean up containers and volumes
make test     # Run tests (core and flow_engine)
make stage    # Start stage environment
make prod     # Start production environment
```

### Code Quality

#### Formatting
```bash
black .
```

#### Linting
```bash
ruff check .
```

#### Type Checking
```bash
mypy .
```

#### Running Tests
```bash
make test
```

## 📝 Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public functions and classes
- Keep functions focused and small

## 📋 Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Run tests and ensure they pass (`make test`)
4. Update documentation if needed
5. Submit a pull request with a clear description

## 📝 Commit Messages

Follow the conventional commits format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for test-related changes
- `chore:` for maintenance tasks

## 🤝 Code Review

- Be responsive to feedback
- Address review comments promptly
- Keep the PR focused and manageable

## 📜 License

By contributing, you agree that your contributions will be licensed under the project's license.

## 🙏 Questions?

Feel free to open an issue if you have any questions about contributing! 