# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Reference Documentation

Read these files before making changes — they are the source of truth for this project:

- **Project description & features:** [README.md](README.md)
- **Setup, architecture, commands, commit convention & design patterns:** [DEVELOPMENT.md](DEVELOPMENT.md)
- **Testing philosophy, conventions, structure & coverage:** [TESTS.md](TESTS.md)
- **Frontend design system, components & template conventions:** [FRONTEND.md](FRONTEND.md)

## Critical Rules

- **Always run commands via `docker compose exec web`** — never run Python, Django, or Ruff commands directly on the host.
- **Read the relevant doc before working** — read `TESTS.md` before writing tests, `FRONTEND.md` before touching templates.
- **Keep documentation up to date** — whenever a relevant change is made (new conventions, architecture decisions, commands, test rules, frontend patterns, etc.), update the affected doc(s): `AGENTS.md`, `CLAUDE.md`, `TESTS.md`, `FRONTEND.md`, or any other file that describes the changed area.

## Common Commands

```bash
# Start full stack
docker compose up --build

# Run all tests
docker compose exec web python manage.py test -v 2 --keepdb --failfast

# Run tests for a specific app
docker compose exec web python manage.py test assets -v 2

# Run a single test class
docker compose exec web python manage.py test assets.views.tests.test_asset_create.AssetCreateViewTests -v 2

# Run with coverage
docker compose exec web python -m coverage run manage.py test -v 2 --failfast
docker compose exec web python -m coverage report

# Lint & format
docker compose exec web ruff check . --fix
docker compose exec web ruff format .

# Django management
docker compose exec web python manage.py migrate
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell
```

## Architecture

**B3 Price Monitoring** is a Django 5.2 investment alert platform. Users register assets (B3 stocks, cryptos, ETFs), define "price tunnels" (upper/lower price limits), and receive automated email alerts via Celery when prices breach those limits.

### Apps

| App | Responsibility |
|-----|---------------|
| `accounts` | Custom `User` model (extends `AbstractUser`), `UserProfile` (avatar), login/logout/register/password flows. `UserProfile` is auto-created via a `post_save` signal. |
| `assets` | `Asset` model (symbol, type, owner) with external API validation on save; `AssetPrice` for historical price records. |
| `tunnels` | `PriceTunnel` model (upper/lower limits, check interval); `PeriodicTaskAssociation` links each tunnel to a `django_celery_beat.PeriodicTask`. |
| `globals` | Shared utilities: `EmailNotificationService`, HTTP status code helpers, exchange rate service. |

### URL Routing

| Prefix | App |
|--------|-----|
| `/admin/` | Django Admin |
| `/accounts/` | Login, logout, registration, password management |
| `/assets/` | Asset CRUD |
| `/tunnels/` | Tunnel CRUD |

### Price Monitoring Flow

```
User creates PriceTunnel
        │
        ▼
TunnelCreateForm.save()
        ├── Creates PriceTunnel in DB
        └── PeriodicTunnelTasksManager.create_periodic_task_for_tunnel()
               ├── Creates IntervalSchedule (Celery Beat)
               ├── Creates PeriodicTask with task kwargs
               └── Creates PeriodicTaskAssociation link
                      │
                      ▼ (at configured interval)
               price_check() — Celery task
                      ├── Fetches current price (YFinanceApiHandler / BrapiApiHandler)
                      ├── Records AssetPrice in DB
                      ├── Checks upper/lower limits
                      └── Sends HTML email via EmailNotificationService if breached
```

### Key Files

| File | Purpose |
|------|---------|
| `assets/models/asset.py` | `Asset` — validates symbol via `YFinanceAssetValidator` on every save where symbol or type changes |
| `assets/services/yfinance/` | `YFinanceApiHandler` (price fetching) + `YFinanceAssetValidator` (symbol validation); share `SYMBOL_MAP` via `constants.py` |
| `assets/services/brapi/` | `BrapiApiHandler` + `BrapiApiAssetValidator` — alternative price source via Brapi API |
| `assets/utils/handlers/base_api_handler.py` | Base HTTP handler with retry logic (3 retries, 2s timeout) |
| `assets/utils/validators/base_asset_validator.py` | `BaseAssetValidator` — ABC with abstract `is_valid` property |
| `assets/forms/asset_form.py` | `AssetForm` — unified create/update form with user-aware duplicate-symbol validation |
| `tunnels/tasks/tunnel_asset_price_check.py` | `price_check()` — main Celery task |
| `tunnels/utils/tunnel_manager.py` | `TunnelManager` — price-check business logic |
| `tunnels/utils/tasks/periodic_tunnel_tasks_manager.py` | `PeriodicTunnelTasksManager` — Celery Beat task lifecycle |
| `globals/services/notifications/email.py` | `EmailNotificationService` — renders and sends HTML email alerts |
| `core/celery.py` | Celery app initialization and configuration |
| `core/settings.py` | Django settings — PostgreSQL, Redis cache, Celery, custom User model |

### Infrastructure

| Service | Purpose | Port |
|---------|---------|------|
| `web` | Django dev server | 8000 |
| `db` | PostgreSQL 18 | 5432 |
| `redis` | Broker & cache | 6379 |
| `celery` | Task worker | — |
| `beat` | Celery Beat scheduler | — |
| `flower` | Celery monitoring UI | 5555 |

## Code Style

- **Linter/Formatter:** Ruff — rules E, F, I, B, UP, DJ, SIM, C4; line length 99; ignored: DJ001
- **Commits:** Conventional Commits — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, etc. Scope = app name (e.g. `fix(assets): ...`)

## Testing Conventions

> Full guide: [TESTS.md](TESTS.md)

- **Framework:** Django `TestCase` — not pytest
- **HTTP status codes:** always `from http import HTTPStatus` → `HTTPStatus.OK`, `HTTPStatus.FOUND`, `HTTPStatus.NOT_FOUND` — never literal integers
- **Test location:** `tests/` subdirectory inside each module, mirroring production structure:
  ```
  assets/
  ├── views/
  │   ├── asset_create.py
  │   └── tests/
  │       └── test_asset_create.py
  ├── models/
  │   └── tests/
  │       └── test_asset.py
  └── forms/
      └── tests/
          └── test_asset_form.py
  ```
- **Setup:** `setUpTestData` for shared read-only fixtures; `setUp` only when tests mutate the object
- **Class naming:** suffix `Tests`, matching the production class — `AssetCreateView` → `AssetCreateViewTests`
- **Coverage minimum:** 80%

## Frontend Conventions

> Full guide: [FRONTEND.md](FRONTEND.md)

- **Stack:** Django Templates + Bootstrap 5.3.3 + Tabler Icons + custom theme CSS
- **Layout:** sidebar + topbar for all authenticated pages; full-screen centered for auth pages
- **All templates** must extend `base.html` (or `base_auth.html` for auth pages)
- **Never use** `{{ form.as_p }}` — always render form fields individually
- **Never hardcode URLs** — always use `{% url %}`
- **Icons:** Tabler Icons only (`ti ti-*` classes); do not add other icon libraries
- **Monetary values:** always `font-monospace fw-bold`
- **Badges:** `bg-*-subtle` + `text-*-emphasis` pattern (e.g. `bg-success-subtle text-success-emphasis`)
- **Primary color:** `#00a76f` (green) via `btn-primary`; upper limits → `text-danger`, lower limits → `text-success`
