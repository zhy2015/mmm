import os
import json
import logging
from typing import Dict, Any

# -----------------------------------------------------------------------------
# Memory Executor: The physical hands of the `mmm` brain.
# 它的职责是：解析 `mmm` 吐出的 JSON 契约，并安全地操作本地文件系统。
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)

class MemoryExecutor:
    def __init__(self, workspace_root: str, max_l3_lines: int = 500):
        self.workspace_root = workspace_root
        self.max_l3_lines = max_l3_lines # 水坝的物理容量限制
        self.l0_paths = {
            "core_memory": os.path.join(workspace_root, "MEMORY.md"),
            "agents": os.path.join(workspace_root, "AGENTS.md")
        }
        self.l3_paths = {
            "daily": os.path.join(workspace_root, "daily"),
            "archive": os.path.join(workspace_root, "archive")
        }

    def execute_write_decision(self, write_decision: Dict[str, Any]) -> bool:
        """执行记忆写入、覆盖、降级或丢弃的物理操作"""
        action = write_decision.get("action")
        layer = write_decision.get("layer")
        content = write_decision.get("content", {})
        
        if action == "discard":
            logger.info("Decision: Discard. Action ignored.")
            return True
            
        if action == "handoff":
            target_skill = write_decision.get("target_skill")
            logger.info(f"Decision: Handoff to {target_skill}. Triggering downstream specialist.")
            return self._trigger_handoff(target_skill, content)

        if layer == "core_memory":
            target_file = self.l0_paths["core_memory"]
        elif layer == "skill":
            target_skill = write_decision.get("target_skill")
            if not target_skill:
                raise ValueError("target_skill is required when layer is 'skill'")
            target_file = os.path.join(self.workspace_root, "skills", f"{target_skill}.md")
        else:
            # 默认降级到 daily 记录
            target_file = os.path.join(self.l3_paths["daily"], "run_snapshots.md")

        return self._safe_write_or_overwrite(target_file, action, content)

    def _safe_write_or_overwrite(self, filepath: str, action: str, content: Dict[str, Any]) -> bool:
        """安全的物理写入操作"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        formatted_entry = f"\n### {content.get('title')}\n{content.get('body')}\n"
        is_l0 = "MEMORY.md" in filepath or "AGENTS.md" in filepath
        
        if action == "overwrite" or is_l0:
            # L0 写入必须是 overwrite 或特权写
            logger.warning(f"Overwriting rules in {filepath}. (Requires AST replacement in production)")
            self._enforce_l0_dam(filepath)
            with open(filepath, "a") as f:
                f.write(f"\n[OVERWRITE RECORD]{formatted_entry}")
        else:
            with open(filepath, "a") as f:
                f.write(formatted_entry)
            # L3/Skill 水坝：滚动截断，防止无限膨胀
            self._enforce_rolling_dam(filepath)
                
        logger.info(f"Successfully executed {action} to {filepath}")
        return True

    def _enforce_l0_dam(self, filepath: str):
        """L0 水坝：硬性约束。如果核心记忆超过一定行数，必须警告人工介入重构"""
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                lines = f.readlines()
                if len(lines) > 200:
                    logger.error(f"DAM BREACH: L0 file {filepath} exceeds 200 lines. Convergence is failing. Refactor required.")

    def _enforce_rolling_dam(self, filepath: str):
        """L3/L2 水坝：滚动日志机制。超过最大行数则砍掉头部旧数据"""
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                lines = f.readlines()
            
            if len(lines) > self.max_l3_lines:
                logger.info(f"DAM ENFORCED: Truncating {filepath} from {len(lines)} to {self.max_l3_lines} lines.")
                # 保留最新的 max_l3_lines 行
                with open(filepath, "w") as f:
                    f.writelines(lines[-self.max_l3_lines:])

    def _trigger_handoff(self, specialist_skill: str, context: Dict[str, Any]) -> bool:
        """调用下游的 skill-creator-enhanced 进行结构重构"""
        logger.info(f"Invoking {specialist_skill} with context: {context['title']}")
        # 实际的 LLM 调用链将在这里发生
        return True

    def _read_file_safe(self, filepath: str) -> str:
        """安全读取文件，不存在则返回空字符串。消除了到处存在的 if os.path.exists 判断。"""
        if not os.path.exists(filepath):
            return ""
        with open(filepath, "r") as f:
            return f.read()

    def _recall_l3_memories(self, queries: list) -> str:
        """从 L3 日志中物理扫描并提取相关的记忆块。"""
        daily_path = os.path.join(self.l3_paths["daily"], "run_snapshots.md")
        content = self._read_file_safe(daily_path)
        
        if not content:
            return f"--- Recalled L3 Memories ---\n(No exact match found for: {', '.join(queries)})"

        recalled_content = []
        blocks = content.split("\n### ")
        
        for block in blocks:
            # 只要任意一个 query 命中，就整块提取 (消除了深层嵌套的 for+if+break)
            if any(q.lower() in block.lower() for q in queries):
                recalled_content.append(f"### {block.strip()}")

        if recalled_content:
            return "--- Recalled L3 Memories ---\n" + "\n\n".join(recalled_content)
        return f"--- Recalled L3 Memories ---\n(No exact match found for: {', '.join(queries)})"

    def execute_read_decision(self, read_decision: Dict[str, Any]) -> str:
        """
        动态上下文加载（Context Assembly）。
        根据 JSON，去硬盘上把对应的 Skill 和 Memory 抽出来，拼成给 LLM 的字符串。
        """
        assembled_context = []
        
        # 1. 强行加载 L0 (Identity)
        for name, path in self.l0_paths.items():
            content = self._read_file_safe(path)
            if content:
                assembled_context.append(f"--- L0 Identity ({name}) ---\n{content}")

        # 2. 按需加载 Skills (L2)
        for skill in read_decision.get("skills_to_load", []):
            skill_path = os.path.join(self.workspace_root, "skills", f"{skill}.md")
            content = self._read_file_safe(skill_path)
            if content:
                assembled_context.append(f"--- Skill Loaded ({skill}) ---\n{content}")

        # 3. 按需加载 L3 (Experience Snapshots)
        memories = read_decision.get("memories_to_recall", [])
        if memories:
            assembled_context.append(self._recall_l3_memories(memories))

        return "\n\n".join(assembled_context)

# 测试入口
if __name__ == "__main__":
    executor = MemoryExecutor("/tmp/mock_workspace")
    print("Memory Executor initialized successfully.")