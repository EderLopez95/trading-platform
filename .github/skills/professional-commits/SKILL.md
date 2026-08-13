---
name: professional-commits
description: 'Author professional git commit messages for the trading-platform following Conventional Commits, enriched with a scope (the affected module/feature) and a task identifier (project/ticket ID). Use when: the user asks to commit, stage-and-commit, write a commit message, amend or reword a commit, or split staged work into logical commits; or when finishing a change and preparing it for git history. Handles type/scope selection from the actual diff, subject/body/footer formatting, breaking-change markers, and task-ID trailers.'
argument-hint: '<task-id> (optional, e.g. TP-123) — omit to infer from branch name or ask'
---

# Professional Commit Messages

Produce commits that are consistent, searchable, and traceable back to a task.
Format = **Conventional Commits** + **scope (module/feature)** + **task ID (project/ticket)**.

## When to Use

- The user says "commit", "commitea", "haz un commit", "write a commit message",
  "stage and commit", "amend", "reword", or "split this into commits".
- You just finished a change and are preparing it for git history.
- The user wants a commit body/footer or help referencing a ticket.

## When NOT to Use

- Pushing, force-pushing, rebasing onto shared branches, or anything that rewrites
  published history — ask the user first (see safety note at the end).
- Merge-conflict resolution or branch management (out of scope).

## Message Format

```
<type>(<scope>): <subject>   [<task-id>]

<body>

<footer>
```

Rendered example:
```
feat(settings): sync telegram cache after save   [TP-142]

The settings page wrote directly through the API and left the
react-query cache stale, so the form showed empty fields until a
manual refresh. Update the cache on mutation success instead.

Refs: TP-142
```

### Header (required, <= 72 chars)
- **type**: one of `feat`, `fix`, `perf`, `refactor`, `docs`, `style`, `test`,
  `build`, `ci`, `chore`, `revert`.
- **scope**: the affected module/feature — see the scope table below. Always include
  a scope in this repo (it is a multi-service monorepo, so an unscoped commit is
  ambiguous).
- **subject**: imperative mood, lowercase, no trailing period
  ("add", not "added"/"adds"). Describe *what changes*, not *how*.
- **task-id**: append the ticket ID at the end of the header in brackets. If there is
  genuinely no task, omit the brackets (do **not** invent an ID).

### Body (optional, wrap at ~72 cols)
- Explain the **why** and any context the diff does not make obvious.
- Use bullet points for multiple independent changes.
- Omit entirely for trivial one-line changes (e.g. `chore(web): bump vite to 8.0.16 [TP-9]`).

### Footer (optional)
- `Refs: <task-id>` (or `Closes: <task-id>` when the commit fully resolves the ticket).
- `BREAKING CHANGE: <description>` for incompatible changes (also add `!` after the
  scope in the header, e.g. `feat(auth)!: ...`).
- `Co-authored-by:` when applicable.

## Scope vocabulary (this repo)

Pick the scope from the part of the tree you actually touched:

| Scope | Area |
|---|---|
| `auth` | auth-service or auth feature (backend or web module) |
| `signal` | signal-service or signals feature |
| `market-data` | market-data-service / MT5 adapter |
| `gateway` | gateway-api HTTP layer |
| `web` | web frontend (cross-cutting: build, router, providers) |
| `settings` | web settings / telegram module |
| `configurations` | web configurations feature |
| `signals` | web signals feature |
| `proto` | `.proto` files + regenerated stubs (see regenerate-grpc-stubs) |
| `db` | Alembic migrations / schema |
| `certs` | TLS / mTLS certs & scripts |
| `infra` | docker-compose, Dockerfiles, nginx, entrypoints |
| `deps` | dependency bumps |

If a commit spans multiple scopes, that is usually a sign it should be **split** into
several commits (see Procedure step 3).

## Procedure

1. **Inspect what is staged.** Run `git status` and `git diff --staged`. If nothing is
   staged, look at `git diff` and decide (with the user) what to stage — never
   `git add -A` blindly; stage the files relevant to one logical change.
2. **Derive the task ID.**
   - Use the argument if provided.
   - Otherwise try to parse it from the branch name (e.g. `feature/TP-142-telegram`
     -> `TP-142`).
   - If still unknown, ask the user once; if they have none, proceed without the
     bracket + `Refs:` trailer rather than fabricating one.
3. **Group into logical commits.** One commit = one coherent change. If the staged diff
   mixes unrelated concerns (e.g. a bug fix + an infra tweak), propose splitting and
   stage each group separately.
4. **Choose type + scope** from the diff, not the user's phrasing.
5. **Write the message** using the format above. Prefer `git commit -F <file>` or a
   here-doc so the body/footer keep their line breaks (a single `-m` collapses them).
6. **Show the message and confirm** before committing when the change is non-trivial.

## Type selection cheatsheet

| If the change... | type |
|---|---|
| adds user-visible behavior | `feat` |
| fixes a bug | `fix` |
| improves speed without changing behavior | `perf` |
| restructures code, no behavior change | `refactor` |
| touches only docs/comments | `docs` |
| formatting/whitespace only | `style` |
| adds/updates tests | `test` |
| build system, Docker, bundler | `build` |
| CI pipelines | `ci` |
| tooling/deps/misc, no src behavior | `chore` |
| reverts a prior commit | `revert` |

## Examples

```
fix(web): navigate to /login via router instead of full reload   [TP-143]

Replace window.location.href with router.navigate and clear the
react-query cache on 401 so a session timeout no longer wipes SPA
state or triggers a full page reload.

Refs: TP-143
```

```
build(infra): inject API_URL at container start   [TP-140]

Serve web/public/config.js and regenerate it from $API_URL via the
nginx entrypoint hook so one image targets multiple environments
without rebuilding.

Refs: TP-140
```

```
feat(proto)!: add UpdateTelegram RPC to AuthService   [TP-151]

BREAKING CHANGE: regenerate stubs in auth-service, gateway-api and
signal-service (see regenerate-grpc-stubs skill).
Refs: TP-151
```

## Safety

- Never run `git push`, `git push --force`, or rewrite published history without
  explicit user confirmation.
- `git commit --amend` / reword is only safe on **local, unpushed** commits — confirm
  the commit has not been pushed before amending.
- Do not use `--no-verify`; let hooks run.
