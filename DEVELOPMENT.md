# Development Guide — B3 Price Monitoring

This document covers everything you need to set up, run, test, and develop the **B3 Price Monitoring** project.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Getting Started (Docker)](#getting-started-docker)
- [Running Locally (without Docker)](#running-locally-without-docker)
- [Useful Commands](#useful-commands)
- [Code Quality & Pre-commit](#code-quality--pre-commit)
- [Commit Convention](#commit-convention)
- [Testing](#testing)
- [Architecture Overview](#architecture-overview)
- [Design & Architectural Patterns Reference](#design--architectural-patterns-reference)
- [Tips & Advice](#tips--advice)

---

## Project Overview

B3 Price Monitoring is a Django-based web application for monitoring stock prices on the Brazilian B3 exchange, cryptocurrencies, and ETFs. Users create "price tunnels" with upper/lower limits and the system automatically monitors prices at configurable intervals, sending email alerts when opportunities arise.

**Core workflow:**

1. User registers and logs in.
5. User creates **Assets** (stocks, cryptos, ETFs) validated against the external Brapi API.
3. User creates **Price Tunnels** with upper/lower limits and a check interval.
4. A **Celery Beat** periodic task is created to monitor the asset price.
5. The **Celery Worker** fetches the current price, records it, and sends email notifications when limits are breached.

---

## Tech Stack

### Production Dependencies

| Library | Purpose |
|---|---|
| **Django 5.2** | Web framework |
| **Celery[redis] >=5.6.2** | Distributed task queue for background price checks |
| **django-celery-beat >=2.1.0** | Database-backed periodic task scheduler |
| **Flower >=2.0.1** | Real-time Celery task monitoring dashboard |
| **Pillow >=12.1.1** | Image processing (user avatars) |
| **psycopg[binary] >=3.3.2** | PostgreSQL database adapter |
| **python-decouple >=3.8** | Environment variable management (`.env` files) |
| **requests >=2.32.5** | HTTP client for external API calls (Brapi) |

### Development Dependencies

| Library | Purpose |
|---|---|
| **Ruff >=0.15.1** | Linter and code formatter (replaces flake8, isort, black) |
| **django-debug-toolbar >=6.2.0** | In-browser debug panel (auto-enabled in `DEBUG=True`) |
| **pre-commit >=4.5.1** | Git hook manager for automated code quality checks |
| **Bandit >=1.9.3** | Security-focused static analysis (currently disabled in pre-commit) |

### Infrastructure

| Service | Image / Version | Purpose |
|---|---|---|
| **PostgreSQL** | `postgres:18-alpine` | Primary database |
| **Redis** | `redis:7-alpine` | Celery message broker and result backend |
| **UV** | `ghcr.io/astral-sh/uv:0.10.2` | Fast Python package installer (used in Dockerfile) |

---

## Project Structure

```
b3_price_monitoring/
├── core/                   # Django project configuration
│   ├── settings.py         # Main settings (DB, apps, middleware, auth, email)
│   ├── urls.py             # Root URL configuration
│   ├── celery.py           # Celery app initialization
│   ├── wsgi.py             # WSGI entrypoint
│   └── asgi.py             # ASGI entrypoint
│
├── accounts/               # User management app
│   ├── models/             # Custom User model + UserProfile
│   ├── views/              # Login, logout, registration, password reset/change
│   ├── forms/              # User registration form
│   ├── signals.py          # Auto-create UserProfile on User creation
│   └── templates/accounts/ # Account-related templates
│
├── assets/                 # Asset management app
│   ├── models/             # Asset + AssetPrice models
│   ├── views/              # CRUD views for assets
│   ├── forms/              # Asset create/update forms
│   ├── services/           # External API integrations
│   │   └── brapi/          # Brapi API handler + validator
│   ├── utils/              # Base API handler, validators
│   └── templates/assets/   # Asset-related templates
│
├── tunnels/                # Price tunnel monitoring app
│   ├── models/             # PriceTunnel + PeriodicTaskAssociation
│   ├── views/              # CRUD views for tunnels
│   ├── forms/              # Tunnel create/update forms
│   ├── tasks/              # Celery tasks (price_check)
│   ├── utils/              # TunnelManager, validators, periodic task management
│   └── templates/tunnels/  # Tunnel-related + notification templates
│
├── globals/                # Shared utilities
│   ├── http_helpers/       # HTTP status code constants and helpers
│   └── services/           # EmailNotificationService
│       └── notifications/  # HTML email sending service
│
├── templates/              # Global templates (base.html)
├── media/                  # User-uploaded files (avatars)
├── manage.py               # Django management entry point
├── pyproject.toml          # Project metadata, dependencies, Ruff config
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Full development stack definition
└── .pre-commit-config.yaml # Pre-commit hooks configuration
```

---

## Environment Variables

Copy the example file and fill in the values:

```bash
cp .env-example .env
```

### Required Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-insecure-abc123...` |
| `DEBUG` | Enable debug mode | `True` |
| `POSTGRES_DB` | PostgreSQL database name | `django_db` |
| `POSTGRES_USER` | PostgreSQL username | `django_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `your-db-password` |
| `POSTGRES_HOST` | Database host | `db` (Docker) or `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |
| `BASE_BRAPI_API_URL` | Brapi API base URL | `https://brapi.dev/api` |
| `BRAPI_API_KEY` | Brapi API token | `your-brapi-key` |


### Optional Variables

| Variable | Description | Default |
|---|---|---|
| `CELERY_BROKER_URL` | Redis URL for Celery broker | `redis://redis:6379/0` |
| `CELERY_RESULT_BACKEND` | Redis URL for Celery results | `redis://redis:6379/0` |
| `EMAIL_BACKEND` | Django email backend | `django.core.mail.backends.console.EmailBackend` |
| `DEFAULT_FROM_EMAIL` | Sender email address | `webmaster@localhost` |

> **Note:** When running with Docker Compose, set `POSTGRES_HOST=db`. When running locally, use `POSTGRES_HOST=localhost`.

---

## Getting Started (Docker)

Docker Compose is the recommended way to run the project. It sets up all services: Django, PostgreSQL, Redis, Celery Worker, Celery Beat, and Flower.

### 1. Clone and configure

```bash
git clone <repository-url>
cd b3_price_monitoring
cp .env-example .env
# Edit .env with your actual values (API keys, passwords, etc.)
```

### 2. Build and start all services

```bash
docker compose up --build
```

This starts **6 services**:

| Service | Container | Port | Description |
|---|---|---|---|
| `web` | `django_web` | [localhost:8000](http://localhost:8000) | Django development server |
| `db` | `postgres` | `5432` | PostgreSQL database |
| `redis` | `redis` | `6379` | Redis (Celery broker) |
| `celery` | `django_celery` | — | Celery worker (processes tasks) |
| `beat` | `django_beat` | — | Celery Beat (schedules periodic tasks) |
| `flower` | `django_flower` | [localhost:5555](http://localhost:5555) | Flower (Celery monitoring UI) |

### 3. Apply database migrations

```bash
docker compose exec web python manage.py migrate
```

### 4. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Access the application

- **Web app:** http://localhost:8000
- **Django Admin:** http://localhost:8000/admin/
- **Flower (task monitoring):** http://localhost:5555

---

## Docker Compose Commands

### Lifecycle

```bash
# Build and start all services (with live logs)
docker compose up --build

# Start in detached mode (background)
docker compose up -d --build

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes database data)
docker compose down -v

# Restart a specific service
docker compose restart web
docker compose restart celery
docker compose restart beat
```

### Running management commands inside the container

```bash
# Django management commands
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py shell
docker compose exec web python manage.py collectstatic

# Open a bash shell in the web container
docker compose exec web sh
```

### Viewing logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f celery
docker compose logs -f beat
docker compose logs -f flower
```

### Rebuilding after dependency changes

```bash
docker compose up --build --force-recreate
```

---

## Running Locally (without Docker)

> **Prerequisites:** Python 3.12+, PostgreSQL, Redis running locally.

### 1. Install dependencies with UV (recommended)

```bash
# Install UV if you don't have it
pip install uv

# Install production + dev dependencies
uv pip install . --group dev

# Or with pip
pip install -e ".[dev]"
```

### 2. Set up environment

```bash
cp .env-example .env
# Edit .env — set POSTGRES_HOST=localhost
```

### 3. Apply migrations and create superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run the development server

```bash
python manage.py runserver
```

### 5. Run Celery Worker (separate terminal)

```bash
python -m celery -A core worker -l info --concurrency=2
```

### 6. Run Celery Beat (separate terminal)

```bash
python -m celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### 7. Run Flower — optional (separate terminal)

```bash
python -m celery -A core flower --port=5555
```

---

## Useful Commands

### Database

```bash
# Create new migrations after model changes
docker compose exec web python manage.py makemigrations

# Apply pending migrations
docker compose exec web python manage.py migrate

# Show migration status
docker compose exec web python manage.py showmigrations

# Open Django shell
docker compose exec web python manage.py shell
```

### Celery

```bash
# Check registered tasks
docker compose exec celery python -m celery -A core inspect registered

# Check active tasks
docker compose exec celery python -m celery -A core inspect active

# Purge all pending tasks
docker compose exec celery python -m celery -A core purge
```

---

## Code Quality & Pre-commit

### Pre-commit Hooks

The project uses [pre-commit](https://pre-commit.com/) with the following hooks:

**On commit:**
- `trailing-whitespace` — removes trailing whitespace
- `end-of-file-fixer` — ensures files end with a newline
- `check-merge-conflict` — prevents committing merge conflict markers
- `check-yaml`, `check-toml`, `check-json` — validates config file syntax
- `debug-statements` — catches leftover `breakpoint()` / `pdb` calls
- `detect-private-key` — prevents committing private keys
- **Ruff lint** — lints code with `--fix` auto-corrections
- **Ruff format** — formats code automatically

**On push:**
- **Run project tests** — executes `docker compose exec web python manage.py test -v 2 --keepdb --failfast`

### Setup pre-commit

```bash
# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type pre-push

# Run all hooks manually
pre-commit run --all-files
```

### Ruff Configuration

Defined in `pyproject.toml`:

- **Target:** Python 3.12
- **Line length:** 99 characters
- **Enabled rules:** pycodestyle (E), pyflakes (F), isort (I), flake8-bugbear (B), pyupgrade (UP), Django-specific (DJ), simplifications (SIM), comprehensions (C4)
- **Ignored:** `DJ001` (nullable CharField)

### Running Ruff manually

```bash
# Lint with auto-fix
ruff check . --fix

# Format code
ruff format .

# Check without fixing (CI mode)
ruff check .
```

---

## Commit Convention

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification. Every commit message must be structured as:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type | Description |
|---|---|
| **feat** | A new feature |
| **fix** | A bug fix |
| **docs** | Documentation-only changes |
| **style** | Changes that do not affect code meaning (whitespace, formatting, semicolons) |
| **refactor** | A code change that neither fixes a bug nor adds a feature |
| **perf** | A code change that improves performance |
| **test** | Adding or correcting tests |
| **build** | Changes that affect the build system or external dependencies |
| **ci** | Changes to CI configuration files and scripts |
| **chore** | Other changes that don't modify src or test files |
| **revert** | Reverts a previous commit |

### Examples

```bash
# Simple feature
git commit -m "feat: add email notification on price breach"

# Feature with scope
git commit -m "feat(tunnels): add upper limit validation"

# Bug fix
git commit -m "fix(assets): correct price format for crypto assets"

# Breaking change (footer notation)
git commit -m "feat(accounts): replace User model with custom AbstractUser" -m "BREAKING CHANGE: existing user table must be migrated"

# Docs
git commit -m "docs: add Conventional Commits section to DEVELOPMENT.md"

# Chore
git commit -m "chore: update Django to 5.2"
```

### Rules

1. The **type** is mandatory and must be lowercase.
2. The **description** must be a concise summary in imperative mood (e.g., "add", not "added" or "adds").
3. A **scope** (in parentheses) is optional but encouraged — use the app name (`accounts`, `assets`, `tunnels`, `globals`, `core`) or a relevant module.
4. Use `BREAKING CHANGE:` in the footer (or `!` after the type/scope) to signal breaking changes.
5. Keep the subject line under 72 characters.

---

## Testing

For the full testing guide — including TDD workflow, conventions, test organization, mocking guidelines, coverage, and best practices — see **[TESTS.md](TESTS.md)**.

**Quick reference:**

```bash
# Docker
docker compose exec web python manage.py test -v 2 --keepdb --failfast

# Local
python manage.py test -v 2 --keepdb --failfast
```

---

## Architecture Overview

### URL Routing

| Prefix | App | Description |
|---|---|---|
| `/admin/` | Django Admin | Built-in admin panel |
| `/accounts/` | `accounts` | Login, logout, registration, password management |
| `/assets/` | `assets` | CRUD for assets (stocks, cryptos, ETFs) |
| `/tunnels/` | `tunnels` | CRUD for price tunnels + monitoring config |

### Authentication Flow

- Custom `User` model extends `AbstractUser` (in `accounts.User`).
- A `UserProfile` (with avatar) is auto-created via a `post_save` signal.
- Login redirects to the asset list (`assets:list`).
- Logout redirects to the login page.
- Password reset is handled via email.

### Price Monitoring Flow

```
User creates Tunnel
       │
       ▼
TunnelCreateForm.save()
       │
       ├── Creates PriceTunnel in DB
       │
       └── PeriodicTunnelTasksManager.create_periodic_task_for_tunnel()
              │
              ├── Creates IntervalSchedule (Celery Beat)
              ├── Creates PeriodicTask with task kwargs
              └── Creates PeriodicTaskAssociation link
                     │
                     ▼
              Celery Beat triggers price_check task
                     │
                     ▼
              price_check() — Celery Worker
                     │
                     ├── Fetches current price (BrapiApiHandler)
                     ├── Records AssetPrice in DB
                     ├── Checks upper/lower limits
                     └── Sends email notification if breached
```

### External API Integration

The project integrates with **Brapi API** (`assets/services/brapi/`) for stocks and crypto data. It is used for both asset validation and price fetching, built on a base `AssetApiHandler` abstraction with retry logic (3 retries, 2-second timeout).

---

## Design & Architectural Patterns Reference

> **Note:** The patterns listed below are **references, not strict rules**. For each feature or module, developers and agents should analyze which design and architectural patterns best fit the specific use case.

### Design Patterns

| Pattern | Description |
|---|---|
| **Factory** | Delegates object creation to a dedicated method or class, decoupling the caller from concrete implementations. |
| **Singleton** | Ensures a class has only one instance and provides a global access point to it. |
| **Strategy** | Defines a family of interchangeable algorithms, letting the caller switch behavior at runtime. |
| **Observer** | Allows objects to subscribe to events and be notified automatically when state changes occur. |
| **Decorator** | Dynamically adds responsibilities to an object without modifying its class. |
| **Adapter** | Converts the interface of a class into another interface that a client expects. |
| **Repository** | Abstracts data access behind a collection-like interface, separating domain logic from persistence. |
| **Command** | Encapsulates a request as an object, allowing parameterization, queuing, and undo operations. |
| **Builder** | Separates the construction of a complex object from its representation, enabling step-by-step creation. |
| **Facade** | Provides a simplified interface to a complex subsystem. |

### Architectural Patterns

| Pattern | Description |
|---|---|
| **MVC (Model-View-Controller)** | Separates the application into Model (data/logic), View (presentation), and Controller (input handling). Django follows the closely related MTV (Model-Template-View) variant. |
| **Layered Architecture** | Organizes code into horizontal layers (presentation, business logic, data access), each depending only on the layer below. |
| **Domain-Driven Design (DDD)** | Centers the architecture around the business domain, using bounded contexts, entities, value objects, and aggregates. |
| **Event-Driven Architecture** | Components communicate through events (messages), enabling loose coupling and asynchronous processing. |
| **Microservices** | Decomposes the system into small, independently deployable services, each owning its data and business logic. |
| **Hexagonal Architecture (Ports & Adapters)** | Isolates the core domain from external systems (databases, APIs, UI) through well-defined ports and adapters. |
| **CQRS (Command Query Responsibility Segregation)** | Separates read and write models, optimizing each side independently. |
| **Service-Oriented Architecture (SOA)** | Structures the application as a collection of loosely coupled, reusable services that communicate over a network. |

### SOLID Principles

| Principle | Description |
|---|---|
| **S — Single Responsibility** | A class should have only one reason to change. |
| **O — Open/Closed** | Software entities should be open for extension but closed for modification. |
| **L — Liskov Substitution** | Subtypes must be substitutable for their base types without altering correctness. |
| **I — Interface Segregation** | Clients should not be forced to depend on interfaces they do not use. |
| **D — Dependency Inversion** | High-level modules should depend on abstractions, not concrete implementations. |

---

## Tips & Advice

### Development Workflow

1. **Always use Docker Compose** for the full stack — it ensures PostgreSQL, Redis, Celery, and Beat are all running together correctly.
2. **Watch Celery logs** (`docker compose logs -f celery`) when debugging task execution issues.
3. **Use Flower** at http://localhost:5555 to monitor task execution, success rates, and timing.
4. **Use Django Admin** at `/admin/` to inspect and manage periodic tasks (`django_celery_beat` models), assets, tunnels, and users.

### Environment

5. **Keep `.env` out of version control.** The `.env-example` is provided as a template — copy it and fill your own values.
6. **Set `POSTGRES_HOST=db`** in `.env` when using Docker Compose, and `POSTGRES_HOST=localhost` for local development.
7. **A Brapi API key is required.** Register at [brapi.dev](https://brapi.dev) to obtain one.
8. The `.env-example` is missing some variables (`BASE_BRAPI_API_URL`, `BRAPI_API_KEY`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`). Consider adding them for easier onboarding.

### Code Quality

9. **Run `pre-commit run --all-files`** before pushing to catch issues early.
10. **Ruff replaces multiple tools** (flake8, isort, black) — use `ruff check . --fix` and `ruff format .` directly if needed.
11. **Bandit** is included as a dev dependency but its pre-commit hook is currently disabled. Consider fixing and re-enabling it for security analysis.

### Database

12. **Always run migrations** after pulling new code: `docker compose exec web python manage.py migrate`.
13. **Be careful with `docker compose down -v`** — the `-v` flag deletes the PostgreSQL data volume, wiping your database.

### Testing

14. **See [TESTS.md](TESTS.md)** for the full testing guide — TDD workflow, conventions, coverage, and best practices.
15. **Tests run in a pre-push hook** — pushing will fail if tests don't pass.

### Celery & Task Monitoring

16. **Celery Beat uses `DatabaseScheduler`** — periodic tasks are managed in the database through `django-celery-beat`, not config files. This means you can create/modify schedules at runtime via Django Admin or programmatically.
17. **If tasks aren't running**, check: (a) Redis is reachable, (b) Celery worker is connected, (c) Beat is running, (d) the periodic task `is_enabled` in Django Admin.
18. **The worker uses `--concurrency=2`** — adjust this in `docker-compose.yml` based on your system resources.
