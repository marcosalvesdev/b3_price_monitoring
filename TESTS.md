# Testing Guide — B3 Price Monitoring

This document defines the testing philosophy, conventions, and best practices for the project. All contributors (humans and AI agents) should follow these guidelines.

---

## Table of Contents

- [TDD Workflow](#tdd-workflow)
- [Test Runner & Configuration](#test-runner--configuration)
- [Test Organization](#test-organization)
- [Test Layers](#test-layers)
- [Naming Conventions](#naming-conventions)
- [Test Structure (AAA Pattern)](#test-structure-aaa-pattern)
- [Setup Strategy](#setup-strategy)
- [Test Data with Factories](#test-data-with-factories)
- [Mocking Guidelines](#mocking-guidelines)
- [HTTP Status Codes in Tests](#http-status-codes-in-tests)
- [Coverage](#coverage)
- [Time-Dependent Tests](#time-dependent-tests)
- [Celery Task Testing](#celery-task-testing)
- [Running Tests](#running-tests)

---

## TDD Workflow

This project follows **Test-Driven Development (TDD)** using the Red-Green-Refactor cycle:

1. **Red** — Write a failing test that defines the expected behavior.
2. **Green** — Write the minimum production code to make the test pass.
3. **Refactor** — Improve the code (both production and test) while keeping all tests green.

### Rules

- **Never write production code without a failing test first.** If you're adding a new feature, view, model method, service, or utility — start with a test.
- **One behavior per test.** Each test method should verify exactly one thing. If a test name needs "and" in it, split it into two tests.
- **Tests are first-class code.** They should be readable, maintainable, and follow the same code quality standards as production code (Ruff linting/formatting applies to tests too).
- **Don't test framework internals.** Don't test that Django's ORM saves to the database or that `reverse()` returns a URL. Test *your* logic and *your* integration with the framework.

---

## Test Runner & Configuration

The project uses **Django's built-in test framework** (`django.test.TestCase`) — not pytest.

```bash
# Run all tests
python manage.py test -v 2 --failfast

# Run tests for a specific app
python manage.py test assets -v 2

# Run a specific test module
python manage.py test tunnels.tasks.tests -v 2

# Run a specific test class
python manage.py test tunnels.views.tests.test_tunnel_create.TunnelCreateViewTests -v 2

# Run a single test method
python manage.py test tunnels.views.tests.test_tunnel_create.TunnelCreateViewTests.test_redirect_if_not_logged_in -v 2
```

### Flags

| Flag | Purpose |
|---|---|
| `-v 2` | Verbose output — shows each test name and result |
| `--failfast` | Stop on first failure (faster feedback loop during TDD) |
| `--keepdb` | Reuse the test database between runs (faster locally) |
| `--parallel` | Run tests in parallel (use when the suite grows large) |

> **Note:** The `RUNNING_TESTS` flag in `core/settings.py` automatically disables Django Debug Toolbar during test runs.

---

## Test Organization

Tests live inside `tests/` subdirectories within each module, mirroring the production code structure. Each test file corresponds to a single production module.

```
app/
├── views/
│   ├── __init__.py
│   ├── asset_create.py
│   ├── asset_list.py
│   └── tests/
│       ├── __init__.py
│       ├── test_asset_create.py
│       └── test_asset_list.py
├── models/
│   ├── __init__.py
│   ├── asset.py
│   └── tests/
│       ├── __init__.py
│       └── test_asset.py
├── forms/
│   ├── __init__.py
│   ├── asset_create.py
│   └── tests/
│       ├── __init__.py
│       └── test_asset_create.py
├── services/
│   └── brapi/
│       ├── __init__.py
│       ├── handler.py
│       └── tests/
│           ├── __init__.py
│           └── test_handler.py
└── utils/
    ├── validators/
    │   ├── __init__.py
    │   ├── asset_validator.py
    │   └── tests/
    │       ├── __init__.py
    │       └── test_asset_validator.py
    └── handlers/
        ├── __init__.py
        ├── asset_api_handler.py
        └── tests/
            ├── __init__.py
            └── test_asset_api_handler.py
```

### Rules

- **One test file per production module.** `asset_create.py` → `test_asset_create.py`.
- **One test class per production class/function.** `AssetCreateView` → `AssetCreateViewTests`.
- **Always create `__init__.py`** in every `tests/` directory.
- **Never put tests in the app-level `tests.py`.** Use the `tests/` subdirectory structure instead. The app-level `tests.py` files are legacy placeholders and should remain empty or be removed.

---

## Test Layers

### Unit Tests

Test a single function, method, or class **in isolation**. External dependencies (APIs, database, email) are mocked.

**Use for:** model methods, validators, utility functions, service logic, Celery task logic.

```python
from unittest.mock import patch
from django.test import TestCase

class TunnelManagerTestCase(TestCase):
    def test_price_is_above_tunnel_limit_returns_true(self):
        manager = TunnelManager(asset_current_price=25, tunnel_upper_limit=20, tunnel_lower_limit=10)
        self.assertTrue(manager.price_is_above_tunnel_limit())
```

### Integration Tests

Test the **interaction between components** — views + forms + models + templates + URL routing. Use Django's test `Client` to make real HTTP requests against the test database.

**Use for:** views (CRUD operations), form validation flows, authentication/authorization, template rendering.

```python
from django.test import TestCase
from django.urls import reverse

class AssetCreateViewTests(TestCase):
    def test_create_valid_post_creates_asset(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("assets:create"), data={...})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
```

### When to Use Each

| Scenario | Layer |
|---|---|
| Model property or method | Unit |
| Validator logic | Unit |
| Service/handler with external API | Unit (mock the API) |
| Celery task logic | Unit (mock dependencies) |
| View returns correct status code | Integration |
| View enforces authentication | Integration |
| Form validation with POST request | Integration |
| User can't access another user's data | Integration |

---

## Naming Conventions

### Test Files

- Prefix: `test_` (required by Django's test discovery).
- Match the production module name: `asset_create.py` → `test_asset_create.py`.

### Test Classes

- Suffix: `Tests` or `TestCase`.
- Match the production class: `AssetCreateView` → `AssetCreateViewTests`.

### Test Methods

Follow the pattern: `test_<action_or_condition>_<expected_result>`

```python
# Good — descriptive and follows the pattern
def test_redirect_if_not_logged_in(self):
def test_create_valid_post_creates_asset(self):
def test_price_is_above_tunnel_limit_returns_true(self):
def test_delete_other_user_asset_returns_404(self):

# Bad — vague or doesn't describe expected behavior
def test_create(self):
def test_it_works(self):
def test_asset_1(self):
```

---

## Test Structure (AAA Pattern)

Every test method follows the **Arrange-Act-Assert** pattern:

```python
def test_price_above_upper_limit_sends_email(self):
    # Arrange — set up test data and preconditions
    asset_price = 35.0
    mock_api_handler = MagicMock()
    mock_api_handler.asset_price.return_value = asset_price

    # Act — execute the behavior being tested
    result = price_check(**self.test_kwargs)

    # Assert — verify the expected outcome
    self.assertIn("above the upper limit", result["message"])
    self.assertEqual(result["price"], 35.0)
```

### Rules

- **Use comments** (`# Arrange`, `# Act`, `# Assert`) for tests with complex setup. For simple tests, the structure should be self-evident.
- **Keep the Act phase to a single line** when possible — that's the thing you're testing.
- **Avoid logic in tests** — no `if`, `for`, or `try/except` in test methods. If you need conditional behavior, write separate tests.

---

## Setup Strategy

### `setUpTestData(cls)` — Preferred for shared read-only data

Class-level setup that runs **once per test class**. Use for data that tests only read (users, assets, URLs). Faster because it doesn't re-create objects for each test.

```python
@classmethod
def setUpTestData(cls):
    cls.user = User.objects.create_user(username="testuser", password="testpass123")
    cls.asset = Asset.objects.create(name="Test Asset", user=cls.user, symbol="TEST1", type="stock")
    cls.url = reverse("assets:detail", kwargs={"pk": cls.asset.pk})
```

### `setUp(self)` — For data that tests modify

Instance-level setup that runs **before every test method**. Use when tests create, update, or delete records.

```python
def setUp(self):
    self.tunnel = PriceTunnel.objects.create(
        asset=self.asset, upper_limit=150.00, lower_limit=100.00, check_interval_minutes=10,
    )
```

### Rule of Thumb

- If the test **reads** the data → `setUpTestData`
- If the test **modifies** the data → `setUp`
- If only one test needs it → set it up inside the test method itself

---

## Test Data with Factories

> **Dependency:** `factory_boy` (add to dev dependencies when adopting)

As the test suite grows, manually creating objects with `Model.objects.create(...)` becomes repetitive and fragile. **Factories** centralize test data creation and make tests more readable.

### Why Factories

```python
# Without factories — verbose, repeated across many test files
cls.user = User.objects.create_user(username="testuser", password="testpass123")
cls.asset = Asset.objects.create(
    name="Test Asset", user=cls.user, symbol="TEST1", type="stock", is_active=True,
)

# With factories — concise and expressive
cls.user = UserFactory()
cls.asset = AssetFactory(user=cls.user)
```

### Factory Location

Place factories in a `factories.py` file inside each app's `tests/` directory:

```
app/
└── tests/
    ├── __init__.py
    ├── factories.py       # All factories for this app
    ├── test_views.py
    └── test_models.py
```

### Factory Example

```python
# assets/tests/factories.py
import factory
from accounts.models import User
from assets.models import Asset


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class AssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Asset

    name = factory.Sequence(lambda n: f"Asset {n}")
    user = factory.SubFactory(UserFactory)
    symbol = factory.Sequence(lambda n: f"TST{n}")
    type = "stock"
    is_active = True
```

### Adoption Strategy

Factories are **recommended but not yet mandatory**. When writing new tests:

1. If the app already has a `factories.py`, use the existing factories.
2. If not, you may create `factories.py` and add factories as needed.
3. Existing tests using `Model.objects.create(...)` don't need to be migrated immediately.

---

## Mocking Guidelines

### When to Mock

| Scenario | Mock? | Why |
|---|---|---|
| External API calls (Brapi, yfinance) | **Always** | Tests must not depend on external services |
| Email sending | **Always** | Don't send real emails in tests |
| Celery task execution | **Always** | Mock the task or use `task.apply()` for synchronous execution |
| Database access | **Rarely** | Django's `TestCase` wraps each test in a transaction and rolls back. Use the real DB |
| Time/dates | **When needed** | Use `freezegun` for time-sensitive logic |
| Internal classes (models, validators) | **Avoid** | Prefer real objects for internal code — mock only at system boundaries |

### How to Mock

Use `unittest.mock.patch` as a decorator on the test method. Patch where the object is **used**, not where it's **defined**:

```python
# Correct — patch where it's imported/used
@patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
def test_api_called(self, mock_handler):
    ...

# Wrong — patching the source module
@patch("assets.utils.handlers.asset_api_handler")
def test_api_called(self, mock_handler):
    ...
```

### Mock Argument Order

When stacking `@patch` decorators, **the bottom decorator maps to the first mock argument**:

```python
@patch("module.ClassC")          # → mock_c (3rd arg)
@patch("module.ClassB")          # → mock_b (2nd arg)
@patch("module.ClassA")          # → mock_a (1st arg)
def test_example(self, mock_a, mock_b, mock_c):
    ...
```

---

## HTTP Status Codes in Tests

Use **`http.HTTPStatus`** from Python's standard library for readable status code assertions:

```python
from http import HTTPStatus

def test_detail_returns_200_for_owner(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, HTTPStatus.OK)

def test_redirect_if_not_logged_in(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, HTTPStatus.FOUND)

def test_other_user_asset_returns_404(self):
    response = self.client.get(other_url)
    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
```

### Common Status Codes

| Constant | Value | Usage |
|---|---|---|
| `HTTPStatus.OK` | 200 | Successful GET, successful form re-render |
| `HTTPStatus.CREATED` | 201 | Resource created (API responses) |
| `HTTPStatus.FOUND` | 302 | Redirect after POST, login redirect |
| `HTTPStatus.BAD_REQUEST` | 400 | Invalid request |
| `HTTPStatus.FORBIDDEN` | 403 | Permission denied |
| `HTTPStatus.NOT_FOUND` | 404 | Resource not found, access denied (ownership) |

> **Note:** The project currently uses a custom `globals.http_helpers.status_codes` module. New tests should use `http.HTTPStatus` instead. Existing tests will be migrated gradually.

---

## Coverage

> **Dependency:** `coverage` (add to dev dependencies when adopting)

### Running Coverage

```bash
# Run tests with coverage measurement
python -m coverage run manage.py test -v 2 --failfast

# Show coverage report in terminal
python -m coverage report

# Generate HTML report (open htmlcov/index.html)
python -m coverage html

# Show only files with less than 100% coverage
python -m coverage report --skip-covered
```

> **Note:** Always use `python -m coverage` instead of bare `coverage`. Inside the Docker container, the `coverage` binary may not be on `$PATH`, but `python -m` always resolves installed modules correctly.

### Configuration (pyproject.toml)

```toml
[tool.coverage.run]
source = ["accounts", "assets", "tunnels", "globals"]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__pycache__/*",
    "*/admin.py",
    "manage.py",
    "core/*",
]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

### Coverage Targets

| Level | Target | Notes |
|---|---|---|
| **Overall project** | ≥ 80% | Minimum threshold — CI should fail below this |
| **New code** | 100% | All new code written via TDD should be fully covered |
| **Critical paths** | 100% | Price checking, email notifications, authentication |

### Adoption Strategy

Coverage is already configured. Remaining steps:

1. Add a coverage step to the GitHub Actions workflow.
2. Add a coverage step to the pre-push hook.

---

## Time-Dependent Tests

> **Dependency:** `freezegun` (add to dev dependencies when adopting)

For testing logic that depends on the current time (e.g., price check timestamps, monitoring intervals):

```python
from freezegun import freeze_time
from django.test import TestCase

class AssetPriceTestCase(TestCase):
    @freeze_time("2025-06-15 14:30:00")
    def test_price_record_has_correct_timestamp(self):
        price = AssetPrice.objects.create(asset=self.asset, price=25.50)
        self.assertEqual(price.created_at.hour, 14)
        self.assertEqual(price.created_at.minute, 30)
```

### Adoption Strategy

`freezegun` is **recommended but not yet installed**. Add it to dev dependencies when time-dependent tests are needed.

---

## Celery Task Testing

Celery tasks are tested as unit tests with **all external dependencies mocked**:

```python
from unittest.mock import MagicMock, patch
from django.test import TestCase

class PriceCheckTaskTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_kwargs = {
            "asset_symbol": "PETR4",
            "asset_id": 1,
            "asset_type": "stock",
            "asset_name": "Petrobras",
            "tunnel_upper_limit": 30.0,
            "tunnel_lower_limit": 20.0,
            "emails_to_notification": ["user@example.com"],
            "user_name": "user_example",
        }

    @patch("module.path.TunnelManager")
    @patch("module.path.asset_api_handler")
    def test_price_within_limits(self, mock_handler, mock_manager):
        # Arrange
        mock_handler.return_value.asset_price.return_value = 25.0
        mock_manager.return_value.price_is_above_tunnel_limit.return_value = False
        mock_manager.return_value.price_is_below_tunnel_limit.return_value = False

        # Act
        result = price_check(**self.test_kwargs)

        # Assert
        self.assertIn("within the limits", result["message"])
```

### Rules

- **Always mock the API handler** — never make real HTTP requests in tests.
- **Always mock the email service** — verify `send_email_with_html_content` was called with correct args.
- **Test all price scenarios** — within limits, above upper, below lower, API failure (returns `None`).

---

## Running Tests

### With Docker (recommended)

```bash
# All tests
docker compose exec web python manage.py test -v 2 --keepdb --failfast

# Specific app
docker compose exec web python manage.py test assets -v 2

# Specific test class
docker compose exec web python manage.py test tunnels.tasks.tests -v 2

# Tests with coverage
docker compose exec web python -m coverage run manage.py test -v 2 --failfast
docker compose exec web python -m coverage report
```

### Locally

```bash
python manage.py test -v 2 --keepdb --failfast
```

### CI/CD

Tests run automatically via GitHub Actions on every push to `main` and on pull requests. See `.github/workflows/tests.yml`.

### Pre-push Hook

Tests also run as a **pre-push Git hook** — pushing will fail if tests don't pass. See the [Code Quality section in DEVELOPMENT.md](DEVELOPMENT.md#code-quality--pre-commit) for hook setup.
