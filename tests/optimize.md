# OpenClaw MMU (mmm) 工程化演进蓝图 (Optimization Roadmap)

> **"Theory and practice sometimes clash. Theory loses. Every single time."**
> 当前体系已完成“三坝+物理闭环”的基建。下一阶段的绝对核心不是“如何记更多”，而是**把人工裁决固化为代码、把记忆老化变成自动化流水线、把脏数据变成可监控的指标**。

---

## 阶段一：裁决工程化 (The Hard Gates)
*目标：消灭主观判断，把读写动作变成可测试的、带有字段约束的流水线。*

### [x] 1. L2 技能元数据门禁 (L2 Schema Enforcer)
- **现状**：L2 (Skills) 目前只是简单的 Markdown 文本堆砌，容易变成半永久垃圾场。
- **动作**：
  - 更新 `schemas/memory-routing.schema.json`，强制 L2 写入时必须携带元数据 Frontmatter。
  - **必填字段**：`created_at`, `last_used_at`, `hit_count`, `downgrade_condition` (什么情况下该废弃)。
  - **验收**：所有新写入的 `skills/*.md` 头部必须包含合规的 YAML/JSON 元数据。

### [x] 2. 读裁决路由表 (Read Routing Playbook)
- **现状**：什么时候读 L2，什么时候读 L3，目前全靠大模型“领悟” `SKILL.md` 的指示。
- **动作**：
  - 在 `SKILL.md` 中硬编码路由决策树：
    - 稳定规则/红线 -> `force_load: L0`
    - 继续执行/延续上下文 -> `load: L2`, `scan: L3`
    - 历史回溯/故障追因 -> `scan: L3` 
  - **验收**：提供至少 10 个测试用例，验证各种 Prompt 下大模型输出的 JSON 是否精准命中最小足够读取，不发生“保险起见全读”。

### [x] 3. 写入四问拦截器 (Write Gate Checklist)
- **现状**：大模型可能会把一次性的 workaround (例如“重启了一下 Docker 好了”) 错误地写进 L0。
- **动作**：
  - 在写入请求到达物理执行器之前，强制增加一个 LLM 审核拦截层（或者在现有 Prompt 中增加极强的反问机制）：
    1. 这是 durable lesson 还是一次性 residue？
    2. 最小正确落层在哪？
    3. 如果新真相成立，是否需要触发 overwrite 抹除旧真相？
  - **验收**：跑测试集，验证一次性 workaround 绝对不会污染 L0。

---

## 阶段二：自动化流转与老化 (The Flow)
*目标：让记忆系统像水一样流动起来，自动清理淤泥。*

### [x] 1. L2 老化与降级机制 (L2 Aging Cron)
- **现状**：写入 L2 后，如果没有 overwrite 就会永远存在。
- **动作**：
  - 编写一个独立的 Python 脚本 (`scripts/core/memory_janitor.py`)。
  - **逻辑**：扫描所有 `skills/*.md`，读取 `last_used_at` 和 `hit_count`。如果超过 30 天未被命中，自动将其降级移入 `archive/` 或合并压缩到 `daily/` 中。
  - **验收**：配合 cronjob 或 heartbeat，证明过期的 skill 会被物理删除或转移。

### [x] 2. L3 到 L2 的自动蒸馏链 (Daily to Rule Pipeline)
- **现状**：L3 里的 daily snapshots 需要人工发现规律，才能提炼成通用 Skill。
- **动作**：
  - 开发一个定期的后台分析 Agent。
  - **逻辑**：读取 `daily/run_snapshots.md`，寻找“Repeated Patterns”（同一个坑踩了三次）。一旦发现，自动生成一份 L2 Candidate JSON 提交给 `mmm` 裁决升层。
  - **验收**：向 daily 中注入 3 条相同的报错修复记录，触发蒸馏器，验证能否自动生成一个合并后的 `skills/xxx_fix.md`。

---

## 阶段三：可观测性与评测 (Observability)
*目标：用数据证明系统在变干净，而不是凭体感。*

### [x] 1. 记忆健康度面板 (Governance Metrics)
- **现状**：我们不知道系统里有多少垃圾，不知道三坝拦截了多少次越权。
- **动作**：
  - 在 `memory_executor.py` 中埋点，将关键动作记录到 `metrics/mmm-governance.csv`。
  - **核心指标**：
    - 拦截写入 L0 的次数（Dam Block Count）。
    - 触发旧真相覆写的次数（Overwrite Count）。
    - 读请求的跨层率（是否经常被迫 L0+L2+L3 全开）。
    - L2 条目的陈旧率。
  - **验收**：执行完一批测试任务后，CSV 能够清晰展示出收敛趋势。

### [x] 2. 闭环追踪与纠错 (Failure-to-MMM Correction)
- **现状**：如果 `mmm` 判断错了（比如把垃圾升成了 L0），修复起来很麻烦。
- **动作**：
  - 建立错误溯源机制。当人工发现记忆库污染时，提供一个一键 rollback 或标记为“Bad Case”的命令。
  - 将这些 Bad Case 喂给 `mmm` 的 Prompt 示例中，作为反面教材（Anti-pattern examples）。
  - **验收**：通过特定的指令，能将当前的错误判断记录归档，并确保同样的错误决策不会再次发生。

---

## ⛔ 绝对不该做的事 (Anti-Patterns for Next Steps)

- **❌ 扩大 L0 的容量限制**：如果 200 行不够，说明你没在做抽象，而是把日志当成了原则。
- **❌ 引入复杂的向量数据库 (Vector DB)**：在我们还没把文件系统的元数据和复审机制跑通之前，引入外部中间件只会掩盖问题。
- **❌ 默认跨层全量读取**：不要为了“怕 AI 不知道”就放开读权限。宁可让任务失败，再通过纠错机制补充经验，也不能破坏“最小按需加载”的铁律。
