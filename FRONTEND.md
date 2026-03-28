# Frontend Guide — B3 Price Monitoring

This document defines the frontend design system, component patterns, and template conventions for the **B3 Price Monitoring** project. The UI is based on a custom admin theme (Bootstrap 5.3) and built with **Django Templates**.

---

## Table of Contents

- [Overview](#overview)
- [Reference Documentation](#reference-documentation)
- [Design Philosophy](#design-philosophy)
- [Theme Assets](#theme-assets)
- [Color Palette](#color-palette)
- [Typography](#typography)
- [Spacing & Layout](#spacing--layout)
- [Navigation](#navigation)
- [Cards](#cards)
- [Buttons](#buttons)
- [Forms](#forms)
- [Tables](#tables)
- [Badges & Status Indicators](#badges--status-indicators)
- [Alerts & Messages](#alerts--messages)
- [Avatars](#avatars)
- [Icons](#icons)
- [Shadows & Depth](#shadows--depth)
- [Dark Mode](#dark-mode)
- [Detail Views](#detail-views)
- [Delete Confirmation Pages](#delete-confirmation-pages)
- [Authentication Pages](#authentication-pages)
- [Django Template System — Reusability Rules](#django-template-system--reusability-rules)
- [Page-Specific Guidelines](#page-specific-guidelines)
- [Dos and Don'ts Summary](#dos-and-donts-summary)

---

## Overview

This is a **financial monitoring web application** for the Brazilian stock market (B3), cryptocurrencies, and ETFs. The frontend uses **Django Templates** with a custom admin theme built on **Bootstrap 5.3.3**. The UI must convey **trust, clarity, and professionalism** — consistent with fintech and investment platforms.

---

## Reference Documentation

When implementing or troubleshooting frontend code, AI agents should consult the official documentation if necessary:

- **Bootstrap 5.3**: https://getbootstrap.com/docs/5.3/getting-started/introduction/
- **Django Template Language**: https://docs.djangoproject.com/en/5.2/ref/templates/language/
- **Django Template Built-in Tags & Filters**: https://docs.djangoproject.com/en/5.2/ref/templates/builtins/
- **Django Forms Rendering**: https://docs.djangoproject.com/en/5.2/topics/forms/#rendering-fields-manually
- **Django Messages Framework**: https://docs.djangoproject.com/en/5.2/ref/contrib/messages/
- **Tabler Icons**: https://tabler.io/icons
- **Theme CSS**: `static/css/theme.css`

---

## Design Philosophy

- **Clean and minimal** — No visual clutter. Every element must serve a purpose. Generous whitespace, clear hierarchy, and restrained use of color.
- **Financial application style** — Formal, data-driven look. Think brokerage dashboards: structured tables, clear numbers, soft neutral backgrounds, and precise alignment.
- **Scannable at a glance** — Investors need to read prices, limits, and statuses quickly. Use typography weight and spacing to guide the eye, not decoration.
- **Consistent pattern** — Every page follows the same layout rhythm, spacing, and component style. No one-off designs.
- **Sidebar-driven navigation** — Collapsible sidebar with a top navbar for user actions.

---

## Theme Assets

The project uses the following frontend dependencies:

| Library | Version | Purpose |
|---|---|---|
| **Bootstrap** | 5.3.3 | Core CSS framework |
| **Tabler Icons** | 2.45.0 | Icon library (webfont) |
| **ApexCharts** | 3.52.0 | Interactive charts (if needed) |
| **SimpleBar** | 6.2.5 | Custom scrollbars |

### Font

The theme uses **Public Sans** from Google Fonts:

```html
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

---

## Color Palette

The theme overrides Bootstrap's default palette. Use the theme's CSS custom properties and utility classes.

### Primary Colors

| Role | Color | CSS Variable | Usage |
|---|---|---|---|
| **Primary** | `#00a76f` (Green) | `--ds-primary` | Main actions, active states, links |
| **Secondary** | `#637381` (Gray) | `--ds-secondary` | Secondary text, muted elements |
| **Success** | `#22c55e` (Light Green) | `--ds-success` | Buy signals, active tunnels, positive states |
| **Info** | `#00b8d9` (Cyan) | `--ds-info` | Informational badges, shipped status |
| **Warning** | `#ffab00` (Amber) | `--ds-warning` | Pending states, caution alerts |
| **Danger** | `#ff5630` (Red-Orange) | `--ds-danger` | Sell signals, errors, destructive actions, inactive tunnels |

### Gray Scale

| Token | Hex | Usage |
|---|---|---|
| **Gray-100** | `#f9fafb` | Light backgrounds, table headers |
| **Gray-200** | `#f4f6f8` | Subtle backgrounds, borders |
| **Gray-300** | `#dfe3e8` | Hover states, dashed borders |
| **Gray-500** | `#919eab` | Placeholder text, muted content |
| **Gray-600** | `#637381` | Secondary text, sidebar nav items |
| **Gray-700** | `#454f5b` | Emphasized text |
| **Gray-800** | `#1c252e` | Strong text, headings |
| **Gray-900** | `#141a21` | Dark backgrounds |

### Usage with Bootstrap Utilities

```html
<!-- Subtle backgrounds for badges and indicators -->
<span class="badge bg-success-subtle text-success-emphasis">Active</span>
<span class="badge bg-danger-subtle text-danger-emphasis">Inactive</span>

<!-- Text colors -->
<p class="text-primary">Primary green text</p>
<small class="text-muted">Secondary info</small>
```

---

## Typography

- **Font family:** Public Sans (loaded via Google Fonts). Falls back to system fonts.
- **Page titles:** `<h2>` with `fw-semibold mb-4`.
- **Section titles / card headers:** `<h5>` with `fw-semibold`.
- **Data labels:** `<small class="text-muted text-uppercase">` or `form-label` class.
- **Monetary values:** `fw-bold` with `font-monospace` for price alignment (e.g., `R$ 48,00`).
- **Status text:** Use `fw-semibold` with contextual color (`text-success`, `text-danger`).

### Font Weights

| Class | Weight | Usage |
|---|---|---|
| `fw-light` | 300 | De-emphasized text |
| `fw-normal` | 400 | Body text |
| `fw-medium` | 500 | Subtle emphasis |
| `fw-semibold` | 600 | Headings, labels, buttons |
| `fw-bold` | 700 | Monetary values, strong emphasis |
| `fw-bolder` | 800 | Display text |

---

## Spacing & Layout

### Spacing Scale

The theme extends Bootstrap's spacing with additional values:

| Class suffix | Size | Pixels |
|---|---|---|
| `1` | 0.25rem | 4px |
| `2` | 0.5rem | 8px |
| `3` | 1rem | 16px |
| `4` | 1.5rem | 24px |
| `5` | 3rem | 48px |
| `6` | 1.25rem | 20px |
| `7` | 1.75rem | 28px |
| `8` | 2rem | 32px |
| `9` | 2.5rem | 40px |

### Layout Structure

The theme uses a **sidebar + content area** layout:

```
┌──────────────────────────────────────────────────┐
│  Top Navbar (glass effect, user actions)          │
├──────┬───────────────────────────────────────────┤
│      │                                           │
│ Side │         Main Content Area                 │
│ bar  │                                           │
│      │                                           │
│ 60px │    .custom-container                      │
│  or  │                                           │
│250px │                                           │
│      │                                           │
└──────┴───────────────────────────────────────────┘
```

- **Sidebar collapsed:** 60px width (icon-only).
- **Sidebar expanded:** 250px width (icon + label).
- **Content area:** Uses `.custom-container` provided by the theme.
- **Top navbar:** Fixed with `backdrop-filter: blur(6px)` glass effect, dashed bottom border.
- **Responsive:** Sidebar collapses on mobile with offcanvas toggle.

### Page Wrapper

All authenticated pages follow this structure:

```html
{% extends "base.html" %}

{% block title %}Page Title — B3 Monitor{% endblock %}

{% block content %}
<div class="custom-container">
    <!-- Breadcrumb (optional) -->
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{% url 'assets:list' %}">Home</a></li>
            <li class="breadcrumb-item active">Page Title</li>
        </ol>
    </nav>

    <!-- Page title -->
    <h2 class="fw-semibold mb-4">Page Title</h2>

    <!-- Page content here -->
</div>
{% endblock %}
```

### Rules

- Use the sidebar + content layout for all authenticated pages.
- Authentication pages (login, register, password reset) use a full-screen centered layout without the sidebar.
- Use Bootstrap grid (`row`, `col-md-*`) for multi-column layouts inside the content area.

---

## Navigation

### Sidebar

The sidebar uses the `.miniSidebar` pattern:

```html
<nav id="miniSidebar" class="miniSidebar">
    <div class="brand-logo">
        <a href="{% url 'assets:list' %}">
            <!-- Logo or brand text -->
            <span class="fw-bold">B3 Monitor</span>
        </a>
    </div>
    <ul class="nav flex-column">
        <li class="nav-item">
            <a class="nav-link" href="{% url 'assets:list' %}">
                <span class="nav-icon"><i class="ti ti-chart-bar"></i></span>
                <span class="nav-text">My Assets</span>
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="{% url 'tunnels:list' %}">
                <span class="nav-icon"><i class="ti ti-arrows-diff"></i></span>
                <span class="nav-text">My Tunnels</span>
            </a>
        </li>
    </ul>
</nav>
```

#### Sidebar Rules

- Nav icons: Use Tabler Icons (`ti ti-*` classes), sized at 20×20px.
- Active state: Apply `text-primary-emphasis` color and `bg-primary-subtle` background.
- Section headings: Use `.nav-heading` (hidden when sidebar is collapsed).
- Border-radius on nav items: `0.5rem`.

### Top Navbar

The top navbar handles user actions and search:

```html
<nav class="navbar navbar-glass">
    <div class="d-flex align-items-center">
        <!-- Sidebar toggle button -->
        <!-- Search (optional) -->
    </div>
    <div class="d-flex align-items-center gap-3">
        <!-- Theme toggle (dark/light) -->
        <!-- User avatar + dropdown -->
    </div>
</nav>
```

- Style: Fixed with glass effect (`backdrop-filter: blur(6px)`), transparent background.
- Bottom border: Dashed `var(--ds-gray-300)`.
- Width: `calc(100% - sidebar_width)`.

### Breadcrumb

```html
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="#">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page">Current Page</li>
    </ol>
</nav>
```

- Link color: `var(--ds-gray-800)`, hover: `var(--ds-primary)`.

---

## Cards

Cards are the **primary content container**. The theme uses elevated cards with rounded corners.

```html
<div class="card card-lg">
    <div class="card-body p-6">
        <h5 class="card-title fw-semibold mb-3">Card Title</h5>
        <!-- content -->
    </div>
</div>
```

### Rules

- Use `card card-lg` for primary content cards — this applies `shadow-xl` and `border-radius-xl` (0.75rem).
- Use `card-lift` class for cards that should elevate on hover (e.g., list items, dashboard stats).
- Borders: None (`border: 0`). Dashed borders only when explicitly needed.
- Padding: Use `p-6` inside `card-body` for comfortable spacing.
- Card headers: Use a `<h5 class="card-title fw-semibold mb-3">` inside the card body. If a card header with a border is needed, use `.card-header` with a dashed bottom border.
- Do **not** use colored card backgrounds unless it's a status indicator or dashboard stat.

---

## Buttons

### Variants

| Action | Class | Example |
|---|---|---|
| Primary action (Create, Save) | `btn btn-primary` | `<button class="btn btn-primary">Save</button>` |
| Secondary action (Cancel, Back) | `btn btn-white` | `<a class="btn btn-white">Cancel</a>` |
| Destructive action (Delete) | `btn btn-subtle-danger` | `<button class="btn btn-subtle-danger">Delete</button>` |
| Ghost action (toolbar) | `btn btn-ghost` | `<button class="btn btn-ghost">Filter</button>` |
| Small inline action (Edit, View) | `btn btn-sm btn-white` | `<a class="btn btn-sm btn-white">Edit</a>` |
| Icon-only button | `btn btn-icon btn-ghost` | `<button class="btn btn-icon btn-ghost"><i class="ti ti-edit"></i></button>` |

### Icon Buttons

```html
<!-- Standard icon button -->
<button class="btn btn-icon btn-ghost">
    <i class="ti ti-edit"></i>
</button>

<!-- Small icon button -->
<button class="btn btn-icon btn-xs btn-ghost">
    <i class="ti ti-trash"></i>
</button>
```

Sizes: `btn-icon` (2.5rem), `btn-icon btn-xs` (1.75rem), `btn-icon btn-sm` (2.1875rem), `btn-icon btn-lg` (3.37rem).

### Rules

- Primary actions use `btn-primary` (green `#00a76f`).
- Secondary/cancel actions use `btn-white` (white background with gray text).
- Destructive actions use `btn-subtle-danger` (light red background with danger text).
- Buttons in forms: Primary on the left, secondary (cancel) on the right, separated by `gap-2` using `d-flex gap-2`.
- Use `btn-ghost` for toolbar actions and toggles.
- Never use `btn-dark` for primary actions — use `btn-primary`.
- Icon buttons should use `btn-icon` class for consistent sizing.

---

## Forms

All forms use standard Bootstrap form classes with theme styling:

```html
<form method="post" novalidate class="needs-validation">
    {% csrf_token %}

    <div class="mb-3">
        <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
        {{ field }}
        {% if field.errors %}
            <div class="invalid-feedback d-block">
                {% for error in field.errors %}{{ error }}{% endfor %}
            </div>
        {% endif %}
        {% if field.help_text %}
            <div class="form-text">{{ field.help_text }}</div>
        {% endif %}
    </div>

    <div class="d-flex gap-2 mt-4">
        <button type="submit" class="btn btn-primary">Save</button>
        <a href="{% url 'cancel_url' %}" class="btn btn-white">Cancel</a>
    </div>
</form>
```

### Password Fields

The theme provides a toggle for password visibility:

```html
<div class="mb-3 position-relative password-field">
    <label class="form-label">Password</label>
    <input type="password" class="form-control">
    <span class="passwordToggler position-absolute" style="right: 20px; top: 50%;">
        <i class="ti ti-eye"></i>
    </span>
</div>
```

### Rules

- **Never use `{{ form.as_p }}`** — Always render fields individually for full control.
- Apply `form-control` class to all text/number/email inputs and `form-select` to dropdowns (set in Django form widget `attrs`).
- Show field errors with `invalid-feedback d-block` directly below the field.
- Show non-field errors (`form.non_field_errors`) at the top of the form inside an `alert alert-danger` div.
- Group related fields with spacing (`mb-3`).
- Monetary fields: Use `font-monospace` on the input for number alignment.
- Add `needs-validation` class to forms for the theme's validation styling.
- Required field labels can use `<span class="text-danger">*</span>` after the label text.

---

## Tables

Use tables for list views (asset list, tunnel list, price history). The theme uses centered, hover-enabled tables with light headers.

```html
<div class="table-responsive">
    <table class="table text-nowrap table-centered table-hover">
        <thead>
            <tr>
                <th>Column</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item.field }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="N" class="text-center text-muted py-4">No items found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

### Rules

- Always wrap in `table-responsive`.
- Use `table-hover` for row highlight on hover.
- Use `table-centered` (theme class) for vertical centering on all cells.
- Use `text-nowrap` to prevent cell content from wrapping.
- Header: `<thead>` with default theme styling (gray-100 background, gray-600 text, no visible borders).
- Empty state: Use `{% empty %}` tag with a centered muted message. Never show an empty table with just headers.
- Action buttons (Edit, Delete, View) go in the last column, right-aligned with `text-end`.
- Monetary values in table cells: `class="font-monospace"`.
- Status columns: Use subtle badges (see Badges section).
- Table borders use dashed style by default in the theme.

---

## Badges & Status Indicators

The theme uses subtle background variants paired with emphasis text colors:

```html
<!-- Active status -->
<span class="badge bg-success-subtle text-success-emphasis">Active</span>

<!-- Inactive status -->
<span class="badge bg-danger-subtle text-danger-emphasis">Inactive</span>

<!-- Pending status -->
<span class="badge bg-warning-subtle text-warning-emphasis">Pending</span>

<!-- Info status -->
<span class="badge bg-info-subtle text-info-emphasis">Shipped</span>

<!-- Asset type -->
<span class="badge bg-secondary-subtle text-secondary-emphasis">Stock</span>
```

### Badge Dot

For compact status indicators:

```html
<span class="badge badge-dot bg-success"></span> <!-- Small filled circle -->
```

### Rules

- Use `bg-*-subtle` + `text-*-emphasis` pattern for all status badges.
- Keep badge text short: "Active", "Inactive", "Stock", "Crypto", "ETF".
- Use `badge-dot` for compact inline status indicators (e.g., in tables next to text).

---

## Alerts & Messages

Use Django's `messages` framework with Bootstrap alerts:

```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    {% endfor %}
{% endif %}
```

Map Django message levels to Bootstrap classes:
- `messages.SUCCESS` → `alert-success`
- `messages.ERROR` → `alert-danger`
- `messages.WARNING` → `alert-warning`
- `messages.INFO` → `alert-info`

Place the messages block inside `base.html`, right after the navbar, inside the content container.

---

## Avatars

The theme provides a comprehensive avatar system:

```html
<!-- Image avatar -->
<img src="{{ user.profile.avatar.url }}" class="avatar avatar-md rounded-circle" alt="Avatar">

<!-- Initials avatar -->
<div class="avatar avatar-md rounded-circle avatar-primary">
    <div class="avatar-initials">JC</div>
</div>

<!-- Avatar with status -->
<div class="avatar avatar-md rounded-circle avatar-indicators avatar-online">
    <img src="..." alt="Avatar">
</div>
```

### Avatar Sizes

| Class | Description |
|---|---|
| `avatar-xs` | Extra small |
| `avatar-sm` | Small |
| `avatar` | Default (3rem) |
| `avatar-md` | Medium |
| `avatar-lg` | Large |
| `avatar-xl` | Extra large |
| `avatar-xxl` | Extra extra large |

### Status Indicators

| Class | Status |
|---|---|
| `avatar-online` | Green circle |
| `avatar-offline` | Gray circle |
| `avatar-away` | Yellow circle |
| `avatar-busy` | Red circle |

### Avatar Groups

```html
<div class="avatar-group">
    <img src="..." class="avatar avatar-sm rounded-circle">
    <img src="..." class="avatar avatar-sm rounded-circle">
</div>
```

---

## Icons

The project uses **Tabler Icons** via webfont.

```html
<!-- Using icon font class -->
<i class="ti ti-chart-bar"></i>
<i class="ti ti-edit"></i>
<i class="ti ti-trash"></i>
<i class="ti ti-plus"></i>
<i class="ti ti-eye"></i>
<i class="ti ti-arrows-diff"></i>
```

### Icon Shapes

For icons inside colored circles (dashboard cards, stats):

```html
<div class="icon-shape icon-lg rounded-circle bg-primary-subtle text-primary">
    <i class="ti ti-chart-bar"></i>
</div>
```

### Icon Sizes

| Class | Description |
|---|---|
| `icon-xxs` | Extra-extra-small |
| `icon-xs` | Extra-small |
| `icon-sm` | Small |
| `icon-md` | Medium |
| `icon-lg` | Large |
| `icon-xl` | Extra-large |

---

## Shadows & Depth

The theme defines a shadow scale via CSS custom properties:

| Class | Usage |
|---|---|
| `shadow-xs` | Subtle elevation (dropdowns) |
| `shadow` | Standard elevation |
| `shadow-sm` | Medium elevation (hover states) |
| `shadow-lg` | Strong elevation |
| `shadow-xl` | Card elevation (primary cards) |
| `shadow-none` | Remove shadow |

Colored shadows are also available: `shadow-primary`, `shadow-success`, `shadow-danger`, `shadow-warning`, `shadow-info`.

---

## Dark Mode

The theme supports dark mode via Bootstrap's `data-bs-theme` attribute:

```html
<!-- Set on <html> or <body> -->
<html data-bs-theme="dark">
```

### Theme Toggle

Implement with a dropdown button using `data-bs-theme-value`:

```html
<button data-bs-theme-value="light">Light</button>
<button data-bs-theme-value="dark">Dark</button>
<button data-bs-theme-value="auto">Auto</button>
```

Theme preference is persisted in `localStorage` by the theme's `color-modes.js` script.

### Rules

- Use `.dark-mode-block` to show elements only in dark mode.
- Use `.dark-mode-none` to hide elements in dark mode.
- All color utilities (`bg-*`, `text-*`) automatically adapt to the current theme.
- Shadows get darker with higher opacity in dark mode.

---

## Detail Views

Detail pages (asset detail, tunnel detail) display data in a **definition-style layout** inside a card:

```html
<div class="card card-lg">
    <div class="card-body p-6">
        <h5 class="card-title fw-semibold mb-3">VALE3 — Vale S.A.</h5>

        <div class="row g-3">
            <div class="col-sm-6">
                <small class="text-muted text-uppercase">Symbol</small>
                <p class="mb-0 fw-semibold">VALE3</p>
            </div>
            <div class="col-sm-6">
                <small class="text-muted text-uppercase">Type</small>
                <p class="mb-0">
                    <span class="badge bg-secondary-subtle text-secondary-emphasis">Stock</span>
                </p>
            </div>
            <div class="col-sm-6">
                <small class="text-muted text-uppercase">Upper Limit</small>
                <p class="mb-0 font-monospace fw-bold text-danger">R$ 70.00</p>
            </div>
            <div class="col-sm-6">
                <small class="text-muted text-uppercase">Lower Limit</small>
                <p class="mb-0 font-monospace fw-bold text-success">R$ 50.00</p>
            </div>
        </div>

        <div class="d-flex gap-2 mt-4">
            <a href="{% url 'edit_url' %}" class="btn btn-sm btn-white">
                <i class="ti ti-edit me-1"></i>Edit
            </a>
            <a href="{% url 'delete_url' %}" class="btn btn-sm btn-subtle-danger">
                <i class="ti ti-trash me-1"></i>Delete
            </a>
        </div>
    </div>
</div>
```

### Rules

- Use a two-column grid (`col-sm-6`) for label/value pairs.
- Labels: `<small class="text-muted text-uppercase">`.
- Values: `<p class="mb-0">` with appropriate font treatment.
- Monetary values always get `font-monospace fw-bold`.
- Upper limits use `text-danger`, lower limits use `text-success` (sell = red, buy = green — standard financial convention).
- Cards use `card card-lg` with `p-6` padding.

---

## Delete Confirmation Pages

```html
<div class="card card-lg">
    <div class="card-body p-6">
        <h5 class="card-title fw-semibold mb-3">Delete Asset</h5>
        <p>Are you sure you want to delete <strong>{{ asset.name }}</strong>? This action cannot be undone.</p>
        <form method="post">
            {% csrf_token %}
            <div class="d-flex gap-2 mt-3">
                <button type="submit" class="btn btn-subtle-danger">Delete</button>
                <a href="{% url 'cancel_url' %}" class="btn btn-white">Cancel</a>
            </div>
        </form>
    </div>
</div>
```

---

## Authentication Pages

Login, registration, and password reset pages use a full-screen centered layout **without the sidebar**:

```html
{% block content %}
<main class="d-flex flex-column justify-content-center vh-100">
    <section>
        <div class="container">
            <div class="row mb-8">
                <div class="col-xl-4 offset-xl-4 col-md-12 col-12 text-center">
                    <h2 class="fw-bold">B3 Monitor</h2>
                </div>
            </div>
            <div class="row justify-content-center">
                <div class="col-xl-5 col-lg-6 col-md-8 col-12">
                    <div class="card card-lg">
                        <div class="card-body p-6">
                            <h5 class="fw-semibold mb-4">Sign In</h5>
                            <!-- form here -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</main>
{% endblock %}
```

### Rules

- Full-screen height with vertical centering (`vh-100`, `d-flex`, `justify-content-center`).
- Card uses `card card-lg` with `p-6` padding.
- Brand/logo centered above the card.
- No sidebar or top navbar on authentication pages.

---

## Django Template System — Reusability Rules

### Template Hierarchy

```
templates/
├── base.html                          # Root layout (sidebar, navbar, Bootstrap, messages, scripts)
├── base_auth.html                     # Auth layout (no sidebar, centered card)
├── partials/
│   ├── _sidebar.html                  # Sidebar navigation
│   ├── _topbar.html                   # Top navbar
│   ├── _form_field.html               # Reusable single form field renderer
│   ├── _form_actions.html             # Submit + Cancel button row
│   ├── _empty_state.html              # "No items found" placeholder
│   ├── _delete_confirm.html           # Generic delete confirmation card
│   └── _messages.html                 # Flash messages block
├── accounts/templates/accounts/       # Account-specific templates
├── assets/templates/assets/           # Asset-specific templates
└── tunnels/templates/tunnels/         # Tunnel-specific templates
```

### Reusable Partials

Create partials in `templates/partials/` and include them with `{% include %}`. Partials are prefixed with `_` (underscore) to distinguish them from full pages.

#### `_messages.html`

Renders Django flash messages. Included in `base.html` once, right before `{% block content %}`.

#### `_sidebar.html`

Sidebar navigation. Included in `base.html`. Handles collapsed/expanded states and active link highlighting.

#### `_topbar.html`

Top navbar. Included in `base.html`. Contains sidebar toggle, search, theme switcher, and user dropdown.

#### `_form_field.html`

Renders a single form field with label, input, errors, and help text:

```html
<!-- templates/partials/_form_field.html -->
<div class="mb-3">
    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
    {{ field }}
    {% if field.errors %}
        <div class="invalid-feedback d-block">
            {% for error in field.errors %}{{ error }}{% endfor %}
        </div>
    {% endif %}
    {% if field.help_text %}
        <div class="form-text">{{ field.help_text }}</div>
    {% endif %}
</div>
```

Usage:

```html
{% for field in form %}
    {% include "partials/_form_field.html" with field=field %}
{% endfor %}
```

#### `_form_actions.html`

Renders the submit and cancel button row:

```html
<!-- templates/partials/_form_actions.html -->
<div class="d-flex gap-2 mt-4">
    <button type="submit" class="btn btn-primary">{{ submit_label|default:"Save" }}</button>
    {% if cancel_url %}
        <a href="{{ cancel_url }}" class="btn btn-white">Cancel</a>
    {% endif %}
</div>
```

Usage:

```html
{% include "partials/_form_actions.html" with submit_label="Create Asset" cancel_url=cancel_url %}
```

#### `_empty_state.html`

Shown when a list view has no items:

```html
<!-- templates/partials/_empty_state.html -->
<div class="text-center py-5">
    <p class="text-muted mb-3">{{ message|default:"No items found." }}</p>
    {% if action_url %}
        <a href="{{ action_url }}" class="btn btn-primary">{{ action_label|default:"Create" }}</a>
    {% endif %}
</div>
```

#### `_delete_confirm.html`

Generic delete confirmation:

```html
<!-- templates/partials/_delete_confirm.html -->
<div class="card card-lg">
    <div class="card-body p-6">
        <h5 class="card-title fw-semibold mb-3">{{ title|default:"Confirm Deletion" }}</h5>
        <p>Are you sure you want to delete <strong>{{ item_name }}</strong>? This action cannot be undone.</p>
        <form method="post">
            {% csrf_token %}
            <div class="d-flex gap-2 mt-3">
                <button type="submit" class="btn btn-subtle-danger">Delete</button>
                <a href="{{ cancel_url }}" class="btn btn-white">Cancel</a>
            </div>
        </form>
    </div>
</div>
```

### Template Rules

1. **Always extend `base.html`** (or `base_auth.html` for auth pages) — Every page template must start with `{% extends %}`.
2. **Use `{% include %}` for repeated UI** — Never copy-paste form fields, button rows, or empty states across templates.
3. **Pass variables with `{% include "..." with var=value %}`** — Keep partials configurable but with sensible defaults.
4. **Keep partials logic-free** — Partials render UI. Business logic stays in views.
5. **Use `{% block %}` for page-level customization** — `head`, `title`, `content`, `scripts` are the standard blocks.
6. **Name templates by action** — `asset_list.html`, `asset_create.html`, `asset_detail.html`, `asset_update.html`, `asset_delete.html`.
7. **Avoid deep template inheritance** — Two levels max: `base.html` → page template.
8. **Use Django `{% url %}` tag for all links** — Never hardcode URLs.
9. **Use `{% csrf_token %}` in every `POST` form** — Non-negotiable.
10. **Prefer `{% empty %}` in loops** — Always handle the empty state in `{% for %}` loops.

---

## Page-Specific Guidelines

### Asset List Page

- Page title: "My Assets"
- "Create Asset" button: Top-right, `btn btn-primary` with `ti ti-plus` icon, aligned with the page title using `d-flex justify-content-between align-items-center`.
- Table columns: Name, Symbol, Type (badge), Created, Actions.
- Actions column: Icon buttons (`btn-icon btn-ghost`) for View and Delete.
- Wrap table inside a `card card-lg`.

### Asset Detail Page

- Show asset info in a `card card-lg` with the definition-style layout.
- Below the asset card, show a section titled "Price Tunnels" listing tunnels for this asset.
- "Create Tunnel" button next to the section title.
- "Edit" and "Delete" buttons at the bottom of the asset card.

### Tunnel List Page

- Page title: "My Tunnels"
- Table columns: Asset (name + symbol), Lower Limit, Upper Limit, Interval, Status (badge), Actions.
- Monetary columns: `font-monospace`.
- Wrap table inside a `card card-lg`.

### Tunnel Detail Page

- `card card-lg` with definition-style layout.
- Show: Asset name, symbol, upper limit (red), lower limit (green), check interval, status badge, created date.
- "Edit" and "Delete" buttons.

### Login Page

- Centered card using auth layout (no sidebar).
- Fields: Email/Username, Password (with visibility toggle).
- "Sign In" button full-width (`w-100 btn btn-primary`).
- Link below: "Don't have an account? Register here."

### Registration Page

- Centered card using auth layout (no sidebar).
- Render all form fields individually.
- "Create Account" button full-width.
- Link below: "Already have an account? Sign in."

---

## Dos and Don'ts Summary

### Do

- Use the theme's CSS custom properties (`--ds-*`) and utility classes.
- Use `btn-primary` (green) for primary actions.
- Use `card card-lg` for primary content containers.
- Use Tabler Icons (`ti ti-*`) for UI icons.
- Use `bg-*-subtle` with `text-*-emphasis` for badges.
- Render form fields individually with error handling.
- Use `font-monospace` for monetary values.
- Create reusable partials for repeated patterns.
- Use `{% empty %}` to handle empty lists gracefully.
- Support dark mode via `data-bs-theme`.
- Use the sidebar + topbar layout for authenticated pages.

### Don't

- Don't use `btn-dark` for primary actions — use `btn-primary`.
- Don't use `{{ form.as_p }}` or `{{ form.as_table }}`.
- Don't write custom CSS when theme classes are available.
- Don't hardcode URLs — always use `{% url %}`.
- Don't copy-paste form field markup — use the `_form_field.html` partial.
- Don't leave empty list states unhandled.
- Don't use bright or saturated colors outside the defined palette.
- Don't ignore the sidebar layout for authenticated pages.
- Don't use inline SVG when Tabler Icons webfont classes are available.
- Don't add external font-awesome or other icon libraries — use Tabler Icons only.
