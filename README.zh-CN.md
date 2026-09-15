<p align="center">
  <img src="assets/banner.png" alt="Xiuqo Agent" width="100%">
</p>

# Xiuqo Agent ☤

<p align="center">
  <a href="https://github.com/xux123171-rgb/xiuqo/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge" alt="English"></a>
</p>

**一个会自我进化的终端 AI 代理。** 它从自己干过的活里学习——难任务之后自动沉淀成可复用的技能、跨会话保持记忆、能搜自己的历史对话。而且它真的能干活：shell、文件、Python 代码内核、真实浏览器自动化、MCP、并行子代理、定时任务。模型随便换——OpenRouter、OpenAI、Anthropic、DeepSeek、智谱、商汤 SenseNova、自建端点——`xiuqo model` 一句话切。

它不粘在你的笔记本上。丢在一台 $5 的 VPS 上，你在微信里遥控它干活（iLink 机器人协议，扫码登录内置）。Telegram/Discord/Slack 适配器也在树里，想要就用。

**这个 fork 为什么存在：** 我天天用 Hermes Agent，想把这台"机器"弄成自己的样子——于是改了 5000+ 个文件的名字，砍掉我永远不打开的东西（Electron 桌面端、Ink TUI、文档站），保留我真正用的一切，更新通道指向我的仓库。CLI 优先，纯 Python，安装路径里一个 Node 都没有。想要完整的 Hermes 体验请去[上游](https://github.com/NousResearch/hermes-agent)——这里是精简过的、有主见的版本。

<table>
<tr><td><b>真正的终端界面</b></td><td>多行编辑、斜杠命令补全、流式工具输出、打断重定向、皮肤主题——全部纯 Python（prompt_toolkit + rich）。没有套壳浏览器，没有 Node。</td></tr>
<tr><td><b>闭环学习</b></td><td>代理自管记忆 + 定期提醒沉淀。复杂任务后自主创建技能，技能在使用中自我改进。历史会话 FTS5 全文检索。兼容 <a href="https://agentskills.io">agentskills.io</a> 标准。</td></tr>
<tr><td><b>微信遥控</b></td><td><code>xiuqo gateway</code> 把个人微信接到同一个 agent 上——扫码、长轮询、收发媒体都通。和终端共享同一份记忆。</td></tr>
<tr><td><b>能打的工具集</b></td><td>带后台 PTY 的终端、文件操作 + <code>apply_patch</code>、Python RPC 代码执行、CDP 浏览器自动化、视觉、语音合成/转写、MCP 客户端、密码自动填充。</td></tr>
<tr><td><b>会分身</b></td><td>并行子代理分头干活；cron 定时任务用自然语言描述，夜间巡检、周报，无人值守跑。</td></tr>
<tr><td><b>到处能跑</b></td><td>Linux、macOS、Windows（原生，不需要 WSL）、WSL2、安卓 Termux。local / SSH / Docker / Modal / Daytona / Vercel 终端后端。</td></tr>
</table>

---

## 一键安装

### Linux / macOS / WSL2 / Termux

```bash
curl -fsSL https://raw.githubusercontent.com/xux123171-rgb/xiuqo/main/scripts/install.sh | bash
```

### Windows（PowerShell）

> 原生 Windows 直接跑，不需要 WSL。想用 WSL2 就用上面的 Linux 命令。

```powershell
iex (irm https://raw.githubusercontent.com/xux123171-rgb/xiuqo/main/scripts/install.ps1)
```

安装器全包：uv、Python 3.11+、没有 Git 就补一个便携版 MinGit。完全不碰你的系统 Python；Windows 装在 `%LOCALAPPDATA%\xiuqo`，其他系统装在 `~/.xiuqo`。

> **国内网络：** GitHub raw 可能断流。克隆走 `https://ghproxy.net/https://github.com/xux123171-rgb/xiuqo.git`，`uv sync` 加 `--default-index https://mirrors.aliyun.com/pypi/simple`。两条兜底都写进安装脚本了。

装完开新终端：

```bash
source ~/.bashrc     # zsh 用 ~/.zshrc；Windows 重开 PowerShell
xiuqo setup          # 选 provider + 模型，填 API key
xiuqo                # 开聊
```

<details>
<summary>手动安装（临时克隆 / CI / 离线机器）</summary>

```bash
git clone https://github.com/xux123171-rgb/xiuqo.git && cd xiuqo
uv sync --locked
.venv/bin/xiuqo setup        # Windows: .venv\Scripts\xiuqo setup
```

给跑在沙箱/agent 宿主里的人提个醒：venv 建在源码树**外面**（`uv venv /某处 --python 3.11 && uv pip install -e .`），防止 agent 一条相对路径清理把自己脚下的运行时扬了。
</details>

---

## 常用命令

```bash
xiuqo                 # 交互聊天
xiuqo model           # 选 provider + 模型
xiuqo tools           # 工具开关
xiuqo gateway         # 消息网关（微信 iLink + 全套适配器）
xiuqo setup           # 全套配置向导
xiuqo cron            # 定时任务
xiuqo skills          # 技能搜索/安装/管理
xiuqo mcp             # MCP 服务器管理，或把自己当 MCP server 跑
xiuqo doctor          # 体检
xiuqo update          # 升级
```

📖 仓库内文档：**[AGENTS.md](AGENTS.md)**（架构深潜）· **[CONTRIBUTING.md](CONTRIBUTING.md)** · **[CHANGELOG.md](CHANGELOG.md)**。行为细节看[上游 Hermes 文档](https://hermes-agent.nousresearch.com/docs)——这个 fork 改的是名字和打包，没改 agent 的脑子。

---

## 和上游砍了什么

| 砍掉的 | 理由 |
|---|---|
| Electron 桌面端 + 安装器 | 终端工具，不要窗口里的浏览器 |
| Ink/Node TUI（`ui-tui/`） | 好看，但为了它安装路径里得多一整个 Node 运行时。`--tui` 现在优雅降级回经典界面 |
| 文档站、contributors 数据、29 个 CI 工作流 | 公司级仓库的家具，留 6 个核心检查：测试、lint、lockfile、供应链 |

其余 Hermes v0.21.2 基线的东西全在：CLI 全部命令、全套工具、网关平台树、dashboard 后端、ACP、沙箱后端、OpenClaw 迁移。

---

## 从 OpenClaw 迁移

照常能用：

```bash
xiuqo claw migrate          # 设置、记忆、技能、白名单一键导入
```

---

## 贡献

欢迎 PR——先看 [CONTRIBUTING.md](CONTRIBUTING.md)。问题和想法开 [Issue](https://github.com/xux123171-rgb/xiuqo/issues)；漏洞请走 [GitHub Advisories](https://github.com/xux123171-rgb/xiuqo/security/advisories/new) 私报，别开公开 issue。

---

## 许可

MIT——见 [LICENSE](LICENSE)。双版权按 MIT 规范：fork 内容 © 2026 xux123171-rgb；核心衍生自 [Hermes Agent](https://github.com/NousResearch/hermes-agent) © 2025 Nous Research。本项目独立维护，Nous Research 不背书也不负责。微信是腾讯的商标；网关走的腾讯 iLink 私有协议，哪天说变就变，补丁随缘更新。
