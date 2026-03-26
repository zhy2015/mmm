import pytest
import os
import tempfile
import sys

# 把 scripts 目录加到系统路径，方便引入 executor
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts", "core"))
from memory_executor import MemoryExecutor

# -----------------------------------------------------------------------------
# Physical Execution Tests
# 这个测试不再只是验证 JSON 格式，而是真正地调用 Executor 去读写硬盘。
# 它在一个临时的沙箱目录中执行，验证 "记忆写入 -> 记忆蒸馏/降级 -> 动态加载" 的真实 I/O 行为。
# -----------------------------------------------------------------------------

@pytest.fixture
def workspace():
    """创建一个干净的临时沙箱目录作为 OpenClaw 的根目录"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # 初始化 L0 核心文件
        with open(os.path.join(temp_dir, "AGENTS.md"), "w") as f:
            f.write("# Default Identity\n")
        with open(os.path.join(temp_dir, "MEMORY.md"), "w") as f:
            f.write("# Core Memory\n")
        yield temp_dir

class TestPhysicalExecution:

    def test_physical_write_and_read_loop(self, workspace):
        """
        验证真实的读写闭环：
        1. 写入 L0 核心规则 (Overwrite)
        2. 写入 L3 降级记忆 (Daily snapshot)
        3. 执行读取组装 (Read Phase)，验证上下文拼接是否正确
        """
        executor = MemoryExecutor(workspace)

        # --- 动作 1：写入核心规则 (Overwrite L0) ---
        write_l0_json = {
            "operation_type": "write",
            "write_decision": {
                "action": "overwrite",
                "layer": "core_memory",
                "rationale": "New test constraint.",
                "content": {
                    "title": "Strict Test Isolation",
                    "body": "Never connect to production DB during tests."
                }
            }
        }
        executor.execute_write_decision(write_decision=write_l0_json["write_decision"])

        # 验证物理文件是否真的被修改了
        memory_path = os.path.join(workspace, "MEMORY.md")
        assert os.path.exists(memory_path)
        with open(memory_path, "r") as f:
            content = f.read()
            assert "Never connect to production DB" in content
            assert "[OVERWRITE RECORD]" in content

        # --- 动作 2：降级记忆 (Write L3) ---
        write_l3_json = {
            "operation_type": "write",
            "write_decision": {
                "action": "write",
                "layer": "none", # 触发降级
                "rationale": "Just a transient snapshot.",
                "content": {
                    "title": "Snapshot: Fixed API bug",
                    "body": "The /users endpoint returned 500. Fixed by adding null check."
                }
            }
        }
        executor.execute_write_decision(write_decision=write_l3_json["write_decision"])

        # 验证是否真的被降级到了 daily 目录
        daily_path = os.path.join(workspace, "daily", "run_snapshots.md")
        assert os.path.exists(daily_path)
        with open(daily_path, "r") as f:
            content = f.read()
            assert "Fixed by adding null check" in content

        # --- 动作 3：动态加载查询 (Read Phase) ---
        read_json = {
            "operation_type": "read",
            "read_decision": {
                "task_intent": "Fix another API bug",
                "skills_to_load": [],
                "memories_to_recall": ["Snapshot: Fixed API bug"]
            }
        }
        # 真实执行组装
        assembled_context = executor.execute_read_decision(read_decision=read_json["read_decision"])

        # 验证拼接结果
        # 1. 必须强行包含 L0 的内容 (即便刚才被 overwrite 修改过)
        assert "Never connect to production DB" in assembled_context
        # 2. 必须包含刚刚拉取的 L3 记忆指令
        assert "Snapshot: Fixed API bug" in assembled_context

    def test_physical_skill_iteration(self, workspace):
        """
        验证蒸馏并写入到特定 Skill 层的功能（含 L2 元数据门禁测试）
        """
        executor = MemoryExecutor(workspace)

        # 假装用户对某个 skill 进行蒸馏迭代
        write_skill_json = {
            "operation_type": "write",
            "write_decision": {
                "action": "write",
                "layer": "skill",
                "target_skill": "data-analyzer",
                "rationale": "Iterating skill based on new edge case.",
                "content": {
                    "title": "Data Analyzer Constraint",
                    "body": "Always clean NaN values before aggregation.",
                    "metadata": {
                        "created_at": "2023-10-25T12:00:00Z",
                        "downgrade_condition": "If a new pandas version auto-cleans NaN"
                    }
                }
            }
        }
        executor.execute_write_decision(write_decision=write_skill_json["write_decision"])

        # 验证该 skill 的物理文件被创建或修改，且包含了元数据
        skill_path = os.path.join(workspace, "skills", "data-analyzer.md")
        assert os.path.exists(skill_path)
        with open(skill_path, "r") as f:
            content = f.read()
            assert "clean NaN values" in content
            assert "created_at: 2023-10-25T12:00:00Z" in content
            assert "downgrade_condition: If a new pandas version auto-cleans NaN" in content

        # 验证动态加载该 Skill
        read_json = {
            "operation_type": "read",
            "read_decision": {
                "task_intent": "Analyze some data",
                "skills_to_load": ["data-analyzer"],
                "memories_to_recall": []
            }
        }
        assembled_context = executor.execute_read_decision(read_decision=read_json["read_decision"])
        assert "clean NaN values" in assembled_context
        assert "downgrade_condition" in assembled_context

    def test_the_ultimate_layer_loop(self, workspace):
        """
        全层级（L0/L2/L3）闭环测试：
        验证不同的记忆被正确地分发到不同的物理位置，
        并且在读取时，能够按照严苛的"按需加载"逻辑进行组装。
        """
        executor = MemoryExecutor(workspace)

        # -----------------------------------------------------
        # 写入阶段 (Write Phase)
        # -----------------------------------------------------

        # 1. 产生 L0 记忆 (身份/原则)
        executor.execute_write_decision(write_decision={
            "action": "overwrite", # L0 应该用 overwrite 才能写入
            "layer": "core_memory",
            "rationale": "Security rule.",
            "content": {
                "title": "Rule: No Delete",
                "body": "Never use 'rm -rf /' under any circumstances."
            }
        })

        # 验证物理文件是否真的被修改了 (确保 L0 写入成功，修复断言错误)
        with open(os.path.join(workspace, "MEMORY.md"), "r") as f:
            l0_content = f.read()
            assert "No Delete" in l0_content

        # 2. 产生 L2 记忆 (本地知识/Skill)
        executor.execute_write_decision(write_decision={
            "action": "write",
            "layer": "skill",
            "target_skill": "python-coder",
            "rationale": "Domain knowledge.",
            "content": {
                "title": "Python Style",
                "body": "Use Type Hints for all function arguments.",
                "metadata": {
                    "created_at": "2023-10-26T10:00:00Z",
                    "downgrade_condition": "If Python 4 removes type hints"
                }
            }
        })

        # 3. 产生 L3 记忆 (历史经历/Snapshot)
        executor.execute_write_decision(write_decision={
            "action": "write",
            "layer": "none", # fallback to L3
            "rationale": "Transient snapshot.",
            "content": {
                "title": "Bug-1234 Fix",
                "body": "The weird timezone bug was fixed by forcing UTC."
            }
        })

        # -----------------------------------------------------
        # 物理位置验证 (确保它们没被混在一起)
        # -----------------------------------------------------
        with open(os.path.join(workspace, "MEMORY.md"), "r") as f:
            l0_content = f.read()
            assert "No Delete" in l0_content
            assert "Python Style" not in l0_content # L2 不能污染 L0

        with open(os.path.join(workspace, "skills", "python-coder.md"), "r") as f:
            l2_content = f.read()
            assert "Python Style" in l2_content

        with open(os.path.join(workspace, "daily", "run_snapshots.md"), "r") as f:
            l3_content = f.read()
            assert "Bug-1234" in l3_content

        # -----------------------------------------------------
        # 读取阶段 (Read Phase)
        # -----------------------------------------------------
        
        # 场景 A：纯聊天。只需要 L0，不需要 L2 和 L3。
        context_a = executor.execute_read_decision({
            "task_intent": "Hello, how are you?",
            "skills_to_load": [],
            "memories_to_recall": []
        })
        assert "No Delete" in context_a # L0 永远在场
        assert "Python Style" not in context_a
        assert "Bug-1234" not in context_a

        # 场景 B：写代码。需要 L0 + L2，不需要 L3。
        context_b = executor.execute_read_decision({
            "task_intent": "Write a python script",
            "skills_to_load": ["python-coder"],
            "memories_to_recall": []
        })
        assert "No Delete" in context_b
        assert "Python Style" in context_b # L2 被按需拉取
        assert "Bug-1234" not in context_b

        # 场景 C：修那个时区 bug。需要 L0 + L2 + L3。
        context_c = executor.execute_read_decision({
            "task_intent": "Fix the timezone issue in the python script",
            "skills_to_load": ["python-coder"],
            "memories_to_recall": ["Bug-1234 Fix"]
        })
        assert "No Delete" in context_c
        assert "Python Style" in context_c
        assert "forcing UTC" in context_c # 必须加载出 L3 记忆的具体内容(Body)，而不仅仅是标题

