# CoCoIRU — Copilot / AI agent instructions

Short, actionable guidance to help an AI coding agent be productive in this repo.

1) Big picture
- Backend: FastAPI app at `app/main.py`. API routes are mounted under `/api/v1` via `app/api/v1/api.py` and modular routers in `app/api/v1/endpoints/`.
- DB: SQLAlchemy + SQLite. Connection and `get_db()` are in `db/session.py`. The production DB file is `database.db` at the repo root; tests use an in-memory SQLite engine (`tests/conftest.py`).
- Frontend: Svelte app lives in `Svelte/`. Frontend code imports from `$lib` (`Svelte/src/lib`). Feature modules (domain-first) are under `Svelte/src/lib/features/` (example: `request/requestItems.ts`).

2) How to run & test (quick commands)
- Install Python deps: `pip install -r requirements.txt` (from repo root).
- Start backend (development): `uvicorn app.main:app --reload --port 8000` (or run the Svelte `api` script described below).
- Start frontend (development):
  - `cd Svelte` then `npm start` to run the Svelte dev server.
  - `cd Svelte` then `npm run api` to start the API (project README documents these exact scripts).
- Run tests: from repo root `pytest -q`. To run a single test: `pytest tests/api/v1/test_items_api.py::test_create_item -q`.

3) Important repo-specific conventions and patterns
- Router-first API: Each resource has a router file in `app/api/v1/endpoints/` (e.g. `items.py`) that calls `crud` and `schemas` in `db/`.
- CRUD layer: Business logic and DB access live in `db/crud.py` (and resource-specific `crud_*` files). Prefer using `crud` functions for DB changes rather than writing raw session code in endpoints.
- Schemas and models: Pydantic schemas are in `db/schemas.py`, ORM models in `db/models.py`.
- DB session handling: Use the `get_db` dependency from `db/session.py`. Tests override `get_db` in `tests/conftest.py` to inject an in-memory session — follow the same pattern for testable endpoints.
- SQLite foreign keys: `db/session.py` enables `PRAGMA foreign_keys=ON` on connect; `db/create_database.py` also enables the pragma when creating DB manually.
- Frontend feature layout: Domain features live under `Svelte/src/lib/features/` with `components/` and a `*.ts` logic file (example: `request/requestItems.ts` uses a Svelte store and defines a `RequestItem` type; `id` is required).

4) Where to add code
- New API endpoints: create `app/api/v1/endpoints/<resource>.py`, implement router and operations, then add `api_router.include_router(...)` inside `app/api/v1/api.py`.
- New DB models/schemas: add to `db/models.py` and `db/schemas.py` respectively, then expose CRUD helpers in `db/crud.py` or a new `db/crud_<resource>.py`.
- Frontend features: add a directory under `Svelte/src/lib/features/` and export from `Svelte/src/lib/index.ts` if needed.

5) Testing & patterns to follow when changing code
- Tests use an in-memory SQLite DB and transaction rollback to keep tests isolated (`tests/conftest.py`). Use dependency override for `get_db` when writing integration tests.
- Use `fastapi.testclient.TestClient` for endpoint tests. See `tests/api/v1/test_items_api.py` for examples of POST/GET/PUT/DELETE flows and DB assertions.

6) Integration points and gotchas
- CORS: `app/main.py` currently allows all origins — acceptable for local/dev but be explicit in production.
- DB path: The app defaults to `sqlite:///./database.db`. Be aware of filesystem location when running in containers or CI.
- Tests rely on `Base.metadata.create_all(bind=engine)` to build schema in-memory; migrations are not present — if you add models, update tests to ensure creation.

7) Helpful examples (copy/paste snippets you can reuse)
- Include a new router in `app/api/v1/api.py`:
  `api_router.include_router(myrouter.router, prefix="/myresource", tags=["MyResource"])`
- Use `get_db` in an endpoint (pattern):
  `def api_create(..., db: Session = Depends(get_db)):`
- Frontend store example (from `requestItems.ts`): `export const requestItems = writable(initialRequestItems);` — store items have `id`, `text`, `value`.

8) If you are unsure
- Prefer reading `app/main.py`, `app/api/v1/api.py`, `db/session.py`, `tests/conftest.py`, and `Svelte/src/lib/features/*` first.
- Ask the maintainer whether the intended runtime is local only or a container/CI pipeline (DB path and start scripts may need adjustment).

---
If you want, I can (a) add a short section with example `uvicorn` and `npm` scripts to `package.json`/README, (b) generate a minimal endpoint template file, or (c) adapt these instructions into Japanese/English variants. Which would you like next?
