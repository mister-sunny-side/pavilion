# Pavilion

A Rust [Dioxus](https://dioxuslabs.com/) blog with Playwright end-to-end tests and GitHub Actions CI.

## Stack

- **Dioxus 0.7.9** (fullstack + router)
- Build-time markdown posts via vendored DioxusLabs `include_mdbook` (`mdbook-gen` + `use-mdbook`)
- **Playwright** via `pytest-playwright` for e2e tests
- **uv** + **ruff** for Python tooling
- **GitHub Actions** for format checks, build, and e2e

## Routes

| Path | Page |
|------|------|
| `/` | Home |
| `/dialogue` | Post list |
| `/dialogue/<slug>` | Markdown post (from `blog-posts/`) |
| `/matter` | Matter |
| `/random` | Random |

## Project layout

```
pavilion/
├─ blog-posts/       # mdBook source (SUMMARY.md + .md posts)
├─ vendor/           # Vendored include_mdbook packages
├─ assets/           # Static assets (favicon, CSS, images)
├─ src/
│  ├─ main.rs        # Entrypoint and route definitions
│  ├─ blog_book.rs   # CodeBlock + generated BookRoute include
│  ├─ components/    # Shared UI (Hero, Echo)
│  └─ views/         # Home, Dialogue, Matter, Random, Navbar
├─ tests/            # Playwright e2e tests
├─ docker/           # Local + artifact Docker/Compose serving
├─ .github/workflows # CI
├─ build.rs          # mdbook-gen codegen
├─ Cargo.toml
├─ Dioxus.toml
└─ pyproject.toml
```

## Authoring dialogue posts

1. Add a markdown file under `blog-posts/src/` (for example `my-post.md`).
2. List it in `blog-posts/src/SUMMARY.md`:

```markdown
# Summary

- [Welcome](welcome.md)
- [My Post](my-post.md)
```

3. Rebuild / let `dx serve` pick up the change. The post appears on `/dialogue` and at `/dialogue/my-post`.

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
