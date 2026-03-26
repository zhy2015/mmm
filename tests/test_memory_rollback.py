import pytest
import os
import tempfile
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts", "core"))
from memory_rollback import MemoryRollback

@pytest.fixture
def workspace():
    with tempfile.TemporaryDirectory() as temp_dir:
        skills_dir = os.path.join(temp_dir, "skills")
        os.makedirs(skills_dir, exist_ok=True)
        yield temp_dir

def test_memory_rollback(workspace):
    """测试意图：错误上浮的 Skill 能够被回滚并记录到反面教材库"""
    skills_dir = os.path.join(workspace, "skills")
    bad_skill_path = os.path.join(skills_dir, "bad-skill.md")
    
    with open(bad_skill_path, "w") as f:
        f.write("### Restart Hack\nJust restart the pod.")

    rollback = MemoryRollback(workspace)
    success = rollback.rollback_skill("bad-skill", "One-off workaround, not a rule.")
    
    assert success
    assert not os.path.exists(bad_skill_path)
    
    bad_cases_path = os.path.join(workspace, "references", "mmm_bad_cases.jsonl")
    assert os.path.exists(bad_cases_path)
    with open(bad_cases_path, "r") as f:
        log_entry = json.loads(f.readline())
        assert log_entry["skill_name"] == "bad-skill"
        assert log_entry["correction_reason"] == "One-off workaround, not a rule."
