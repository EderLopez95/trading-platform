# CLAUDE.md

Guidance for AI coding agents (and developers) working in this repository. Keep this file accurate: when architecture, commands, or conventions change, update it in the same PR.

## 1. What this is

**Trading Platform** — a microservices system that generates trading signals from market data and delivers them to users (with Telegram notifications). It is composed of four Python backend services communicating over **gRPC (mutual TLS in prod)**, a **FastAPI HTTP gateway**, and a **React + TypeScript + Vite** web client. PostgreSQL is the shared database (one instance, per-service schemas).

```
Browser ──HTTP──> gateway-api ──gRPC──> auth-service ──> Postgres (schema: auth)
                       │
                       └────────gRPC──> signal-service ──> Postgres (schema: signals)
                                              │
                                              ├──gRPC──> auth-service
                                              └──gRPC──> market-data-service ──> MetaTrader5
```

## 2. Services overview

| Service | Path | Exposes | Port | DB schema | Talks to |
|---|---|---|---|---|---|
| gateway-api | [services/gateway-api](services/gateway-api) | FastAPI HTTP | 8080 | — | auth-service, signal-service |
| auth-service | [services/auth-service](services/auth-service) | gRPC | 5051 | `auth` | Postgres |
| signal-service | [services/signal-service](services/signal-service) | gRPC | 5052 | `signals` | auth-service, market-data-service, Postgres |
| market-data-service | [services/market-data-service](services/market-data-service) | gRPC | 5053 | — | MetaTrader5 (Windows host) |
| web | [web](web) | Nginx static (SPA) | 3002 → 80 | — | gateway-api |
| postgres | (docker-compose) | PostgreSQL 15 | 5432 | — | — |

**Important runtime note:** `market-data-service` is NOT part of [docker-compose.yml](docker-compose.yml). It depends on `MetaTrader5` (Windows-only) and runs on the **Windows host**, reached from Docker via `host.docker.internal:5053`. `docker-compose up` alone does not start it — run it manually with `python -u -m main`.

## 3. Architecture — hexagonal / clean layers

Every backend service follows the same layered structure under `app/`. Respect the dependency direction: `api → application → domain`, with `infrastructure` implementing domain ports. **Do not let `domain` import from `infrastructure` or `api`.**

| Layer | Responsibility | Example |
|---|---|---|
| `api/` | Transport adapters (gRPC servicers / FastAPI routes), request/response schemas, mappers | [services/gateway-api/app/api/routes/auth.py](services/gateway-api/app/api/routes/auth.py), [services/auth-service/app/api/auth_service.py](services/auth-service/app/api/auth_service.py) |
| `application/` | Use cases / orchestration services; depends on domain ports | [services/gateway-api/app/application/services/auth_service.py](services/gateway-api/app/application/services/auth_service.py) |
| `domain/` | Entities, ports (abstract interfaces), exceptions, business rules (strategies, indicators) | [services/auth-service/app/domain/entities/user.py](services/auth-service/app/domain/entities/user.py), [services/gateway-api/app/domain/ports/auth_port.py](services/gateway-api/app/domain/ports/auth_port.py) |
| `infrastructure/` | DB (SQLAlchemy models/repositories/mappers), gRPC clients, protobuf stubs, MT5 adapter, security | [services/auth-service/app/infrastructure/database/user_repository_impl.py](services/auth-service/app/infrastructure/database/user_repository_impl.py) |
| `config/` | `settings.py` with env loading + `validate_settings()` | [services/auth-service/app/config/settings.py](services/auth-service/app/config/settings.py) |
| `core/` | Cross-cutting: JSON logging, error handlers, middleware, registries | [services/gateway-api/app/core/errors/handlers.py](services/gateway-api/app/core/errors/handlers.py) |

`signal-service` is the richest domain: it additionally contains `domain/strategies`, `domain/indicators`, `domain/formatters`, `infrastructure/scheduler`, and `infrastructure/notifications`.

## 4. gRPC & protobuf

gRPC clients live in `app/infrastructure/grpc/clients/`. Generated stubs live in `app/infrastructure/protos/generated/` (`*_pb2.py`, `*_pb2_grpc.py`).

### `.proto` source of truth and copies
Each `.proto` is authored in its owning service, then **copied** into consumers:

- `auth.proto` — owned by auth-service; copied to gateway-api and signal-service.
- `signal.proto` — owned by signal-service; copied to gateway-api.
- `market_data.proto` — owned by market-data-service; copied to signal-service.

