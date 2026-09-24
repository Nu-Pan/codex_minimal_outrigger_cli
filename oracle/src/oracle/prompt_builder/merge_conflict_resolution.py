"""run join と session join に共通する競合解消 prompt の構築定義。"""

from oracle.acp_builder.basic import FileAccessMode
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDHeader, SDTagBlock

from .complete_prompt import build_complete_prompt


def build_merge_conflict_resolution_prompt(
    *,
    source_commit: str,
    target_commit: str,
    file_access_mode: FileAccessMode,
    path_context: AgentCallPathContext,
    aux_static_prompt: tuple[SDHeader | SDTagBlock, ...] = (),
    aux_dynamic_prompt: tuple[SDHeader | SDTagBlock, ...] = (),
) -> list[SDHeader | SDTagBlock]:
    """進行中の merge を内容の統合と検証まで委ねる prompt を構築する。

    Args:
        source_commit: merge 前に確定した、取り込む branch の HEAD。
        target_commit: merge 前に確定した、取り込み先 branch の HEAD。
        file_access_mode: 呼び出し元の編集範囲に対応するアクセス mode。
        path_context: merge が進行中の worktree から構築した context。
        aux_static_prompt: 呼び出し元固有の追加指示。
        aux_dynamic_prompt: 呼び出し元固有の参照入力。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/merge_conflict_resolution.md` の
        「agent への入力と正確な定義の委譲」を参照。
        差分と競合 path は埋め込まず、agent が読み取り専用の Git 操作で取得する。
    """
    # 両 join で共通の目的・参照入力と policy 選択を一箇所で構築する。
    return build_complete_prompt(
        task="""
        - 統合対象 <cmoc_ref target="merge_input"/> の両 commit の変更意図を踏まえ、`{{work-root}}` で進行中の merge の内容競合を解消し、必要な付随修正と検証まで行うこと
        """,
        scope="""
        - 両 commit の共通祖先からの変更、進行中の競合状態、および関連する oracle を判断材料とし、統合に必要な関連ファイルを調査すること
        """,
        file_access_mode=file_access_mode,
        path_context=path_context,
        aux_static_prompt=[
            SDHeader(
                "統合対象の取得方法",
                """
                - cwd と `{{work-root}}` が示す repository で、指定された source・target commit の共通祖先と両側の変更を Git から取得すること
                - 進行中の merge の Git index と working tree から競合状態を読み取ること。rename・削除など、conflict marker のない競合も確認すること
                - Git 履歴・差分の参照にもファイルアクセス境界を適用すること
                - 取得に失敗した場合は空差分や競合なしとして扱わず、取得できなかった対象と理由を報告すること
                """,
            ),
            *aux_static_prompt,
        ],
        aux_dynamic_prompt=[
            SDTagBlock(
                "merge_input",
                SDHeader(
                    "統合対象",
                    f"- source（取り込む側）: `{source_commit}`\n"
                    f"- target（取り込み先の merge 前）: `{target_commit}`",
                ),
            ),
            *aux_dynamic_prompt,
        ],
        oracle_and_realization_basic=True,
        oracle_policy=True,
        realization_policy=True,
        conflict_resolution_policy=True,
        routing_policy=True,
    )
