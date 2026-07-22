# Pavilion

A small, simple, fast blogging site built with [Dioxus](https://dioxuslabs.com/).

Pavilion aims to stay lightweight: write posts, publish them, and keep the surface area small. The current app is a Jumpstart fullstack scaffold (`/`, `/blog/:id`) with Playwright e2e coverage and GitHub Actions CI.

## Roadmap

- **Markdown posts** — render simple markdown files into clean blog posts
- **Basic comments** — add lightweight commenting once posts are markdown-backed

## Stack

- **Dioxus 0.7.9** (fullstack + router)
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
├─ docker/           # Local + artifact Docker/Compose serving
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

On pushes to `main`/`master` only (after lint + e2e pass), a **publish** job builds a release web bundle and uploads it as the `pavilion-web` Actions artifact (`server` binary + `public/` static/WASM assets). Download it from the workflow run’s Artifacts section.

## Docker

Two serving paths under `docker/`:

**Local (build from source)**

```bash
docker compose -f docker/compose.local.yml up --build
```

**Published CI artifact**

```bash
# After a successful master publish job:
gh run download <run-id> -n pavilion-web -D docker/artifact
docker compose -f docker/compose.artifact.yml up --build
```

Both expose the site on http://localhost:8080 (`IP`/`PORT` / `DIOXUS_PUBLIC_PATH` are set for the release `server` binary).
