# mmm

`mmm` 是一套给 AI 用的“记忆收敛”方法，不是让 AI 记得更多，而是让它**只留下真正该留下的东西**。

它的核心目标很简单：
- 区分什么值得进入长期记忆
- 避免把噪音、临时过程、一次性 workaround 升级成“真理”
- 在不同层之间做最小正确落点：该进核心记忆、系统规则、参考资料、还是只留在当天运行记录里
- 避免旧规则和新规则并存，导致系统出现“双重真相”

换句话说，`mmm` 不是一个“帮 AI 存档”的方案，而是一个**帮 AI 做判断、压缩、覆盖、降级和收敛**的方案。

## 这套东西解决什么问题

很多 AI 系统一旦开始“会记忆”，很快就会出现这些问题：
- 什么都想记，最后核心记忆变成流水账
- 旧规则没删，新规则又写进去，系统越来越自相矛盾
- 明明只是一次临时试错，却被误写成长期方法
- 技能层、系统层、记忆层边界混乱，哪里都塞一点，最后没人知道哪份才算准

`mmm` 的设计就是专门对付这些问题。

它把“记忆”看成一种**收敛武器**，不是存储桶。
重点不是“保留更多”，而是“过滤错的，留下真的”。

## 核心理念

### 1. Candidate is not memory
一个 lesson、观察、纠错、经验，刚出现时只是 candidate，不等于已经值得写入长期记忆。

### 2. 默认拒绝，除非它配得上
`mmm` 的默认姿态不是“尽量记下来”，而是“先拒绝，除非它真的值得保留”。

最近、痛苦、花了很多时间，不等于它值得长期保留。
真正的门槛是：**未来是否还会稳定复用，是否会持续影响判断。**

### 3. 核心记忆必须小而有行为塑形力
核心记忆不是历史回放。
它应该只放：
- 稳定偏好
- 稳定规则
- 已落地能力
- 重要工作流 / 架构决策
- 高价值索引

### 4. 单一真相优先
如果新旧规则冲突，应该收敛到一个当前真相，而不是把两个版本一起留在核心层“以防万一”。

### 5. 先判断落层，再决定是否改技能
很多系统一出问题就想改 skill。
`mmm` 的观点是：先判断这到底是不是 skill layer 的问题。
很多 lesson 其实只该进 `MEMORY.md`、`AGENTS.md`、`TOOLS.md`、`references/` 或 daily memory，根本不需要动 skill。

## 它通常怎么工作

一条 candidate 进来后，`mmm` 会沿着一条固定的收敛链处理：

1. 到底有没有 durable lesson？
2. 它属于哪一类：fact / preference / procedure / safety boundary / capability / run snapshot / raw event / workaround？
3. 它是在扩展当前真相，还是在挑战当前真相？
4. 最小正确落点是哪一层？
5. 应该 write、overwrite、downgrade、archive，还是 discard？

所以它输出的不是“我帮你记住了”，而是一个**裁决结果**。

## 适合谁

这套东西特别适合：
- 正在做 agent / AI assistant / long-term memory system 的人
- 已经有多层记忆、技能系统、daily memory、system prompt 的团队
- 经常遇到“记忆越来越多，但越来越乱”的系统
- 希望把 AI 从“会记很多”推进到“会收敛、会裁决、会保持 SSOT”的人

## 目录说明

这个临时包里现在放的是一个可分享的最小体系：

- `skills/mmm/SKILL.md`：给 AI 读的，上游收敛判断入口
- `skills/skill-creator-enhanced/SKILL.md`：当问题明确落到 skill layer 后使用的下游 specialist
- `AGENTS.md`：仓库级运行姿态，说明为什么采用 mmm-first convergence
- `MEMORY.md`：极简索引版核心记忆骨架
- `references/system-intro.md`：帮助其他用户快速理解该怎么接入
- `README.md`：给人读的总体说明

## 如何快速引入这套体系

如果你想把它接到自己的 agent 里，最简单的方法通常是：

1. 先把 `skills/mmm/SKILL.md` 放进你现有的 skill system
2. 在你的系统里明确：凡是涉及 durable lesson、记忆落层、SSOT 覆盖、run snapshot 去留、是否该上升到 skill layer 的问题，先路由到 `mmm`
3. 让它只负责“判断与裁决”，不要让它顺手接管所有下游改写动作
4. 保持核心记忆小，把运行细节、当天上下文、trace、具体案例留在 lower layers

一句话版：

> `mmm` 不是 memory storage manager，而是 memory convergence judge。

## 额外说明

这个导出包刻意没有包含你的个人隐私文件、用户资料、日常记忆、对话记录或任何绑定你个人环境的内容。
它只保留了适合分享和复用的 `mmm` 核心说明与引导材料。
