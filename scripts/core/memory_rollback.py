import os
import json
import logging
import shutil

logger = logging.getLogger(__name__)

class MemoryRollback:
    """
    闭环纠错与回滚机制。
    如果发现 mmm 做出了错误的裁决（例如错误地上浮了一次性的 residue），
    通过这个工具一键回滚，并将错误记录到反面教材库中。
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.skills_dir = os.path.join(workspace_root, "skills")
        self.bad_cases_path = os.path.join(workspace_root, "references", "mmm_bad_cases.jsonl")
        
    def rollback_skill(self, target_skill: str, reason: str):
        """回滚一个被错误提升到 L2 的 Skill，并记录反面教材"""
        skill_path = os.path.join(self.skills_dir, f"{target_skill}.md")
        if not os.path.exists(skill_path):
            logger.error(f"Skill {target_skill} does not exist.")
            return False

        with open(skill_path, "r") as f:
            content = f.read()

        # 记录到 Bad Cases 库
        os.makedirs(os.path.dirname(self.bad_cases_path), exist_ok=True)
        bad_case = {
            "type": "false_promotion_to_l2",
            "skill_name": target_skill,
            "content": content,
            "correction_reason": reason
        }
        with open(self.bad_cases_path, "a") as f:
            f.write(json.dumps(bad_case) + "\n")

        # 物理删除该 Skill
        os.remove(skill_path)
        logger.info(f"Successfully rolled back {target_skill} and logged to bad cases.")
        return True

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    rollback = MemoryRollback("/tmp/mock_workspace")
    # rollback.rollback_skill("restart-docker-hack", "This was a one-off residue, not a durable rule.")
