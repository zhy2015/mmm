import os
import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class MemoryDistiller:
    """
    负责从 L3 的流水账（Daily Snapshots）中寻找重复的模式，
    并将它们提炼为 L2 (Skill) 的候选规则。
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.daily_path = os.path.join(workspace_root, "daily", "run_snapshots.md")
        
    def _read_l3_blocks(self) -> List[str]:
        """按块读取 L3 日志"""
        if not os.path.exists(self.daily_path):
            return []
        with open(self.daily_path, "r") as f:
            content = f.read()
        return [block.strip() for block in content.split("\n### ") if block.strip()]

    def analyze_and_distill(self) -> List[Dict]:
        """
        核心蒸馏逻辑。
        在真实生产中，这里会调用 LLM：把所有 L3 块扔给大模型，问它有没有重复踩的坑。
        这里我们提供一个简化的正则/关键词聚类 mock 演示。
        返回需要升层到 L2 的 Write Decision JSON 列表。
        """
        blocks = self._read_l3_blocks()
        if not blocks:
            return []
            
        # Mock LLM Detection Logic:
        # 假设大模型发现 "Docker" 和 "Network" 的报错在 L3 中出现了 3 次以上
        # 这里用简单的词频统计模拟
        keyword_counts = {}
        for block in blocks:
            words = block.lower().split()
            # 简化：只统计包含 docker 的块
            if "docker" in words:
                keyword_counts["docker"] = keyword_counts.get("docker", 0) + 1

        candidates = []
        for kw, count in keyword_counts.items():
            if count >= 3:
                logger.info(f"Detected repeated pattern for '{kw}' ({count} times). Generating L2 Candidate.")
                # 生成升层候选 JSON
                candidate = {
                    "operation_type": "write",
                    "write_decision": {
                        "action": "write",
                        "layer": "skill",
                        "target_skill": f"distilled-{kw}-rules",
                        "rationale": f"Automatically distilled after {count} repeated occurrences in daily logs.",
                        "content": {
                            "title": f"{kw.capitalize()} Best Practices",
                            "body": f"Avoid common {kw} issues discovered in daily runs. (Auto-generated)",
                            "metadata": {
                                "created_at": "auto",
                                "downgrade_condition": "If this pattern is no longer relevant"
                            }
                        }
                    }
                }
                candidates.append(candidate)
                
        return candidates

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    distiller = MemoryDistiller("/tmp/mock_workspace")
    candidates = distiller.analyze_and_distill()
    for c in candidates:
        print(json.dumps(c, indent=2))
