import pytest
import os
import tempfile
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts", "core"))
from memory_executor import MemoryExecutor

@pytest.fixture
def workspace():
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "AGENTS.md"), "w") as f:
            f.write("# Default Identity\n")
        with open(os.path.join(temp_dir, "MEMORY.md"), "w") as f:
            f.write("# Core Memory\n")
        yield temp_dir

def test_write_gate_one_off_residue(workspace):
    """测试意图：拦截一次性的 workaround，防止污染 L0"""
    executor = MemoryExecutor(workspace)
    # LLM 按照 Write Gate Checklist 判断为一次性经验，降级到 L3
    write_decision = {
        "operation_type": "write",
        "write_decision": {
            "action": "write",
            "layer": "none", # 强制降级到 L3
            "rationale": "One-off residue: restarting docker fixed the issue today. Not a durable lesson.",
            "content": {
                "title": "Docker Restart Fix",
                "body": "Restarted docker to fix the network issue."
            }
        }
    }
    executor.execute_write_decision(write_decision["write_decision"])
    
    # 验证 L0 没有被污染
    with open(os.path.join(workspace, "MEMORY.md"), "r") as f:
        assert "Docker Restart Fix" not in f.read()

def test_write_gate_durable_lesson(workspace):
    """测试意图：持久化的核心红线，允许进入 L0"""
    executor = MemoryExecutor(workspace)
    write_decision = {
        "operation_type": "write",
        "write_decision": {
            "action": "overwrite",
            "layer": "core_memory",
            "rationale": "Durable global redline: Never use docker-compose v1.",
            "content": {
                "title": "Docker Compose Redline",
                "body": "MUST use docker-compose v2 exclusively."
            }
        }
    }
    executor.execute_write_decision(write_decision["write_decision"])
    
    with open(os.path.join(workspace, "MEMORY.md"), "r") as f:
        assert "Docker Compose Redline" in f.read()
