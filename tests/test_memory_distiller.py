import pytest
import os
import tempfile
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts", "core"))
from memory_distiller import MemoryDistiller

@pytest.fixture
def workspace():
    with tempfile.TemporaryDirectory() as temp_dir:
        daily_dir = os.path.join(temp_dir, "daily")
        os.makedirs(daily_dir, exist_ok=True)
        yield temp_dir

def test_daily_to_rule_distillation(workspace):
    """测试意图：如果同一个错误在 L3 出现了 3 次，系统应该自动生成 L2 的升级候选"""
    daily_path = os.path.join(workspace, "daily", "run_snapshots.md")
    
    # 模拟写入 3 次同样的踩坑记录
    with open(daily_path, "w") as f:
        f.write("\n### Docker Error 1\nFailed to connect to docker daemon.\n")
        f.write("\n### Docker Error 2\nAnother docker issue with networking.\n")
        f.write("\n### Docker Error 3\nRestarted docker again to fix the bug.\n")
        f.write("\n### Random Typo\nFixed a typo in python script.\n") # 噪音

    distiller = MemoryDistiller(workspace)
    candidates = distiller.analyze_and_distill()
    
    # 验证是否成功蒸馏出 Docker 的规则，且没有蒸馏出 Typo
    assert len(candidates) == 1
    decision = candidates[0]["write_decision"]
    assert decision["layer"] == "skill"
    assert "docker" in decision["target_skill"]
    assert decision["rationale"].startswith("Automatically distilled")
