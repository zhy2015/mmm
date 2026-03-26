import os
import re
import datetime
import shutil
import logging

logger = logging.getLogger(__name__)

class MemoryJanitor:
    def __init__(self, workspace_root: str, max_age_days: int = 30):
        self.workspace_root = workspace_root
        self.max_age_days = max_age_days
        self.skills_dir = os.path.join(workspace_root, "skills")
        self.archive_dir = os.path.join(workspace_root, "archive")
        
    def _parse_frontmatter(self, content: str) -> dict:
        """解析我们定义的简易 HTML 注释风格的前置元数据"""
        meta = {}
        # 匹配 <!-- ... --> 中的内容
        match = re.search(r"<!--\s*(.*?)\s*-->", content, re.DOTALL)
        if match:
            lines = match.group(1).split("\n")
            for line in lines:
                if ":" in line:
                    key, val = line.split(":", 1)
                    meta[key.strip()] = val.strip()
        return meta

    def run_aging_process(self):
        """扫描所有 L2 Skill，进行老化判断"""
        if not os.path.exists(self.skills_dir):
            return

        os.makedirs(self.archive_dir, exist_ok=True)
        now = datetime.datetime.now(datetime.timezone.utc)

        for filename in os.listdir(self.skills_dir):
            if not filename.endswith(".md"):
                continue
                
            filepath = os.path.join(self.skills_dir, filename)
            with open(filepath, "r") as f:
                content = f.read()

            meta = self._parse_frontmatter(content)
            
            # 如果没有元数据，或者没有 created_at/last_used_at，默认给个基准时间
            last_used_str = meta.get("last_used_at") or meta.get("created_at")
            
            if last_used_str and last_used_str != "unknown":
                try:
                    last_used_date = datetime.datetime.fromisoformat(last_used_str.replace("Z", "+00:00"))
                    age_days = (now - last_used_date).days
                    
                    if age_days > self.max_age_days:
                        logger.info(f"Skill {filename} has aged {age_days} days. Moving to archive.")
                        shutil.move(filepath, os.path.join(self.archive_dir, filename))
                except ValueError:
                    logger.warning(f"Failed to parse date {last_used_str} for {filename}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    janitor = MemoryJanitor("/tmp/mock_workspace")
    janitor.run_aging_process()
