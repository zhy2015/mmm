# mmm

`mmm` 是一套面向 AI agent / assistant 的**记忆收敛方法**。

它不是教 AI “记更多”，而是教 AI **只保留真正值得保留的东西**：
- 什么该进入长期记忆
- 什么只该留在低层记录
- 什么时候应该覆盖旧规则，而不是把新旧都留下
- 什么时候根本不该写入，而应该直接丢弃

如果把普通 memory system 看作“存储器”，那 `mmm` 更像一个**裁决器（judge）**。

---

## 这是什么

`mmm` 的核心目标不是扩容记忆，而是做 **memory convergence**：

- 防止噪音升级成长期真相
- 防止系统里同时存在多个互相冲突的版本
- 防止把一次性试错误写成稳定方法
- 防止记忆层、技能层、参考层、daily 层混在一起

一句话说：

> `mmm` 关心的不是“能不能记住”，而是“这件事到底配不配被记住，以及应该记到哪一层”。

---

## 它解决什么问题

很多 AI 系统一旦开始做长期记忆，很快会出现这些典型问题：

- 什么都想存，最后核心记忆变成流水账
- 新规则写进去了，旧规则还留着，系统越来越矛盾
- 明明只是一次临时 workaround，却被误当成长期方法
- 真实有价值的 lesson 和大量过程噪音混在一起
- 一看到问题就改 skill，结果其实只是记忆落层没判断清楚

`mmm` 就是专门为这些问题设计的。

它把“记忆”看成一种**收敛机制**，而不是归档机制。

---

## 核心理念

### 1. Candidate is not memory
任何 lesson、经验、修正、观察，刚出现时都只是 **candidate**。
它还不是长期记忆。

### 2. 默认拒绝，除非它配得上
`mmm` 的默认姿态不是“先记下来再说”，而是：

**先拒绝，除非它真的值得长期保留。**

最近、痛苦、花时间，并不自动说明它有长期价值。
真正的门槛是：
- 未来是否会稳定复用
- 是否会持续影响判断
- 是否构成新的单一真相（SSOT）

### 3. 核心记忆必须小而有行为塑形力
核心记忆不是历史回放。
它应该主要承载：
- 稳定偏好
- 稳定规则
- 已落地能力
- 重要架构 / 工作流决策
- 高价值索引

### 4. 单一真相优先
如果新旧规则冲突，系统应该收敛到一个当前版本。
而不是把两个版本同时留在核心层“以防万一”。

### 5. 先判断落层，再决定是否改技能
不是所有 lesson 都该进入 skill layer。
很多内容其实只该落到：
- `MEMORY.md`
- `AGENTS.md`
- `TOOLS.md`
- `references/`
- daily memory

所以 `mmm` 是**先做判断，再决定是否下发给 skill specialist**。

---

## 它通常怎么工作

面对一条新的 candidate，`mmm` 会做一条固定的收敛链：

1. 它到底是不是 durable lesson？
2. 它属于哪类：fact / preference / procedure / safety boundary / capability / run snapshot / raw event / workaround？
3. 它是在扩展当前真相，还是在替换当前真相？
4. 最小正确落点是哪一层？
5. 应该 write、overwrite、downgrade、archive，还是 discard？

所以它给出的不是“我帮你存一下”，而是一份**裁决结果**。

---

## 仓库里主要有什么

这个仓库是一个**可分享的最小体系版本**，重点区分“给 AI 读”和“给人读”的部分。

### 主要给 AI 读
- `skills/mmm/SKILL.md`  
  上游收敛判断入口。AI 应该优先读这个。
- `skills/skill-creator-enhanced/SKILL.md`  
  当问题已经明确落到 skill layer 后，再交给它处理。

### 主要给人读
- `README.md`  
  帮人快速理解这套体系到底是什么。
- `AGENTS.md`  
  说明仓库级运行姿态，尤其是为什么采用 `mmm-first convergence`。
- `MEMORY.md`  
  一个极简版核心记忆骨架，示范这套方法想让核心层长什么样。
- `references/system-intro.md`  
  给接入者看的快速说明。

---

## 推荐怎么接入

如果你想把这套东西接进自己的 agent / assistant，通常可以这样做：

1. 把 `skills/mmm/SKILL.md` 放进你的 skill system
2. 明确一条路由规则：凡是涉及 durable lesson、记忆落层、SSOT 覆盖、run snapshot 去留、是否该上升到 skill layer 的问题，先走 `mmm`
3. 让 `mmm` 负责“判断与裁决”，不要让它顺手接管所有下游改写动作
4. 如果已经明确落到 skill layer，再交给 `skill-creator-enhanced`
5. 保持核心记忆小，把运行细节、trace、具体案例、当日上下文留在 lower layers

最短版理解：

> `mmm` = memory convergence judge  
> 不是 memory storage manager

---

## 适合谁

这套东西尤其适合：
- 在做 AI agent / AI assistant / long-term memory system 的人
- 已经有多层记忆、skills、daily memory、system prompt 的团队
- 遇到“记忆越来越多，但系统越来越乱”的项目
- 想把 AI 从“会记很多”推进到“会收敛、会裁决、会保持 SSOT”的人

---

## 设计边界

这个导出仓库刻意**不包含**：
- 用户隐私文件
- 用户画像
- 对话记录
- daily memory
- 私有 references
- 任何绑定某个个人环境的运行上下文

它只保留适合公开分享和复用的最小核心材料。

---

## 给人的一句话介绍

如果你要向别人解释这个项目，可以直接这么说：

> `mmm` 是一套给 AI agent 用的记忆收敛方法。它不解决“怎么记更多”，而是解决“什么该记、记到哪层、旧真相怎么覆盖、新旧冲突怎么收敛、什么时候该丢掉而不是保存”。
