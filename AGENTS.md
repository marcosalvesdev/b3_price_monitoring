# AI Agents Guide — B3 Price Monitoring

This file serves as the entry point for AI agents working on this project.

## Project Context

- **Project description and features:** See [README.md](README.md)
- **Development guidelines, architecture, setup, and conventions:** See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Frontend design system, components, and template conventions:** See [FRONTEND.md](FRONTEND.md)
- **Testing philosophy, conventions, and best practices:** See [TESTS.md](TESTS.md)

Agents should read these files before making changes to the codebase.

## Rules

- **Always use `docker compose exec web`** to run any command in the project (e.g., `manage.py`, `coverage`, `ruff`). Never run commands directly on the host machine. This ensures project isolation and consistency with the Docker-based development environment.
