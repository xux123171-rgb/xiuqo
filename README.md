# Xiuqo Agent ☤

> A self-improving AI agent for your terminal — pure Python CLI with a WeChat gateway.

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green" alt="License: MIT"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/中文-README-red" alt="中文"></a>
</p>

Xiuqo is an open-source terminal AI agent: chat with any LLM provider (OpenRouter, OpenAI, Anthropic, DeepSeek, Zhipu, SenseNova, local endpoints…), and it **works**, not just talks — shell, files, patches, a Python code kernel, real browser automation, MCP servers, parallel subagents, scheduled cron jobs.

What makes it different is the **learning loop**: it writes reusable skills from experience, improves them during use, keeps persistent memory across sessions, and can search its own past conversations.

## Highlights

| | |
|---|---|
| **Rich terminal interface** | Multiline editing, slash-command autocomplete, streaming tool output, themable skins — pure Python, zero extra runtimes |
| **Any model, no lock-in** | `xiuqo model` switches provider/model live; credential pools rotate keys automatically |
| **A closed learning loop** | Skills self-create & self-improve, agent-curated memory, FTS5 session search |
| **WeChat gateway** | Chat with your local agent from a personal WeChat account (iLink Bot API, QR login) — plus the full messaging gateway platform |
| **Tool-calling that matters** | terminal + background PTY, file ops, `apply_patch`, Python RPC code execution, CDP browser automation, vision, TTS/STT, MCP, delegation, cron, vault autofill |
| **Runs anywhere** | Linux, macOS, Windows, Termux; local / SSH / Docker / Modal / Daytona / Vercel sandbox backends |

## Quick start

```bash
git clone https://github.com/xux123171-rgb/xiuqo.git && cd xiuqo
uv sync --extra dev          # or: pip install -e .
.venv/bin/xiuqo setup        # pick provider + model (API keys go to ~/.xiuqo/.env)
.venv/bin/xiuqo              # interactive chat
```

Windows: use `.venv\Scripts\xiuqo` instead.

## CLI at a glance

```
xiuqo                       interactive chat
xiuqo --tui                 (falls back to the classic interface in this build)
xiuqo chat -q "..."         one-shot query
xiuqo model / moa / fallback    provider & model management
xiuqo setup / doctor / status   configuration & health
xiuqo gateway               messaging bridges (WeChat included)
xiuqo cron / skills / mcp / plugins / vault   capabilities
xiuqo sessions / insights / journey           history & analytics
xiuqo backup / security / verify              ops
```

In-session slash commands (`/help` for the full list): `/new /model /compress /rollback /diff /yolo /voice /skin /copy` …

## Documentation

In-repo docs: see `CONTRIBUTING.md` and the `xiuqo` skill (`skills/autonomous-ai-agents/xiuqo-agent/`), which mirrors the upstream Hermes Agent guide adapted for this fork.

## Credits & license

MIT — see [LICENSE](LICENSE).

Xiuqo is a derivative work of [Hermes Agent](https://github.com/NousResearch/hermes-agent) by [Nous Research](https://nousresearch.com), also MIT-licensed (Copyright (c) 2025 Nous Research). This fork keeps the full agent core, CLI, and WeChat gateway, rebranded and maintained independently by [@xux123171-rgb](https://github.com/xux123171-rgb). Hermes is not affiliated with, endorsing, or supporting this project.
