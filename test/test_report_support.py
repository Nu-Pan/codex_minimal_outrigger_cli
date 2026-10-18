"""report 検査 helper が現在の本文と独立した検査結果を使うことを確認する。"""

import _report_support as report_support
import pytest
import yaml
from _report_support import (
    assert_report_layout,
    original_report_input,
    report_metadata,
    report_section,
    report_text,
)


@pytest.mark.parametrize(
    "metadata_loader",
    dict.fromkeys((yaml.SafeLoader, getattr(yaml, "CSafeLoader", yaml.SafeLoader))),
    ids=lambda loader: loader.__name__,
)
def test_report_helpers_keep_content_boundaries_and_independent_metadata(
    monkeypatch, metadata_loader
):
    """同じ見出しの report を交互に読み、章境界・原文・失敗の検出を保つ。"""
    monkeypatch.setattr(report_support, "_REPORT_YAML_LOADER", metadata_loader)
    # backend ごとに実際の解析を通し、直前のケースの cache で代用しない。
    report_support._parse_report_metadata.cache_clear()
    for revision in ("first", "updated with longer text", "first"):
        original = f"# 指示 {revision}\n\n`原文` & <target>"
        details = f"{revision}\n\n### 内側の見出し\n\n詳細本文\n\n"
        content = (
            f"# report {revision}\n\n"
            "## 次の操作\n\n確認する\n\n"
            f"## 元の指示\n\n```text\n{original}\n```\n\n"
            f"## 詳細結果\n\n{details}"
            "## 実行記録\n\n`command` &amp; result\n\n"
            f"## 実行情報\n\n```yaml\nexecution_id: {revision}\n"
            f"result:\n  paths:\n    - {revision}\n"
            'values: ["", null, true, false, 0, 1.25, [], {}, "null", '
            '"日本語\\n次の行", "\\\\n"]\n```\n'
        )

        assert_report_layout(content)
        assert original_report_input(content) == original
        assert report_section(content, "詳細結果") == "\n" + details
        assert report_text(report_section(content, "実行記録")) == "command & result"
        metadata = report_metadata(content)
        values = [
            "",
            None,
            True,
            False,
            0,
            1.25,
            [],
            {},
            "null",
            "日本語\n次の行",
            r"\n",
        ]
        expected = {
            "execution_id": revision,
            "result": {"paths": [revision]},
            "values": values,
        }
        assert metadata == expected
        assert [type(value) for value in metadata["values"]] == [
            type(value) for value in values
        ]
        metadata["execution_id"] = "modified by caller"
        metadata["result"]["paths"].append("modified by caller")
        assert report_metadata(content) == expected

        with pytest.raises(AssertionError, match="report section is missing"):
            report_section(content, "存在しない章")
        # 直前の正常な report と同じ見出しでも、空行を失った本文は拒否する。
        malformed = content.replace("\n\n## 実行情報", "\n## 実行情報")
        with pytest.raises(AssertionError):
            assert_report_layout(malformed)
