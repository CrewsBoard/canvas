# Canvas

A modern FastAPI-based application for managing and orchestrating AI agents using CrewAI.

## 🚀 Overview

Canvas is a powerful platform that leverages CrewAI to create, manage, and orchestrate AI agents. It provides a robust
API interface for interacting with AI agents and managing their workflows.

## 📋 Features

- FastAPI-based REST API
- CrewAI integration for AI agent management
- SQLModel for database operations
- Modern async architecture
- Comprehensive API documentation
- CORS support
- Development server with hot reload
- Docker support for easy deployment
- Separate UI service

## 🛠️ Development Status

> **Note**: This project is currently under active development. Features and documentation are being added regularly.

### Current Development Focus

- Core API structure
- Basic agent management
- Database integration
- Configuration management
- Docker containerization

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
├── scripts/               # Development scripts
├── .github/               # GitHub configuration
└── .venv/                 # Virtual environment
```

## 🤝 Contributing

For detailed information about contributing to this project, including setup instructions and development workflow, please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) file.

## 📝 License

This project is licensed under the terms of the LICENSE file in the root of this repository.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [SQLModel](https://sqlmodel.tiangolo.com/)

## 📅 Changelog

### [Unreleased]

- Updated Python version to 3.11
- Added Docker support with core and UI services
- Added environment configuration
- Added contribution guidelines
- Added Makefile-based development workflow

---

*This README will be updated as the project evolves. Last updated: [Current Date]*
