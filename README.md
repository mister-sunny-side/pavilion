# Pavilion

A Rust [Dioxus](https://dioxuslabs.com/) blog with Playwright end-to-end tests and GitHub Actions CI.

## Stack

- **Dioxus 0.7.9** (fullstack + router) — Jumpstart blog scaffold (`/`, `/blog/:id`)
- **Playwright** via `pytest-playwright` for e2e tests
- **uv** + **ruff** for Python tooling
- **GitHub Actions** for format checks, build, and e2e

## Project layout

```
pavilion/
├─ assets/           # Static assets (favicon, CSS, images)
├─ src/
│  ├─ main.rs        # Entrypoint and route definitions
│  ├─ components/    # Shared UI (Hero, Echo)
│  └─ views/         # Home, Blog, Navbar layout
├─ tests/            # Playwright e2e tests
├─ .github/workflows # CI
├─ Cargo.toml
├─ Dioxus.toml
└─ pyproject.toml
```

## Prerequisites

- Rust stable + `wasm32-unknown-unknown` target
- [Dioxus CLI](https://dioxuslabs.com/learn/0.7/getting_started): `curl -LsSf https://dioxus.dev/install.sh | sh`
- [uv](https://docs.astral.sh/uv/): `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Develop

```bash
dx serve --platform web
```

Automatic Tailwind is enabled via `tailwind.css` next to `Cargo.toml`.

## Format / lint

```bash
uv sync --extra dev
uv run pre-commit install

# Manual
cargo fmt --all
uv run ruff format .
uv run ruff check .
```

## E2E tests

```bash
uv sync --extra dev
uv run playwright install

# Terminal 1
dx serve --platform web --port 8080

# Terminal 2
uv run pytest tests/ -v
```

## CI

On pull requests and pushes to `main`/`master`, GitHub Actions:

1. Checks Rust (`cargo fmt`) and Python (`ruff`) formatting
2. Builds the Dioxus web app
3. Starts `dx serve` and runs Playwright e2e tests
