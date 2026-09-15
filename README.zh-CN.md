# Xiuqo Agent ☤

> 会自我进化的终端 AI 代理——纯 Python CLI + 微信网关。

Xiuqo 是一个开源终端 AI agent：接任意模型（OpenRouter、OpenAI、Anthropic、DeepSeek、智谱、商汤 SenseNova、本地端点……），而且**真干活**——shell、文件、补丁、Python 代码内核、真实浏览器自动化、MCP、并行子 agent、定时任务。

它最特别的是**学习闭环**：从经验里自动沉淀可复用的技能、使用中改进技能、跨会话持久记忆、能搜自己的历史对话。

## 特性一览

| | |
|---|---|
| **真正的终端界面** | 多行编辑、斜杠命令补全、流式工具输出、皮肤主题——纯 Python，无额外运行时 |
| **任意模型不锁定** | `xiuqo model` 热切换 provider/模型；多密钥自动轮换 |
| **闭环学习** | 技能自创建自改进、代理自管记忆、FTS5 会话检索 |
| **微信网关** | 个人微信（iLink Bot API，扫码登录）远程指挥本地 agent；同时保留完整消息网关框架 |
| **能打的工具集** | 终端+后台 PTY、文件操作、`apply_patch`、Python RPC 代码执行、CDP 浏览器自动化、视觉、语音合成/转写、MCP、任务委派、cron、密码自动填充 |
| **跑在哪都行** | Linux / macOS / Windows / Termux；local / SSH / Docker / Modal / Daytona / Vercel 后端 |

## 快速开始

```bash
git clone https://github.com/xux123171-rgb/xiuqo.git && cd xiuqo
uv sync --extra dev          # 或 pip install -e .
.venv/bin/xiuqo setup        # 选 provider + 模型（API key 写入 ~/.xiuqo/.env）
.venv/bin/xiuqo              # 交互聊天（加 --tui 上完整终端界面）
```

Windows 用 `.venv\Scripts\xiuqo`。国内网络建议配 GitHub 加速镜像 + 清华 pip 源。

## 命令速查

```
xiuqo                       交互聊天
xiuqo --tui                 （本构建自动回退到经典界面）
xiuqo chat -q "..."         单发查询
xiuqo model / moa / fallback    模型与 provider 管理
xiuqo setup / doctor / status   配置与健康检查
xiuqo gateway               消息网关（含微信）
xiuqo cron / skills / mcp / plugins / vault   能力管理
xiuqo sessions / insights / journey           历史与分析
```

会话内斜杠命令见 `/help`。

## 致谢与许可

MIT — 见 [LICENSE](LICENSE)。

Xiuqo 衍生自 [Nous Research](https://nousresearch.com) 的开源项目 [Hermes Agent](https://github.com/NousResearch/hermes-agent)（同为 MIT，Copyright (c) 2025 Nous Research）。本 fork 完整保留其 agent 核心、CLI 与微信网关，改名换皮后由 [@xux123171-rgb](https://github.com/xux123171-rgb) 独立维护。Nous Research 与本项目无关联、亦不为其背书。
