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

def test_read_routing_stable_rules(workspace):
    """测试意图：询问稳定规则（只加载 L0/L2，不查 L3）"""
    executor = MemoryExecutor(workspace)
    # LLM 按照 Playbook 应该输出的 JSON
    read_decision = {
        "operation_type": "read",
        "read_decision": {
            "task_intent": "What are our coding guidelines?",
            "skills_to_load": ["coding-guidelines"],
            "memories_to_recall": [], # 遵守 Playbook，不查 L3
            "rationale": "Stable rules query, loading L0 and L2 only."
        }
    }
    context = executor.execute_read_decision(read_decision["read_decision"])
    assert "L0 Identity" in context

def test_read_routing_task_continuation(workspace):
    """测试意图：继续昨天的任务（加载 L2 和 L3）"""
    executor = MemoryExecutor(workspace)
    read_decision = {
        "operation_type": "read",
        "read_decision": {
            "task_intent": "Keep working on the python script",
            "skills_to_load": ["python-coder"],
            "memories_to_recall": ["python script progress"],
            "rationale": "Task continuation needs L2 domain knowledge and L3 recent state."
        }
    }
    context = executor.execute_read_decision(read_decision["read_decision"])
    assert "L0 Identity" in context
    assert "Recalled L3 Memories" in context

def test_read_routing_historical_tracing(workspace):
    """测试意图：历史回溯/故障追因（主要扫描 L3）"""
    executor = MemoryExecutor(workspace)
    read_decision = {
        "operation_type": "read",
        "read_decision": {
            "task_intent": "Why did the database migration fail yesterday?",
            "skills_to_load": [],
            "memories_to_recall": ["database migration fail", "error 500"],
            "rationale": "Historical tracing needs L3 scan."
        }
    }
    context = executor.execute_read_decision(read_decision["read_decision"])
    assert "Recalled L3 Memories" in context

# 在实际的生产中，这个测试套件可以通过接入一个 Mocked LLM 或者真实 LLM 
# 来验证 "Prompt -> JSON" 这一步是否严格遵守了 Playbook。
# 这里我们用静态断言来验证 Executor 的执行路径是畅通的。
