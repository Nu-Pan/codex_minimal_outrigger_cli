"""report 検査 helper が現在の本文と独立した検査結果を使うことを確認する。"""

import pytest
from _report_support import (
    assert_report_layout,
    original_report_input,
    report_metadata,
    report_section,
    report_text,
)


def test_report_helpers_keep_content_boundaries_and_independent_metadata():
    """同じ見出しの report を交互に読み、章境界・原文・失敗の検出を保つ。"""
    for revision in ("first", "updated with longer text", "first"):
        original = f"# 指示 {revision}\n\n`原文` & <target>"
        details = f"{revision}\n\n### 内側の見出し\n\n詳細本文\n\n"
        content = (
            f"# report {revision}\n\n"
            "## 次の操作\n\n確認する\n\n"
            f"## 元の指示\n\n```text\n{original}\n```\n\n"
            f"## 詳細結果\n\n{details}"
            "## 実行記録\n\n`command` &amp; result\n\n"
            f"## 実行情報\n\n```yaml\nexecution_id: {revision}\n```\n"
        )

        assert_report_layout(content)
        assert original_report_input(content) == original
        assert report_section(content, "詳細結果") == "\n" + details
        assert report_text(report_section(content, "実行記録")) == "command & result"
        metadata = report_metadata(content)
        assert metadata == {"execution_id": revision}
        metadata["execution_id"] = "modified by caller"
        assert report_metadata(content) == {"execution_id": revision}

        with pytest.raises(AssertionError, match="report section is missing"):
            report_section(content, "存在しない章")
        # 直前の正常な report と同じ見出しでも、空行を失った本文は拒否する。
        malformed = content.replace("\n\n## 実行情報", "\n## 実行情報")
        with pytest.raises(AssertionError):
            assert_report_layout(malformed)
