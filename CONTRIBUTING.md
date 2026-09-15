# Contributing to Xiuqo Agent

Thanks for taking the time! This guide covers dev setup, architecture, and how to get a PR merged.

Xiuqo is a CLI-first fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent) (MIT).
It keeps the agent core, the full CLI tool suite, the messaging gateway (WeChat included), and the
skill/memory systems — without the desktop app or the Ink TUI.

---

## Before You Start

1. **Search existing issues** before opening or coding anything new.
2. For bugs: reproduce with `xiuqo doctor` output attached.
3. For features: open an issue first and wait for a 👍 before investing heavily.

## Development Setup

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Git** | |
| **Python 3.11–3.13** | uv installs it if missing |
| **uv** | https://docs.astral.sh/uv/ |

### Install from source

```bash
git clone https://github.com/xux123171-rgb/xiuqo.git && cd xiuqo
uv sync --extra dev          # or --locked for the exact lockfile set
.venv/bin/xiuqo setup        # configure a provider + model
```

Windows: the venv lives at `.venv\Scripts\`.

### Run the tests

```bash
.venv/bin/python -m pytest tests/agent/ tests/tools/ tests/xiuqo_cli/ -q \
    --basetemp=/tmp/xiuqo-pt -p no:cacheprovider
```

Notes:
- Keep test temp dirs outside your real home (`--basetemp`).
- A handful of tests are POSIX-only (`fcntl`, `AF_UNIX`, `os.geteuid`) and fail on
  stock Windows by design — they are skipped/expected upstream.
- Set `XIUQO_HOME` to a scratch directory when running anything that touches config,
  so tests never read your real `~/.xiuqo`.

## Project Structure

```
xiuqo_cli/     CLI: entry, chat loop, setup/doctor/gateway/skills/... commands
agent/         Agent core: conversation loop, context compression, provider adapters
tools/         Tool implementations (terminal, files, browser, web, mcp, memory, ...)
gateway/       Messaging gateway (WeChat/iLink, api_server, webhook, ...)
plugins/       Plugin trees (platform adapters, model providers, image gen, ...)
skills/        Bundled skills (the learning system's seed knowledge)
optional-skills/  Community/niche skills not loaded by default
cron/          Scheduler internals
tests/         Pytest suite (mirrors the source layout)
scripts/       Installers, build helpers, banner/art generators
docs live in:  README.md, README.zh-CN.md, AGENTS.md, SECURITY.md
```

`AGENTS.md` (repo root) documents the architecture for both humans and AI
assistants — read it before larger refactors.

## Code Style

- Python ≥3.11, formatted per repo lint config (`ruff` via the dev extra).
- Exact-pinned dependencies in `pyproject.toml` — never introduce version ranges
  without a written justification (supply-chain posture inherited from upstream).
- Provider-specific deps belong in an optional extra + `tools/lazy_deps.py`,
  not in core `dependencies`.
- Keep diff surfaces small; one logical change per PR.

## Adding a Tool

1. Implement under `tools/`, register in the toolset map used by `xiuqo_cli/tools_config.py`.
2. Add tests under `tests/tools/`.
3. Update the tool listing in `README.md` if it's user-facing.

## Adding a Skill

Skills are markdown procedures in `skills/<category>/<name>/SKILL.md` with YAML
frontmatter (`name`, `description`, …). Put niche/community skills in
`optional-skills/`. A skill should encode a *reusable procedure*, not a one-off log.

## Security

Never commit real credentials, internal URLs, or user data. Test fixtures use
obviously-fake keys (`ghp_ab...cdef`, `AKIAIO...MPLE`) — keep it that way.
Report vulnerabilities privately via
[GitHub Security Advisories](https://github.com/xux123171-rgb/xiuqo/security/advisories/new)
(see [SECURITY.md](SECURITY.md)).

## Pull Request Process

1. Branch from `main`; keep history rebaseable.
2. PR body fills the template: what, why, how verified.
3. Green CI on the six shipped workflows (tests, lint, lockfile, supply-chain).
4. Maintainer merges; squash preferred.

## License

By contributing you agree your contributions are licensed under the MIT license,
same as the project (which includes the upstream Hermes Agent copyright notice).
