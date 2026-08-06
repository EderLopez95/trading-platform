---
name: regenerate-grpc-stubs
description: 'Sync and regenerate gRPC/protobuf stubs across the trading-platform services after editing a .proto file. Use when: adding/removing/changing an RPC, message, or field in auth.proto, signal.proto, or market_data.proto; fixing runtime gRPC errors like "method not implemented", mismatched field numbers, or ModuleNotFoundError on *_pb2 imports; or when a proto copy is out of sync between services. Handles the owner→consumer copy fan-out, per-service protoc regeneration, and the required import-path fix in generated *_pb2_grpc.py files.'
argument-hint: '<proto> = auth | signal | market_data (optional; omit to sync all)'
---

# Regenerate gRPC / Protobuf Stubs

This repo has **no codegen automation** and each `.proto` is duplicated across the
services that use it. Editing a `.proto` without syncing every copy and regenerating
every service's stubs is the **#1 source of runtime gRPC failures** here (see
[CLAUDE.md](../../../CLAUDE.md) §4 and §12).

## When to Use

- You changed an RPC, message, enum, or field in a `.proto`.
- You see gRPC errors: `UNIMPLEMENTED`, wrong field values, `AttributeError` on a
  generated class, or `ModuleNotFoundError: No module named '<name>_pb2'`.
- A proto copy drifted between services and needs re-syncing.

## Proto ownership & fan-out

Each proto is **authored in its owning service** and **copied verbatim** into consumers.
The owner is the source of truth — always edit the owner copy first.

| Proto | Owner (edit here) | Copied into (consumers) |
|---|---|---|
| `auth.proto` | auth-service | gateway-api, signal-service |
| `signal.proto` | signal-service | gateway-api |
| `market_data.proto` | market-data-service | signal-service |

Every service stores its proto at:
```
services/<service>/app/infrastructure/protos/<name>.proto
```
and its stubs at:
```
services/<service>/app/infrastructure/protos/generated/<name>_pb2.py
services/<service>/app/infrastructure/protos/generated/<name>_pb2_grpc.py
```

## Procedure

### 1. Edit the owner proto only
Make your change in the **owner** service's `.proto` (table above).

### 2. Run the sync script (does copy + regen + import fix)
```powershell
# From the repo root, with a Python env that has grpc_tools installed:
./.github/skills/regenerate-grpc-stubs/scripts/sync_protos.ps1 -Proto auth
# omit -Proto to sync all three protos
./.github/skills/regenerate-grpc-stubs/scripts/sync_protos.ps1
```
The [sync_protos.ps1](./scripts/sync_protos.ps1) script:
1. Copies the owner `.proto` to every consumer path.
2. Runs `python -m grpc_tools.protoc` into each service's `generated/` folder.
3. **Fixes the import** in each `*_pb2_grpc.py` (see the gotcha below).

### 3. Manual fallback (if you can't run the script)
For **each** service that has the proto (owner + consumers), from that service's
`app/infrastructure/protos` directory:
```powershell
python -m grpc_tools.protoc -I . --python_out=generated --grpc_python_out=generated <name>.proto
```
Then open the regenerated `generated/<name>_pb2_grpc.py` and change the top import
from the tool's default:
```python
import <name>_pb2 as <name>__pb2
```
to the package-absolute path this project requires:
```python
from app.infrastructure.protos.generated import <name>_pb2 as <name>__pb2
```

### 4. Validate
- Confirm all copies are byte-identical: the consumer `.proto` matches the owner.
- Confirm each `generated/<name>_pb2_grpc.py` uses the
  `from app.infrastructure.protos.generated import ...` import.
- Smoke-test the affected services (`python -m main`, or `python -u -m main` for
  market-data-service) and exercise the RPC through gateway-api. Check logs:
  `docker compose logs -f <service>`.

## ⚠️ Critical gotcha: the import path

`grpc_tools.protoc` emits a bare `import <name>_pb2` at the top of the generated
`*_pb2_grpc.py`. That does **not** resolve at runtime because the services import
stubs via the package path `app.infrastructure.protos.generated`. If you skip the
import fix you'll get `ModuleNotFoundError` when the service starts. The script
handles this automatically; the manual path requires editing it by hand.

## Checklist (don't skip a copy)

- [ ] Edited the **owner** proto only.
- [ ] Copied to **every** consumer (see fan-out table).
- [ ] Regenerated stubs in **every** service that has the proto.
- [ ] Fixed the `*_pb2_grpc.py` import in every regenerated file.
- [ ] Smoke-tested the affected services end-to-end.