### RPCs defined
- **AuthService**: `Register`, `Login`, `Validate`, `UpdateTelegram`, `GetUser`, `GetUsers`
- **SignalService**: `CreateConfiguration`, `GetConfigurations`, `UpdateConfiguration`, `DeleteConfiguration`, `ToggleConfiguration`, `GetAnalysisStatus`, `ToggleAnalysis`, `GetSignals`, `StreamSignals` (server-streaming; powers the real-time WebSocket), `RefreshRegistries`, `GetStrategies`, `GetSymbols`, `GetTimeframes`
- **MarketDataService**: `GetCandles`, `GetSymbols`

### ⚠️ Regenerating stubs (required after ANY `.proto` change)
There is no codegen automation. If you edit a `.proto`, you must:
1. Update **every copy** of that proto across services.
2. Regenerate stubs in **each** service's protos directory:
   ```sh
   # run from the service's protos directory (contains the .proto + generated/)
   python -m grpc_tools.protoc -I . --python_out=generated --grpc_python_out=generated <name>.proto
   ```
Forgetting a copy or a regen is the most common source of runtime gRPC errors here.

## 5. Web frontend (React 19 + TypeScript + Vite)

Feature-module architecture under `web/src/`:

```
src/
  app/         providers (QueryProvider, AuthProvider), router
  modules/     auth, configurations, settings, signals  (feature slices)
  shared/      components (ui/), layouts, services (apiClient)
  styles/      _variables.scss, global.scss
```

Each module slice follows: `api/` (raw axios calls) → `hooks/` (react-query wrappers) → `components/` (UI), with `services/` (zod schemas) and `types/`. Example: [web/src/modules/configurations](web/src/modules/configurations).

Key facts:
- **Data fetching:** `@tanstack/react-query`. Provider in [web/src/app/providers/QueryProvider.tsx](web/src/app/providers/QueryProvider.tsx).
- **Real-time signals:** [web/src/modules/signals/hooks/useSignalsSocket.ts](web/src/modules/signals/hooks/useSignalsSocket.ts) opens a WebSocket to the gateway at `ws(s)://<API_URL>/ws/signals?token=<jwt>`; on each message it calls `invalidateQueries(["signals"])` so the table refetches. The gateway bridges this to the `StreamSignals` gRPC server-stream (see §4).
- **HTTP client:** single axios instance in [web/src/shared/services/apiClient.ts](web/src/shared/services/apiClient.ts). `baseURL = VITE_API_URL`; request interceptor injects `Authorization: Bearer <token>` (from `localStorage`) and an `X-Request-Id` uuid; response interceptor clears token and redirects to `/login` on 401 (except auth endpoints).
- **Routing:** [web/src/app/router/router.tsx](web/src/app/router/router.tsx), mounted via `RouterProvider` in [web/src/App.tsx](web/src/App.tsx).
- **Forms:** `react-hook-form` + `zod` via `@hookform/resolvers`. Schema per feature under `services/`.
- **Styling:** SCSS modules (`*.module.scss`). Shared tokens/mixins in [web/src/styles/_variables.scss](web/src/styles/_variables.scss). Import with `@use '.../variables' as *;`.
- **Path alias:** `@` → `src` (configured in [web/vite.config.ts](web/vite.config.ts) and [web/tsconfig.app.json](web/tsconfig.app.json)).

## 6. Commands

### Full stack (Docker)
```sh
cd certs && ./generate-certs.sh   # or ./generate-certs.ps1 on PowerShell — run once / on rotation
cd ..
docker-compose down -v
docker-compose up --build
```
Start `market-data-service` separately on the Windows host (see §2).

### Backend service (local dev)
```sh
python -m venv .venv
.venv/Scripts/activate                     # Windows
python -m pip install -r requirements-dev.txt
# configure .env.local
python -m main                             # market-data-service: python -u -m main
```
`auth-service` and `signal-service` run Alembic migrations automatically via `entrypoint.sh` in Docker. Locally: `alembic upgrade head`.

### Web
```sh
cd web
npm install
npm run dev        # Vite dev server
npm run build      # tsc -b && vite build
npm run lint       # eslint
```

### Alembic (auth-service, signal-service)
```sh
alembic revision --autogenerate -m "message"   # verify the file; add schema= if needed
alembic upgrade head
```

## 7. Configuration & environment

Settings are read in `app/config/settings.py`. When `ENV=local`, `.env.local` is loaded; otherwise env comes from the process (docker-compose sets `ENV=prod`). `validate_settings()` fails fast on missing required vars.

