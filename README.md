# Canvas

A modern FastAPI-based application for managing and orchestrating AI agents using CrewAI.

## 🚀 Overview

Canvas is a powerful platform that leverages CrewAI to create, manage, and orchestrate AI agents. It provides a robust API interface for interacting with AI agents and managing their workflows.

## 📋 Features

- FastAPI-based REST API
- CrewAI integration for AI agent management
- SQLModel for database operations
- Modern async architecture
- Comprehensive API documentation
- CORS support
- Development server with hot reload

## 🛠️ Development Status

> **Note**: This project is currently under active development. Features and documentation are being added regularly.

### Current Development Focus
- Core API structure
- Basic agent management
- Database integration
- Configuration management

## 🏗️ Project Structure

```
canvas/
├── core/                    # Core application code
│   ├── configs/            # Configuration files
│   ├── controllers/        # Request handlers
│   ├── daos/              # Data Access Objects
│   ├── dtos/              # Data Transfer Objects
│   ├── repositories/      # Database repositories
│   ├── services/          # Business logic
│   ├── tests/             # Test files
│   ├── main.py            # Application entry point
│   └── routers.py         # API route definitions
├── shared/                 # Shared utilities and common code
├── .github/               # GitHub configuration
└── .venv/                 # Virtual environment
```

## ⚙️ Prerequisites

- Python 3.10.11 or higher
- uv package manager

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/CrewsBoard/canvas.git
cd canvas
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

## 🏃 Running the Application

Start the development server:
```bash
export PYTHONPATH="$PYTHONPATH:$(pwd)" && gunicorn -w 4 -k uvicorn.workers.UvicornWorker core.main:create_app # or python -m core.main
```

The API will be available at:
- API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

## 🧪 Development

### Code Formatting
```bash
black .
```

### Linting
```bash
ruff check .
```

### Type Checking
```bash
mypy .
```

### Running Tests
```bash
pytest
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the terms of the LICENSE file in the root of this repository.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [SQLModel](https://sqlmodel.tiangolo.com/)

## 📅 Changelog

### [Unreleased]
- Initial project setup
- Basic FastAPI application structure
- Database integration with SQLModel
- Configuration management with Pydantic Settings
- Development tools setup (Black, Ruff, MyPy, Pytest)

---

*This README will be updated as the project evolves. Last updated: [Current Date]*
