# Changelog

All notable changes to Xiuqo Agent are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-09-15

Initial public release. Xiuqo is a deep rebrand of
[Hermes Agent](https://github.com/NousResearch/hermes-agent) v0.21.2
(upstream commit `b9271bcb`), MIT-licensed with upstream copyright retained.

### Added
- `xiuqo_cli/main_tui_launch.py`: graceful degradation — `--tui` now falls back
  to the classic interface when Ink assets are not shipped, instead of crashing.
- `scripts/build_banner.py`, `scripts/patrick_v3.py`: reproducible brand art
  generators (pixel wordmark + mascot) for README and terminal banners.
- China-network install hints in both READMEs (ghproxy.net mirror, Aliyun PyPI index).

### Changed
- Global rename `hermes` → `xiuqo` across 5100+ files: package modules, console
  scripts (`xiuqo`, `xiuqo-agent`, `xiuqo-acp`), environment variables
  (`XIUQO_HOME`, `XIUQO_*`), config home (`~/.xiuqo`), state DB, profiles,
  skills, docs and user-facing strings. Upstream Nous model names and doc URLs
  are intentionally preserved.
- Identity texts (SOUL/prompt builder/banners) now describe Xiuqo as an
  open-source terminal agent; update/release channels point at
  `xux123171-rgb/xiuqo`.
- Security contact moved to GitHub Security Advisories only.

### Removed
- Electron desktop app, bootstrap installer, docs website, contributors dataset,
  JS test harness (`tests-js`), upstream-inherited CI workflows and Dependabot
  config (29 workflows dropped; core test/lint/lockfile/supply-chain kept).
- Ink TUI package (`ui-tui/`, 484 files) — the Python bridge (`tui_gateway/`)
  remains for the web dashboard backend.

### Known limitations
- Version is pinned to the Hermes Agent v0.21.2 baseline; upstream changes after
  `b9271bcb` are not merged.
- WeChat gateway rides Tencent's private iLink Bot API and may break without notice.
- `xiuqo desktop` / `dashboard` commands referencing removed UIs report
  "source not found"; this is expected for this build.