Required env per service:
- **auth-service:** `ENV`, `DATABASE_URL`, `JWT_SECRET`, `ENCRYPTION_KEY` (+ `GRPC_SSL_CERT`/`GRPC_SSL_KEY` for TLS)
- **gateway-api:** `ENV`, `AUTH_SERVICE_HOST`, `SIGNAL_SERVICE_HOST`, `JWT_SECRET`; `TRUSTED_CA_CERT` required when `GATEWAY_SERVICE_SECURE=true`
- **signal-service:** `ENV`, `DATABASE_URL`, `MARKET_DATA_SERVICE_HOST`, `AUTH_SERVICE_HOST`; `TRUSTED_CA_CERT` required when `SIGNAL_SERVICE_SECURE=true`
- **market-data-service:** `ENV`
- **web:** `VITE_API_URL` (dev/local → `http://localhost:8080`)

`ENCRYPTION_KEY` is a Fernet key used by auth-service to encrypt `telegram_token` / `telegram_chat_id` at rest:
```sh
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 8. Security & TLS

- **mTLS between services (prod):** a single root CA signs per-service certs. Generate with [certs/generate-certs.sh](certs/generate-certs.sh) / [certs/generate-certs.ps1](certs/generate-certs.ps1). Services mount `./certs` read-only and trust `root-ca.pem`. Secure channels are gated by `*_SECURE` env flags in each service's settings.
- **Auth:** JWT (`JWT_SECRET`). Gateway validates tokens via auth-service `Validate`; protected routes use the `get_current_user` dependency.
- **Secrets at rest:** Telegram credentials are Fernet-encrypted in `auth.users`. Never log or return decrypted secrets to the browser without an explicit reason — prefer masking.
- **CORS:** gateway currently allows only `http://localhost:3002` (see [services/gateway-api/main.py](services/gateway-api/main.py)). Update deliberately.
- The committed `JWT_SECRET` / `ENCRYPTION_KEY` in docker-compose are **dev-only**; do not reuse in real deployments.

## 9. Database

Single PostgreSQL 15 instance, `trading_platform` database, per-service schemas:
- `auth.users` — credentials + encrypted Telegram fields (auth-service migrations)
- `signals.configurations`, `signals.signals`, `signals.user_settings` (signal-service migrations)

Schemas/tables are created **only** via Alembic (do not hand-run the SQL in the README; it is reference-only). Migrations live in each service's `migrations/versions/`.

## 10. Conventions

**Python**
- snake_case for modules/functions, PascalCase for classes.
- Domain-specific custom exceptions in `domain/exceptions*`; map them to gRPC status codes (in servicers) or FastAPI handlers (gateway `core/errors/handlers.py`).
- JSON structured logging via `python-json-logger`; call `setup_logging()` at startup. Gateway attaches a request-id through `logging_middleware`.
- Constructor injection through domain ports (abstract base classes); concrete adapters are wired in the api layer (route/servicer factory functions like `get_service()`).
- Repositories return domain entities via mappers; keep SQLAlchemy models out of `application`/`domain`.

**TypeScript / React**
- Function components only; one component per file, default export.
- API call → react-query hook → component. Keep axios calls in `api/`, never in components.
- Validation with zod schemas colocated in `services/`; infer form types from the schema.
- Use the `@/` alias for absolute imports; SCSS modules for styling.

## 11. Testing

There are **no first-party tests** in the repo yet (no `test_*.py`, `*.test.ts(x)`, `*.spec.ts(x)`, and no pytest/vitest/jest config). If you add tests, also add the runner config and document the command here. Until then, validate changes by:
- Backend: `python -m main` for the affected service + exercise via gateway; check `docker compose logs -f <service>`.
- Web: `npm run build` (type-check) and `npm run lint`.

## 12. Gotchas (read before editing)

1. **Proto edits need multi-copy sync + per-service regen** (see §4). This is the #1 breakage source.
2. **market-data-service is external** to compose and Windows/MT5-bound; `docker-compose up` won't start it.
3. **Certs must exist** before `docker-compose up` when `*_SECURE=true`; regenerate on rotation.
4. **Migrations run on container start** for auth/signal services; the DB must be reachable or the entrypoint retries in a loop.
5. **Gateway holds long-lived gRPC clients** (module-level `SignalClient()` in auth routes) — be careful with import-time side effects.
6. Keep the layer dependency direction intact; putting infrastructure imports in `domain` breaks the architecture.
