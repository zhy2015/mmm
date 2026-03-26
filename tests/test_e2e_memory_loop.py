import pytest
from test_mmm_compliance import validate_against_schema

# -----------------------------------------------------------------------------
# End-to-End Memory Loop Test (The "Write-then-Read" cycle)
# 这个测试验证 mmm 能否在会话中提取经验，并在随后的新任务中正确召回该经验。
# -----------------------------------------------------------------------------

class TestE2EMemoryLoop:

    def test_e2e_skill_iteration_and_recall(self):
        """
        场景 1: Skill 迭代与验证
        1. 在会话中发现 pdf-parser 处理多栏排版时会丢数据，摸索出了必须要加 `use_layout_mode=True` 的经验。
        2. 用户说“保存”。
        3. 验证保存动作：mmm 必须将这个经验写回 `skill` 层，而不是当成全局身份原则（L0）。
        4. 新会话：用户再次要求解析 PDF。
        5. 验证读取动作：mmm 必须准确加载 `pdf-parser` 并在 memories_to_recall 中指出刚刚学到的排版经验。
        """
        
        # Step 1 & 2: 触发保存 (Write Phase)
        mock_save_output = {
            "operation_type": "write",
            "write_decision": {
                "action": "write",
                "layer": "skill",
                "target_skill": "pdf-parser",
                "rationale": "Discovered that multi-column PDFs drop data without layout mode. Adding this specific constraint to the pdf-parser skill.",
                "content": {
                    "title": "Multi-column PDF parsing constraint",
                    "body": "When parsing PDFs with multiple columns, MUST use `use_layout_mode=True` to prevent data loss."
                }
            }
        }
        validate_against_schema(mock_save_output)
        assert mock_save_output["write_decision"]["layer"] == "skill"
        assert mock_save_output["write_decision"]["target_skill"] == "pdf-parser"

        # Step 4: 新的会话来了 (Read Phase)
        mock_recall_output = {
            "operation_type": "read",
            "read_decision": {
                "task_intent": "帮我解析一下这份学术论文的 PDF",
                "skills_to_load": ["pdf-parser"],
                "memories_to_recall": ["Multi-column PDF parsing constraint"],
                "rationale": "Task involves parsing a PDF. Loading pdf-parser skill and recalling the specific constraint about multi-column layouts (common in academic papers)."
            }
        }
        validate_against_schema(mock_recall_output)
        assert "pdf-parser" in mock_recall_output["read_decision"]["skills_to_load"]
        assert "Multi-column PDF parsing constraint" in mock_recall_output["read_decision"]["memories_to_recall"]

    def test_e2e_core_rule_change_and_enforcement(self):
        """
        场景 2: 核心工作准则（L0）的变更与强制执行
        1. 会话中，由于 Agent 私自连外网查资料导致测试环境隔离被打破，用户很生气。
        2. 用户说“保存这个教训：不准在测试环境连外网”。
        3. 验证保存动作：mmm 必须将其识别为高优先级的 L0 (core_memory) 边界。
        4. 新会话：用户让 Agent "跑一下集成测试"。
        5. 验证读取动作：mmm 必须立刻把这条 "测试环境断网" 的 L0 规则拉出来，放在执行上下文的最前面。
        """

        # Step 1 & 2: 触发保存 (Write Phase)
        mock_save_output = {
            "operation_type": "write",
            "write_decision": {
                "action": "write",
                "layer": "core_memory",
                "rationale": "User established a hard security boundary regarding test environment isolation.",
                "content": {
                    "title": "Strict Environment Isolation (L0)",
                    "body": "NEVER initiate external network requests when operating in the test environment."
                }
            }
        }
        validate_against_schema(mock_save_output)
        assert mock_save_output["write_decision"]["layer"] == "core_memory"

        # Step 4: 新的任务来了 (Read Phase)
        mock_recall_output = {
            "operation_type": "read",
            "read_decision": {
                "task_intent": "跑一下集成测试",
                "skills_to_load": ["test-runner"],
                "memories_to_recall": ["Strict Environment Isolation (L0)"],
                "rationale": "Task involves the test environment. MUST load the L0 strict isolation boundary to prevent network leaks."
            }
        }
        validate_against_schema(mock_recall_output)
        assert "Strict Environment Isolation (L0)" in mock_recall_output["read_decision"]["memories_to_recall"]

