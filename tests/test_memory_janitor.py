import pytest
import os
import tempfile
import sys
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts", "core"))
from memory_janitor import MemoryJanitor

@pytest.fixture
def workspace():
    with tempfile.TemporaryDirectory() as temp_dir:
        skills_dir = os.path.join(temp_dir, "skills")
        os.makedirs(skills_dir, exist_ok=True)
        yield temp_dir

def test_l2_aging_cron(workspace):
    """测试意图：超过 30 天未使用的 Skill 将被归档"""
    skills_dir = os.path.join(workspace, "skills")
    archive_dir = os.path.join(workspace, "archive")
    
    # 构造一个 40 天前的 skill
    old_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=40)).isoformat()
    old_skill_path = os.path.join(skills_dir, "old-skill.md")
    with open(old_skill_path, "w") as f:
        f.write(f"<!--\ncreated_at: {old_date}\n-->\n### Old Skill\n...")

    # 构造一个 10 天前的 skill
    recent_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=10)).isoformat()
    recent_skill_path = os.path.join(skills_dir, "recent-skill.md")
    with open(recent_skill_path, "w") as f:
        f.write(f"<!--\ncreated_at: {recent_date}\n-->\n### Recent Skill\n...")

    # 执行清理
    janitor = MemoryJanitor(workspace, max_age_days=30)
    janitor.run_aging_process()

    # 验证 old-skill 被移动到了 archive
    assert not os.path.exists(old_skill_path)
    assert os.path.exists(os.path.join(archive_dir, "old-skill.md"))

    # 验证 recent-skill 仍然在 skills 目录
    assert os.path.exists(recent_skill_path)
    assert not os.path.exists(os.path.join(archive_dir, "recent-skill.md"))
