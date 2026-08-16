"""oracle review の新規所見列挙用 prompt 文面と起動パラメータの構築定義。"""

# std
from pathlib import Path

from oracle.acp_builder.basic import (
    AgentCallParameter,
    FileAccessMode,
    ModelClass,
    ReasoningEffort,
)
from oracle.other.path_model import (
    AgentCallPathContext,
    resolve_real_path,
)

# cmoc
from oracle.other.struct_doc import StructCodeBlock, StructDoc, render_as_markdown
from oracle.prompt_builder.complete_prompt import build_complete_prompt


def build_oracle_review_enumerate_finding_parameter(
    oracle_path: Path,
    related_findings: str,
    *,
    agent_call_cwd: Path,
) -> AgentCallParameter:
    """
    `cmoc oracle review` サブコマンド、新規所見列挙用。
    AI エージェント呼び出しパラメータを構築する。

    oracle_path: Path
        レビュー対象 oracle file のパス

    related_findings: str
        現状の所見リストのうち、レビュー対象ファイルと関連するもの

    agent_call_cwd: Path
        oracle review agent call を実行する worktree
    """
    # 隔離済み review worktree を起点に prompt と起動パラメータを構築する
    path_context = AgentCallPathContext(agent_call_cwd=agent_call_cwd)

    # プロンプト
    prompt = build_complete_prompt(
        summary="""
        - あなたはソフトウェア仕様断片のレビュー担当です
        - `{{oracle-path}}` を起点に `{{oracle-root}}` ツリー内の oracle file をレビューすること
        - 必要なら `{{oracle-path}}` 以外の関連する oracle file も読むこと
        """,
        goal="""
        - 指定の Structured Output schema に従って所見が列挙されていること
        - 既知の関連所見と重複しない新規所見だけが列挙されていること
        - 新規所見が無い場合は空配列を返していること
        """,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        path_context=path_context,
        aux_dynamic_prompt=[
            StructDoc(
                "既知の関連所見",
                StructCodeBlock(
                    "text",
                    related_findings,
                ),
            )
        ],
        aux_placeholder_def={
            "oracle-path": resolve_real_path(oracle_path, path_context),
            "oracle-root": resolve_real_path(
                Path("{{work-root}}/oracle"), path_context
            ),
        },
        oracle_and_realization_basic=True,
        oracle_review_policy=True,
        routing_policy=True,
    )
    # パラメータを生成して返す
    return AgentCallParameter(
        agent_call_kind=build_oracle_review_enumerate_finding_parameter.__name__,
        model_class=ModelClass.EFFICIENCY,
        reasoning_effort=ReasoningEffort.MAX,
        file_access_mode=FileAccessMode.PURE_ORACLE_READ,
        prompt=render_as_markdown(prompt),
        structured_output_schema_path=Path(__file__).with_suffix(".json"),
        agent_call_cwd=path_context.agent_call_cwd,
        run_indexing_preflight=True,
    )
