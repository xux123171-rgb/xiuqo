# Xiuqo CLI Reference

Live sources when anything looks stale: `xiuqo --help`, `xiuqo <command> --help`,
https://hermes-agent.nousresearch.com/docs/reference/cli-commands

### Global Flags

```
xiuqo [flags] [command]        (no subcommand = interactive chat)

  --version, -V             Show version
  -z, --oneshot PROMPT      One-shot: print ONLY the final response (for scripts/pipes)
  -m MODEL  --provider P    Model/provider override for this invocation
  -t, --toolsets LIST       Comma-separated toolsets for this invocation
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --tui / --cli             Force the Ink TUI / classic REPL
  --ignore-rules            Skip AGENTS.md/SOUL.md/memory/skill injection
  --safe-mode               Disable ALL customizations (troubleshooting)
  --pass-session-id         Include session ID in system prompt
```

### Chat

```
xiuqo chat [flags]
  -q, --query TEXT          Single query, non-interactive
  --image PATH              Attach a local image to a single query
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --max-turns N             Cap tool-calling iterations
  --source TAG              Session source tag (default: cli)
```
(plus the global flags above)

### Configuration

```
xiuqo setup [section]      Wizard (model|tts|terminal|gateway|tools|agent)
xiuqo model                Interactive model/provider picker
xiuqo fallback [add|remove|list]  Fallback provider chain
xiuqo config [show|edit|get|set|unset|path|env-path|check|migrate]
xiuqo login / logout       OAuth sign-in / clear stored auth
xiuqo doctor [--fix]       Check dependencies and config
xiuqo status [--all]       Component status
```

### Tools & Skills

```
xiuqo tools [list|enable NAME|disable NAME]   Per-platform toolsets (curses UI with no args)

xiuqo skills list|browse|search QUERY|inspect ID
xiuqo skills install ID    Hub identifier OR a direct https://…/SKILL.md URL
xiuqo skills config        Enable/disable skills per platform
xiuqo skills check|update|uninstall|publish PATH
xiuqo skills tap add REPO  Add a GitHub repo as a skill source
xiuqo bundles              Skill bundles (one /<name> alias loads several skills)
```

### MCP Servers

```
xiuqo mcp add NAME (--url or --command) | remove | list | test NAME
xiuqo mcp catalog | install NAME     Curated catalog install
xiuqo mcp configure NAME             Toggle tool selection
xiuqo mcp serve                      Run Xiuqo as an MCP server
```
Details (transport, tool discovery, catalog): `references/native-mcp.md`.

### Gateway (Messaging Platforms)

```
xiuqo gateway run|install|start|stop|restart|status|setup
```

20+ platforms: Telegram, Discord, Slack, WhatsApp (Baileys + Business Cloud API), iMessage (Photon — `xiuqo photon setup`), Signal, Email, SMS, Matrix, Mattermost, Teams, LINE, SimpleX, ntfy, Google Chat, Home Assistant, DingTalk, Feishu, WeCom, Weixin, API Server, Webhooks. Open WebUI connects via the API Server adapter. Most adapters ship under `plugins/platforms/`.
Docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

### Sessions

```
xiuqo sessions list|browse|rename ID TITLE|delete ID|export OUT|prune|stats
```

### Cron / Webhooks

```
xiuqo cron list|create SCHED|edit ID|pause|resume|run ID|remove|status
    Schedules: '30m', 'every 2h', '0 9 * * *', ISO timestamp
xiuqo webhook subscribe NAME|list|remove NAME|test NAME
```
Webhook payloads/routes: `references/webhooks.md`.

### Profiles

```
xiuqo profile list|create NAME (--clone|--clone-all|--clone-from)|use|show|delete
xiuqo profile rename A B | alias NAME | export NAME | import FILE
```

### Credentials & Pools

```
xiuqo auth                 Interactive credential manager
xiuqo auth add [PROVIDER]  Add OAuth or API-key credential (nous, openai-codex, qwen-oauth, …)
xiuqo auth list|remove P IDX|reset PROVIDER|status
```
Multiple credentials per provider form a pool that rotates automatically and skips exhausted keys.

### Other

```
xiuqo desktop / gui        Native desktop app
xiuqo dashboard            Web admin panel + embedded chat (--stop / --status)
xiuqo proxy                OpenAI-compatible local proxy backed by an OAuth provider
xiuqo portal               Quick setup / sign in via Nous Portal
xiuqo kanban <verb>        Multi-agent work-queue board
xiuqo project              Named multi-folder workspaces
xiuqo skin list|use|set    Switch/tweak skins (see references/themes.md)
xiuqo pets <verb>          Pet mascots (see references/petdex.md)
xiuqo memory setup|status|off|reset   Memory provider
xiuqo secrets bitwarden|onepassword   External secret stores
xiuqo moa                  Mixture-of-Agents slots
xiuqo hooks / security / backup / import / checkpoints / console
xiuqo logs [-f] [errors]   View agent/error logs
xiuqo send                 One-off message through a gateway platform
xiuqo pairing / plugins / insights / journey / computer-use
xiuqo acp                  ACP server (IDE integration)
xiuqo completion bash|zsh|fish
xiuqo update / uninstall / claw migrate
```

Plugin- and provider-supplied subcommands (e.g. `xiuqo photon setup`) only appear once their plugin is installed/active.

### Where to Find Things

| Looking for... | Location |
|---|---|
| Config options | `xiuqo config edit` · [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Tools / toolsets | `xiuqo tools list` · [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) |
| Skills catalog | `xiuqo skills browse` · [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `xiuqo model` · [Providers guide](https://hermes-agent.nousresearch.com/docs/integrations/providers) |
| Env variables | `xiuqo config env-path` · [Env vars reference](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) |
| Gateway logs | `~/.xiuqo/logs/gateway.log` (or `xiuqo logs`) |
| Sessions | `xiuqo sessions browse` (reads state.db) |
