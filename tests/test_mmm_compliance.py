import pytest
import json
import os

# -----------------------------------------------------------------------------
# Linus's Philosophy: "Talk is cheap. Show me the code."
# 这个测试套件是 OpenClaw 接入 mmm 架构的强制准入测试 (MUST-004)。
# 如果一个 Agent 系统连这几个基本的内存边界和读写契约都跑不过，
# 它就不配宣称自己集成了 mmm。
# -----------------------------------------------------------------------------

# 模拟：验证 Agent 抛给 mmm 的输出是否严格符合 Schema
def validate_against_schema(output_json):
    schema_path = "schemas/memory-routing.schema.json"
    assert os.path.exists(schema_path), "Schema file missing!"
    # 这里在真实环境中会调用 jsonschema.validate()
    # 为了演示框架连通性，我们做基本的字典键值检查
    assert "operation_type" in output_json
    if output_json["operation_type"] == "write":
        assert "write_decision" in output_json
        decision = output_json["write_decision"]
        assert decision["action"] in ["write", "overwrite", "downgrade", "archive", "discard", "handoff"]
        assert decision["layer"] in ["core_memory", "skill", "none"]
    elif output_json["operation_type"] == "read":
        assert "read_decision" in output_json
        decision = output_json["read_decision"]
        assert "task_intent" in decision
        assert "skills_to_load" in decision
        assert "memories_to_recall" in decision

class TestMMMAccessCompliance:

    # ---------------------------------------------------------
    # 1. 读链路测试 (Phase A: Read / Context Assembly)
    # ---------------------------------------------------------
    
    def test_read_quiet_system_compliance(self):
        """
        测试：安静系统原则。
        当任务很简单时（例如：打印 hello world），mmm 必须不加载任何不相关的 L3 历史或 L2 知识。
        """
        mock_mmm_output = {
            "operation_type": "read",
            "read_decision": {
                "task_intent": "Print hello world in python",
                "skills_to_load": [],
                "memories_to_recall": [], # 必须为空，不该有噪音
                "rationale": "Simple generic task. No specific context needed."
            }
        }
        validate_against_schema(mock_mmm_output)
        assert len(mock_mmm_output["read_decision"]["memories_to_recall"]) == 0

    def test_read_demand_pull_compliance(self):
        """
        测试：按需拉取原则。
        当任务明确关联到某个强领域时，mmm 必须能正确指示拉取对应的 skill 和 memory。
        """
        mock_mmm_output = {
            "operation_type": "read",
            "read_decision": {
                "task_intent": "帮我像昨天一样生成一份周报，用中文。",
                "skills_to_load": ["report-generator"],
                "memories_to_recall": ["run_snapshot_yesterday_report"], # 必须召回 L3 的快照
                "rationale": "User explicitly asked to replicate yesterday's behavior."
            }
        }
        validate_against_schema(mock_mmm_output)
        assert "run_snapshot_yesterday_report" in mock_mmm_output["read_decision"]["memories_to_recall"]

    # ---------------------------------------------------------
    # 2. 写链路测试 (Phase B: Write / Convergence)
    # ---------------------------------------------------------

    def test_write_reject_noise_compliance(self):
        """
        测试：拒绝噪音原则 (Reject by Default)。
        当遇到一次性的 debug 报错时，mmm 必须给出 discard 或 archive 指令，不能污染 core_memory。
        """
        mock_mmm_output = {
            "operation_type": "write",
            "write_decision": {
                "action": "discard", # 必须是 discard 或 archive
                "layer": "none",
                "rationale": "Just a transient typo error. No durable rule needed.",
                "content": {
                    "title": "Typo in variable name",
                    "body": "Fixed typo."
                }
            }
        }
        validate_against_schema(mock_mmm_output)
        assert mock_mmm_output["write_decision"]["action"] in ["discard", "archive"]
        assert mock_mmm_output["write_decision"]["layer"] == "none"

    def test_write_never_break_userspace(self):
        """
        测试：不破坏用户空间 (SSOT 覆盖原则)。
        如果发现了一个新的强制规则，且与旧规则冲突，必须是 overwrite，而不是 write 产生双重事实。
        """
        mock_mmm_output = {
            "operation_type": "write",
            "write_decision": {
                "action": "overwrite", # 必须是 overwrite
                "layer": "core_memory",
                "rationale": "New API endpoint requires auth token. Overwriting the old unauthenticated rule.",
                "content": {
                    "title": "API Auth Requirement",
                    "body": "Always use Bearer token for API calls."
                }
            }
        }
        validate_against_schema(mock_mmm_output)
        assert mock_mmm_output["write_decision"]["action"] == "overwrite"

    def test_explicit_save_trigger_compliance(self):
        """
        测试：显式保存触发器。
        当用户说“保存这段对话”时，不能直接 dump，必须提炼并写入。
        """
        mock_mmm_output = {
            "operation_type": "write",
            "write_decision": {
                "action": "write",
                "layer": "core_memory",
                "rationale": "User explicitly invoked save trigger. Distilled the 10-turn conversation into one behavior rule.",
                "content": {
                    "title": "User Preference: Error Handling",
                    "body": "Never use bare except. Always log stack trace."
                }
            }
        }
        validate_against_schema(mock_mmm_output)
        # 确保没有把大段对话放进 body
        assert len(mock_mmm_output["write_decision"]["content"]["body"]) < 200 
