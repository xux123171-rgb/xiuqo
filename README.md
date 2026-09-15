<p align="center">
  <img src="assets/banner.png" alt="Xiuqo Agent" width="100%">
</p>

# Xiuqo Agent ☤

<p align="center">
  <a href="https://github.com/xux123171-rgb/xiuqo/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11--3.13-blue?style=for-the-badge" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Runtime-pure%20Python%20%E2%80%94%20no%20Node-FFD700?style=for-the-badge" alt="pure python"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/Lang-中文-red?style=for-the-badge" alt="中文"></a>
</p>

**A self-improving AI agent that lives in your terminal.** It learns from what it does — writing reusable skills after hard tasks, keeping memory across sessions, searching its own past conversations. It also just *works*: shell, files, a Python code kernel, real browser automation, MCP servers, parallel subagents, scheduled jobs. Any provider you want — OpenRouter, OpenAI, Anthropic, DeepSeek, Zhipu, SenseNova, your own endpoint — and `xiuqo model` switches between them mid-conversation.

It's not glued to your laptop. Run it on a $5 VPS and message it from WeChat while it works. The gateway speaks to personal WeChat through the iLink bot API (QR login built in), and Telegram/Discord/Slack adapters are still in the tree if you want them.

**Why this fork exists:** I use Hermes Agent daily and wanted the machine to feel like my own — so I renamed 5,000+ files, gutted what I never open (the Electron desktop app, the Ink TUI, the docs site), kept everything I actually use, and pointed the updater at my repo. CLI-first, pure Python, no Node runtime anywhere in the install path. If you want the full Hermes experience, [upstream](https://github.com/NousResearch/hermes-agent) is the place — this is the trimmed, opinionated version.

<table>
<tr><td><b>A real terminal interface</b></td><td>Multiline editing, slash-command autocomplete, streaming tool output, interrupt-and-redirect, themable skins — in pure Python (prompt_toolkit + rich). Zero browser-electrons, zero Node.</td></tr>
<tr><td><b>A closed learning loop</b></td><td>Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills improve themselves during use. FTS5 search over your past sessions. Compatible with the <a href="https://agentskills.io">agentskills.io</a> standard.</td></tr>
<tr><td><b>Chat from WeChat</b></td><td><code>xiuqo gateway</code> bridges a personal WeChat account to the same agent — QR scan, long-poll, media included. Same session memory as the terminal.</td></tr>
<tr><td><b>Tools that matter</b></td><td>Terminal with background PTYs, file ops + <code>apply_patch</code>, Python RPC code execution, CDP browser automation, vision, TTS/STT, MCP client, password-vault autofill, todo/goals.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Cron scheduler for nightly audits and weekly reports, in natural language, running unattended.</td></tr>
<tr><td><b>Runs anywhere</b></td><td>Linux, macOS, Windows (native, no WSL needed), WSL2, Termux on Android. Local / SSH / Docker / Modal / Daytona / Vercel sandbox terminal backends.</td></tr>
</table>

---

## Quick Install

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://raw.githubusercontent.com/xux123171-rgb/xiuqo/main/scripts/install.sh | bash
```

### Windows (native, PowerShell)

> Native Windows runs Xiuqo without WSL — CLI, gateway, and tools all work natively. If you'd rather use WSL2, the Linux command above works there too.

```powershell
iex (irm https://raw.githubusercontent.com/xux123171-rgb/xiuqo/main/scripts/install.ps1)
```

The installer handles everything: uv, Python 3.11+, and a portable Git Bash (MinGit) if you don't already have Git. Nothing touches your system Python; the whole install lives under `%LOCALAPPDATA%\xiuqo` (Windows) or `~/.xiuqo` (everything else).

> **China network:** GitHub raw can stall on the mainland. Clone via `https://ghproxy.net/https://github.com/xux123171-rgb/xiuqo.git` and add `--default-index https://mirrors.aliyun.com/pypi/simple` to `uv sync`. Both are wired into the installers as fallbacks.

After installation:

```bash
source ~/.bashrc     # or: source ~/.zshrc / restart PowerShell
xiuqo setup          # pick provider + model, paste API keys
xiuqo                # start chatting!
```

<details>
<summary>Manual install (throwaway clones, CI, offline boxes)</summary>

```bash
git clone https://github.com/xux123171-rgb/xiuqo.git && cd xiuqo
uv sync --locked
.venv/bin/xiuqo setup        # Windows: .venv\Scripts\xiuqo setup
```

Tip for sandboxed/agent hosts: keep the venv **outside** the source tree (`uv venv /path/outside --python 3.11 && uv pip install -e .`) so a relative-path cleanup run by the agent can't wipe the runtime it's standing in.
</details>

---

## Getting Started

```bash
xiuqo                 # Interactive chat — start a conversation
xiuqo model           # Choose LLM provider + model
xiuqo tools           # Configure which tools are enabled
xiuqo config set      # Set individual config values
xiuqo gateway         # Messaging bridges (WeChat iLink, + adapter tree)
xiuqo setup           # Full setup wizard (everything at once)
xiuqo cron            # Scheduled tasks
xiuqo skills          # Search / install / manage skills
xiuqo mcp             # MCP servers, or run Xiuqo itself as one
xiuqo doctor          # Diagnose issues
xiuqo update          # Pull the latest version
```

📖 In-repo docs: **[AGENTS.md](AGENTS.md)** (architecture, in depth) · **[CONTRIBUTING.md](CONTRIBUTING.md)** · **[CHANGELOG.md](CHANGELOG.md)**. Upstream [Hermes docs](https://hermes-agent.nousresearch.com/docs) still explain the behavior — this fork changed names and packaging, not how the agent thinks.

---

## CLI vs Messaging Quick Reference

Two entry points: run `xiuqo` in a terminal, or run `xiuqo gateway` and talk to it from WeChat. Slash commands carry over between both.

| Action                     | CLI                                  | Messaging                            |
| -------------------------- | ------------------------------------ | ------------------------------------ |
| Start chatting             | `xiuqo`                              | `xiuqo gateway setup && xiuqo gateway run`, then DM the bot |
| Fresh conversation         | `/new`                               | `/new`                               |
| Change model               | `/model [provider:model]`            | `/model [provider:model]`            |
| Compress context / usage   | `/compress`, `/usage`, `/insights`   | same                                 |
| Browse skills              | `/skills` or `/<skill-name>`          | `/<skill-name>`                      |
| Interrupt current work     | `Ctrl+C`                             | `/stop` or just send a new message   |
| Approve a dangerous command| inline prompt                        | `/approve`, `/deny`                  |

---

## What I Cut vs Upstream

| Removed | Reason |
|---|---|
| Electron desktop app, bootstrap installer | CLI tool. Didn't want a browser in a window. |
| Ink/Node TUI (`ui-tui/`) | Was beautiful, cost a whole Node runtime in the install path. `--tui` now degrades to the classic interface. |
| docs website, contributors dataset, 29 CI workflows | Repo furniture for a company-scale project. Six checks kept: tests, lint, lockfile, supply-chain. |

Everything else from the Hermes v0.21.2 baseline is here: the full CLI command surface, all tool families, the whole gateway platform tree, web dashboard backend, ACP, sandbox backends, OpenClaw migration.

---

## Migrating from OpenClaw

Still works:

```bash
xiuqo claw migrate          # import settings, memories, skills, allowlists
```

---

## Contributing

PRs welcome — read [CONTRIBUTING.md](CONTRIBUTING.md) first. Bug reports and questions go in [Issues](https://github.com/xux123171-rgb/xiuqo/issues). Security reports go through [GitHub Advisories](https://github.com/xux123171-rgb/xiuqo/security/advisories/new), never public issues.

---

## License

MIT — see [LICENSE](LICENSE). Dual-copyrighted per MIT: fork content © 2026 xux123171-rgb; the core is derived from [Hermes Agent](https://github.com/NousResearch/hermes-agent) © 2025 Nous Research. This project is independent — Nous Research doesn't endorse it and doesn't maintain it. WeChat is a Tencent trademark; the gateway rides Tencent's private iLink bot API and may break whenever they do — patches land here when they do.
